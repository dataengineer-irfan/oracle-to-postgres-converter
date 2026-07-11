--------------------------------------------------------
--  DDL for Table P_ALT_ID_TB
--------------------------------------------------------

  CREATE TABLE "P_ALT_ID_TB" ("P_SYS_ID" NUMBER(10,0), "P_ALT_ID_SK" NUMBER(10,0), "P_ALT_ID" VARCHAR2(15), "P_ALT_ID_TY_CD" VARCHAR2(3), "P_ALT_ID_BEG_DT" DATE, "P_ALT_ID_SVC_LOCN_CD" VARCHAR2(3), "P_ALT_ID_END_DT" DATE DEFAULT '31-DEC-9999', "P_TAX_RPT_IND" VARCHAR2(1), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_ALT_ID_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_ALT_ID_TB"."P_ALT_ID_SK" IS 'Provider Alternate Identifier Surrogate Key'
   COMMENT ON COLUMN "P_ALT_ID_TB"."P_ALT_ID" IS 'An alternate identifier for a Provider.  This may be used when a Provider is assigned an ID different than their primary ID (i.e. NABP Number, DEA Number) by a Customer or has multiple identifiers it can be recognized by.'
   COMMENT ON COLUMN "P_ALT_ID_TB"."P_ALT_ID_TY_CD" IS 'The Provider Alternate Identifier Type Code identifies the source of the identifier.'
   COMMENT ON COLUMN "P_ALT_ID_TB"."P_ALT_ID_BEG_DT" IS 'Provider Alternate ID Begin Date.'
   COMMENT ON COLUMN "P_ALT_ID_TB"."P_ALT_ID_SVC_LOCN_CD" IS 'Provider Alternate ID Service Location Code..'
   COMMENT ON COLUMN "P_ALT_ID_TB"."P_ALT_ID_END_DT" IS 'Provider Alternate ID End Date.'
   COMMENT ON COLUMN "P_ALT_ID_TB"."P_TAX_RPT_IND" IS 'Provider Tax Report Indicator.'
   COMMENT ON COLUMN "P_ALT_ID_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_ALT_ID_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_ALT_ID_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_ALT_ID_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_ALT_ID_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_ALT_ID_TB"  IS 'The Provider Alternative ID Table is for Provider Cross Reference.'
