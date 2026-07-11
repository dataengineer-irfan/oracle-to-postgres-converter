--------------------------------------------------------
--  DDL for Table P_LANG_TB
--------------------------------------------------------

  CREATE TABLE "P_LANG_TB" ("P_SYS_ID" NUMBER(10,0), "P_LANG_SK" NUMBER(10,0), "P_LANG_CD" VARCHAR2(2), "P_PRIM_LANG_IND" VARCHAR2(1), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_LANG_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_LANG_TB"."P_LANG_SK" IS 'Provider Language Surrogate Key'
   COMMENT ON COLUMN "P_LANG_TB"."P_LANG_CD" IS 'This is a language that the provider can support.'
   COMMENT ON COLUMN "P_LANG_TB"."P_PRIM_LANG_IND" IS 'A yes/no indicator which indicates which is the provider''s primary language.'
   COMMENT ON COLUMN "P_LANG_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_LANG_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_LANG_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_LANG_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_LANG_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_LANG_TB"  IS 'The Provider Language Table contains the languages that the provider can speak and/or interpret.'
