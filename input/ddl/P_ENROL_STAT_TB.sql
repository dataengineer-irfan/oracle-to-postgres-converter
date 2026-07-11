--------------------------------------------------------
--  DDL for Table P_ENROL_STAT_TB
--------------------------------------------------------

  CREATE TABLE "P_ENROL_STAT_TB" ("P_SYS_ID" NUMBER(10,0), "P_ENROL_STAT_SK" NUMBER(10,0), "P_ENROL_STAT_BEG_DT" DATE, "P_ENROL_STAT_END_DT" DATE DEFAULT '31-DEC-9999', "P_ENROL_STAT_TY_CD" VARCHAR2(2), "P_ENROL_STAT_RSN_CD" VARCHAR2(3), "P_RTRCTV_ELIG_IND" VARCHAR2(1), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_ENROL_STAT_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_ENROL_STAT_TB"."P_ENROL_STAT_SK" IS 'Provider Enrollment Status Surrogate Key'
   COMMENT ON COLUMN "P_ENROL_STAT_TB"."P_ENROL_STAT_BEG_DT" IS 'The effective date for the provider''s status regarding participation as a Medicaid provider.'
   COMMENT ON COLUMN "P_ENROL_STAT_TB"."P_ENROL_STAT_END_DT" IS 'Ending date for providers status code.'
   COMMENT ON COLUMN "P_ENROL_STAT_TB"."P_ENROL_STAT_TY_CD" IS 'This is the enrollment status of the provider.  The enrollment status is the primary mechanism that tracks the enrollment of a provider into the Medicaid program.'
   COMMENT ON COLUMN "P_ENROL_STAT_TB"."P_ENROL_STAT_RSN_CD" IS 'Provider Status Reason Code.'
   COMMENT ON COLUMN "P_ENROL_STAT_TB"."P_RTRCTV_ELIG_IND" IS 'This field indicates if the Provider is Retroactively Eligible.  This indicates if the provider was given special consideration at the time of enrollment approval, to be eligible prior to the date when the application was received.'
   COMMENT ON COLUMN "P_ENROL_STAT_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_ENROL_STAT_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_ENROL_STAT_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_ENROL_STAT_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_ENROL_STAT_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_ENROL_STAT_TB"  IS 'The Provider Enroll Status Table contains the enrollment statuses with their effective date.'
