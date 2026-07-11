--------------------------------------------------------
--  DDL for Table P_LTR_REQ_TB
--------------------------------------------------------

  CREATE TABLE "P_LTR_REQ_TB" ("P_SYS_ID" NUMBER(10,0), "G_COTS_LTR_REQ_SK" NUMBER(10,0), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_LTR_REQ_TB"."P_SYS_ID" IS 'The p-sys-id is the internal primary index to the provider database.'
   COMMENT ON COLUMN "P_LTR_REQ_TB"."G_COTS_LTR_REQ_SK" IS 'System generated sequential number.  '
   COMMENT ON COLUMN "P_LTR_REQ_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_LTR_REQ_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_LTR_REQ_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_LTR_REQ_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_LTR_REQ_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_LTR_REQ_TB"  IS 'The Provider Letter Cross Reference Table. When events occur that require a letter to be sent to the provider, a row is inserted into this table serving as triggers for letter generation.'
