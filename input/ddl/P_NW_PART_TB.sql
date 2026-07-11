--------------------------------------------------------
--  DDL for Table P_NW_PART_TB
--------------------------------------------------------

  CREATE TABLE "P_NW_PART_TB" ("P_SYS_ID" NUMBER(10,0), "P_NW_PART_SK" NUMBER(10,0), "R_NW_ID" VARCHAR2(10), "P_NW_BEG_DT" DATE, "P_NW_END_DT" DATE DEFAULT '31-DEC-9999', "P_NW_STAT_CD" VARCHAR2(2), "P_NWST_RSN_CD" VARCHAR2(3), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_NW_PART_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_NW_PART_TB"."P_NW_PART_SK" IS 'Provider Network Participation Surrogate Key'
   COMMENT ON COLUMN "P_NW_PART_TB"."R_NW_ID" IS 'Reference Network ID.'
   COMMENT ON COLUMN "P_NW_PART_TB"."P_NW_BEG_DT" IS 'Provider Network Begin Date.'
   COMMENT ON COLUMN "P_NW_PART_TB"."P_NW_END_DT" IS 'Provider Network End Date.'
   COMMENT ON COLUMN "P_NW_PART_TB"."P_NW_STAT_CD" IS 'Provider Network Status Code.'
   COMMENT ON COLUMN "P_NW_PART_TB"."P_NWST_RSN_CD" IS 'Provider Network Status (NWST) Reason Code Describes why a provider''s status in a particular network changed (moved out of area, etc.)'
   COMMENT ON COLUMN "P_NW_PART_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_NW_PART_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_NW_PART_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_NW_PART_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_NW_PART_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_NW_PART_TB"  IS 'Provider Network Participation Table'
