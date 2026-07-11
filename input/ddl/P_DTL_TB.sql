--------------------------------------------------------
--  DDL for Table P_DTL_TB
--------------------------------------------------------

  CREATE TABLE "P_DTL_TB" ("P_SYS_ID" NUMBER(10,0), "P_TY_CLASS_CD" VARCHAR2(1), "P_REC_TY_CD" VARCHAR2(1) DEFAULT 'A', "P_APPL_NUM" VARCHAR2(15), "P_LOCN_CD" VARCHAR2(1), "P_RA_SORT_SEQ_CD" VARCHAR2(1), "P_RA_PRT_SUSP_CD" VARCHAR2(1), "P_PRACT_TY_CD" VARCHAR2(1), "P_INDIV_GRP_CD" VARCHAR2(1), "P_OWNER_TY_CD" VARCHAR2(1), "P_NF_CLASS_CD" VARCHAR2(2), "P_PHARM_CLASS_CD" VARCHAR2(2), "P_DBA_NAM" VARCHAR2(60), "P_DBA_ORG_IND" VARCHAR2(1), "P_DBA_LAST_NAM" VARCHAR2(35), "P_DBA_FIRST_NAM" VARCHAR2(25), "P_DBA_MID_NAM" VARCHAR2(25), "P_DBA_SFX_NAM" VARCHAR2(10), "P_NAM" VARCHAR2(60), "P_NAM_ORG_IND" VARCHAR2(1) DEFAULT 'N', "P_LAST_NAM" VARCHAR2(35), "P_FIRST_NAM" VARCHAR2(25), "P_MID_NAM" VARCHAR2(25), "P_SFX_NAM" VARCHAR2(10), "P_MCARE_FY_MO_NUM" VARCHAR2(2), "P_MCAID_FY_MO_NUM" VARCHAR2(2), "P_COST_STTLMT_DT" DATE, "P_BLLTN_MEDM_CD" VARCHAR2(1), "P_BLLTN_COPY_NUM" NUMBER(5,0), "P_MCARE_IND" VARCHAR2(1), "P_BKUP_WHOLD_IND" VARCHAR2(1), "P_MULTI_LOCN_IND" VARCHAR2(1), "P_PRFT_IND" VARCHAR2(1), "P_REVER_DT" DATE, "P_BLNG_CD" VARCHAR2(1), "P_PROF_TECH_CD" VARCHAR2(1), "P_IHS_IND" VARCHAR2(1), "P_SOLE_COMM_IND" VARCHAR2(1), "P_EPSDT_ONLY_IND" VARCHAR2(1), "P_ADD_DT" DATE, "P_SORT_NAM" VARCHAR2(60), "P_STATE_MATCH_IND" VARCHAR2(1), "P_PHNTC_SORT_NAM" VARCHAR2(4), "P_ENROL_ACTN_CD" VARCHAR2(1), "P_TPL_AUD_DT" DATE, "P_TPL_AUD_TY_CD" VARCHAR2(1), "P_DUPL_OVRRD_IND" VARCHAR2(1), "P_CANCEL_APPL_IND" VARCHAR2(1), "P_DOB_DT" DATE, "P_FSCL_END_MO_NUM" VARCHAR2(2), "P_BIRTH_CNTRY_CD" VARCHAR2(3), "P_GENDER_CD" VARCHAR2(1), "P_OPEN_24_IND" VARCHAR2(1), "P_BIRTH_STATE_CD" VARCHAR2(2), "P_RACE_CD" VARCHAR2(1), "P_TITLE_CD" VARCHAR2(5), "P_HNDCPD_ACCS_IND" VARCHAR2(1), "P_TEACH_HOSP_IND" VARCHAR2(1), "P_TDD_TTY_IND" VARCHAR2(1), "P_DBA_FMR_NAM" VARCHAR2(60), "P_IN_KIND_IND" VARCHAR2(1), "P_DBA_YRS_NUM" NUMBER(3,0), "P_DRIVE_THRU_IND" VARCHAR2(1), "P_CURR_ALT_ID" VARCHAR2(15), "P_CURR_ALT_ID_TY_CD" VARCHAR2(3), "P_PEER_GRP_CD" VARCHAR2(2), "P_OTHER_LANG_TEXT" VARCHAR2(40), "P_PHNTC_LAST_NAM" VARCHAR2(4), "P_PHNTC_FIRST_NAM" VARCHAR2(4), "P_PHARM_DLVRY_SVC_IND" VARCHAR2(1), "G_CMN_ENTY_SK" NUMBER(10,0), "G_NOTE_SET_SK" NUMBER(10,0), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_WEB_USER_ID" VARCHAR2(30), "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_DTL_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_DTL_TB"."P_TY_CLASS_CD" IS 'The Provider Type Class Code is the classification of the Provider Type.

1 = Physician, 2 = Dentist, 3 = Pharmacy, 4 = Institution'
   COMMENT ON COLUMN "P_DTL_TB"."P_REC_TY_CD" IS 'This field is used to segregate those provider records that are still in the enrollment process from those that have completed the process and have been accepted as enrolled providers.'
   COMMENT ON COLUMN "P_DTL_TB"."P_APPL_NUM" IS 'A unique number assigned to each provider enrollment application form. This number is used to track the progress of the provider''s enrollment up to approval or denial. The number is assigned by the system at the time the data from the enrollment for is en'
   COMMENT ON COLUMN "P_DTL_TB"."P_LOCN_CD" IS 'Indicates if the provider''s practice location is in-state, out-of-state or on the border.'
   COMMENT ON COLUMN "P_DTL_TB"."P_RA_SORT_SEQ_CD" IS 'This code indicates how the remittance advice is sorted before it is sent to the provider.'
   COMMENT ON COLUMN "P_DTL_TB"."P_RA_PRT_SUSP_CD" IS 'Whether to include Suspended claims into Remittance Advice'
   COMMENT ON COLUMN "P_DTL_TB"."P_PRACT_TY_CD" IS 'This code indicates the legal organization that the provider belongs to.'
   COMMENT ON COLUMN "P_DTL_TB"."P_INDIV_GRP_CD" IS 'The Provider Individual or Group Code identifies whether the provider?s practice is an individual or group practice, for example:

I ? Individual provider / sole proprietorship

G ? Group provider / corporate partnership

B ? Independent practitioner / sole proprietor group



 '
   COMMENT ON COLUMN "P_DTL_TB"."P_OWNER_TY_CD" IS 'Describes the type of ownership for the provider.'
   COMMENT ON COLUMN "P_DTL_TB"."P_NF_CLASS_CD" IS 'This code indicates what type of nursing care is provided.'
   COMMENT ON COLUMN "P_DTL_TB"."P_PHARM_CLASS_CD" IS 'This explains what type of business a pharmacy provider participates in.'
   COMMENT ON COLUMN "P_DTL_TB"."P_DBA_NAM" IS 'The provider''s "doing business as" name.'
   COMMENT ON COLUMN "P_DTL_TB"."P_DBA_ORG_IND" IS 'Indicates that the DBA name is an organizational name.'
   COMMENT ON COLUMN "P_DTL_TB"."P_DBA_LAST_NAM" IS 'The doing business as last name.'
   COMMENT ON COLUMN "P_DTL_TB"."P_DBA_FIRST_NAM" IS 'The doing business as first name.'
   COMMENT ON COLUMN "P_DTL_TB"."P_DBA_MID_NAM" IS 'The doing business as middle initial.'
   COMMENT ON COLUMN "P_DTL_TB"."P_DBA_SFX_NAM" IS 'The doing business as name suffix.'
   COMMENT ON COLUMN "P_DTL_TB"."P_NAM" IS 'The legal name of the provider.'
   COMMENT ON COLUMN "P_DTL_TB"."P_NAM_ORG_IND" IS 'Indicates that the legal name of the provider is organizational.'
   COMMENT ON COLUMN "P_DTL_TB"."P_LAST_NAM" IS 'The legal last name of a provider.'
   COMMENT ON COLUMN "P_DTL_TB"."P_FIRST_NAM" IS 'The legal first name of a provider.'
   COMMENT ON COLUMN "P_DTL_TB"."P_MID_NAM" IS 'The legal middle name of a provider.'
   COMMENT ON COLUMN "P_DTL_TB"."P_SFX_NAM" IS 'The legal suffix of a provider.'
   COMMENT ON COLUMN "P_DTL_TB"."P_MCARE_FY_MO_NUM" IS 'The month number in which the providers Medicare Fiscal Year begins.'
   COMMENT ON COLUMN "P_DTL_TB"."P_MCAID_FY_MO_NUM" IS 'The month in which the providers Medicaid Fiscal Year begins.'
   COMMENT ON COLUMN "P_DTL_TB"."P_COST_STTLMT_DT" IS 'Date of the provider''s cost settlement with the State.'
   COMMENT ON COLUMN "P_DTL_TB"."P_BLLTN_MEDM_CD" IS 'The medium used to send bulletins to the provider.'
   COMMENT ON COLUMN "P_DTL_TB"."P_BLLTN_COPY_NUM" IS 'Number of copies of bulletins the provider needs to receive.'
   COMMENT ON COLUMN "P_DTL_TB"."P_MCARE_IND" IS 'A y/n value indicating if medicare providers were requested.'
   COMMENT ON COLUMN "P_DTL_TB"."P_BKUP_WHOLD_IND" IS 'Indicates the provider''s current W9 or tax withholding status, as related to B-Notice processing.'
   COMMENT ON COLUMN "P_DTL_TB"."P_MULTI_LOCN_IND" IS 'This indicates whether a provider practices in multiple locations and has more than one provider number.  This indicator will have a value of ''Y'' of ''N''.  It will default to ''N'' when the row is inserted.'
   COMMENT ON COLUMN "P_DTL_TB"."P_PRFT_IND" IS 'This indicates if this provider is a profit of non-profit provider.  This indicator will have a value of ''Y'' of ''N''.  It will default to ''Y'' (for profit) when the row is inserted.'
   COMMENT ON COLUMN "P_DTL_TB"."P_REVER_DT" IS 'This indicates  the date by which the provider must reverify selected data.  It has a DATE format and will default to ''0001-01-01'' when the row  is inserted.'
   COMMENT ON COLUMN "P_DTL_TB"."P_BLNG_CD" IS 'This indicates who can bill (submit claims) and who can provide services.'
   COMMENT ON COLUMN "P_DTL_TB"."P_PROF_TECH_CD" IS 'Provider Professional Technical Indicator'
   COMMENT ON COLUMN "P_DTL_TB"."P_IHS_IND" IS 'This indicates if the provider is an Indian Health Service provider.  This indicator will have a value of ''Y'' or ''N''.  It will default to ''N'' when the row is inserted.'
   COMMENT ON COLUMN "P_DTL_TB"."P_SOLE_COMM_IND" IS 'This indicates whether the provider participates in a community program.  This indicator will have a value of ''Y'' or ''N''.  It will default to ''N'' when the row is inserted.'
   COMMENT ON COLUMN "P_DTL_TB"."P_EPSDT_ONLY_IND" IS 'This indicates that the provider can only provide services for the EPSDT program.  This indicator will have a value of ''Y'' or ''N''.  It will default to ''N'' when the row is inserted.'
   COMMENT ON COLUMN "P_DTL_TB"."P_ADD_DT" IS 'The date the provider was added to the system.'
   COMMENT ON COLUMN "P_DTL_TB"."P_SORT_NAM" IS 'This is the provider sort name.'
   COMMENT ON COLUMN "P_DTL_TB"."P_STATE_MATCH_IND" IS 'This field indicates if the provider is eligible for state matching funds.'
   COMMENT ON COLUMN "P_DTL_TB"."P_PHNTC_SORT_NAM" IS 'This is the provider phonetic sort name.'
   COMMENT ON COLUMN "P_DTL_TB"."P_ENROL_ACTN_CD" IS 'A code indicating if the provider enrollment form being processed is for an initial enrollment or for a change of ownership.'
   COMMENT ON COLUMN "P_DTL_TB"."P_TPL_AUD_DT" IS 'The date of the last TPL audit for this provider.'
   COMMENT ON COLUMN "P_DTL_TB"."P_TPL_AUD_TY_CD" IS 'Indicated the type of TPL audit last performed for this provider.'
   COMMENT ON COLUMN "P_DTL_TB"."P_DUPL_OVRRD_IND" IS 'This indicator is checked when the user wants to override a duplicate SSN or TIN condition during provider enrollment.'
   COMMENT ON COLUMN "P_DTL_TB"."P_CANCEL_APPL_IND" IS 'This is an indicator for canceling a provider application.'
   COMMENT ON COLUMN "P_DTL_TB"."P_DOB_DT" IS 'Provider Date of Birth'
   COMMENT ON COLUMN "P_DTL_TB"."P_FSCL_END_MO_NUM" IS 'This indicates the month when the fiscal year ends for the provider.  Default to 00.'
   COMMENT ON COLUMN "P_DTL_TB"."P_BIRTH_CNTRY_CD" IS 'Country where the provider was born'
   COMMENT ON COLUMN "P_DTL_TB"."P_GENDER_CD" IS 'This code represents the provider''s gender.'
   COMMENT ON COLUMN "P_DTL_TB"."P_OPEN_24_IND" IS 'Tells if a provider is open 24 hours.'
   COMMENT ON COLUMN "P_DTL_TB"."P_BIRTH_STATE_CD" IS 'State where the provider was born'
   COMMENT ON COLUMN "P_DTL_TB"."P_RACE_CD" IS 'Provider Race Code.'
   COMMENT ON COLUMN "P_DTL_TB"."P_TITLE_CD" IS 'The provider''s title (MD, RN, LPN, etc...)'
   COMMENT ON COLUMN "P_DTL_TB"."P_HNDCPD_ACCS_IND" IS 'Provider Handicapped Accessible Indicator.'
   COMMENT ON COLUMN "P_DTL_TB"."P_TEACH_HOSP_IND" IS 'Provider Teach Hospital Indicator.'
   COMMENT ON COLUMN "P_DTL_TB"."P_TDD_TTY_IND" IS 'Provider TDD TTY Indicator'
   COMMENT ON COLUMN "P_DTL_TB"."P_DBA_FMR_NAM" IS 'Provider Name'
   COMMENT ON COLUMN "P_DTL_TB"."P_IN_KIND_IND" IS 'Provider In Kind Indicator

If Yes, the provider is a type of state agency that provides Medicaid services.  It is used during final payment calculations if a provider is in-kind, the payment is reduced to the amount that will be covered by Federal match money, so additional state-budgeted money is not transferred from DHHS to the other agency.'
   COMMENT ON COLUMN "P_DTL_TB"."P_DBA_YRS_NUM" IS 'The doing business as Year.'
   COMMENT ON COLUMN "P_DTL_TB"."P_DRIVE_THRU_IND" IS 'Provider Drive Through Indicator.'
   COMMENT ON COLUMN "P_DTL_TB"."P_CURR_ALT_ID" IS 'Provider Current Alternate ID.'
   COMMENT ON COLUMN "P_DTL_TB"."P_CURR_ALT_ID_TY_CD" IS 'The Provider Alternate Identifier Type Code identifies the source of the identifier.'
   COMMENT ON COLUMN "P_DTL_TB"."P_PEER_GRP_CD" IS 'Provider Peer Group Code'
   COMMENT ON COLUMN "P_DTL_TB"."P_OTHER_LANG_TEXT" IS 'Provider Other Language Code'
   COMMENT ON COLUMN "P_DTL_TB"."P_PHNTC_LAST_NAM" IS 'Provider Phonetic Last Name'
   COMMENT ON COLUMN "P_DTL_TB"."P_PHNTC_FIRST_NAM" IS 'Provider Phonetic First Name'
   COMMENT ON COLUMN "P_DTL_TB"."P_PHARM_DLVRY_SVC_IND" IS 'Indicates that the pharmacy offers delivery of pharmaceuticals or durable medical equipment.'
   COMMENT ON COLUMN "P_DTL_TB"."G_CMN_ENTY_SK" IS 'Common Entity Surrogate Key (pointing to the contact management data for the enrolled provider).'
   COMMENT ON COLUMN "P_DTL_TB"."G_NOTE_SET_SK" IS 'Surrogate Key'
   COMMENT ON COLUMN "P_DTL_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_DTL_TB"."G_WEB_USER_ID" IS 'User ID used in the web interface.'
   COMMENT ON COLUMN "P_DTL_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_DTL_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_DTL_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_DTL_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_DTL_TB"  IS 'The Provider Detail Table is the main provider Table, holding data that occurs once for a provider.'
