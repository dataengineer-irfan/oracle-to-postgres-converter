"""
data_generator.py — Synthesize realistic test rows from learned ColumnProfiles and rules.yml.

Architecture
────────────
1. PatternAnalyzer & RulesEngine provide per-column generation strategies.
2. DataGenerator uses an EXPLICIT FK registry:
   - PROVIDER_FK_MAP contains authoritative FK->PK declarations for every known
     relationship in the Provider schema. This is merged with heuristic detection
     at startup; explicit entries always take priority.
   - Tracks every generated PK value under its column name.
   - Child FK columns look up their parent pool and pick an existing value.
3. Tables are generated in topological order (parents first, always).
4. If the topological sort cannot satisfy a dependency (e.g. circular), a
   post-generation _fix_orphan_fks() pass repairs any remaining orphans.
5. Zero orphans are guaranteed after the repair pass.
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

from config import AUDIT_USER
from pattern_analyzer import (
    ColumnProfile,
    STRAT_DATE, STRAT_ENUM, STRAT_FAKER,
    STRAT_FLOAT_RANGE, STRAT_FREE_TEXT,
    STRAT_INT_RANGE, STRAT_NULL, STRAT_RULE, STRAT_SEQUENTIAL, STRAT_TIMESTAMP,
)
from rules_engine import ColumnRule, RulesEngine

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Oracle month helpers
# ---------------------------------------------------------------------------
_MONTHS = ["JAN","FEB","MAR","APR","MAY","JUN",
           "JUL","AUG","SEP","OCT","NOV","DEC"]

_MONTH_FROM_NUM = {i+1: m for i, m in enumerate(_MONTHS)}
_MONTH_TO_NUM   = {m: i+1 for i, m in enumerate(_MONTHS)}


def _oracle_date_to_date(val: str) -> Optional[date]:
    val_clean = val.strip().upper()
    if "31-DEC-99" in val_clean or "9999" in val_clean:
        return date(2099, 12, 31)
    m = re.match(r"^(\d{1,2})-([A-Za-z]{3})-(\d{2,4})", val_clean)
    if not m:
        return None
    day  = int(m.group(1))
    mon  = _MONTH_TO_NUM.get(m.group(2), 1)
    year = int(m.group(3))
    if year < 100:
        year = 2000 + year
    try:
        return date(year, mon, day)
    except ValueError:
        return None


def _iso_date_to_date(val: str) -> Optional[date]:
    try:
        return date.fromisoformat(val[:10])
    except ValueError:
        return None


def _parse_date_bound(val: str) -> Optional[date]:
    return _oracle_date_to_date(val) or _iso_date_to_date(val)


def _strip_prefix(name: str) -> str:
    """Remove leading p_ / g_ / t_ / l_ prefixes."""
    for pre in ("p_", "g_", "t_", "l_"):
        if name.startswith(pre):
            return name[len(pre):]
    return name


def _fk_suffix_matches(child_col: str, parent_col: str) -> bool:
    if child_col == parent_col:
        return True
    c_core = _strip_prefix(child_col)
    p_core = _strip_prefix(parent_col)
    if c_core.endswith("_" + parent_col):
        return True
    if c_core.endswith("_" + p_core):
        return True
    if c_core == p_core:
        return True
    return False


# ---------------------------------------------------------------------------
# PROVIDER_FK_MAP — Authoritative FK declarations for the Provider schema
# ---------------------------------------------------------------------------
PROVIDER_FK_MAP: dict[tuple[str, str], tuple[str, str]] = {
    ("c_hdr_aux_tb", "b_sys_id"): ("c_hdr_parent_tb", "b_sys_id"),
    ("c_hdr_aux_tb", "c_tcn_num"): ("c_hdr_parent_tb", "c_tcn_num"),
    ("c_hdr_tb", "b_sys_id"): ("c_hdr_parent_tb", "b_sys_id"),
    ("c_hdr_tb", "c_tcn_num"): ("c_hdr_parent_tb", "c_tcn_num"),
    ("c_li_tb", "b_sys_id"): ("c_hdr_parent_tb", "b_sys_id"),
    ("c_li_tb", "c_tcn_num"): ("c_hdr_parent_tb", "c_tcn_num"),
    ("g_adr_phone_usg_tb", "g_adr_sk"): ("g_adr_usg_tb", "g_adr_sk"),
    ("g_adr_phone_usg_tb", "g_adr_usg_seq_num"): ("g_adr_usg_tb", "g_adr_usg_seq_num"),
    ("g_adr_phone_usg_tb", "g_adr_usg_ty_cd"): ("g_adr_usg_tb", "g_adr_usg_ty_cd"),
    ("g_adr_phone_usg_tb", "g_cmn_enty_sk"): ("g_phone_usg_tb", "g_cmn_enty_sk"),
    ("g_adr_phone_usg_tb", "g_phone_sk"): ("g_phone_usg_tb", "g_phone_sk"),
    ("g_adr_phone_usg_tb", "g_phone_usg_seq_num"): ("g_phone_usg_tb", "g_phone_usg_seq_num"),
    ("g_adr_phone_usg_tb", "g_phone_usg_ty_cd"): ("g_phone_usg_tb", "g_phone_usg_ty_cd"),
    ("g_adr_usg_tb", "g_adr_sk"): ("g_adr_tb", "g_adr_sk"),
    ("g_adr_usg_tb", "g_cmn_enty_sk"): ("g_cmn_enty_tb", "g_cmn_enty_sk"),
    ("g_cmn_enty_rep_xref_tb", "g_cmn_enty_sk"): ("g_cmn_enty_tb", "g_cmn_enty_sk"),
    ("g_cmn_enty_rep_xref_tb", "g_rep_sk"): ("g_rep_tb", "g_rep_sk"),
    ("g_cmn_enty_tb", "g_note_set_sk"): ("g_note_set_tb", "g_note_set_sk"),
    ("g_cmn_revw_tb", "g_cmn_enty_sk"): ("g_cmn_enty_tb", "g_cmn_enty_sk"),
    ("g_cmn_revw_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("g_cmn_revw_tb", "r_clm_exc_cd"): ("r_clm_exc_tb", "r_clm_exc_cd"),
    ("g_cmn_revw_tb", "r_lob_cd"): ("r_lob_dtl_tb", "r_lob_cd"),
    ("g_cmn_revw_tb", "r_text_locn_cd"): ("r_text_locn_tb", "r_text_locn_cd"),
    ("g_cots_ltr_req_recr_tb", "g_adr_sk"): ("g_adr_usg_tb", "g_adr_sk"),
    ("g_cots_ltr_req_recr_tb", "g_adr_usg_seq_num"): ("g_adr_usg_tb", "g_adr_usg_seq_num"),
    ("g_cots_ltr_req_recr_tb", "g_adr_usg_ty_cd"): ("g_adr_usg_tb", "g_adr_usg_ty_cd"),
    ("g_cots_ltr_req_recr_tb", "g_cmn_enty_sk"): ("g_adr_usg_tb", "g_cmn_enty_sk"),
    ("g_cots_ltr_req_recr_tb", "g_cots_ltr_req_sk"): ("g_cots_ltr_req_tb", "g_cots_ltr_req_sk"),
    ("g_cots_ltr_req_recr_tb", "g_e_adr_sk"): ("g_e_adr_usg_tb", "g_e_adr_sk"),
    ("g_cots_ltr_req_recr_tb", "g_e_adr_usg_seq_num"): ("g_e_adr_usg_tb", "g_e_adr_usg_seq_num"),
    ("g_cots_ltr_req_recr_tb", "g_e_adr_usg_ty_cd"): ("g_e_adr_usg_tb", "g_e_adr_usg_ty_cd"),
    ("g_cots_ltr_req_tb", "g_alert_based_on_col_nam"): ("r_dd_col_tb", "r_col_nam"),
    ("g_cots_ltr_req_tb", "g_alert_based_on_table_nam"): ("r_dd_col_tb", "r_table_nam"),
    ("g_cots_ltr_req_tb", "g_cots_ltr_tmplt_key_data"): ("g_cots_ltr_tmplt_tb", "g_cots_ltr_tmplt_key_data"),
    ("g_cots_ltr_req_tb", "g_note_seq_num"): ("g_note_tb", "g_note_seq_num"),
    ("g_cots_ltr_req_tb", "g_note_set_sk"): ("g_note_tb", "g_note_set_sk"),
    ("g_cots_ltr_req_tb", "g_notfy_alert_user_id"): ("g_user_tb", "g_user_id"),
    ("g_cots_ltr_req_tb", "g_user_id"): ("g_user_tb", "g_user_id"),
    ("g_cr_cmn_enty_xref_tb", "g_cmn_enty_sk"): ("g_cmn_enty_tb", "g_cmn_enty_sk"),
    ("g_cr_cmn_enty_xref_tb", "g_cr_sk"): ("g_cr_tb", "g_cr_sk"),
    ("g_cr_tb", "g_cr_crtd_by_work_unit_sk"): ("g_work_unit_tb", "g_work_unit_sk"),
    ("g_cr_tb", "g_crspd_asgn_to_work_unit_sk"): ("g_work_unit_tb", "g_work_unit_sk"),
    ("g_cr_tb", "g_crspd_cat_sk"): ("g_crspd_cat_tb", "g_crspd_cat_sk"),
    ("g_cr_tb", "g_crspd_last_upd_work_unit_sk"): ("g_work_unit_tb", "g_work_unit_sk"),
    ("g_cr_tb", "g_crspd_open_work_unit_sk"): ("g_work_unit_tb", "g_work_unit_sk"),
    ("g_cr_tb", "g_lob_hrarchy_sk"): ("g_lob_hrarchy_tb", "g_lob_hrarchy_sk"),
    ("g_cr_tb", "g_note_set_sk"): ("g_note_set_tb", "g_note_set_sk"),
    ("g_cr_tb", "g_rep_sk"): ("g_rep_tb", "g_rep_sk"),
    ("g_cr_tb", "g_sprvsr_revwd_work_unit_sk"): ("g_work_unit_tb", "g_work_unit_sk"),
    ("g_cr_tb", "r_lob_cd"): ("r_lob_dtl_tb", "r_lob_cd"),
    ("g_crspd_cat_tb", "g_call_script_sk"): ("g_call_script_tb", "g_call_script_sk"),
    ("g_crspd_cat_tb", "g_dflt_route_to_work_unit_sk"): ("g_work_unit_tb", "g_work_unit_sk"),
    ("g_e_adr_usg_tb", "g_cmn_enty_sk"): ("g_cmn_enty_tb", "g_cmn_enty_sk"),
    ("g_e_adr_usg_tb", "g_e_adr_sk"): ("g_e_adr_tb", "g_e_adr_sk"),
    ("g_phone_usg_tb", "g_cmn_enty_sk"): ("g_cmn_enty_tb", "g_cmn_enty_sk"),
    ("g_phone_usg_tb", "g_phone_sk"): ("g_phone_tb", "g_phone_sk"),
    ("g_pye_pyr_eft_setup_tb", "g_bank_adr_sk"): ("g_adr_tb", "g_adr_sk"),
    ("g_pye_pyr_eft_setup_tb", "g_cmn_enty_sk"): ("g_pye_pyr_tb", "g_cmn_enty_sk"),
    ("g_pye_pyr_eft_setup_tb", "g_prov_adr_sk"): ("g_adr_tb", "g_adr_sk"),
    ("g_pye_pyr_tb", "g_cmn_enty_sk"): ("g_cmn_enty_tb", "g_cmn_enty_sk"),
    ("g_pye_pyr_tb", "g_note_set_sk"): ("g_note_set_tb", "g_note_set_sk"),
    ("g_rep_tb", "g_note_set_sk"): ("g_note_set_tb", "g_note_set_sk"),
    ("g_rep_tb", "g_rep_cmn_enty_sk"): ("g_cmn_enty_tb", "g_cmn_enty_sk"),
    ("g_spec_enty_tb", "g_spec_enty_sk"): ("g_cmn_enty_tb", "g_cmn_enty_sk"),
    ("g_spec_enty_tb", "r_lob_cd"): ("r_lob_dtl_tb", "r_lob_cd"),
    ("g_user_tb", "g_case_fltr_nam"): ("g_case_fltr_tb", "g_case_fltr_nam"),
    ("g_user_tb", "g_cr_fltr_nam"): ("g_cr_fltr_tb", "g_cr_fltr_nam"),
    ("g_user_tb", "g_user_work_unit_sk"): ("g_work_unit_tb", "g_work_unit_sk"),
    ("p_affl_tb", "p_grp_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_affl_tb", "p_mbr_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_affl_tx", "p_grp_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_affl_tx", "p_mbr_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_alt_id_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_appl_stat_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_blng_medm_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_care_crd_tx", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_clia_cert_tb", "p_clia_num"): ("p_clia_lab_tb", "p_clia_num"),
    ("p_clia_cert_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_clia_lab_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_clia_prov_tb", "p_clia_num"): ("p_clia_lab_tb", "p_clia_num"),
    ("p_clia_prov_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_cmn_lic_upload_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_cos_stat_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_dsh_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_dsh_tx", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_dtl_ext_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_dtl_tb", "g_cmn_enty_sk"): ("g_cmn_enty_tb", "g_cmn_enty_sk"),
    ("p_dtl_tb", "g_note_set_sk"): ("g_note_set_tb", "g_note_set_sk"),
    ("p_dtl_tx", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_eligible_recip_entry_form_tn", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_enrol_affl_tb", "p_enrol_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_enrol_affl_tb", "p_grp_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_enrol_affl_tb", "p_mbr_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_enrol_affl_tx", "p_enrol_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_enrol_alt_id_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_enrol_stat_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_enrol_stat_tx", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_enrol_tp_info_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_enrol_tp_txn_info_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_event_rsn_tb", "p_event_sk"): ("p_event_tb", "p_event_sk"),
    ("p_event_rsn_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_event_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_faci_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_glbl_endrsmnts_sought_tn", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_glbl_endrsmnts_tn", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_hcidea_alt_id_tb", "p_hcidea_sys_id"): ("p_hcidea_prov_tb", "p_hcidea_sys_id"),
    ("p_hcidea_prov_adr_mcaid_tb", "p_hcidea_adr_sys_id"): ("p_hcidea_prov_adr_tb", "p_hcidea_adr_sys_id"),
    ("p_hcidea_prov_adr_mcaid_tb", "p_hcidea_sys_id"): ("p_hcidea_prov_tb", "p_hcidea_sys_id"),
    ("p_hcidea_prov_adr_phone_tb", "p_hcidea_adr_sys_id"): ("p_hcidea_prov_adr_tb", "p_hcidea_adr_sys_id"),
    ("p_hcidea_prov_adr_phone_tb", "p_hcidea_sys_id"): ("p_hcidea_prov_tb", "p_hcidea_sys_id"),
    ("p_hcidea_prov_adr_spi_tb", "p_hcidea_adr_sys_id"): ("p_hcidea_prov_adr_tb", "p_hcidea_adr_sys_id"),
    ("p_hcidea_prov_adr_spi_tb", "p_hcidea_sys_id"): ("p_hcidea_prov_tb", "p_hcidea_sys_id"),
    ("p_hcidea_prov_adr_tb", "p_hcidea_sys_id"): ("p_hcidea_prov_tb", "p_hcidea_sys_id"),
    ("p_hcidea_prov_deg_tb", "p_hcidea_sys_id"): ("p_hcidea_prov_tb", "p_hcidea_sys_id"),
    ("p_hcidea_prov_lic_tb", "p_hcidea_sys_id"): ("p_hcidea_prov_tb", "p_hcidea_sys_id"),
    ("p_hcidea_prov_specl_tb", "p_hcidea_sys_id"): ("p_hcidea_prov_tb", "p_hcidea_sys_id"),
    ("p_hcidea_prov_txnmy_tb", "p_hcidea_sys_id"): ("p_hcidea_prov_tb", "p_hcidea_sys_id"),
    ("p_if_1915i_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_if_pt_ps_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_if_sandata_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_if_therap_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_interp_svc_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_lang_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_lic_cert_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_ltr_req_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_mc_prtcptn_tn", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_mcare_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_nonmed_prov_recip_tn", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_nppes_npi_src_other_id_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_nppes_npi_src_txnmy_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_num_bed_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_nw_part_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_nw_part_tb", "r_nw_id"): ("r_prov_nw_tb", "r_nw_id"),
    ("p_ofc_hrs_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_oig_prov_match_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_oig_prov_xref_tb", "p_oig_sk"): ("p_oig_tb", "p_oig_sk"),
    ("p_oig_prov_xref_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_owner_xref_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_ownrshp_chg_req_tn", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_pbm_nw_prtcptn_tb", "p_nw_part_sk"): ("p_nw_part_tb", "p_nw_part_sk"),
    ("p_pbm_nw_prtcptn_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_prev_mcaid_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_prev_nam_tn", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_prog_info_req_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_prov_cnty_tn", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_qsp_prov_recip_tn", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_qsp_qstnr_initialed_resp_tn", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_qsp_qstnr_tn", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_qstnr_advrs_legal_actn_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_qstnr_exclsn_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_qstnr_other_state_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_qstnr_ovr_pmt_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_qstnr_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_ra_medm_tb", "g_prov_adr_sk"): ("g_adr_tb", "g_adr_sk"),
    ("p_ra_medm_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_ra_medm_tx", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_req_attach_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_reval_stat_tn", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_revldtn_appl_stat_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_revldtn_stat_trkng_tb", "p_revldtn_trkng_sk"): ("p_revldtn_appl_stat_tb", "p_revldtn_trkng_sk"),
    ("p_revldtn_stat_trkng_tb", "p_sys_id"): ("p_revldtn_appl_stat_tb", "p_sys_id"),
    ("p_rpt_pharm_upd_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_rsk_scrn_tn", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_scrng_risk_lvl_asgn_hist_tb", "p_scrng_sk"): ("p_scrng_tb", "p_scrng_sk"),
    ("p_scrng_risk_lvl_asgn_hist_tb", "p_sys_id"): ("p_scrng_tb", "p_sys_id"),
    ("p_specl_need_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_specl_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_trng_crse_tb", "g_note_set_sk"): ("g_note_set_tb", "g_note_set_sk"),
    ("p_trng_rgstr_tb", "g_cmn_enty_sk"): ("g_cmn_enty_tb", "g_cmn_enty_sk"),
    ("p_trng_rgstr_tb", "p_trng_crse_id"): ("p_trng_sessn_tb", "p_trng_crse_id"),
    ("p_trng_rgstr_tb", "p_trng_sessn_id"): ("p_trng_sessn_tb", "p_trng_sessn_id"),
    ("p_trng_sessn_tb", "g_note_set_sk"): ("g_note_set_tb", "g_note_set_sk"),
    ("p_trng_sessn_tb", "p_trng_crse_id"): ("p_trng_crse_tb", "p_trng_crse_id"),
    ("p_tx_tb", "g_cmn_enty_sk"): ("g_cmn_enty_tb", "g_cmn_enty_sk"),
    ("p_txnmy_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_ty_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("p_web_dsply_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("r_list_dtl_tb", "r_func_area_cd"): ("r_list_hdr_tb", "r_func_area_cd"),
    ("r_list_dtl_tb", "r_list_num"): ("r_list_hdr_tb", "r_list_num"),
    ("r_mpst_hdr_tb", "g_note_set_sk"): ("g_note_set_tb", "g_note_set_sk"),
    ("r_prov_nw_tb", "g_cmn_enty_sk"): ("g_cmn_enty_tb", "g_cmn_enty_sk"),
    ("r_prov_nw_tb", "g_note_set_sk"): ("g_note_set_tb", "g_note_set_sk"),
    ("r_prov_nw_tb", "p_mco_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("r_vv_tb", "r_vv_domain_nam"): ("r_vv_domain_tb", "r_vv_domain_nam"),
    ("w_tp_prov_xref_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("w_tp_prov_xref_tb", "w_tp_id"): ("w_tp_tb", "w_tp_id"),
    ("w_tp_tb", "g_cmn_enty_sk"): ("g_cmn_enty_tb", "g_cmn_enty_sk"),
    ("w_tp_tb", "g_note_set_sk"): ("g_note_set_tb", "g_note_set_sk"),
    ("w_tp_tb", "p_sys_id"): ("p_dtl_tb", "p_sys_id"),
    ("w_tp_tb", "t_carr_id"): ("t_carr_tb", "t_carr_id"),

}

_KNOWN_ROOT_PARENTS = {
    "g_cmn_enty_tb", "g_adr_tb", "p_dtl_tb", "p_event_tb", "p_hcidea_prov_tb",
    "p_nw_part_tb", "p_trng_crse_tb", "g_note_set_tb", "g_phone_tb", "g_e_adr_tb"
}


class DataGenerator:
    """
    Generates synthetic rows for all tables using learned ColumnProfiles and RulesEngine rules.
    """

    def __init__(
        self,
        profiles      : dict[str, dict[str, ColumnProfile]],
        output_dir    : Path,
        rows_per_table: int = 1000,
        seed          : int = 12345,
        rules_engine  : Optional[RulesEngine] = None,
    ) -> None:
        self._profiles     = profiles
        self._out_dir      = output_dir
        self._rows         = rows_per_table
        self._seed         = seed
        self._rules_engine = rules_engine or RulesEngine()

        random.seed(seed)
        self._fake = Faker()
        Faker.seed(seed)

        self._out_dir.mkdir(parents=True, exist_ok=True)

        self._pk_registry: dict[str, dict[str, list[Any]]] = {}
        self._fk_map: dict[tuple[str, str], tuple[str, str]] = {}
        self._unique_registry: dict[str, set[Any]] = {}

        self._parent_of: dict[str, tuple[str, str]] = {}
        self._order = self._build_fk_map_and_order()

    def generate_all(self) -> dict[str, int]:
        results: dict[str, int] = {}
        remaining = [t for t in self._order if t in self._profiles]
        max_rounds = len(remaining) + 2

        for round_num in range(max_rounds):
            if not remaining:
                break

            generated_this_round: list[str] = []
            deferred: list[str] = []

            for table in remaining:
                if self._is_table_ready(table):
                    try:
                        count = self._generate_table(table)
                        results[table] = count
                        logger.info("  [R%d] Generated %d rows for %s.", round_num + 1, count, table)
                    except Exception as exc:  # noqa: BLE001
                        logger.error("  Failed %s: %s", table, exc, exc_info=True)
                        results[table] = 0
                    generated_this_round.append(table)
                else:
                    deferred.append(table)

            if not generated_this_round and deferred:
                logger.warning("No progress; forcing %d deferred tables: %s", len(deferred), deferred)
                for table in deferred:
                    try:
                        count = self._generate_table(table)
                        results[table] = count
                        logger.info("  [Force] Generated %d rows for %s.", count, table)
                    except Exception as exc:  # noqa: BLE001
                        logger.error("  Failed %s: %s", table, exc, exc_info=True)
                        results[table] = 0
                remaining = []
                break

            remaining = deferred

        logger.info("Post-generation FK orphan repair pass ...")
        repaired = self._fix_orphan_fks()
        if repaired:
            logger.warning("  Repaired %d orphan FK values.", repaired)
        else:
            logger.info("  FK integrity OK — zero orphans.")

        return results

    def generate_one(self, table_name: str) -> int:
        return self._generate_table(table_name)

    def output_path(self, table_name: str) -> Path:
        return self._out_dir / f"{table_name.upper()}.csv"

    def validate_fk_integrity(self) -> dict[tuple[str, str], int]:
        report: dict[tuple[str, str], int] = {}
        for (child_tbl, child_col), (parent_tbl, parent_col) in self._fk_map.items():
            parent_pool = set(
                str(v) for v in
                self._pk_registry.get(parent_tbl, {}).get(parent_col, [])
            )
            if not parent_pool:
                continue

            csv_path = self.output_path(child_tbl)
            if not csv_path.exists():
                continue

            with open(csv_path, newline="", encoding="utf-8") as fh:
                rows = list(csv.DictReader(fh))

            child_vals = [
                str(r.get(child_col, "") or "")
                for r in rows
                if r.get(child_col, "")
            ]
            orphans = [v for v in child_vals if v not in parent_pool]
            if orphans:
                report[(child_tbl, child_col)] = len(orphans)
                logger.warning(
                    "  FK ORPHANS: %s.%s -> %s.%s : %d/%d are orphans",
                    child_tbl, child_col, parent_tbl, parent_col,
                    len(orphans), len(child_vals),
                )
        return report

    def _is_table_ready(self, table: str) -> bool:
        for col in self._profiles.get(table, {}):
            mapping = self._fk_map.get((table, col))
            if mapping:
                p_tbl, p_col = mapping
                if not self._pk_registry.get(p_tbl, {}).get(p_col, []):
                    return False
        return True

    def _identify_pk_columns(self) -> dict[str, tuple[str, str]]:
        col_table_map: dict[str, set[str]] = {}
        for tbl, cols in self._profiles.items():
            for col in cols:
                col_table_map.setdefault(col, set()).add(tbl)

        parent_of: dict[str, tuple[str, str]] = {}
        for col, tables in col_table_map.items():
            if len(tables) == 1:
                only_tbl = next(iter(tables))
                parent_of[col] = (only_tbl, col)
                continue

            best_tbl   = None
            best_score = -9999.0

            for tbl in tables:
                prof  = self._profiles[tbl][col]
                score = 0.0

                if prof.strategy == STRAT_SEQUENTIAL:
                    score += 25.0
                if prof.is_unique:
                    score += 15.0
                elif prof.strategy == STRAT_INT_RANGE:
                    score += 5.0

                tbl_stem = tbl.lower()
                for pre in ("p_", "g_", "t_", "l_"):
                    if tbl_stem.startswith(pre):
                        tbl_stem = tbl_stem[len(pre):]
                for suf in ("_tb", "_tx", "_tn"):
                    if tbl_stem.endswith(suf):
                        tbl_stem = tbl_stem[: -len(suf)]

                has_own_surrogate = False
                for other_col in self._profiles[tbl]:
                    if other_col == col:
                        continue
                    oc = _strip_prefix(other_col)
                    if oc in (f"{tbl_stem}_sk", f"{tbl_stem}_sys_id", f"{tbl_stem}_id"):
                        has_own_surrogate = True
                        break

                if has_own_surrogate:
                    score -= 20.0
                else:
                    score += 30.0

                if prof.strategy == STRAT_SEQUENTIAL and prof.int_start > 0:
                    score -= prof.int_start / 1_000_000_000.0

                if score > best_score:
                    best_score = score
                    best_tbl   = tbl

            if best_tbl:
                parent_of[col] = (best_tbl, col)

        return parent_of

    def _build_fk_map_and_order(self) -> list[str]:
        all_tables = list(self._profiles.keys())
        self._parent_of = self._identify_pk_columns()

        deps: dict[str, set[str]] = {t: set() for t in all_tables}
        self._fk_map = {}

        for (child_tbl, child_col), (p_tbl, p_col) in PROVIDER_FK_MAP.items():
            if (child_tbl not in self._profiles
                    or child_col not in self._profiles.get(child_tbl, {})
                    or p_tbl not in self._profiles):
                continue
            self._fk_map[(child_tbl, child_col)] = (p_tbl, p_col)
            deps[child_tbl].add(p_tbl)

        for child_tbl in all_tables:
            for child_col in self._profiles[child_tbl]:
                if (child_tbl, child_col) in self._fk_map:
                    continue
                # Removed heuristic matching to avoid cyclic dependencies.
                # All true FKs are now in PROVIDER_FK_MAP.

        in_deg = {t: len(deps[t]) for t in all_tables}
        queue  = [t for t in all_tables if in_deg[t] == 0]
        order: list[str] = []

        while queue:
            node = queue.pop(0)
            order.append(node)
            for t in all_tables:
                if node in deps[t]:
                    deps[t].discard(node)
                    in_deg[t] -= 1
                    if in_deg[t] == 0:
                        queue.append(t)

        for t in all_tables:
            if t not in order:
                order.append(t)

        return order

    def _generate_table(self, table_name: str) -> int:
        profiles = self._profiles[table_name]
        columns  = list(profiles.keys())
        out_path = self.output_path(table_name)

        fk_info: dict[str, tuple[str, str]] = {}
        for col in columns:
            mapping = self._fk_map.get((table_name, col))
            if mapping:
                p_tbl, p_col = mapping
                if (
                    p_tbl in self._pk_registry
                    and p_col in self._pk_registry[p_tbl]
                    and self._pk_registry[p_tbl][p_col]
                ):
                    fk_info[col] = (p_tbl, p_col)

        seq_state: dict[str, int] = {}
        for col, prof in profiles.items():
            if prof.strategy == STRAT_SEQUENTIAL:
                # Add a large random offset so multiple runs don't collide
                offset = random.randint(10000, 9000000)
                seq_state[col] = prof.int_start + offset

        # ── Guarantee every parent has ≥1 child row (round-robin pre-assignment) ─
        primary_fk_col: str | None = None
        primary_fk_pool: list = []
        for col in columns:
            mapping = self._fk_map.get((table_name, col))
            if mapping:
                p_tbl, p_col = mapping
                pool = self._pk_registry.get(p_tbl, {}).get(p_col, [])
                if pool and len(pool) > len(primary_fk_pool):
                    primary_fk_col  = col
                    primary_fk_pool = list(pool)

        rr_assignments: list = []
        if primary_fk_col and primary_fk_pool:
            shuffled = list(primary_fk_pool)
            random.shuffle(shuffled)
            # first n_pool rows: one per parent; extras: random
            rr_assignments = list(shuffled)
            extras = [random.choice(primary_fk_pool)
                      for _ in range(max(0, self._rows - len(primary_fk_pool)))]
            rr_assignments.extend(extras)
            random.shuffle(rr_assignments)

        rows: list[dict[str, Any]] = []
        for row_idx in range(self._rows):
            row: dict[str, Any] = {}
            for col in columns:
                if col == primary_fk_col and rr_assignments:
                    row[col] = rr_assignments[row_idx]   # guaranteed coverage
                else:
                    prof = profiles[col]
                    row[col] = self._generate_cell(
                        table_name, col, prof, fk_info, seq_state
                    )
            self._apply_row_constraints(table_name, row, profiles)
            for col in columns:
                if isinstance(row[col], (date, datetime)):
                    row[col] = self._format_date_val(row[col], profiles[col])
            rows.append(row)

        with open(out_path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=columns, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            writer.writerows(rows)

        self._register_pk_values(table_name, profiles, rows)
        return len(rows)

    def _register_pk_values(
        self,
        table_name: str,
        profiles  : dict[str, ColumnProfile],
        rows      : list[dict[str, Any]],
    ) -> None:
        self._pk_registry.setdefault(table_name, {})
        for col, prof in profiles.items():
            if prof.strategy == STRAT_SEQUENTIAL or prof.is_unique:
                vals = [r[col] for r in rows if r[col] is not None]
                if vals:
                    self._pk_registry[table_name].setdefault(col, []).extend(vals)

    def _fix_orphan_fks(self) -> int:
        total_repaired = 0
        for (child_tbl, child_col), (parent_tbl, parent_col) in self._fk_map.items():
            parent_pool = [
                str(v) for v in
                self._pk_registry.get(parent_tbl, {}).get(parent_col, [])
            ]
            if not parent_pool:
                continue

            csv_path = self.output_path(child_tbl)
            if not csv_path.exists():
                continue

            with open(csv_path, newline="", encoding="utf-8") as fh:
                reader  = csv.DictReader(fh)
                headers = reader.fieldnames or []
                rows    = list(reader)

            if child_col not in headers:
                continue

            parent_set = set(parent_pool)
            repaired   = 0
            for row in rows:
                val = row.get(child_col, "")
                if val and str(val) not in parent_set:
                    row[child_col] = random.choice(parent_pool)
                    repaired += 1

            if repaired:
                with open(csv_path, "w", newline="", encoding="utf-8") as fh:
                    writer = csv.DictWriter(fh, fieldnames=headers, quoting=csv.QUOTE_ALL)
                    writer.writeheader()
                    writer.writerows(rows)
                total_repaired += repaired

        return total_repaired

    def _generate_cell(
        self,
        table_name: str,
        col       : str,
        prof      : ColumnProfile,
        fk_info   : dict[str, tuple[str, str]],
        seq_state : dict[str, int],
    ) -> Any:
        if col in fk_info:
            p_tbl, p_col = fk_info[col]
            pool = self._pk_registry.get(p_tbl, {}).get(p_col, [])
            if pool:
                if prof.null_rate > 0 and random.random() < prof.null_rate:
                    return None
                return random.choice(pool)

        for attempt in range(150):
            val = self._generate_raw(table_name, col, prof, seq_state)
            if val is None:
                return None
            if isinstance(val, str) and prof.max_length and prof.max_length > 0:
                val = val[: prof.max_length]
            if not prof.is_unique:
                return val
            reg = self._unique_registry.setdefault(col, set())
            if val not in reg:
                reg.add(val)
                return val
        if isinstance(val, str) and prof.max_length and prof.max_length > 0:
            val = val[: prof.max_length]
        return val

    def _generate_raw(
        self,
        table_name: str,
        col       : str,
        prof      : ColumnProfile,
        seq_state : dict[str, int],
    ) -> Any:
        if prof.null_rate > 0 and random.random() < prof.null_rate:
            return None

        # Check rules engine
        rule = self._rules_engine.get_rule_for_column(table_name, col)
        if rule:
            rule_val = self._rules_engine.generate_value(rule)
            if rule_val is not None:
                return rule_val

        s = prof.strategy

        if s == STRAT_NULL:
            return None
        if s == STRAT_SEQUENTIAL:
            seq_state[col] += prof.int_step
            return seq_state[col]
        if s == STRAT_INT_RANGE:
            return random.randint(prof.int_min, max(prof.int_max, prof.int_min))
        if s == STRAT_FLOAT_RANGE:
            return round(random.uniform(prof.float_min, prof.float_max), 2)
        if s == STRAT_ENUM:
            if not prof.sample_values:
                return None
            return random.choices(prof.sample_values, weights=prof.weights, k=1)[0]
        if s == STRAT_DATE:
            return self._random_date(prof)
        if s == STRAT_TIMESTAMP:
            return self._random_timestamp(prof)
        if s == STRAT_RULE:
            if prof.regex_pattern:
                try:
                    import rstr
                    return rstr.xeger(prof.regex_pattern)
                except Exception:
                    return self._fake.bothify(prof.regex_pattern.replace("[0-9]", "#").replace("[A-Z]", "?"))
            return self._call_faker(prof.faker_tag, prof.max_length)
        if s == STRAT_FAKER:
            val = self._call_faker(prof.faker_tag, prof.max_length)
            if prof.strip_non_digits:
                val = re.sub(r"\D", "", val)
            if prof.max_length and len(val) > prof.max_length:
                val = val[: prof.max_length]
            return val
        if s == STRAT_FREE_TEXT:
            if not prof.sample_values:
                return None
            return random.choice(prof.sample_values)
        return None

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
        return datetime(
            rand_d.year, rand_d.month, rand_d.day,
            random.randint(0, 23),
            random.randint(0, 59),
            random.randint(0, 59),
            random.randint(0, 999999),
        )

    def _apply_row_constraints(
        self,
        table_name: str,
        row       : dict[str, Any],
        profiles  : dict[str, ColumnProfile],
    ) -> None:
        # Evaluate conditional rules from RulesEngine
        for col in row:
            rule = self._rules_engine.get_rule_for_column(table_name, col, row)
            if rule and rule.applies_to and "condition" in rule.applies_to:
                val = self._rules_engine.generate_value(rule, row)
                if val is not None:
                    row[col] = val

        # Audit columns override
        for col in row:
            if col in ("g_aud_user_id", "g_aud_add_user_id",
                       "g_aud_upd_user_id", "g_web_user_id", "audit_user"):
                row[col] = AUDIT_USER

        now_dt  = datetime.now()
        add_col = next((c for c in row if c in ("g_aud_add_ts", "add_dt", "crt_ts")), None)
        aud_col = next((c for c in row if c in ("g_aud_ts", "upd_ts", "mod_ts")), None)

        if add_col:
            row[add_col] = now_dt
        if aud_col:
            row[aud_col] = now_dt

        begin_patterns = ["beg_dt", "start_dt", "eff_dt", "add_dt", "bth_dt", "dob_dt", "crt_ts", "effective_dt"]
        end_patterns   = ["end_dt", "term_dt", "trmn_dt", "cancel_dt", "rever_dt", "exp_dt", "expr_dt", "discont_dt", "termination_dt"]

        begins = [c for c in row if row[c] is not None and any(p in c for p in begin_patterns)]
        ends   = [c for c in row if row[c] is not None and any(p in c for p in end_patterns)]

        def _as_date(v: Any) -> Optional[date]:
            if isinstance(v, datetime):
                return v.date()
            if isinstance(v, date):
                return v
            if isinstance(v, str):
                return _parse_date_bound(v)
            return None

        for b_col in begins:
            for e_col in ends:
                b_val = row[b_col]
                e_val = row[e_col]
                b_d = _as_date(b_val)
                e_d = _as_date(e_val)
                if b_d and e_d and e_d <= b_d:
                    new_e = b_d + timedelta(days=random.randint(30, 365 * 5))
                    if isinstance(e_val, datetime):
                        row[e_col] = datetime.combine(new_e, e_val.time())
                    elif isinstance(e_val, date):
                        row[e_col] = new_e
                    elif isinstance(e_val, str):
                        row[e_col] = self._format_date_val(new_e, profiles[e_col])

    def _format_date_val(self, val: date | datetime, prof: ColumnProfile) -> str:
        if isinstance(val, datetime):
            if prof.is_oracle_fmt:
                mon = _MONTH_FROM_NUM[val.month]
                h12 = val.hour % 12 or 12
                mer = "AM" if val.hour < 12 else "PM"
                ns  = val.microsecond * 1000
                return (
                    f"{val.day:02d}-{mon}-{str(val.year)[-2:]:>02s} "
                    f"{h12:02d}.{val.minute:02d}.{val.second:02d}.{ns:09d} {mer}"
                )
            return val.strftime("%Y-%m-%d %H:%M:%S.%f")
        else:
            if prof.is_oracle_fmt:
                mon = _MONTH_FROM_NUM[val.month]
                return f"{val.day:02d}-{mon}-{str(val.year)[-2:]:>02s}"
            return val.isoformat()

    def _call_faker(self, tag: str, max_length: int) -> str:
        fake = self._fake

        if tag == "audit_user":
            return AUDIT_USER

        if tag == "license":
            states = ["TX", "CA", "NY", "FL", "IL", "PA", "OH", "GA", "NC", "MI", "ND"]
            return f"{random.choice(states)}-MD-{random.randint(10000, 99999)}"

        if tag == "npi":
            # 10-digit NPI: starts with 1 or 2, 9 digits + Luhn check digit
            prefix = str(random.choice([1, 2]))
            body = "".join(str(random.randint(0, 9)) for _ in range(8))
            digits = [int(d) for d in (prefix + body)]
            # Luhn calculation for NPI prefix 80840
            full_prefix = [8, 0, 8, 4, 0] + digits
            doubled = [(d * 2 if i % 2 == 0 else d) for i, d in enumerate(reversed(full_prefix))]
            total = sum(d - 9 if d > 9 else d for d in doubled)
            checksum = (10 - (total % 10)) % 10
            return f"{prefix}{body}{checksum}"

        if tag == "dea":
            # DEA: 2 letters (1st: A/B/F/G/M/P) + 6 digits + 7th checksum digit
            first = random.choice(["A", "B", "F", "G", "M", "P"])
            second = fake.last_name()[0].upper()
            d = [random.randint(0, 9) for _ in range(6)]
            checksum = ((d[0] + d[2] + d[4]) + 2 * (d[1] + d[3] + d[5])) % 10
            return f"{first}{second}{''.join(map(str, d))}{checksum}"

        if tag == "tin":
            return "".join(str(random.randint(0, 9)) for _ in range(9))

        if tag == "uuid":
            return str(uuid.uuid4())

        if tag == "provider_id":
            return fake.bothify("??#######").upper()

        if tag == "company":
            prefixes = ["Sanford", "Mayo Clinic", "Mercy", "St. Jude", "Trinity", "Valley Care", "Midwest", "Centura", "Kaiser", "Methodist"]
            suffixes = ["Medical Center", "Health System", "Dialysis Center", "Physicians Group", "Hospital", "Specialty Clinic", "Lab Services"]
            return f"{random.choice(prefixes)} {random.choice(suffixes)}"

        if tag == "name":
            credentials = ["MD", "DO", "RN", "NP", "PA", "DPM"]
            return f"Dr. {fake.name()}, {random.choice(credentials)}"

        dispatch: dict[str, Any] = {
            "last_name"     : fake.last_name,
            "first_name"    : fake.first_name,
            "street_address": fake.street_address,
            "city"          : fake.city,
            "state_abbr"    : fake.state_abbr,
            "zipcode"       : fake.zipcode,
            "phone_number"  : fake.phone_number,
            "email"         : fake.email,
            "url"           : fake.url,
            "date_of_birth" : lambda: fake.date_of_birth(minimum_age=22, maximum_age=75).strftime("%Y-%m-%d"),
        }
        fn = dispatch.get(tag)
        if fn is None:
            return fake.word()
        return str(fn())
