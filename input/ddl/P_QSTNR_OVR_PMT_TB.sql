--------------------------------------------------------
--  DDL for Table P_QSTNR_OVR_PMT_TB
--------------------------------------------------------

  CREATE TABLE "P_QSTNR_OVR_PMT_TB" ("P_SYS_ID" NUMBER(10,0), "P_QSTNR_SEQ_NUM" NUMBER(5,0), "P_QSTNR_FED_PROG_NAM" VARCHAR2(50), "P_QSTNR_FIRST_NAM" VARCHAR2(25), "P_QSTNR_LAST_NAM" VARCHAR2(35), "P_QSTNR_MI_NAM" VARCHAR2(1), "P_QSTNR_SFX_NAM" VARCHAR2(10), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_QSTNR_OVR_PMT_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_QSTNR_OVR_PMT_TB"."P_QSTNR_SEQ_NUM" IS 'Sequence Number'
   COMMENT ON COLUMN "P_QSTNR_OVR_PMT_TB"."P_QSTNR_FED_PROG_NAM" IS 'Provider Questionnaire Federal Program Name'
   COMMENT ON COLUMN "P_QSTNR_OVR_PMT_TB"."P_QSTNR_FIRST_NAM" IS 'Provider Questionnaire First Name'
   COMMENT ON COLUMN "P_QSTNR_OVR_PMT_TB"."P_QSTNR_LAST_NAM" IS 'Provider Questionnaire Last Name'
   COMMENT ON COLUMN "P_QSTNR_OVR_PMT_TB"."P_QSTNR_MI_NAM" IS 'Provider Questionnaire Middle Initial'
   COMMENT ON COLUMN "P_QSTNR_OVR_PMT_TB"."P_QSTNR_SFX_NAM" IS 'Provider Questionnaire Suffix Name'
   COMMENT ON COLUMN "P_QSTNR_OVR_PMT_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_QSTNR_OVR_PMT_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_QSTNR_OVR_PMT_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_QSTNR_OVR_PMT_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_QSTNR_OVR_PMT_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_QSTNR_OVR_PMT_TB"  IS 'Provider Questionnaire Over Payment Table'
