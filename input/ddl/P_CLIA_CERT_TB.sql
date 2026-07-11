--------------------------------------------------------
--  DDL for Table P_CLIA_CERT_TB
--------------------------------------------------------

  CREATE TABLE "P_CLIA_CERT_TB" ("P_CLIA_NUM" VARCHAR2(10), "P_CLIA_CERT_LI_NUM" VARCHAR2(2), "P_CLIA_CERT_TY_CD" VARCHAR2(1), "P_CLIA_CERT_BEG_DT" DATE DEFAULT '01-JAN-0001', "P_CLIA_CERT_END_DT" DATE DEFAULT '31-DEC-9999', "P_CLIA_LAB_TY_CD" VARCHAR2(1), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "P_CLIA_CERT_SEQ_NUM" NUMBER(5,0)) 

   COMMENT ON COLUMN "P_CLIA_CERT_TB"."P_CLIA_NUM" IS 'The CLIA number assigned to the provider regarding the provider''s certification as a laboratory provider of services.  This field is updated through the HCFA OSCAR interface.'
   COMMENT ON COLUMN "P_CLIA_CERT_TB"."P_CLIA_CERT_LI_NUM" IS 'Line item number for CLIA Certification.'
   COMMENT ON COLUMN "P_CLIA_CERT_TB"."P_CLIA_CERT_TY_CD" IS 'The type of CLIA certification that a provider has.'
   COMMENT ON COLUMN "P_CLIA_CERT_TB"."P_CLIA_CERT_BEG_DT" IS 'P_CLIA_CERT_EFF_DT'
   COMMENT ON COLUMN "P_CLIA_CERT_TB"."P_CLIA_CERT_END_DT" IS 'Prov. Cert Expiration Date'
   COMMENT ON COLUMN "P_CLIA_CERT_TB"."P_CLIA_LAB_TY_CD" IS 'Providers Lab Type code for CLIA number.'
   COMMENT ON COLUMN "P_CLIA_CERT_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_CLIA_CERT_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_CLIA_CERT_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_CLIA_CERT_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_CLIA_CERT_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_CLIA_CERT_TB"  IS 'The Provider CLIA Certification Table holds information on lab procedures that the provider is certified to perform.'
