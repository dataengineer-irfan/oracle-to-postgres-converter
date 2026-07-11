--------------------------------------------------------
--  DDL for Table P_ENROL_TP_TXN_INFO_TB
--------------------------------------------------------

  CREATE TABLE "P_ENROL_TP_TXN_INFO_TB" ("P_SYS_ID" NUMBER(10,0), "P_TXN_TP_INFO_SK" NUMBER(10,0), "P_TXN_TY_CD" VARCHAR2(5), "W_TXN_DRCTN_CD" VARCHAR2(2), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_ENROL_TP_TXN_INFO_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_ENROL_TP_TXN_INFO_TB"."P_TXN_TP_INFO_SK" IS 'Provider Enrollment Trading Partner Transaction Information Surrogate Key'
   COMMENT ON COLUMN "P_ENROL_TP_TXN_INFO_TB"."P_TXN_TY_CD" IS 'Provider Transaction Type Code'
   COMMENT ON COLUMN "P_ENROL_TP_TXN_INFO_TB"."W_TXN_DRCTN_CD" IS 'x12 transaction direction table 
(Eg. Inbound, Outbound)'
   COMMENT ON COLUMN "P_ENROL_TP_TXN_INFO_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_ENROL_TP_TXN_INFO_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_ENROL_TP_TXN_INFO_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_ENROL_TP_TXN_INFO_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_ENROL_TP_TXN_INFO_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_ENROL_TP_TXN_INFO_TB"  IS 'Provider Enrollment Trading Partner Transaction Information Table'
