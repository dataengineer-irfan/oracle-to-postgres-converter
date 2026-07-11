--------------------------------------------------------
--  DDL for Table P_LIC_CERT_TB
--------------------------------------------------------

  CREATE TABLE "P_LIC_CERT_TB" ("P_SYS_ID" NUMBER(10,0), "P_LIC_CERT_SK" NUMBER(10,0), "P_LIC_CERT_NUM" VARCHAR2(15), "P_LIC_CERT_CD" VARCHAR2(4), "P_LIC_CERT_IND_CD" VARCHAR2(1), "P_LIC_CERT_BEG_DT" DATE, "P_LIC_CERT_END_DT" DATE DEFAULT '31-DEC-9999', "P_LIC_RSTRCT_CD" VARCHAR2(1) DEFAULT 'N', "P_LIC_VRFY_IND" VARCHAR2(1) DEFAULT 'N', "P_LIC_CERT_AGCY_CD" VARCHAR2(3), "P_LIC_PRMT_ID" VARCHAR2(30), "P_LIC_CERT_STATE_CD" VARCHAR2(2), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_LIC_CERT_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_LIC_CERT_TB"."P_LIC_CERT_SK" IS 'Provider License Certificate Surrogate Key'
   COMMENT ON COLUMN "P_LIC_CERT_TB"."P_LIC_CERT_NUM" IS 'The provider''s certification number.'
   COMMENT ON COLUMN "P_LIC_CERT_TB"."P_LIC_CERT_CD" IS 'The type of license certification for a provider.'
   COMMENT ON COLUMN "P_LIC_CERT_TB"."P_LIC_CERT_IND_CD" IS 'Tells whether the row is for a license or certification'
   COMMENT ON COLUMN "P_LIC_CERT_TB"."P_LIC_CERT_BEG_DT" IS 'Identifies the effective date of the provider''s license.'
   COMMENT ON COLUMN "P_LIC_CERT_TB"."P_LIC_CERT_END_DT" IS 'The date on which the provider''s license is to expire.'
   COMMENT ON COLUMN "P_LIC_CERT_TB"."P_LIC_RSTRCT_CD" IS 'The reason that a provider''s license is restricted.'
   COMMENT ON COLUMN "P_LIC_CERT_TB"."P_LIC_VRFY_IND" IS 'Indicates whether the provider''s license has been verified.'
   COMMENT ON COLUMN "P_LIC_CERT_TB"."P_LIC_CERT_AGCY_CD" IS 'Provider License Board Name Code.'
   COMMENT ON COLUMN "P_LIC_CERT_TB"."P_LIC_PRMT_ID" IS 'The name of the Permit holder associtated with the provider''s license or permit.'
   COMMENT ON COLUMN "P_LIC_CERT_TB"."P_LIC_CERT_STATE_CD" IS 'The provider''s certification State Code.'
   COMMENT ON COLUMN "P_LIC_CERT_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_LIC_CERT_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_LIC_CERT_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_LIC_CERT_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_LIC_CERT_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_LIC_CERT_TB"  IS 'The Provider License Certification Table contains license information for a provider.'
