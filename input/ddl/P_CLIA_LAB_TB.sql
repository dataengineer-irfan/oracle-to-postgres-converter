--------------------------------------------------------
--  DDL for Table P_CLIA_LAB_TB
--------------------------------------------------------

  CREATE TABLE "P_CLIA_LAB_TB" ("P_CLIA_NUM" VARCHAR2(10), "P_CLIA_LAB_PAY_IND" VARCHAR2(1), "P_CLIA_FED_TAX_ID" VARCHAR2(9), "P_CLIA_MCARE_NUM" VARCHAR2(12), "P_CLIA_UPD_DT" DATE, "P_CLIA_ADD_DT" DATE, "P_CLIA_LAB_NAM" VARCHAR2(50), "P_CLIA_NPI_NUM" VARCHAR2(10), "G_CMN_ENTY_SK" NUMBER(10,0), "G_NOTE_SET_SK" NUMBER(10,0), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_CLIA_LAB_TB"."P_CLIA_NUM" IS 'The CLIA number assigned to the provider regarding the provider''s certification as a laboratory provider of services.  This field is updated through the HCFA OSCAR interface.'
   COMMENT ON COLUMN "P_CLIA_LAB_TB"."P_CLIA_LAB_PAY_IND" IS 'Providers Payment indicator for CLIA Lab charges.'
   COMMENT ON COLUMN "P_CLIA_LAB_TB"."P_CLIA_FED_TAX_ID" IS 'The provider''s federal tax identification number.'
   COMMENT ON COLUMN "P_CLIA_LAB_TB"."P_CLIA_MCARE_NUM" IS 'The provider''s Medicare number.'
   COMMENT ON COLUMN "P_CLIA_LAB_TB"."P_CLIA_UPD_DT" IS 'Date of update for CLIA number.'
   COMMENT ON COLUMN "P_CLIA_LAB_TB"."P_CLIA_ADD_DT" IS 'Cate address changed for CLIA information.'
   COMMENT ON COLUMN "P_CLIA_LAB_TB"."P_CLIA_LAB_NAM" IS 'The legal name of the provider.'
   COMMENT ON COLUMN "P_CLIA_LAB_TB"."P_CLIA_NPI_NUM" IS 'Indicates the provider''s National Provider ID.'
   COMMENT ON COLUMN "P_CLIA_LAB_TB"."G_CMN_ENTY_SK" IS 'Specifies that this is a Base Table.  Thus, each row has a corresponding row in Common Entity.'
   COMMENT ON COLUMN "P_CLIA_LAB_TB"."G_NOTE_SET_SK" IS 'Surrogate Key'
   COMMENT ON COLUMN "P_CLIA_LAB_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_CLIA_LAB_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_CLIA_LAB_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_CLIA_LAB_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_CLIA_LAB_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_CLIA_LAB_TB"  IS 'Provider Clinical Laboratory Information Act (CLIA) Laboratory Table'
