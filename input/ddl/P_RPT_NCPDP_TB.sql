--------------------------------------------------------
--  DDL for Table P_RPT_NCPDP_TB
--------------------------------------------------------

  CREATE TABLE "P_RPT_NCPDP_TB" ("P_RPT_NCPDP_SK" NUMBER(10,0), "P_IFACE_PRCS_DT" DATE, "P_NCPDP_SUCCESS_IND" VARCHAR2(1), "P_MCAID_ALT_ID" VARCHAR2(15), "P_NCPDP_ALT_ID" VARCHAR2(15), "P_SORT_NAM" VARCHAR2(60), "P_NPI_ALT_ID" VARCHAR2(15), "B_NPI_BEG_DT" DATE, "B_NPI_END_DT" DATE, "P_NCPDP_UPD_CD" VARCHAR2(1), "P_ERR_FLD_NAM" VARCHAR2(30), "P_ERR_FLD_DATA" VARCHAR2(50), "P_ERR_MSG_TEXT" VARCHAR2(50), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_RPT_NCPDP_TB"."P_RPT_NCPDP_SK" IS 'Provider Report NCPDP Surrogate Key'
   COMMENT ON COLUMN "P_RPT_NCPDP_TB"."P_IFACE_PRCS_DT" IS 'Interface Process Date'
   COMMENT ON COLUMN "P_RPT_NCPDP_TB"."P_NCPDP_SUCCESS_IND" IS 'The indicator identifies if the record is an update record or an error record.'
   COMMENT ON COLUMN "P_RPT_NCPDP_TB"."P_MCAID_ALT_ID" IS 'Provider Medicaid ID'
   COMMENT ON COLUMN "P_RPT_NCPDP_TB"."P_NCPDP_ALT_ID" IS 'Provider NCPDP ID'
   COMMENT ON COLUMN "P_RPT_NCPDP_TB"."P_SORT_NAM" IS 'This is the provider sort name.'
   COMMENT ON COLUMN "P_RPT_NCPDP_TB"."P_NPI_ALT_ID" IS 'Provider NPI Number'
   COMMENT ON COLUMN "P_RPT_NCPDP_TB"."B_NPI_BEG_DT" IS 'NCPDP begin date coming from the interface'
   COMMENT ON COLUMN "P_RPT_NCPDP_TB"."B_NPI_END_DT" IS 'NCPDP begin date coming from the interface'
   COMMENT ON COLUMN "P_RPT_NCPDP_TB"."P_NCPDP_UPD_CD" IS 'NCPDP Update Code'
   COMMENT ON COLUMN "P_RPT_NCPDP_TB"."P_ERR_FLD_NAM" IS 'Name of the field due to what the NCPDP record got an error.'
   COMMENT ON COLUMN "P_RPT_NCPDP_TB"."P_ERR_FLD_DATA" IS 'Value in the field due to what the NCPDP record got an error.'
   COMMENT ON COLUMN "P_RPT_NCPDP_TB"."P_ERR_MSG_TEXT" IS 'Error Message that is thrown for the NCPDP record.'
   COMMENT ON COLUMN "P_RPT_NCPDP_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_RPT_NCPDP_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_RPT_NCPDP_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
