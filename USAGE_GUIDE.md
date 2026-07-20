# Oracle to PostgreSQL Converter & Synthetic Test Data Generator: User Guide

A complete guide for running DDL conversions, metadata repository generation, rule-driven synthetic data creation, and bulk-loading into PostgreSQL.

---

## 🚀 1. Quick Start Commands (IDE / Terminal)

Run these commands from your terminal or IDE (VSCode, PyCharm, or Antigravity Terminal) inside the `oracle_to_postgres` project directory:

### Full Pipeline: Convert DDL, Generate Data & Load to PostgreSQL
```bash
python generate_data.py --rows 1000
```

### Step-by-Step Execution

#### Step A: Convert DDL & Create Tables + Foreign Keys in PostgreSQL
```bash
python converter.py
```

#### Step B: Generate & Bulk-Load 1,000 Rows per Table into PostgreSQL
```bash
python generate_data.py --rows 1000
```

### Generate Synthetic CSV Files Only (No Database Connection Needed)
```bash
python generate_data.py --generate-only --rows 1000
```

### Single Table Generation & Load
```bash
python generate_data.py --table p_dtl_tb --rows 1000
```

### Run Test Suite
```bash
python tests/smoke_test.py
```

---

## 📋 2. Pipeline Architecture & Feature Overview

```
                         ┌─────────────────────────────┐
                         │ Oracle DDLs (input/ddl/*.sql)│
                         └──────────────┬──────────────┘
                                        │
┌───────────────────────────────────────▼──────────────────────────────────────┐
│ DDL Converter & Metadata Loader                                             │
│  - Parses Oracle DDLs                                                        │
│  - Enriches PK/FK from input/ddl/Primary-Foreign keys.xlsx / .sql            │
│  - Generates output/ddl/*.sql & output/ddl/all_fk_constraints.sql            │
└───────────────────────────────────────┬──────────────────────────────────────┘
                                        │
┌───────────────────────────────────────▼──────────────────────────────────────┐
│ Pattern Analyzer & Rules Engine (rules.yml)                                  │
│  - Learns per-column profiles from input/data/*.csv                          │
│  - Prioritizes Column Name Semantics & rules.yml                             │
│  - Prevents copying sample CSV values for business text/names                 │
└───────────────────────────────────────┬──────────────────────────────────────┘
                                        │
┌───────────────────────────────────────▼──────────────────────────────────────┐
│ Data Generator (Topological Parent-First Execution)                           │
│  - Parent Tables (p_dtl_tb, etc.) generated first                            │
│  - Child Tables pick parent PKs to guarantee 0 FK orphan rows                │
│  - Post-generation _fix_orphan_fks() audit pass                              │
└───────────────────────────────────────┬──────────────────────────────────────┘
                                        │
┌───────────────────────────────────────▼──────────────────────────────────────┐
│ PostgreSQL Bulk Loader (Schema: provider)                                    │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔑 3. Foreign Key & Referential Integrity Rules

### What Happens if a Child Table is Inserted Before a Parent Table?
If you attempt to insert child records (e.g. `p_enrol_stat_tb`) into PostgreSQL when parent records (`p_dtl_tb`) do not exist, PostgreSQL's Foreign Key constraint enforces referential integrity and rejects the query:

> `ERROR: insert or update on table "p_enrol_stat_tb" violates foreign key constraint "p_enrol_stat_f1"`  
> `DETAIL: Key (p_sys_id)=(900001) is not present in table "p_dtl_tb".`

### How the Data Generator Solves This:
1. **Topological Order**: Parent tables (`p_dtl_tb`, `p_event_tb`, `p_hcidea_prov_tb`) are always generated and loaded **before** child tables (`p_enrol_stat_tb`, `p_alt_id_tb`).
2. **PK Registration**: Generated parent PKs are registered in memory.
3. **Child FK Selection**: Child tables select FK values strictly from valid parent PK pools.
4. **Post-Generation Repair**: Automated audit (`_fix_orphan_fks`) repairs any orphan values prior to loading into PostgreSQL.

---

## 🛠️ 4. Enterprise `rules.yml` Configuration

Columns configured in `rules.yml` override default generation logic:

- **Sequences**:
  ```yaml
  p_sys_id:
    generator: sequence
    start: 900001
    increment: 1
  ```
- **Code Choices**:
  ```yaml
  p_alt_id_ty_cd:
    generator: choice
    values: ["NPI", "DEA", "MCR", "ND"]
  ```
- **Regex Synthesizer**:
  ```yaml
  p_owner_tax_id:
    generator: regex
    pattern: "[0-9]{9}"
  ```
- **Conditional Table Rules**:
  ```yaml
  p_alt_id_npi:
    generator: regex
    pattern: "[0-9]{10}"
    applies_to:
      table: p_alt_id_tb
      column: p_alt_id
      condition: "p_alt_id_ty_cd = 'NPI'"
  ```

---

## 💡 5. Semantic Column Detection

Columns without explicit `rules.yml` entries are automatically categorized using column name keywords:

| Column Intent | Keywords / Patterns | Generator Output |
| :--- | :--- | :--- |
| **First Name** | `first_name`, `frst_nam`, `fname`, `first_nm` | Realistic First Name |
| **Last Name** | `last_name`, `lst_nam`, `sort_nam`, `surname`, `lname` | Realistic Last Name (e.g. 980+ unique names per 1,000 rows) |
| **Full Name** | `full_name`, `provider_name`, `prov_nam`, `contact_nam` | Realistic Full Name (e.g. "Dr. Sarah Jenkins, MD") |
| **Organization Name** | `org_nm`, `org_name`, `dba_nam`, `company`, `p_nam` | Realistic Healthcare Provider Org (e.g. "Mayo Clinic Health System") |
| **Email** | `email`, `mail_addr`, `email_addr` | Realistic Email |
| **Phone / Fax** | `phone`, `fax`, `mobile`, `tel` | Realistic Phone Number |
| **Address** | `address`, `addr1`, `addr2`, `street` | Realistic Street Address |
| **City / State / Zip** | `city`, `state`, `zip`, `postal_code` | Realistic City, State Abbreviation, Zipcode |
| **NPI** | `npi`, `npi_num` | 10-Digit NPI with Luhn Checksum |
| **DEA** | `dea`, `dea_num` | DEA Format (2 letters + 6 digits + checksum) |
| **Tax ID / SSN / EIN** | `tin`, `tax_id`, `ssn`, `ein` | 9-Digit Tax Identifier |
| **License** | `license`, `lic_num`, `cert_num` | Realistic State Medical License (e.g. `ND123456`) |
| **Audit User** | `g_aud_user_id`, `g_aud_add_user_id` | Configured `AUDIT_USER` ("SYSTEM") |

---

## ⚙️ 6. Command Line Arguments Summary

### `generate_data.py` CLI Options
| Argument | Description | Default |
| :--- | :--- | :--- |
| `--rows N` | Number of synthetic rows per table | `1000` (or `ROWS_PER_TABLE` in `config.py`) |
| `--generate-only` | Generate CSV files only; skip PostgreSQL load | `False` |
| `--table NAME` | Generate/load a single table only | `None` (all tables) |
| `--schema NAME` | Target PostgreSQL schema | `provider` |
| `--seed N` | Random seed for reproducible synthetic data | `12345` |
| `--no-truncate` | Skip `TRUNCATE TABLE` before load | `False` |

---

## 📁 7. Project Directory Layout

```
oracle_to_postgres/
├── config.py                 # Central environment & DB settings
├── converter.py              # DDL converter CLI orchestrator
├── data_generator.py         # Smart synthetic data generator engine
├── data_loader.py            # Sample CSV loader
├── datatype_mapper.py        # Oracle -> PostgreSQL type mapper
├── db.py                     # PostgreSQL database connection manager
├── ddl_converter.py          # Core DDL converter with PK/FK enrichment
├── generate_data.py          # Generator CLI entry point
├── metadata_loader.py        # PK/FK Excel & SQL metadata loader
├── pattern_analyzer.py       # Column profile pattern analyzer
├── postgres_loader.py        # PostgreSQL bulk loader
├── rules_engine.py           # Enterprise rules.yml parser & engine
├── rules.yml                 # Column generation rules
├── USAGE_GUIDE.md            # This user guide
├── input/
│   ├── data/                 # Sample CSV files
│   └── ddl/                  # Oracle DDL files & Primary-Foreign keys.xlsx/.sql
├── output/
│   ├── ddl/                  # Converted PostgreSQL DDLs & all_fk_constraints.sql
│   └── logs/                 # Execution logs
├── generated_data/           # Generated synthetic CSV files
└── tests/
    ├── __init__.py
    ├── smoke_test.py         # Integration & unit test suite
    └── test_gemini.py        # Gemini API test
```
