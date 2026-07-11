--------------------------------------------------------
--  DDL for Table P_APPL_STAT_TB
--------------------------------------------------------

  CREATE TABLE "P_APPL_STAT_TB" ("P_SYS_ID" NUMBER(10,0), "P_APPL_STAT_SK" NUMBER(10,0), "P_APPL_STAT_CD" VARCHAR2(3), "P_APPL_STAT_DT" DATE, "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_APPL_STAT_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_APPL_STAT_TB"."P_APPL_STAT_SK" IS 'Provider Application Status Surrogate Key'
   COMMENT ON COLUMN "P_APPL_STAT_TB"."P_APPL_STAT_CD" IS 'Provider application status.'
   COMMENT ON COLUMN "P_APPL_STAT_TB"."P_APPL_STAT_DT" IS 'Provider application status date.'
   COMMENT ON COLUMN "P_APPL_STAT_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_APPL_STAT_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_APPL_STAT_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_APPL_STAT_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_APPL_STAT_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_APPL_STAT_TB"  IS 'Provider Application Status Table'
