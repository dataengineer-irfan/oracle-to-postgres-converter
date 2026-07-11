--------------------------------------------------------
--  DDL for Table P_PROV_HRARCHY_TB
--------------------------------------------------------

  CREATE TABLE "P_PROV_HRARCHY_TB" ("P_PROV_HRARCHY_NUM" NUMBER(10,0), "P_PROV_HRARCHY_QLFR_CD" VARCHAR2(3), "P_PROV_HRARCHY_DESC" VARCHAR2(80), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_PROV_HRARCHY_TB"."P_PROV_HRARCHY_NUM" IS 'Provider Identifier Hierarchy Number'
   COMMENT ON COLUMN "P_PROV_HRARCHY_TB"."P_PROV_HRARCHY_QLFR_CD" IS 'Provider Identifier Hierarchy Qualifier Sequence Number'
   COMMENT ON COLUMN "P_PROV_HRARCHY_TB"."P_PROV_HRARCHY_DESC" IS 'Provider Identifier Hierarchy  Qualifier Description'
   COMMENT ON COLUMN "P_PROV_HRARCHY_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_PROV_HRARCHY_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_PROV_HRARCHY_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_PROV_HRARCHY_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_PROV_HRARCHY_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_PROV_HRARCHY_TB"  IS 'Used to establish the order of identifiers to be tested during Claims adjudication, to determine the distinct provider entity referenced by a claim ? Billing, Rendering, Referring, Attending, etc'
