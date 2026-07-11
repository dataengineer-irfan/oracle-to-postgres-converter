--------------------------------------------------------
--  DDL for Table P_CLIA_PROV_TB
--------------------------------------------------------

  CREATE TABLE "P_CLIA_PROV_TB" ("P_SYS_ID" NUMBER(10,0), "P_CLIA_PROV_SK" NUMBER(10,0), "P_CLIA_NUM" VARCHAR2(10), "P_CLIA_PROV_BEG_DT" DATE DEFAULT '01-JAN-0001', "P_CLIA_PROV_END_DT" DATE DEFAULT '31-DEC-9999', "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_CLIA_PROV_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_CLIA_PROV_TB"."P_CLIA_PROV_SK" IS 'Provider CLIA Surrogate Key'
   COMMENT ON COLUMN "P_CLIA_PROV_TB"."P_CLIA_NUM" IS 'The CLIA number assigned to the provider regarding the provider''s certification as a laboratory provider of services.  This field is updated through the HCFA OSCAR interface.'
   COMMENT ON COLUMN "P_CLIA_PROV_TB"."P_CLIA_PROV_BEG_DT" IS 'Provider CLIA Begin Date.'
   COMMENT ON COLUMN "P_CLIA_PROV_TB"."P_CLIA_PROV_END_DT" IS 'Provider CLIA End Date.'
   COMMENT ON COLUMN "P_CLIA_PROV_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_CLIA_PROV_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_CLIA_PROV_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_CLIA_PROV_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_CLIA_PROV_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_CLIA_PROV_TB"  IS 'The Provider CLIA Provider Table cross references the CLIA number to an internal MMIS provider system identifier (P_SYS_ID).'
