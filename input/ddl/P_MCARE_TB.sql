--------------------------------------------------------
--  DDL for Table P_MCARE_TB
--------------------------------------------------------

  CREATE TABLE "P_MCARE_TB" ("P_SYS_ID" NUMBER(10,0), "P_MCARE_SK" NUMBER(10,0), "P_MCARE_ALT_ID" VARCHAR2(15), "P_MCARE_PART_CD" VARCHAR2(3), "P_MCARE_BEG_DT" DATE, "P_MCARE_END_DT" DATE DEFAULT '31-DEC-9999', "T_CARR_ID" VARCHAR2(10), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_MCARE_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_MCARE_TB"."P_MCARE_SK" IS 'Provider Medicare Surrogate Key'
   COMMENT ON COLUMN "P_MCARE_TB"."P_MCARE_ALT_ID" IS 'The provider''s Medicare number.'
   COMMENT ON COLUMN "P_MCARE_TB"."P_MCARE_PART_CD" IS 'Provider Medicare Part Code.'
   COMMENT ON COLUMN "P_MCARE_TB"."P_MCARE_BEG_DT" IS 'The provider''s begin date of Medicare participation.'
   COMMENT ON COLUMN "P_MCARE_TB"."P_MCARE_END_DT" IS 'The provider''s end date of Medicare participation.'
   COMMENT ON COLUMN "P_MCARE_TB"."T_CARR_ID" IS 'The medicare carrier id.'
   COMMENT ON COLUMN "P_MCARE_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_MCARE_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_MCARE_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_MCARE_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_MCARE_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_MCARE_TB"  IS 'The Provider Medicare Table is used to cross reference a provider medicare ID''s to their Medicaid ID.'
