-- ============================================================
-- System Reference and Parameter Lookup Tables (r_ prefix)
-- Table count: 5
-- Generated: 2026-07-15 11:24
-- ============================================================

SET search_path TO provider;

-- ---- Table: R_LIST_DTL_TB ----
CREATE TABLE provider.r_list_dtl_tb (
    r_func_area_cd      VARCHAR(50),
    r_list_num          BIGINT,
    r_list_dtl_sk       BIGINT PRIMARY KEY,
    r_lob_cd            VARCHAR(50),
    r_list_beg_dt       VARCHAR(100),
    r_list_beg_value    VARCHAR(255),
    r_void_dt           VARCHAR(100),
    r_list_end_dt       VARCHAR(100),
    r_list_end_value    VARCHAR(255),
    r_list_sort_num     VARCHAR(50),
    l_hibernate_ver_num BIGINT,
    g_aud_user_id       VARCHAR(100),
    g_aud_ts            VARCHAR(100),
    g_aud_add_user_id   VARCHAR(100),
    g_aud_add_ts        VARCHAR(100)
);

-- ---- Table: R_LIST_HDR_TB ----
CREATE TABLE provider.r_list_hdr_tb (
    r_func_area_cd      VARCHAR(50),
    r_list_num          BIGINT,
    r_list_desc         VARCHAR(255),
    r_list_ty_cd        VARCHAR(50),
    r_list_busn_nam     VARCHAR(255),
    g_note_set_sk       VARCHAR(50),
    r_domain_nam        VARCHAR(255),
    l_hibernate_ver_num BIGINT,
    g_aud_user_id       VARCHAR(100),
    g_aud_ts            VARCHAR(100),
    g_aud_add_user_id   VARCHAR(100),
    g_aud_add_ts        VARCHAR(100),
    PRIMARY KEY (r_func_area_cd, r_list_num)
);

-- ---- Table: R_PARAM_DTL_TB ----
CREATE TABLE provider.r_param_dtl_tb (
    r_func_area_cd      VARCHAR(50),
    r_param_num         BIGINT,
    r_param_dtl_sk      BIGINT PRIMARY KEY,
    r_lob_cd            VARCHAR(50),
    r_param_beg_dt      VARCHAR(100),
    r_void_dt           VARCHAR(100),
    r_param_end_dt      VARCHAR(100),
    r_param_value_dt    VARCHAR(100),
    r_param_value_ts    VARCHAR(100),
    r_param_value_amt   VARCHAR(50),
    r_param_value_pct   VARCHAR(50),
    r_param_value_num   NUMERIC,
    r_param_value_data  VARCHAR(255),
    l_hibernate_ver_num BIGINT,
    g_aud_user_id       VARCHAR(100),
    g_aud_ts            VARCHAR(100),
    g_aud_add_user_id   VARCHAR(100),
    g_aud_add_ts        VARCHAR(100)
);

-- ---- Table: R_PARAM_TB ----
CREATE TABLE provider.r_param_tb (
    r_func_area_cd      VARCHAR(50),
    r_param_num         BIGINT,
    r_param_nam         VARCHAR(255),
    r_param_ty_cd       VARCHAR(50),
    g_note_set_sk       VARCHAR(50),
    l_hibernate_ver_num BIGINT,
    g_aud_user_id       VARCHAR(100),
    g_aud_ts            VARCHAR(100),
    g_aud_add_user_id   VARCHAR(100),
    g_aud_add_ts        VARCHAR(100),
    PRIMARY KEY (r_func_area_cd, r_param_num)
);

-- ---- Table: R_VV_TB ----
CREATE TABLE provider.r_vv_tb (
    r_vv_domain_nam     VARCHAR(255),
    r_vv_cd             VARCHAR(100),
    r_void_dt           VARCHAR(100),
    r_vv_short_desc     VARCHAR(255),
    r_vv_long_desc      VARCHAR(1000),
    l_hibernate_ver_num BIGINT,
    g_aud_user_id       VARCHAR(100),
    g_aud_ts            VARCHAR(100),
    g_aud_add_user_id   VARCHAR(100),
    g_aud_add_ts        VARCHAR(100),
    r_cnstnt_text       VARCHAR(255),
    r_used_in_appl_ind  VARCHAR(10),
    PRIMARY KEY (r_vv_domain_nam, r_vv_cd)
);
