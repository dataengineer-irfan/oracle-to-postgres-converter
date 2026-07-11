--------------------------------------------------------
--  DDL for Table P_TXNMY_TB
--------------------------------------------------------

  CREATE TABLE "P_TXNMY_TB" ("P_SYS_ID" NUMBER(10,0), "P_TXNMY_SK" NUMBER(10,0), "P_TXNMY_CD" VARCHAR2(10), "P_TXNMY_BEG_DT" DATE, "P_TXNMY_END_DT" DATE DEFAULT '31-DEC-9999', "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_TXNMY_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_TXNMY_TB"."P_TXNMY_SK" IS 'Provider Taxonomy Surrogate Key'
   COMMENT ON COLUMN "P_TXNMY_TB"."P_TXNMY_CD" IS 'The Taxonomy code for the provider, as per HIPAA requirements.'
   COMMENT ON COLUMN "P_TXNMY_TB"."P_TXNMY_BEG_DT" IS 'The begin date for the taxonomy code.'
   COMMENT ON COLUMN "P_TXNMY_TB"."P_TXNMY_END_DT" IS 'The date a provider taxonomy code ends.'
   COMMENT ON COLUMN "P_TXNMY_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_TXNMY_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_TXNMY_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_TXNMY_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_TXNMY_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_TXNMY_TB"  IS 'The Provider TaxonomyTable contains Provider Taxonomy codes for HIPAA compliance.'
