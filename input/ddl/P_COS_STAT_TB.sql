--------------------------------------------------------
--  DDL for Table P_COS_STAT_TB
--------------------------------------------------------

  CREATE TABLE "P_COS_STAT_TB" ("P_SYS_ID" NUMBER(10,0), "P_COS_STAT_SK" NUMBER(10,0), "C_COS_CD" VARCHAR2(3), "P_COS_STAT_BEG_DT" DATE, "P_COS_STAT_END_DT" DATE DEFAULT '31-DEC-9999', "P_COS_STAT_RSN_CD" VARCHAR2(2), "P_COS_STAT_TY_CD" VARCHAR2(2), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_COS_STAT_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_COS_STAT_TB"."P_COS_STAT_SK" IS 'Provider Category of Service (COS) Surrogate Key'
   COMMENT ON COLUMN "P_COS_STAT_TB"."C_COS_CD" IS 'This field defines the Category of Service of a claim.  The category of service defines the type of service reflected in the claim.'
   COMMENT ON COLUMN "P_COS_STAT_TB"."P_COS_STAT_BEG_DT" IS 'Category of Service Begin Date'
   COMMENT ON COLUMN "P_COS_STAT_TB"."P_COS_STAT_END_DT" IS 'The end date of the COS status.  This is derived by the system and is always protected online.'
   COMMENT ON COLUMN "P_COS_STAT_TB"."P_COS_STAT_RSN_CD" IS 'The reason that the status was assigned.'
   COMMENT ON COLUMN "P_COS_STAT_TB"."P_COS_STAT_TY_CD" IS 'This is the status for a category of service for a  provider.'
   COMMENT ON COLUMN "P_COS_STAT_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_COS_STAT_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_COS_STAT_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_COS_STAT_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_COS_STAT_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_COS_STAT_TB"  IS 'The Provider Category of Service Status Table defines what categories of service the provider is eligible to perform.'
