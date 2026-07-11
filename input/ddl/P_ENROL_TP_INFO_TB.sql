--------------------------------------------------------
--  DDL for Table P_ENROL_TP_INFO_TB
--------------------------------------------------------

  CREATE TABLE "P_ENROL_TP_INFO_TB" ("P_SYS_ID" NUMBER(10,0), "P_ISP_IND" VARCHAR2(1), "P_VND_NAM" VARCHAR2(50), "P_BLNG_AGENT_NAM" VARCHAR2(50), "W_SFTWR_NAM" VARCHAR2(50), "W_VER_ID" VARCHAR2(40), "W_SFTWR_PRTCL_CD" VARCHAR2(2), "G_CMN_ENTY_SK" NUMBER(10,0), "G_NOTE_SET_SK" NUMBER(10,0), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "W_TXN_DRCTN_CD" VARCHAR2(2)) 

   COMMENT ON COLUMN "P_ENROL_TP_INFO_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_ENROL_TP_INFO_TB"."P_ISP_IND" IS 'Provider Internet Service Provider Indicator'
   COMMENT ON COLUMN "P_ENROL_TP_INFO_TB"."P_VND_NAM" IS 'Provider Vendor Name'
   COMMENT ON COLUMN "P_ENROL_TP_INFO_TB"."P_BLNG_AGENT_NAM" IS 'Provider Billing Agency Name'
   COMMENT ON COLUMN "P_ENROL_TP_INFO_TB"."W_SFTWR_NAM" IS 'Name of the software product.'
   COMMENT ON COLUMN "P_ENROL_TP_INFO_TB"."W_VER_ID" IS 'Version identifier or number of the software.'
   COMMENT ON COLUMN "P_ENROL_TP_INFO_TB"."W_SFTWR_PRTCL_CD" IS 'e.g.

01    COMPLETE

02    KERMIT

03    MQ SERIES

04    SNA'
   COMMENT ON COLUMN "P_ENROL_TP_INFO_TB"."G_CMN_ENTY_SK" IS 'Surrogate Key'
   COMMENT ON COLUMN "P_ENROL_TP_INFO_TB"."G_NOTE_SET_SK" IS 'Surrogate Key'
   COMMENT ON COLUMN "P_ENROL_TP_INFO_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_ENROL_TP_INFO_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_ENROL_TP_INFO_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_ENROL_TP_INFO_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_ENROL_TP_INFO_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_ENROL_TP_INFO_TB"  IS 'Provider Enrollment Trading Partner Information Table'
