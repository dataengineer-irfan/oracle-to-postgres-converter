--------------------------------------------------------
--  DDL for Table P_PREV_MCAID_TB
--------------------------------------------------------

  CREATE TABLE "P_PREV_MCAID_TB" ("P_SYS_ID" NUMBER(10,0), "P_PREV_MCAID_SK" NUMBER(10,0), "P_PREV_MCAID_ALT_ID" VARCHAR2(15), "P_PREV_BEG_DT" DATE, "P_PREV_END_DT" DATE DEFAULT '31-DEC-9999', "P_FED_TAX_ID" VARCHAR2(9), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_PREV_MCAID_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_PREV_MCAID_TB"."P_PREV_MCAID_SK" IS 'Provider Previous Medicaid Surrogate Key'
   COMMENT ON COLUMN "P_PREV_MCAID_TB"."P_PREV_MCAID_ALT_ID" IS 'The previous Medicaid ID used by a provider.'
   COMMENT ON COLUMN "P_PREV_MCAID_TB"."P_PREV_BEG_DT" IS 'THe begining date of a previous Medicaid ID for a provider.'
   COMMENT ON COLUMN "P_PREV_MCAID_TB"."P_PREV_END_DT" IS 'The ending date of a previous Medicaid ID for a provider.'
   COMMENT ON COLUMN "P_PREV_MCAID_TB"."P_FED_TAX_ID" IS 'The provider''s federal tax identification number.'
   COMMENT ON COLUMN "P_PREV_MCAID_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_PREV_MCAID_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_PREV_MCAID_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_PREV_MCAID_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_PREV_MCAID_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_PREV_MCAID_TB"  IS 'Provider Previous Medicaid Table'
