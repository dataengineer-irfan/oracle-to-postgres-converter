--------------------------------------------------------
--  DDL for Table P_OIG_PROV_XREF_TB
--------------------------------------------------------

  CREATE TABLE "P_OIG_PROV_XREF_TB" ("P_SYS_ID" NUMBER(10,0), "P_OIG_SK" NUMBER(10,0), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_OIG_PROV_XREF_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_OIG_PROV_XREF_TB"."P_OIG_SK" IS 'A sequence number assigen to OIG records to make each row unique.'
   COMMENT ON COLUMN "P_OIG_PROV_XREF_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_OIG_PROV_XREF_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_OIG_PROV_XREF_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_OIG_PROV_XREF_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_OIG_PROV_XREF_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_OIG_PROV_XREF_TB"  IS 'The Provider Office Inspector General Table (OIG) is used to match providers with an OIG.'
