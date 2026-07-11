"""
pattern_analyzer.py — Learn per-column data patterns from sample CSV files.

For each column, a ColumnProfile is built that captures:
  • The column's inferred type / generation strategy
  • Enumeration values (with weights derived from sample frequency)
  • Numeric / date ranges
  • Null rate
  • String length statistics
  • Whether a Faker provider should be used
  • Uniqueness and digit-only constraints to prevent DB load failures

The analysis is entirely data-driven — no schema-specific logic.
It works equally well for Provider, Claims, Member, Eligibility, etc.
"""
from __future__ import annotations

import csv
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Oracle date / timestamp patterns
# ---------------------------------------------------------------------------
_ORACLE_DATE_RE = re.compile(
    r"^\d{1,2}-[A-Za-z]{3}-(\d{2}|\d{4})$"
)
_ORACLE_TS_RE = re.compile(
    r"^\d{1,2}-[A-Za-z]{3}-(\d{2}|\d{4})\s+\d{1,2}[.:]\d{2}[.:]\d{2}"
)
_ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_ISO_TS_RE   = re.compile(r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}")


# ---------------------------------------------------------------------------
# Faker intent keywords (matched against lowercase column name)
# ---------------------------------------------------------------------------
_FAKER_RULES: list[tuple[list[str], str]] = [
    # (keyword suffixes/substrings, faker_tag)
    (["_last_nam", "_last_name", "last_nam", "lname"],         "last_name"),
    (["_first_nam", "_first_name", "first_nam", "fname", "_first_nm"], "first_name"),
    (["_mid_nam", "_mid_name", "middle_nam", "_mid_nm"],       "first_name"),
    (["_contact_nam", "_contact_name", "_contct_nam", "_attn_nam"], "name"),
    (["_addr", "_adr", "_street", "_address"],                  "street_address"),
    (["_city"],                                                  "city"),
    (["_state_cd", "_state_code"],                              "state_abbr"),
    (["_zip", "_postal", "_post_cd"],                           "zipcode"),
    (["_phone", "_tel", "_fax", "_phn_num", "phn_num"],         "phone_number"),
    (["_email", "_mail"],                                       "email"),
    (["_url", "_website"],                                      "url"),
    (["_company", "_org_nm", "_org_name", "_firm"],             "company"),
    (["_npi_num", "npi_num", "_npi_no", "npi_no", "_npi_id"],   "numerify_10"),   # 10-digit NPI
    (["_ssn", "_tin", "_tax_id"],                               "ssn"),
    (["_dob", "_birth_dt", "_date_of_birth"],                   "date_of_birth"),
]


# ---------------------------------------------------------------------------
# Strategy constants
# ---------------------------------------------------------------------------
STRAT_NULL        = "null"          # always NULL
STRAT_ENUM        = "enum"          # weighted random from observed values
STRAT_SEQUENTIAL  = "sequential"    # monotone integer sequence
STRAT_INT_RANGE   = "int_range"     # uniform integer in [min, max]
STRAT_FLOAT_RANGE = "float_range"   # uniform float  in [min, max]
STRAT_DATE        = "date"          # random date within observed range
STRAT_TIMESTAMP   = "timestamp"     # random timestamp within range
STRAT_FAKER       = "faker"         # Faker provider
STRAT_FREE_TEXT   = "free_text"     # random choice from sample values


@dataclass
class ColumnProfile:
    """Complete description of one column's generation strategy."""
    name        : str
    strategy    : str

    # Enum / free-text
    sample_values: list[str] = field(default_factory=list)   # raw non-null strings
    weights      : list[float] = field(default_factory=list) # same length as sample_values

    # Numeric
    int_min  : int   = 0
    int_max  : int   = 0
    float_min: float = 0.0
    float_max: float = 0.0
    int_step : int   = 1          # for sequential
    int_start: int   = 0          # for sequential (last seen value)

    # Date / timestamp
    date_min : str = ""
    date_max : str = ""
    is_oracle_fmt: bool = True    # True = Oracle DD-MON-YY; False = ISO

    # Faker
    faker_tag: str = ""

    # Nullability
    null_rate: float = 0.0

    # Max observed string length (for truncation safety)
    max_length: int = 255

    # Helper properties for database safety and referential scoring
    is_unique       : bool = False
    strip_non_digits: bool = False


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

class PatternAnalyzer:
    """
    Analyse all sample CSV files in *data_dir* and return a dict of
    ``{ table_name: { col_name: ColumnProfile } }``.
    """

    def __init__(self, data_dir: Path) -> None:
        self._data_dir = data_dir

    # ------------------------------------------------------------------ #
    # Public                                                               #
    # ------------------------------------------------------------------ #

    def analyze_all(self) -> dict[str, dict[str, ColumnProfile]]:
        """Return profiles for every CSV file found in *data_dir*."""
        result: dict[str, dict[str, ColumnProfile]] = {}
        csv_files = sorted(self._data_dir.glob("*.csv"))
        logger.info("Pattern analyzer: found %d CSV files.", len(csv_files))
        for path in csv_files:
            table_name = self._stem_to_table(path.stem)
            try:
                profiles = self._analyze_file(path)
                result[table_name] = profiles
                logger.debug("  Analyzed %s (%d columns)", table_name, len(profiles))
            except Exception as exc:  # noqa: BLE001
                logger.warning("  Failed to analyze %s: %s", path.name, exc)
        return result

    def analyze_one(self, csv_path: Path) -> dict[str, ColumnProfile]:
        """Analyze a single CSV file and return its column profiles."""
        return self._analyze_file(csv_path)

    # ------------------------------------------------------------------ #
    # Internal                                                             #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _stem_to_table(stem: str) -> str:
        """Convert filename stem to lowercase table name."""
        clean = re.sub(r"_DATA_TABLE$", "", stem, flags=re.IGNORECASE)
        return clean.lower()

    def _analyze_file(self, path: Path) -> dict[str, ColumnProfile]:
        """Read CSV and build a ColumnProfile for every column."""
        with open(path, newline="", encoding="utf-8-sig") as fh:
            reader  = csv.DictReader(fh)
            headers = reader.fieldnames or []
            rows    = list(reader)

        profiles: dict[str, ColumnProfile] = {}
        for col in headers:
            col_clean = col.strip()
            values = [r[col].strip() if r.get(col) else "" for r in rows]
            profiles[col_clean.lower()] = self._profile_column(col_clean, values)
        return profiles

    def _profile_column(self, col_name: str, raw_values: list[str]) -> ColumnProfile:
        """Determine the generation strategy for one column."""
        lower_col   = col_name.lower()
        non_null    = [v for v in raw_values if v]
        total       = len(raw_values)
        null_count  = total - len(non_null)
        null_rate   = null_count / total if total else 1.0
        max_len     = max((len(v) for v in non_null), default=0)
        is_unique   = len(non_null) > 0 and len(non_null) == len(set(non_null))

        # Trivially null column
        if not non_null:
            return ColumnProfile(name=lower_col, strategy=STRAT_NULL, null_rate=1.0)

        # ── Timestamp ────────────────────────────────────────────────── #
        if self._all_match(_ORACLE_TS_RE, non_null) or self._all_match(_ISO_TS_RE, non_null):
            d_min, d_max = self._date_range(non_null)
            oracle_fmt   = self._all_match(_ORACLE_TS_RE, non_null)
            return ColumnProfile(
                name=lower_col, strategy=STRAT_TIMESTAMP,
                date_min=d_min, date_max=d_max, is_oracle_fmt=oracle_fmt,
                null_rate=null_rate, is_unique=is_unique
            )

        # ── Date ─────────────────────────────────────────────────────── #
        if self._all_match(_ORACLE_DATE_RE, non_null) or self._all_match(_ISO_DATE_RE, non_null):
            d_min, d_max = self._date_range(non_null)
            oracle_fmt   = self._all_match(_ORACLE_DATE_RE, non_null)
            return ColumnProfile(
                name=lower_col, strategy=STRAT_DATE,
                date_min=d_min, date_max=d_max, is_oracle_fmt=oracle_fmt,
                null_rate=null_rate, is_unique=is_unique
            )

        # ── Code / indicator check ───────────────────────────────────── #
        # Columns with suffixes like _cd, _ind, _class, _type, _status are codes.
        # They should NOT be treated as Faker fields (even if they contain '_nam' like 'p_prev_nam_seq_num')
        # and should not be treated as sequential ranges if we can avoid it.
        is_code_like = any(
            suffix in lower_col
            for suffix in ["_cd", "_code", "_ind", "_type", "_ty", "_class", "_status", "_stat"]
        )

        # ── Faker check ──────────────────────────────────────────────── #
        # Only use Faker if column is not code-like and max length > 1
        faker_tag = ""
        if max_len > 1 and not is_code_like:
            faker_tag = self._detect_faker(lower_col)

        if faker_tag:
            strip_digits = non_null and all(v.isdigit() for v in non_null)
            # If strip_digits is True, we must strictly preserve the max observed length
            # to avoid exceeding the database column limit (e.g. phone or zip codes).
            col_max_len = max_len if strip_digits else max(max_len, 50)
            return ColumnProfile(
                name=lower_col, strategy=STRAT_FAKER, faker_tag=faker_tag,
                null_rate=null_rate, max_length=col_max_len,
                is_unique=is_unique, strip_non_digits=strip_digits
            )

        # ── Code / flag fallback to enumeration ──────────────────────── #
        distinct = sorted(set(non_null))
        if is_code_like:
            weights = [non_null.count(v) / len(non_null) for v in distinct]
            return ColumnProfile(
                name=lower_col, strategy=STRAT_ENUM,
                sample_values=distinct, weights=weights,
                null_rate=null_rate, max_length=max_len,
                is_unique=is_unique
            )

        # ── Numeric check ────────────────────────────────────────────── #
        if self._all_numeric(non_null):
            # Integer vs float
            if all("." not in v for v in non_null):
                ints = [int(v) for v in non_null]
                # Sequential detection: only when all values are unique
                is_seq = False
                if len(ints) >= 2 and len(ints) == len(set(ints)):
                    steps = [ints[i+1] - ints[i] for i in range(len(ints)-1)]
                    if len(set(steps)) == 1 and steps[0] > 0:
                        is_seq = True

                if is_seq:
                    return ColumnProfile(
                        name=lower_col, strategy=STRAT_SEQUENTIAL,
                        int_start=max(ints), int_step=steps[0],
                        null_rate=null_rate, is_unique=True
                    )
                return ColumnProfile(
                    name=lower_col, strategy=STRAT_INT_RANGE,
                    int_min=min(ints), int_max=max(ints),
                    null_rate=null_rate, is_unique=is_unique
                )
            else:
                floats = [float(v) for v in non_null]
                return ColumnProfile(
                    name=lower_col, strategy=STRAT_FLOAT_RANGE,
                    float_min=min(floats), float_max=max(floats),
                    null_rate=null_rate, is_unique=is_unique
                )

        # ── Enumeration ──────────────────────────────────────────────── #
        if len(distinct) <= max(8, len(non_null)):
            weights = [non_null.count(v) / len(non_null) for v in distinct]
            return ColumnProfile(
                name=lower_col, strategy=STRAT_ENUM,
                sample_values=distinct, weights=weights,
                null_rate=null_rate, max_length=max_len,
                is_unique=is_unique
            )

        # ── Free text fallback ───────────────────────────────────────── #
        return ColumnProfile(
            name=lower_col, strategy=STRAT_FREE_TEXT,
            sample_values=non_null,
            null_rate=null_rate, max_length=max_len,
            is_unique=is_unique
        )

    # ── Helper methods ────────────────────────────────────────────────── #

    @staticmethod
    def _detect_faker(col_name: str) -> str:
        """Return a faker_tag if the column name matches a Faker pattern, else ''."""
        # Guard against matching code or metadata fields (like phonetic columns '_phntc_')
        if any(suffix in col_name for suffix in ["_seq_num", "_sk", "_cd", "_ind", "_dt", "_date", "_code", "_type", "_ty", "_status", "_stat", "_phntc_", "phntc_"]):
            return ""
        for keywords, tag in _FAKER_RULES:
            for kw in keywords:
                if kw in col_name:
                    return tag
        return ""

    @staticmethod
    def _all_match(pattern: re.Pattern, values: list[str]) -> bool:
        return bool(values) and all(pattern.match(v) for v in values)

    @staticmethod
    def _all_numeric(values: list[str]) -> bool:
        try:
            [float(v) for v in values]
            return True
        except ValueError:
            return False

    @staticmethod
    def _date_range(values: list[str]) -> tuple[str, str]:
        """Return (min_val, max_val) as raw strings for date/timestamp columns."""
        sorted_vals = sorted(values)
        return sorted_vals[0], sorted_vals[-1]
