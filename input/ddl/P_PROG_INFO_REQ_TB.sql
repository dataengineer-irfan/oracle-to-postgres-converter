--------------------------------------------------------
--  DDL for Table P_PROG_INFO_REQ_TB
--------------------------------------------------------

  CREATE TABLE "P_PROG_INFO_REQ_TB" ("P_SYS_ID" NUMBER(10,0), "P_PROG_INFO_REQ_SK" NUMBER(10,0), "P_PROG_INFO_REQ_CD" VARCHAR2(3), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_PROG_INFO_REQ_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_PROG_INFO_REQ_TB"."P_PROG_INFO_REQ_SK" IS 'Provider Program Information Request Surrogate Key'
   COMMENT ON COLUMN "P_PROG_INFO_REQ_TB"."P_PROG_INFO_REQ_CD" IS 'Provider Program Information Request Code'
   COMMENT ON COLUMN "P_PROG_INFO_REQ_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_PROG_INFO_REQ_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_PROG_INFO_REQ_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_PROG_INFO_REQ_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_PROG_INFO_REQ_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_PROG_INFO_REQ_TB"  IS 'The Provider Program Information Request Table.'
