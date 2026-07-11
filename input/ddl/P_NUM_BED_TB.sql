--------------------------------------------------------
--  DDL for Table P_NUM_BED_TB
--------------------------------------------------------

  CREATE TABLE "P_NUM_BED_TB" ("P_SYS_ID" NUMBER(10,0), "P_NUM_BED_SK" NUMBER(10,0), "P_BED_TY_CD" VARCHAR2(2), "P_NUM_BED_BEG_DT" DATE, "P_NUM_BED_END_DT" DATE DEFAULT '31-DEC-9999', "P_BED_NUM" NUMBER(10,0), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_NUM_BED_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_NUM_BED_TB"."P_NUM_BED_SK" IS 'Provider Number Bed Surrogate Key'
   COMMENT ON COLUMN "P_NUM_BED_TB"."P_BED_TY_CD" IS 'Provider Bed Tyep Code..'
   COMMENT ON COLUMN "P_NUM_BED_TB"."P_NUM_BED_BEG_DT" IS 'The date when the number of beds 

could be used as accurate counts.'
   COMMENT ON COLUMN "P_NUM_BED_TB"."P_NUM_BED_END_DT" IS 'The date when the number of beds 

stop reflecting an exact count.'
   COMMENT ON COLUMN "P_NUM_BED_TB"."P_BED_NUM" IS 'Provider Bed Number.'
   COMMENT ON COLUMN "P_NUM_BED_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_NUM_BED_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_NUM_BED_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_NUM_BED_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_NUM_BED_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_NUM_BED_TB"  IS 'The Provider Number Bed Table contains counts of categories of hospital patients.'
