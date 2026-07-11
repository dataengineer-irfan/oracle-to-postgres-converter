--------------------------------------------------------
--  DDL for Table P_OWNER_XREF_TB
--------------------------------------------------------

  CREATE TABLE "P_OWNER_XREF_TB" ("P_SYS_ID" NUMBER(10,0), "P_OWNER_TAX_ID" NUMBER(10,0), "P_OWNER_XREF_SK" NUMBER(10,0), "P_OWNER_BEG_DT" DATE, "P_FED_TAX_ID" VARCHAR2(9), "P_OWNER_END_DT" DATE DEFAULT '31-DEC-9999', "P_OWNER_PCT" NUMBER(5,2), "P_PRSNL_REL_CD" VARCHAR2(1), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "P_OWNER_DTL_SEQ_NUM" NUMBER(6,0)) 

   COMMENT ON COLUMN "P_OWNER_XREF_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_OWNER_XREF_TB"."P_OWNER_TAX_ID" IS 'Owner Tax ID.'
   COMMENT ON COLUMN "P_OWNER_XREF_TB"."P_OWNER_XREF_SK" IS 'Provider Owner Xref Surrogate Key'
   COMMENT ON COLUMN "P_OWNER_XREF_TB"."P_OWNER_BEG_DT" IS 'The date that ownership begins.'
   COMMENT ON COLUMN "P_OWNER_XREF_TB"."P_FED_TAX_ID" IS 'The provider''s federal tax identification number.'
   COMMENT ON COLUMN "P_OWNER_XREF_TB"."P_OWNER_END_DT" IS 'The date that ownership ended'
   COMMENT ON COLUMN "P_OWNER_XREF_TB"."P_OWNER_PCT" IS 'Owner Percentage.'
   COMMENT ON COLUMN "P_OWNER_XREF_TB"."P_PRSNL_REL_CD" IS 'Provider Personal Relationship Indicator'
   COMMENT ON COLUMN "P_OWNER_XREF_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_OWNER_XREF_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_OWNER_XREF_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_OWNER_XREF_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_OWNER_XREF_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_OWNER_XREF_TB"  IS 'The provider Owner Cross Reference Table contains the cross reference of owners ID''s to provider ID''s.'
