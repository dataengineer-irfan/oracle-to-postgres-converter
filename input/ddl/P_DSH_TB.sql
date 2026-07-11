--------------------------------------------------------
--  DDL for Table P_DSH_TB
--------------------------------------------------------

  CREATE TABLE "P_DSH_TB" ("P_SYS_ID" NUMBER(10,0), "P_DSH_SK" NUMBER(10,0), "P_DSH_BEG_DT" DATE, "P_DSH_END_DT" DATE DEFAULT '31-DEC-9999', "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_DSH_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_DSH_TB"."P_DSH_SK" IS 'Provider Disproportionate Surrogate Key'
   COMMENT ON COLUMN "P_DSH_TB"."P_DSH_BEG_DT" IS 'This is the beginning date that the provider qualifies as being a disproportionate share provider.  The default tis current date.'
   COMMENT ON COLUMN "P_DSH_TB"."P_DSH_END_DT" IS 'This is the ending date that the provider qualifies as being a disproportionate share provider.  The default is "9999-12-31"'
   COMMENT ON COLUMN "P_DSH_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_DSH_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_DSH_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_DSH_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_DSH_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_DSH_TB"  IS 'The Provider Disproportionate Share Table holds information on the date spans that a provider is considered a disproportionate share provider.  This means the provider does a large amount of business with the State.'
