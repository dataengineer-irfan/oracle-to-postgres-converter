--------------------------------------------------------
--  DDL for Table P_AFFL_TB
--------------------------------------------------------

  CREATE TABLE "P_AFFL_TB" ("P_GRP_SYS_ID" NUMBER(10,0), "P_MBR_SYS_ID" NUMBER(10,0), "P_AFFL_SK" NUMBER(10,0), "P_AFFL_BEG_DT" DATE, "P_AFFL_TY_CD" VARCHAR2(1), "P_AFFL_END_DT" DATE DEFAULT '31-DEC-9999', "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_AFFL_TB"."P_GRP_SYS_ID" IS 'This coulmn is used in the provider affilation table to store the P_SYS_ID of the group provider.'
   COMMENT ON COLUMN "P_AFFL_TB"."P_MBR_SYS_ID" IS 'This column is used in the provider affilaiton table to store the sys ID of the member provider.'
   COMMENT ON COLUMN "P_AFFL_TB"."P_AFFL_SK" IS 'Provider Affiliation Surrogate Key'
   COMMENT ON COLUMN "P_AFFL_TB"."P_AFFL_BEG_DT" IS 'Begin date of a provider''s affiliation with a group, etc.'
   COMMENT ON COLUMN "P_AFFL_TB"."P_AFFL_TY_CD" IS 'The type of affiliation that links a provider with another provider.'
   COMMENT ON COLUMN "P_AFFL_TB"."P_AFFL_END_DT" IS 'End date of a provider''s affiliation with a group, etc.'
   COMMENT ON COLUMN "P_AFFL_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_AFFL_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_AFFL_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_AFFL_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_AFFL_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_AFFL_TB"  IS 'The Provider Affiliation Table links groups to group members, billing agents (if billing agents exist) to their provider members, and associations to their members.'
