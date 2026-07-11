--------------------------------------------------------
--  DDL for Table P_TY_SPECL_XREF_TB
--------------------------------------------------------

  CREATE TABLE "P_TY_SPECL_XREF_TB" ("P_TY_CD" VARCHAR2(3), "P_SPECL_CD" VARCHAR2(3), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_TY_SPECL_XREF_TB"."P_TY_CD" IS 'A code that designates the State''s classification of providers.'
   COMMENT ON COLUMN "P_TY_SPECL_XREF_TB"."P_SPECL_CD" IS 'A code indicating a provider''s certified medical specialty.'
   COMMENT ON COLUMN "P_TY_SPECL_XREF_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_TY_SPECL_XREF_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_TY_SPECL_XREF_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_TY_SPECL_XREF_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_TY_SPECL_XREF_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_TY_SPECL_XREF_TB"  IS 'The Provider Type Specialty Cross Reference Table serves as a reference of what specialties are valid for each provider type.'
