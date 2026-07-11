--------------------------------------------------------
--  DDL for Table P_TRNG_RGSTR_TB
--------------------------------------------------------

  CREATE TABLE "P_TRNG_RGSTR_TB" ("P_TRNG_CRSE_ID" VARCHAR2(10), "P_TRNG_SESSN_ID" VARCHAR2(10), "G_PROV_CMN_ENTY_SK" NUMBER(10,0), "G_PROV_CMN_ENTY_TY_CD" VARCHAR2(2), "P_EXTL_ENTY_ID" VARCHAR2(15), "P_EXTL_ENTY_ID_TY_CD" VARCHAR2(3), "P_TRNG_CNFRM_NUM" NUMBER(10,0), "P_TRNG_RGSTR_NUM" NUMBER(10,0), "P_TRNG_ATNDD_NUM" NUMBER(10,0), "P_TRNG_WAITG_LIST_IND" VARCHAR2(1), "P_TRNG_STAT_CD" VARCHAR2(1), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_TRNG_RGSTR_TB"."P_TRNG_CRSE_ID" IS 'Provider Training Course Identifier'
   COMMENT ON COLUMN "P_TRNG_RGSTR_TB"."P_TRNG_SESSN_ID" IS 'Provider Training Session Identifier'
   COMMENT ON COLUMN "P_TRNG_RGSTR_TB"."G_PROV_CMN_ENTY_SK" IS 'Surrogate Key for the Common Entity.  This value may be referred to as Payer ID on some UI screens.'
   COMMENT ON COLUMN "P_TRNG_RGSTR_TB"."G_PROV_CMN_ENTY_TY_CD" IS 'Common entity type code'
   COMMENT ON COLUMN "P_TRNG_RGSTR_TB"."P_EXTL_ENTY_ID" IS 'Provider Training External Entity Identifier'
   COMMENT ON COLUMN "P_TRNG_RGSTR_TB"."P_EXTL_ENTY_ID_TY_CD" IS 'Provider Training External Entity Identifier Type Code'
   COMMENT ON COLUMN "P_TRNG_RGSTR_TB"."P_TRNG_CNFRM_NUM" IS 'Provider Training Confirmation Number'
   COMMENT ON COLUMN "P_TRNG_RGSTR_TB"."P_TRNG_RGSTR_NUM" IS 'Provider Training Registered Number'
   COMMENT ON COLUMN "P_TRNG_RGSTR_TB"."P_TRNG_ATNDD_NUM" IS 'Provider Training Attended Number'
   COMMENT ON COLUMN "P_TRNG_RGSTR_TB"."P_TRNG_WAITG_LIST_IND" IS 'Provider Training Waiting List Indicator'
   COMMENT ON COLUMN "P_TRNG_RGSTR_TB"."P_TRNG_STAT_CD" IS 'Provider Training Status Code'
   COMMENT ON COLUMN "P_TRNG_RGSTR_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_TRNG_RGSTR_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_TRNG_RGSTR_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_TRNG_RGSTR_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_TRNG_RGSTR_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_TRNG_RGSTR_TB"  IS 'Provider Training Table'
