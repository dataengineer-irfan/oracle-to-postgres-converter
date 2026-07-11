--------------------------------------------------------
--  DDL for Table P_WEB_DSPLY_TB
--------------------------------------------------------

  CREATE TABLE "P_WEB_DSPLY_TB" ("P_SYS_ID" NUMBER(10,0), "P_DO_NOT_DSPLY_CD" VARCHAR2(2), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_WEB_DSPLY_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_WEB_DSPLY_TB"."P_DO_NOT_DSPLY_CD" IS 'This Code determines which fields should not be displayed on a provider''s web page.'
   COMMENT ON COLUMN "P_WEB_DSPLY_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_WEB_DSPLY_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_WEB_DSPLY_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_WEB_DSPLY_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_WEB_DSPLY_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_WEB_DSPLY_TB"  IS 'The Proivder Web Display Table will be used to determine which fields should not be displayed on a provider''s web page.'
