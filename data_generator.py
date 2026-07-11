"""
data_generator.py — Synthesize realistic test rows from learned ColumnProfiles.

Generation rules
────────────────
* STRAT_NULL        — always None
* STRAT_SEQUENTIAL  — integer incremented from the last sample value
* STRAT_ENUM        — weighted random from observed distinct values
* STRAT_INT_RANGE   — random int in [min, max]
* STRAT_FLOAT_RANGE — random float in [min, max] (same decimal precision)
* STRAT_DATE        — random date between date_min and date_max
* STRAT_TIMESTAMP   — random timestamp between date_min and date_max
* STRAT_FAKER       — Faker provider call
* STRAT_FREE_TEXT   — random choice from sample values (with optional variation)

Foreign-key integrity
──────────────────────
Shared columns and suffix-matched columns (e.g. grp_sys_id referencing sys_id)
are automatically mapped. Parent tables generate values first, and child tables
draw values from the parent's generated pool. This guarantees referential integrity.

Output
──────
One CSV per table in *output_dir* (default: generated_data/).
"""
from __future__ import annotations

import csv
import logging
import random
import re
import uuid
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Optional

from faker import Faker

from pattern_analyzer import (
    ColumnProfile,
    STRAT_DATE, STRAT_ENUM, STRAT_FAKER,
    STRAT_FLOAT_RANGE, STRAT_FREE_TEXT,
    STRAT_INT_RANGE, STRAT_NULL, STRAT_SEQUENTIAL, STRAT_TIMESTAMP,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Oracle month names
# ---------------------------------------------------------------------------
_MONTHS = ["JAN","FEB","MAR","APR","MAY","JUN",
           "JUL","AUG","SEP","OCT","NOV","DEC"]

_MONTH_FROM_NUM = {i+1: m for i, m in enumerate(_MONTHS)}
_MONTH_TO_NUM   = {m: i+1 for i, m in enumerate(_MONTHS)}


def _oracle_date_to_date(val: str) -> Optional[date]:
    """Parse DD-MON-YY or DD-MON-YYYY to a Python date."""
    m = re.match(r"^(\d{1,2})-([A-Za-z]{3})-(\d{2,4})", val.strip())
    if not m:
        return None
    day  = int(m.group(1))
    mon  = _MONTH_TO_NUM.get(m.group(2).upper(), 1)
    year = int(m.group(3))
    if year < 100:
        year = 2000 + year if year < 50 else 1900 + year
    try:
        return date(year, mon, day)
    except ValueError:
        return None


def _iso_date_to_date(val: str) -> Optional[date]:
    try:
        return date.fromisoformat(val[:10])
    except ValueError:
        return None


def _date_to_oracle(d: date, include_time: bool = False) -> str:
    mon = _MONTH_FROM_NUM[d.month]
    day = str(d.day).zfill(2)
    yr  = str(d.year)[-2:].zfill(2)
    if include_time:
        return f"{day}-{mon}-{yr} 12.00.00.000000000 PM"
    return f"{day}-{mon}-{yr}"


def _parse_date_bound(val: str) -> Optional[date]:
    """Try Oracle then ISO parsing."""
    return _oracle_date_to_date(val) or _iso_date_to_date(val)


def _decimal_places(values: list[str]) -> int:
    """Return max decimal places observed in sample float strings."""
    places = 0
    for v in values:
        if "." in v:
            places = max(places, len(v.split(".")[1]))
    return places


# ---------------------------------------------------------------------------
# DataGenerator
# ---------------------------------------------------------------------------

class DataGenerator:
    """
    Generates synthetic rows for all tables using learned ColumnProfiles.

    Parameters
    ----------
    profiles   : { table_name: { col_name: ColumnProfile } }
    output_dir : destination for generated CSV files
    rows_per_table : how many rows to generate per table
    seed       : random seed for reproducibility
    """

    def __init__(
        self,
        profiles      : dict[str, dict[str, ColumnProfile]],
        output_dir    : Path,
        rows_per_table: int = 1000,
        seed          : int = 12345,
    ) -> None:
        self._profiles  = profiles
        self._out_dir   = output_dir
        self._rows      = rows_per_table
        self._seed      = seed

        random.seed(seed)
        self._fake = Faker()
        Faker.seed(seed)

        self._out_dir.mkdir(parents=True, exist_ok=True)

        # Pool of generated FK values: { col_name: [list of generated values] }
        self._fk_pool : dict[str, list[Any]] = {}

        # Mappings of (child_table, child_col) -> parent_col
        self._fk_mappings: dict[tuple[str, str], str] = {}

        # Registry to enforce global uniqueness for unique columns
        self._unique_registry: dict[str, set[Any]] = {}

        # Ordered list of table names (parents before children)
        self._order   = self._compute_generation_order()

    # ------------------------------------------------------------------ #
    # Public                                                               #
    # ------------------------------------------------------------------ #

    def generate_all(self) -> dict[str, int]:
        """
        Generate rows for every table.

        Returns { table_name: rows_written }.
        """
        results: dict[str, int] = {}
        for table in self._order:
            if table not in self._profiles:
                continue
            try:
                count = self._generate_table(table)
                results[table] = count
                logger.info("  Generated %d rows for %s.", count, table)
            except Exception as exc:  # noqa: BLE001
                logger.error("  Failed to generate %s: %s", table, exc)
                results[table] = 0
        return results

    def generate_one(self, table_name: str) -> int:
        """Generate rows for a single table and return row count."""
        return self._generate_table(table_name)

    def output_path(self, table_name: str) -> Path:
        return self._out_dir / f"{table_name.upper()}.csv"

    # ------------------------------------------------------------------ #
    # FK ordering and matching                                             #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _is_fk_match(child_col: str, parent_col: str) -> bool:
        """Return True if child_col is likely a foreign key referencing parent_col."""
        if child_col == parent_col:
            return True
        p_core = parent_col[2:] if parent_col.startswith("p_") else parent_col
        c_core = child_col[2:] if child_col.startswith("p_") else child_col
        # Suffix matching logic for key-like suffix structures
        if (p_core.endswith("_id") or p_core.endswith("_sk") or p_core.endswith("_num") or p_core in ("sys_id", "sk")):
            if c_core.endswith("_" + p_core) or c_core.endswith(p_core):
                return True
        return False

    def _compute_generation_order(self) -> list[str]:
        """
        Topologically sort tables so parents are generated before children.

        We score potential parent tables for each shared column.
        """
        all_tables = list(self._profiles.keys())

        # Build a map: col_name -> set of tables that have it
        col_table_map: dict[str, set[str]] = {}
        for tbl, cols in self._profiles.items():
            for col in cols:
                col_table_map.setdefault(col, set()).add(tbl)

        # child_tbl -> set of parent tables
        deps: dict[str, set[str]] = {t: set() for t in all_tables}

        # Step 1: Score and identify the primary parent table for key columns
        parent_cols: dict[str, str] = {} # { col_name: parent_table }
        for col, tables in col_table_map.items():
            best_parent = None
            best_score = -99999.0

            for tbl in tables:
                score = 0.0
                prof = self._profiles[tbl][col]

                # 1. Uniqueness
                if prof.is_unique:
                    score += 15.0
                if prof.strategy == STRAT_SEQUENTIAL:
                    score += 10.0
                elif prof.strategy in (STRAT_INT_RANGE, STRAT_FLOAT_RANGE):
                    score += 5.0

                # 2. Table stem prefix match
                tbl_stem = tbl.lower()
                if tbl_stem.startswith("p_"):
                    tbl_stem = tbl_stem[2:]
                for suffix in ["_tb", "_tx", "_tn"]:
                    if tbl_stem.endswith(suffix):
                        tbl_stem = tbl_stem[:-len(suffix)]

                if tbl_stem in col:
                    score += 20.0

                # 3. Reduce score if table has its own separate surrogate key
                for other_col in self._profiles[tbl]:
                    if other_col != col:
                        if other_col in (f"p_{tbl_stem}_sk", f"p_{tbl_stem}_id", f"{tbl_stem}_sk", f"{tbl_stem}_id"):
                            score -= 15.0

                if score > best_score:
                    best_score = score
                    best_parent = tbl

            if best_parent:
                parent_cols[col] = best_parent

        # Step 2: Establish topological dependencies and child-to-parent mappings
        self._fk_mappings = {}
        for child_tbl in all_tables:
            for child_col in self._profiles[child_tbl]:
                for p_col, parent_tbl in parent_cols.items():
                    if child_tbl == parent_tbl:
                        continue
                    if self._is_fk_match(child_col, p_col):
                        deps[child_tbl].add(parent_tbl)
                        self._fk_mappings[(child_tbl, child_col)] = p_col
                        logger.debug("FK mapped: %s.%s -> %s.%s", child_tbl, child_col, parent_tbl, p_col)
                        break

        # Kahn's topological sort
        in_degree = {t: len(deps[t]) for t in all_tables}
        queue = [t for t in all_tables if in_degree[t] == 0]
        order: list[str] = []

        while queue:
            node = queue.pop(0)
            order.append(node)
            for t in all_tables:
                if node in deps[t]:
                    deps[t].discard(node)
                    in_degree[t] -= 1
                    if in_degree[t] == 0:
                        queue.append(t)

        # Add any remaining tables
        for t in all_tables:
            if t not in order:
                order.append(t)

        return order

    # ------------------------------------------------------------------ #
    # Table generation                                                     #
    # ------------------------------------------------------------------ #

    def _generate_table(self, table_name: str) -> int:
        """Generate rows for one table, write CSV, update FK pool."""
        profiles = self._profiles[table_name]
        columns  = list(profiles.keys())
        out_path = self.output_path(table_name)

        # Determine which columns draw from already-generated parent tables
        fk_cols = self._identify_fk_cols(table_name, columns)

        # Track sequential state per column
        seq_state = {
            col: prof.int_start
            for col, prof in profiles.items()
            if prof.strategy == STRAT_SEQUENTIAL
        }

        rows: list[dict[str, Any]] = []
        for _ in range(self._rows):
            row = {}
            for col in columns:
                prof = profiles[col]
                row[col] = self._generate_value(col, prof, fk_cols, seq_state)
            
            # Apply row-level constraints (dates and audit columns)
            self._apply_row_constraints(row, table_name, profiles)
            
            # Format dates to string representations
            for col in columns:
                prof = profiles[col]
                if isinstance(row[col], (date, datetime)):
                    row[col] = self._format_date_val(row[col], prof)

            rows.append(row)

        # Write CSV
        with open(out_path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=columns, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            writer.writerows(rows)

        # Update FK pool for key columns (use exact col name if generated, or matching mappings)
        # To maintain FK pools for child tables that reference child columns by different names
        # (e.g. child tables referencing p_sys_id using p_grp_sys_id), we record the generated values
        # under the mapped parent column name in the pool.
        for col in columns:
            prof = profiles[col]
            if prof.strategy in (STRAT_SEQUENTIAL, STRAT_INT_RANGE) or prof.is_unique:
                pool = [r[col] for r in rows if r[col] is not None]
                self._fk_pool.setdefault(col, []).extend(pool)

        return len(rows)

    def _identify_fk_cols(
        self, table_name: str, columns: list[str]
    ) -> dict[str, str]:
        """Return { col_name: fk_pool_col } for columns drawing from parent tables."""
        fk = {}
        for col in columns:
            p_col = self._fk_mappings.get((table_name, col))
            if p_col:
                fk[col] = p_col
        return fk

    # ------------------------------------------------------------------ #
    # Single-value generation                                              #
    # ------------------------------------------------------------------ #

    def _generate_value(
        self,
        col       : str,
        prof      : ColumnProfile,
        fk_cols   : dict[str, str],
        seq_state : dict[str, int],
    ) -> Any:
        """Return a single generated value with uniqueness constraints."""
        # FK values draw directly from parent pool
        if col in fk_cols:
            p_col = fk_cols[col]
            if self._fk_pool.get(p_col):
                # FKs can be nullable
                if prof.null_rate > 0 and random.random() < prof.null_rate:
                    return None
                return random.choice(self._fk_pool[p_col])

        # Enforce uniqueness if required by looping up to 100 times
        for _ in range(100):
            val = self._generate_raw_value(col, prof, seq_state)
            if val is None:
                return None
            if not prof.is_unique:
                return val
            
            registry = self._unique_registry.setdefault(col, set())
            if val not in registry:
                registry.add(val)
                return val
        
        return val

    def _generate_raw_value(
        self,
        col       : str,
        prof      : ColumnProfile,
        seq_state : dict[str, int],
    ) -> Any:
        """Emits the raw unformatted synthetic value."""
        if prof.null_rate > 0 and random.random() < prof.null_rate:
            return None

        strategy = prof.strategy

        if strategy == STRAT_NULL:
            return None

        if strategy == STRAT_SEQUENTIAL:
            seq_state[col] += prof.int_step
            return seq_state[col]

        if strategy == STRAT_INT_RANGE:
            lo = prof.int_min
            hi = max(prof.int_max, lo)
            return random.randint(lo, hi)

        if strategy == STRAT_FLOAT_RANGE:
            val = random.uniform(prof.float_min, prof.float_max)
            return round(val, 2)

        if strategy == STRAT_ENUM:
            if not prof.sample_values:
                return None
            return random.choices(prof.sample_values, weights=prof.weights, k=1)[0]

        if strategy == STRAT_DATE:
            return self._random_date(prof)

        if strategy == STRAT_TIMESTAMP:
            return self._random_timestamp(prof)

        if strategy == STRAT_FAKER:
            val = self._call_faker(prof.faker_tag, prof.max_length)
            if prof.strip_non_digits:
                val = re.sub(r"\D", "", val)
            if prof.max_length and len(val) > prof.max_length:
                val = val[:prof.max_length]
            return val

        if strategy == STRAT_FREE_TEXT:
            if not prof.sample_values:
                return None
            return random.choice(prof.sample_values)

        return None

    # ------------------------------------------------------------------ #
    # Date / timestamp helpers                                             #
    # ------------------------------------------------------------------ #

    def _random_date(self, prof: ColumnProfile) -> date:
        d_min = _parse_date_bound(prof.date_min) or date(2000, 1, 1)
        d_max = _parse_date_bound(prof.date_max) or date(2030, 12, 31)
        if d_min > d_max:
            d_min, d_max = d_max, d_min
        delta = (d_max - d_min).days
        return d_min + timedelta(days=random.randint(0, max(delta, 0)))

    def _random_timestamp(self, prof: ColumnProfile) -> datetime:
        d_min = _parse_date_bound(prof.date_min) or date(2000, 1, 1)
        d_max = _parse_date_bound(prof.date_max) or date(2030, 12, 31)
        if d_min > d_max:
            d_min, d_max = d_max, d_min
        delta_days = (d_max - d_min).days
        rand_d = d_min + timedelta(days=random.randint(0, max(delta_days, 0)))
        h = random.randint(0, 23)
        mi = random.randint(0, 59)
        s  = random.randint(0, 59)
        us = random.randint(0, 999999)
        return datetime(rand_d.year, rand_d.month, rand_d.day, h, mi, s, us)

    # ------------------------------------------------------------------ #
    # Date/Time Constraint enforcement & formatting                        #
    # ------------------------------------------------------------------ #

    def _apply_row_constraints(
        self, row: dict[str, Any], table_name: str, profiles: dict[str, ColumnProfile]
    ) -> None:
        """Adjusts date, audit, and text fields to maintain logical integrity."""
        # 1. Configured audit user IDs
        for col in row:
            if col in ("g_aud_user_id", "g_aud_add_user_id", "g_aud_upd_user_id", "g_web_user_id"):
                from config import AUDIT_USER
                row[col] = AUDIT_USER

        # 2. Add / Audit dates
        now_dt = datetime.now()
        add_col = next((c for c in row if c == "g_aud_add_ts"), None)
        aud_col = next((c for c in row if c == "g_aud_ts"), None)

        if add_col and row[add_col] is not None:
            # Shift add_ts to be within past year
            add_val = now_dt - timedelta(days=random.randint(1, 365), seconds=random.randint(0, 86400))
            row[add_col] = add_val
        
        if aud_col and row[aud_col] is not None:
            if add_col and row[add_col] is not None:
                # Audit ts must be >= Add ts
                row[aud_col] = row[add_col] + timedelta(days=random.randint(0, 30), seconds=random.randint(0, 86400))
            else:
                row[aud_col] = now_dt

        # 3. Begin Date < End Date
        date_cols = [c for c in row if isinstance(row[c], (date, datetime))]
        begin_patterns = ["beg_dt", "start_dt", "eff_dt", "add_dt", "upd_dt"]
        end_patterns = ["end_dt", "term_dt", "cancel_dt", "rever_dt"]

        begins = [c for c in date_cols if any(p in c for p in begin_patterns)]
        ends = [c for c in date_cols if any(p in c for p in end_patterns)]

        for b_col in begins:
            for e_col in ends:
                b_val = row[b_col]
                e_val = row[e_col]
                if b_val and e_val:
                    b_date = b_val.date() if isinstance(b_val, datetime) else b_val
                    e_date = e_val.date() if isinstance(e_val, datetime) else e_val
                    if e_date <= b_date:
                        new_e_date = b_date + timedelta(days=random.randint(30, 365 * 5))
                        if isinstance(e_val, datetime):
                            row[e_col] = datetime.combine(new_e_date, e_val.time())
                        else:
                            row[e_col] = new_e_date

    def _format_date_val(self, val: date | datetime, prof: ColumnProfile) -> str:
        """Formats dates to Oracle DD-MON-YY or ISO format."""
        if isinstance(val, datetime):
            if prof.is_oracle_fmt:
                mon = _MONTH_FROM_NUM[val.month]
                day = str(val.day).zfill(2)
                yr  = str(val.year)[-2:].zfill(2)
                h = val.hour
                meridian = "AM" if h < 12 else "PM"
                h12 = h % 12 or 12
                ns = val.microsecond * 1000
                return (
                    f"{day}-{mon}-{yr} "
                    f"{h12:02d}.{val.minute:02d}.{val.second:02d}.{ns:09d} {meridian}"
                )
            return val.strftime("%Y-%m-%d %H:%M:%S.%f")
        else: # date
            if prof.is_oracle_fmt:
                mon = _MONTH_FROM_NUM[val.month]
                day = str(val.day).zfill(2)
                yr  = str(val.year)[-2:].zfill(2)
                return f"{day}-{mon}-{yr}"
            return val.isoformat()

    # ------------------------------------------------------------------ #
    # Faker dispatch                                                        #
    # ------------------------------------------------------------------ #

    def _call_faker(self, tag: str, max_length: int) -> str:
        fake = self._fake
        
        # Alphanumeric license or certifications
        if tag == "license":
            return f"ND{random.randint(100000, 9999999)}"
        # Valid-looking 10-digit NPIs starting with 1 or 2
        elif tag == "npi":
            return str(random.choice([1, 2])) + "".join(str(random.randint(0, 9)) for _ in range(9))
        # DEA checksummed registration numbers
        elif tag == "dea":
            first_letter = random.choice(["A", "B", "F", "G", "M", "P"])
            second_letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            digits = [random.randint(0, 9) for _ in range(6)]
            sum1 = digits[0] + digits[2] + digits[4]
            sum2 = digits[1] + digits[3] + digits[5]
            total = sum1 + 2 * sum2
            check_digit = total % 10
            digits.append(check_digit)
            return f"{first_letter}{second_letter}{''.join(map(str, digits))}"
        # 9-digit tax identifier / EIN / SSN
        elif tag == "tin":
            return "".join(str(random.randint(0, 9)) for _ in range(9))
        # Standard UUID
        elif tag == "uuid":
            return str(uuid.uuid4())
        # Provider Alt ID / Medicaid ID
        elif tag == "provider_id":
            return fake.bothify("??#######").upper()

        dispatch: dict[str, Any] = {
            "last_name"      : fake.last_name,
            "first_name"     : fake.first_name,
            "name"           : fake.name,
            "street_address" : fake.street_address,
            "city"           : fake.city,
            "state_abbr"     : fake.state_abbr,
            "zipcode"        : fake.zipcode,
            "phone_number"   : fake.phone_number,
            "email"          : fake.email,
            "url"            : fake.url,
            "company"        : fake.company,
            "date_of_birth"  : lambda: fake.date_of_birth().strftime("%Y-%m-%d"),
        }
        fn = dispatch.get(tag)
        if fn is None:
            return fake.word()
        val = str(fn())
        return val
