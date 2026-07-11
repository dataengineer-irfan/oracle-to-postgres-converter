--------------------------------------------------------
--  DDL for Table P_TRNG_CRSE_TB
--------------------------------------------------------

  CREATE TABLE "P_TRNG_CRSE_TB" ("P_TRNG_CRSE_ID" VARCHAR2(10), "P_TRNG_CRSE_STAT_CD" VARCHAR2(1), "P_TRNG_CRSE_TITLE_DESC" VARCHAR2(80), "P_TRNG_CRSE_TY_CD" VARCHAR2(1), "G_NOTE_SET_SK" NUMBER(10,0), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_TRNG_CRSE_TB"."P_TRNG_CRSE_ID" IS 'Provider Training Course Identifier'
   COMMENT ON COLUMN "P_TRNG_CRSE_TB"."P_TRNG_CRSE_STAT_CD" IS 'Provider Training Course Status Code'
   COMMENT ON COLUMN "P_TRNG_CRSE_TB"."P_TRNG_CRSE_TITLE_DESC" IS 'Provider Training Course Title Description'
   COMMENT ON COLUMN "P_TRNG_CRSE_TB"."P_TRNG_CRSE_TY_CD" IS 'Provider Training Course Type Code'
   COMMENT ON COLUMN "P_TRNG_CRSE_TB"."G_NOTE_SET_SK" IS 'Surrogate Key'
   COMMENT ON COLUMN "P_TRNG_CRSE_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_TRNG_CRSE_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_TRNG_CRSE_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_TRNG_CRSE_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_TRNG_CRSE_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_TRNG_CRSE_TB"  IS 'Provider Training Course Table'
