--------------------------------------------------------
--  DDL for Table P_TAX_NTC_TB
--------------------------------------------------------

  CREATE TABLE "P_TAX_NTC_TB" ("P_SYS_ID" NUMBER(10,0), "P_BKUP_WHOLD_IND" VARCHAR2(1), "P_1ST_BNOTE_DT" DATE, "P_1ST_BNOTE_YR_NUM" VARCHAR2(4), "P_2ND_BNOTE_DT" DATE, "P_2ND_BNOTE_YR_NUM" VARCHAR2(4), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_TAX_NTC_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_TAX_NTC_TB"."P_BKUP_WHOLD_IND" IS 'Provider Tax Backup Withhold Indicator.'
   COMMENT ON COLUMN "P_TAX_NTC_TB"."P_1ST_BNOTE_DT" IS 'The date of the first IRS B-notice'
   COMMENT ON COLUMN "P_TAX_NTC_TB"."P_1ST_BNOTE_YR_NUM" IS 'The tax year for which the first IRS B-notice was recevied.'
   COMMENT ON COLUMN "P_TAX_NTC_TB"."P_2ND_BNOTE_DT" IS 'The date of the second IRS B-notice.'
   COMMENT ON COLUMN "P_TAX_NTC_TB"."P_2ND_BNOTE_YR_NUM" IS 'The tax year for which the second IRS B-notice was received'
   COMMENT ON COLUMN "P_TAX_NTC_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_TAX_NTC_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_TAX_NTC_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_TAX_NTC_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_TAX_NTC_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_TAX_NTC_TB"  IS 'The Provider TAX Notice Table holds the providers IRS B-notice and withholding information by tax ID.'
