"""
pattern_analyzer.py — Learn per-column data patterns from sample CSV files and rules.yml.

For each column, a ColumnProfile is built that captures:
  • The column's inferred type / generation strategy
  • Enumeration values (with weights derived from sample frequency)
  • Numeric / date ranges
  • Null rate
  • String length statistics
  • Whether a Faker provider or RulesEngine rule should be used
  • Uniqueness and digit-only constraints to prevent DB load failures

Column names and rules.yml take priority over sample CSV values for business text.
"""
from __future__ import annotations

import csv
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from rules_engine import ColumnRule, RulesEngine

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
# Priority: Column Name Semantics
# ---------------------------------------------------------------------------
_FAKER_RULES: list[tuple[list[str], str]] = [
    (["first_name", "frst_nam", "fname", "first_nm", "fst_nam", "mid_nam", "middle_name",
      "hcidea_first_nam", "owner_first_nam", "dba_first_nam"], "first_name"),

    (["last_name", "lst_nam", "sort_nam", "surname", "lname", "last_nm", "fmr_nam", "prev_nam",
      "hcidea_last_nam", "owner_last_nam", "dba_last_nam"], "last_name"),

    (["full_name", "provider_name", "prov_name", "prov_nam", "contact_name", "contact_nam",
      "contct_nam", "attn_nam", "g_attn_nam", "user_name", "person_name", "auth_nam", "exec_nam",
      "rep_nam", "title_nam", "owner_busn_attn_nam", "owner_title_nam"], "name"),

    (["org_nm", "org_name", "dba_nam", "company", "firm", "p_nam", "busn_nam",
      "legal_nam", "legal_name", "fac_nam", "facility_name", "hosp_nam", "agency_nam",
      "lab_nam", "vend_nam", "owner_busn_nam", "owner_dba_nam"], "company"),

    (["email", "mail_addr", "mail_address", "email_addr", "email_address"], "email"),

    (["phone", "fax", "mobile", "tel", "phn_num", "cell", "contact_num", "tty", "tdd"], "phone_number"),

    (["address", "addr1", "addr2", "adr_line", "adr_ln", "street", "str_adr", "mail_adr",
      "g_line1_adr", "g_line2_adr", "g_line3_adr", "g_line4_adr", "g_usps_line1_adr", "g_usps_line2_adr"], "street_address"),

    (["city", "cty_nam", "city_nam", "g_city_nam", "town"], "city"),

    (["state_cd", "state_code", "st_cd", "birth_state_cd", "g_us_state_cd"], "state_abbr"),

    (["zip", "postal_code", "post_cd", "zip_cd", "zip_code", "postcode", "g_zip5_cd"], "zipcode"),

    (["dob", "birth_dt", "birth_date", "dob_dt", "bth_dt", "owner_dob_dt", "hcidea_birth_dt"], "date_of_birth"),

    (["license", "lic_num", "lic_no", "cert_num", "lic_nbr", "st_lic_num"], "license"),

    (["npi", "npi_num", "npi_no", "npi_id", "p_alt_id"], "npi"),

    (["tin", "tax_id", "ssn", "ein", "tax_num", "ssn_num", "owner_tax_id", "owner_ssn_num"], "tin"),

    (["dea", "dea_num", "dea_no", "dea_id"], "dea"),

    (["uuid", "guid"], "uuid"),

    (["mcare_id", "mcare_num", "mcare_alt_id", "mcaid_id", "mcaid_num", "mcaid_alt_id",
      "alt_id_val", "alt_id_num", "prov_num", "prov_id",
      "owner_mcare_id", "owner_mcaid_id"], "provider_id"),

    (["aud_user_id", "aud_add_user_id", "user_id", "crt_user_id"], "audit_user"),
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
STRAT_RULE        = "rule"          # rules.yml rule-driven generator


@dataclass
class ColumnProfile:
    """Complete description of one column's generation strategy."""
    name        : str
    strategy    : str

    # Enum / free-text / choice
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

    # Faker / Rule
    faker_tag: str = ""
    rule_id  : str = ""
    regex_pattern: str = ""

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

    def __init__(self, data_dir: Path, rules_engine: Optional[RulesEngine] = None) -> None:
        self._data_dir = data_dir
        self._rules_engine = rules_engine or RulesEngine()

    def analyze_all(self) -> dict[str, dict[str, ColumnProfile]]:
        """Return profiles for every CSV file found in *data_dir* and common DDL dir."""
        result: dict[str, dict[str, ColumnProfile]] = {}
        search_dirs = [self._data_dir, self._data_dir.parent / "ddl" / "common"]
        csv_files = []
        for sdir in search_dirs:
            if sdir.exists():
                csv_files.extend(sorted(sdir.glob("*.csv")))

        logger.info("Pattern analyzer: found %d CSV files across data and common dirs.", len(csv_files))
        for path in csv_files:
            table_name = self._stem_to_table(path.stem)
            try:
                profiles = self._analyze_file(path, table_name)
                result[table_name] = profiles
                logger.debug("  Analyzed %s (%d columns)", table_name, len(profiles))
            except Exception as exc:  # noqa: BLE001
                logger.warning("  Failed to analyze %s: %s", path.name, exc)

        # Parse DDL files for common tables if missing from CSV list
        common_ddl_dir = self._data_dir.parent / "ddl" / "common"
        if common_ddl_dir.exists():
            for sql_file in sorted(common_ddl_dir.glob("*.sql")):
                from ddl_converter import DDLConverter
                conv = DDLConverter(schema="provider", common_schema="common")
                res = conv.convert_file(sql_file)
                tbl = res.table_name.lower()
                if tbl in ("g_cmn_enty_tb", "g_adr_tb", "g_adr_usg_tb") and tbl not in result:
                    # Synthesize column profiles from SQL statement
                    profiles: dict[str, ColumnProfile] = {}
                    for stmt in res.pg_statements:
                        if "CREATE TABLE" in stmt:
                            # Match column names
                            col_matches = re.findall(r"^\s*([A-Za-z0-9_$#]+)\s+([A-Za-z0-9_()]+)", stmt, re.MULTILINE)
                            for cname, ctype in col_matches:
                                clower = cname.lower()
                                if clower not in ("create", "table", "constraint", "primary", "foreign", "key"):
                                    profiles[clower] = self._profile_column(clower, [], tbl)
                    if profiles:
                        result[tbl] = profiles
                        logger.info("Synthesized DDL profile for common table %s (%d columns)", tbl, len(profiles))

        return result

    def analyze_one(self, csv_path: Path) -> dict[str, ColumnProfile]:
        """Analyze a single CSV file and return its column profiles."""
        table_name = self._stem_to_table(csv_path.stem)
        return self._analyze_file(csv_path, table_name)

    def enrich_with_db_schema(
        self,
        db_manager: Any,
        profiles: dict[str, dict[str, ColumnProfile]],
    ) -> None:
        """Query PostgreSQL information_schema.columns to cap ColumnProfile max_length to DDL constraints."""
        try:
            conn = db_manager.connect()
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT table_name, column_name, character_maximum_length, is_nullable
                    FROM information_schema.columns 
                    WHERE table_schema IN ('provider', 'common');
                """)
                for tbl, col, maxlen, is_null in cur.fetchall():
                    tbl_l = tbl.lower()
                    col_l = col.lower()
                    if tbl_l in profiles and col_l in profiles[tbl_l]:
                        prof = profiles[tbl_l][col_l]
                        if maxlen is not None:
                            prof.max_length = maxlen
                        if is_null == 'NO':
                            prof.null_rate = 0.0
            logger.info("Enriched profiles with DDL max length and NOT NULL constraints from PostgreSQL.")
        except Exception as exc:  # noqa: BLE001
            logger.warning("Could not query DB schema for column constraints: %s", exc)

    # ------------------------------------------------------------------ #
    # Internal                                                             #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _stem_to_table(stem: str) -> str:
        """Convert filename stem to lowercase table name."""
        clean = re.sub(r"_DATA_TABLE$", "", stem, flags=re.IGNORECASE)
        return clean.lower()

    def _analyze_file(self, path: Path, table_name: str) -> dict[str, ColumnProfile]:
        """Read CSV and build a ColumnProfile for every column."""
        with open(path, newline="", encoding="utf-8-sig") as fh:
            reader  = csv.DictReader(fh)
            headers = reader.fieldnames or []
            rows    = list(reader)

        profiles: dict[str, ColumnProfile] = {}
        for col in headers:
            col_clean = col.strip()
            values = [r[col].strip() if r.get(col) else "" for r in rows]
            profiles[col_clean.lower()] = self._profile_column(col_clean, values, table_name)
        return profiles

    def _profile_column(self, col_name: str, raw_values: list[str], table_name: str = "") -> ColumnProfile:
        """Determine the generation strategy for one column, prioritizing rules and semantic names."""
        lower_col   = col_name.lower()
        non_null    = [v for v in raw_values if v]
        total       = len(raw_values)
        null_count  = total - len(non_null)
        null_rate   = null_count / total if total else 1.0
        max_len     = max((len(v) for v in non_null), default=0)
        is_unique   = len(non_null) > 0 and len(non_null) == len(set(non_null))

        # 0. Check Rules Engine explicit rules first
        rule = self._rules_engine.get_rule_for_column(table_name, lower_col)
        if rule:
            if rule.generator == "sequence":
                return ColumnProfile(
                    name=lower_col, strategy=STRAT_SEQUENTIAL,
                    int_start=rule.start, int_step=rule.increment,
                    rule_id=rule.rule_id, null_rate=null_rate, is_unique=True,
                )
            if rule.generator == "choice":
                weights = [1.0 / len(rule.values)] * len(rule.values) if rule.values else []
                return ColumnProfile(
                    name=lower_col, strategy=STRAT_ENUM,
                    sample_values=rule.values, weights=weights,
                    rule_id=rule.rule_id, null_rate=null_rate, max_length=max_len,
                )
            if rule.generator == "regex":
                return ColumnProfile(
                    name=lower_col, strategy=STRAT_RULE,
                    rule_id=rule.rule_id, regex_pattern=rule.pattern,
                    null_rate=null_rate, max_length=max(max_len, 50),
                    is_unique=True,
                )

        # 1. Identifier check — MUST be before null check so empty-sample PKs get SEQUENTIAL
        if self._is_identifier_col(lower_col):
            ints = [int(v) for v in non_null if v.isdigit()]
            int_start = max(ints) if ints else 1000000
            return ColumnProfile(
                name=lower_col, strategy=STRAT_SEQUENTIAL,
                int_start=int_start, int_step=1,
                null_rate=0.0, is_unique=True
            )

        # 2. Null check (after identifier check so PKs are never NULL)
        if not non_null:
            return ColumnProfile(name=lower_col, strategy=STRAT_NULL, null_rate=1.0)

        # 3. Timestamp check
        if self._all_match(_ORACLE_TS_RE, non_null) or self._all_match(_ISO_TS_RE, non_null):
            d_min, d_max = self._date_range(non_null)
            oracle_fmt   = self._all_match(_ORACLE_TS_RE, non_null)
            return ColumnProfile(
                name=lower_col, strategy=STRAT_TIMESTAMP,
                date_min=d_min, date_max=d_max, is_oracle_fmt=oracle_fmt,
                null_rate=null_rate, is_unique=is_unique
            )

        # 4. Date check
        if self._all_match(_ORACLE_DATE_RE, non_null) or self._all_match(_ISO_DATE_RE, non_null):
            d_min, d_max = self._date_range(non_null)
            oracle_fmt   = self._all_match(_ORACLE_DATE_RE, non_null)
            return ColumnProfile(
                name=lower_col, strategy=STRAT_DATE,
                date_min=d_min, date_max=d_max, is_oracle_fmt=oracle_fmt,
                null_rate=null_rate, is_unique=is_unique
            )

        # 5. Semantic Column Detection (High Priority: Column Name over sample text)
        faker_tag = self._detect_faker(lower_col)
        if faker_tag:
            strip_digits = faker_tag in ("phone_number", "zipcode", "npi", "tin")
            col_max_len = max_len if strip_digits else max(max_len, 50)
            sem_unique = is_unique or (faker_tag in ("npi", "dea", "license", "tin", "email", "uuid", "first_name", "last_name", "name", "company"))

            return ColumnProfile(
                name=lower_col, strategy=STRAT_FAKER, faker_tag=faker_tag,
                null_rate=null_rate, max_length=col_max_len,
                is_unique=sem_unique, strip_non_digits=strip_digits
            )

        # 6. Business Code / Indicator Check (e.g. _cd, _ind, _flag, _status)
        is_code = self._is_business_code_col(lower_col)
        distinct = sorted(set(non_null))
        if is_code:
            weights = [non_null.count(v) / len(non_null) for v in distinct]
            return ColumnProfile(
                name=lower_col, strategy=STRAT_ENUM,
                sample_values=distinct, weights=weights,
                null_rate=null_rate, max_length=max_len,
                is_unique=is_unique
            )

        # 7. Numeric range check
        if self._all_numeric(non_null):
            if all("." not in v for v in non_null):
                ints = [int(v) for v in non_null]
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

        # 8. Enum fallback (ONLY for short code lists, never for text names)
        if len(distinct) <= max(8, len(non_null)) and not self._is_text_field(lower_col):
            weights = [non_null.count(v) / len(non_null) for v in distinct]
            return ColumnProfile(
                name=lower_col, strategy=STRAT_ENUM,
                sample_values=distinct, weights=weights,
                null_rate=null_rate, max_length=max_len,
                is_unique=is_unique
            )

        # 9. Free text / Faker fallback for general text
        if self._is_text_field(lower_col):
            return ColumnProfile(
                name=lower_col, strategy=STRAT_FAKER, faker_tag="company",
                null_rate=null_rate, max_length=max(max_len, 50),
                is_unique=True,
            )

        return ColumnProfile(
            name=lower_col, strategy=STRAT_FREE_TEXT,
            sample_values=non_null,
            null_rate=null_rate, max_length=max_len,
            is_unique=is_unique
        )

    # ── Helper methods ────────────────────────────────────────────────── #

    @staticmethod
    def _is_text_field(col_name: str) -> bool:
        """Return True if column represents a general text name or description."""
        lower_col = col_name.lower()
        text_keywords = ["nam", "name", "desc", "text", "addr", "city", "comment", "note", "title"]
        return any(kw in lower_col for kw in text_keywords)

    @staticmethod
    def _is_identifier_col(col_name: str) -> bool:
        lower_col = col_name.lower()
        if lower_col.endswith("_seq_num") or lower_col.endswith("_sk") or lower_col == "sk":
            return True

        if lower_col.endswith("_sys_id") or lower_col == "sys_id":
            stem = lower_col
            for pre in ("p_", "g_", "t_", "l_"):
                if stem.startswith(pre):
                    stem = stem[len(pre):]
                    break
            core = stem[: -len("_sys_id")]
            _FK_QUALIFIERS = {"grp", "mbr", "enrol", "b"}
            if core in _FK_QUALIFIERS:
                return False
            return True

        if lower_col.endswith("_id"):
            if not any(sem in lower_col for sem in [
                "tax_id", "npi", "dea", "license", "payer",
                "user_id", "alt_id", "mcare", "mcaid", "ein",
            ]):
                return True
        return False

    @staticmethod
    def _is_business_code_col(col_name: str) -> bool:
        """Return True if the column represents a business code, flag, or status."""
        if any(col_name.endswith(suffix) for suffix in ["_cd", "_ty_cd", "_ind", "_flag", "_status"]):
            return True
        if col_name in ["gender", "status", "gender_cd", "status_cd"]:
            return True
        return False

    @staticmethod
    def _detect_faker(col_name: str) -> str:
        """Return a faker_tag if the column name matches a Faker pattern, else ''."""
        if any(suffix in col_name for suffix in ["_seq_num", "_sk", "_phntc_", "phntc_"]):
            return ""

        lower_col = col_name.lower()
        ends_with_code = any(lower_col.endswith(s) for s in ["_cd", "_ind", "_flag", "_status", "_type", "_class"])

        for keywords, tag in _FAKER_RULES:
            for kw in keywords:
                if kw in lower_col:
                    if ends_with_code:
                        if not (kw.endswith("_cd") or kw.endswith("_code") or kw.endswith("_ind") or kw.endswith("_flag") or kw == lower_col):
                            continue
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
        sorted_vals = sorted(values)
        return sorted_vals[0], sorted_vals[-1]
