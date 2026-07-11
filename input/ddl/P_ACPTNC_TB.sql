--------------------------------------------------------
--  DDL for Table P_ACPTNC_TB
--------------------------------------------------------

  CREATE TABLE "P_ACPTNC_TB" ("P_SYS_ID" NUMBER(10,0), "P_ACPTNC_SK" NUMBER(10,0), "P_ACPTNC_CD" VARCHAR2(2), "P_ACPTNC_DT" DATE, "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_ACPTNC_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_ACPTNC_TB"."P_ACPTNC_SK" IS 'Provider Acceptance Sequence Number'
   COMMENT ON COLUMN "P_ACPTNC_TB"."P_ACPTNC_CD" IS 'Code stating the provider''s patient acceptance status'
   COMMENT ON COLUMN "P_ACPTNC_TB"."P_ACPTNC_DT" IS 'The date that the acceptance code goes into effect'
   COMMENT ON COLUMN "P_ACPTNC_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_ACPTNC_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_ACPTNC_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_ACPTNC_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_ACPTNC_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_ACPTNC_TB"  IS 'Provider Acceptance Table'
