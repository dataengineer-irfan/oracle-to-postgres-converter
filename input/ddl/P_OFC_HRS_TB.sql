--------------------------------------------------------
--  DDL for Table P_OFC_HRS_TB
--------------------------------------------------------

  CREATE TABLE "P_OFC_HRS_TB" ("P_SYS_ID" NUMBER(10,0), "P_OFC_HRS_SK" NUMBER(10,0), "P_DAY_OF_WK_CD" VARCHAR2(1), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "P_OFC_CLOSE_TM_TEXT" VARCHAR2(10) DEFAULT 0, "P_OFC_OPEN_TM_TEXT" VARCHAR2(10) DEFAULT 0) 

   COMMENT ON COLUMN "P_OFC_HRS_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_OFC_HRS_TB"."P_OFC_HRS_SK" IS 'Provider Office Hours Surrogate Key'
   COMMENT ON COLUMN "P_OFC_HRS_TB"."P_DAY_OF_WK_CD" IS 'Idicator for which day of the week this provider is available.'
   COMMENT ON COLUMN "P_OFC_HRS_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_OFC_HRS_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_OFC_HRS_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_OFC_HRS_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_OFC_HRS_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_OFC_HRS_TB"  IS 'The Provider Office Hours Table contains Provider Managed Care office hours and days of the week.'
