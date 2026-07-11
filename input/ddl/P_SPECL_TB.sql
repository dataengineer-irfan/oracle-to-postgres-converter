--------------------------------------------------------
--  DDL for Table P_SPECL_TB
--------------------------------------------------------

  CREATE TABLE "P_SPECL_TB" ("P_SYS_ID" NUMBER(10,0), "P_SPECL_SK" NUMBER(10,0), "P_SPECL_CD" VARCHAR2(3), "P_SPECL_BEG_DT" DATE, "P_SPECL_END_DT" DATE DEFAULT '31-DEC-9999', "P_SPECL_CERT_NUM" VARCHAR2(10), "P_STATE_CD" VARCHAR2(2), "P_SPECL_CERT_BOARD_CD" VARCHAR2(40), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_SPECL_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_SPECL_TB"."P_SPECL_SK" IS 'Provider Specialty Surrogate Key'
   COMMENT ON COLUMN "P_SPECL_TB"."P_SPECL_CD" IS 'A code indicating a provider''s certified medical specialty.'
   COMMENT ON COLUMN "P_SPECL_TB"."P_SPECL_BEG_DT" IS 'The begin date of the provider''s specialty participation.'
   COMMENT ON COLUMN "P_SPECL_TB"."P_SPECL_END_DT" IS 'The end date of the provider''s specialty participation.'
   COMMENT ON COLUMN "P_SPECL_TB"."P_SPECL_CERT_NUM" IS 'The provider''s certification number.'
   COMMENT ON COLUMN "P_SPECL_TB"."P_STATE_CD" IS 'The standard 2 character abbreviation for the state.'
   COMMENT ON COLUMN "P_SPECL_TB"."P_SPECL_CERT_BOARD_CD" IS 'Provider License Board Name Code.'
   COMMENT ON COLUMN "P_SPECL_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_SPECL_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_SPECL_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_SPECL_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_SPECL_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_SPECL_TB"  IS 'The Provider Specialty Table contains the specialties that apply to specific providers.'
