# Oracle → PostgreSQL DDL Converter

A production-quality Python CLI tool that converts Oracle DDL files into
PostgreSQL-compatible SQL and optionally executes them directly in your
PostgreSQL database.

---

## Features

| Capability | Details |
|---|---|
| **Type mapping** | NUMBER, VARCHAR2, CHAR, DATE, TIMESTAMP, CLOB, BLOB, RAW, LONG |
| **Constraint handling** | PRIMARY KEY, UNIQUE, CHECK preserved; FOREIGN KEY deferred |
| **FK deferral** | All FKs applied in a single batch after all tables are created |
| **Storage clause removal** | TABLESPACE, SEGMENT CREATION, PCTFREE, INITRANS, STORAGE(…), etc. |
| **Default conversion** | SYSDATE → CURRENT_TIMESTAMP, SYS_GUID() → gen_random_uuid() |
| **Formatted output** | Column-aligned, lowercase-identifier PostgreSQL DDL |
| **Error isolation** | One table failing never stops the remaining 79 |
| **Sample data** | Loads up to 2 CSV rows per table via ON CONFLICT DO NOTHING |
| **Logging** | Timestamped log file in output/logs/ + console output |

---

## Project Structure

```
oracle_to_postgres/
├── input/
│   ├── ddl/              ← Place your Oracle .sql files here
│   └── data/             ← Place sample data CSV files here (optional)
├── output/
│   ├── ddl/              ← Converted PostgreSQL .sql files (auto-created)
│   └── logs/             ← Execution log files (auto-created)
│
├── config.py             ← Central configuration (reads from .env)
├── db.py                 ← PostgreSQL connection manager (psycopg v3)
├── datatype_mapper.py    ← Oracle → PostgreSQL type mapping engine
├── ddl_converter.py      ← Full DDL parser and converter
├── sql_executor.py       ← Schema creation and DDL execution
├── data_loader.py        ← CSV sample-data loader
├── converter.py          ← Orchestrator and CLI entry point
│
├── .env.example          ← Template — copy to .env and fill in credentials
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure your database

```bash
copy .env.example .env
```

Edit `.env`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password_here
PG_SCHEMA=provider
EXECUTE_DDL=true
LOAD_SAMPLE_DATA=true
```

### 3. Add your Oracle DDL files

Copy all Oracle `.sql` files into `input/ddl/`:

```
input/ddl/P_ACPTNC_TB.sql
input/ddl/P_PRVDR_TB.sql
...
```

### 4. (Optional) Add sample data CSV files

Name each CSV after its table (case-insensitive):

```
input/data/P_ACPTNC_TB.csv
input/data/P_PRVDR_TB.csv
...
```

CSV format:
```csv
acptnc_id,acptnc_nm,crtd_dt
1,Sample Acceptance,2024-01-01
2,Another Record,2024-01-02
```

> **Note:** Column headers in the CSV are case-insensitive. Only the first 2 rows are inserted.

### 5. Run the converter

```bash
# Full pipeline: convert + execute + load sample data
python converter.py

# Convert only (no database connection required)
python converter.py --convert-only

# Convert + execute, but skip CSV data loading
python converter.py --no-data

# Use a different schema
python converter.py --schema staging
```

---

## Output Files

### Per-table converted DDL

`output/ddl/<original_stem>.sql` — one file per Oracle DDL file:

```sql
-- ==================================================================
-- PostgreSQL DDL  :  provider.p_acptnc_tb
-- Source file     :  P_ACPTNC_TB.sql
-- Generated       :  2024-01-15 09:30:00
-- Schema          :  provider
-- ==================================================================

SET search_path TO provider;

DROP TABLE IF EXISTS provider.p_acptnc_tb CASCADE;

CREATE TABLE provider.p_acptnc_tb (
    acptnc_id    bigint                   NOT NULL,
    acptnc_nm    varchar(100)             NOT NULL,
    crtd_dt      date    DEFAULT CURRENT_TIMESTAMP  NOT NULL,
    CONSTRAINT pk_p_acptnc_tb PRIMARY KEY (acptnc_id),
    CONSTRAINT uq_p_acptnc_tb_nm UNIQUE (acptnc_nm)
);

CREATE INDEX IF NOT EXISTS idx_p_acptnc_tb_dt
    ON provider.p_acptnc_tb (crtd_dt);

COMMENT ON TABLE provider.p_acptnc_tb IS 'Acceptance table';
```

### All FK constraints

`output/ddl/all_fk_constraints.sql` — all deferred FK ALTER statements:

```sql
ALTER TABLE provider.p_child_tb
    ADD CONSTRAINT fk_p_child_tb_parent
    FOREIGN KEY (parent_id)
    REFERENCES provider.p_parent_tb (acptnc_id);
```

### Execution log

`output/logs/conversion_YYYYMMDD_HHMMSS.log`

---

## Data Type Mapping Reference

| Oracle | PostgreSQL |
|--------|-----------|
| `NUMBER(1,0)` / `NUMBER(2,0)` | `SMALLINT` |
| `NUMBER(3,0)` … `NUMBER(8,0)` | `INTEGER` |
| `NUMBER(9,0)` … `NUMBER(38,0)` | `BIGINT` |
| `NUMBER(p,s)` where s > 0 | `NUMERIC(p,s)` |
| `NUMBER` | `NUMERIC` |
| `VARCHAR2(n)` | `VARCHAR(n)` |
| `CHAR(n)` | `CHAR(n)` |
| `DATE` | `DATE` |
| `TIMESTAMP(6)` | `TIMESTAMP` |
| `CLOB` / `NCLOB` | `TEXT` |
| `BLOB` | `BYTEA` |
| `RAW(n)` | `BYTEA` |
| `LONG` | `TEXT` |
| `LONG RAW` | `BYTEA` |
| `FLOAT` | `DOUBLE PRECISION` |
| `XMLTYPE` | `XML` |

## Default Value Mapping

| Oracle | PostgreSQL |
|--------|-----------|
| `SYSDATE` | `CURRENT_TIMESTAMP` |
| `SYSTIMESTAMP` | `CURRENT_TIMESTAMP` |
| `SYS_GUID()` | `gen_random_uuid()` |
| `USER` | `CURRENT_USER` |
| `TO_DATE(…)` | `CURRENT_DATE` |
| Numeric / string literals | Preserved as-is |

---

## Example Execution Summary

```
----------------------------------------------------
  ORACLE → POSTGRESQL  ·  CONVERSION SUMMARY
----------------------------------------------------
  Total Tables        :  80
  Conversion OK       :  80
  Execution OK        :  79
  Failed              :  1
  Sample Rows Loaded  :  158
----------------------------------------------------

  ► Failed tables:
    [EXEC]  p_some_table         (P_SOME_TABLE.sql)
            relation "provider.p_other_table" does not exist
```

---

## Oracle Clauses Removed

The following Oracle-only clauses are completely stripped from the output:

- `TABLESPACE`
- `SEGMENT CREATION [IMMEDIATE|DEFERRED]`
- `PCTFREE`, `PCTUSED`, `INITRANS`, `MAXTRANS`
- `STORAGE(INITIAL … NEXT … MINEXTENTS …)`
- `BUFFER_POOL`, `FLASH_CACHE`, `CELL_FLASH_CACHE`
- `COMPRESS`, `NOCOMPRESS`
- `LOGGING`, `NOLOGGING`
- `PARALLEL`, `NOPARALLEL`
- `ENABLE`, `DISABLE` (column/constraint level)
- `USING INDEX` (after PK/UK constraints)
- `SUPPLEMENTAL LOG DATA`
- `ENABLE ROW MOVEMENT`
- `COMPUTE STATISTICS`

---

## Requirements

- Python 3.12+
- PostgreSQL 13+
- `psycopg[binary]` >= 3.1
- `sqlparse` >= 0.5
- `python-dotenv` >= 1.0
