--------------------------------------------------------
--  DDL for Table P_ENROL_AFFL_TB
--------------------------------------------------------

  CREATE TABLE "P_ENROL_AFFL_TB" ("P_ENROL_SYS_ID" NUMBER(10,0), "P_ENROL_AFFL_SEQ_NUM" NUMBER(5,0), "P_MBR_SYS_ID" NUMBER(10,0), "P_GRP_SYS_ID" NUMBER(10,0), "P_AFFL_MCAID_ID" VARCHAR2(15), "P_AFFL_NAM" VARCHAR2(35), "P_AFFL_BEG_DT" DATE, "P_AFFL_END_DT" DATE, "P_AFFL_TY_CD" VARCHAR2(1), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_ENROL_AFFL_TB"."P_ENROL_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_ENROL_AFFL_TB"."P_ENROL_AFFL_SEQ_NUM" IS 'Sequence Number'
   COMMENT ON COLUMN "P_ENROL_AFFL_TB"."P_MBR_SYS_ID" IS 'Provider Member System Identifier: If the enrolling provider is an individual, this will be the same as the p enrolling system ID.  If the enrolling provider is a group, and the member provider that the group has identified as being affiliated with the group is found on the system, then this field will be populated with that member provider''s P-SYS-ID.'
   COMMENT ON COLUMN "P_ENROL_AFFL_TB"."P_GRP_SYS_ID" IS 'Provider Group System Identifier: If the enrolling provider is a group, this will be the same as the p enrolling system ID.  If the enrolling provider is an individual, and the group provider that the has been identified as being affiliated with the individual is found on the system, then this field will be populated with that group provider''s P-SYS-ID.'
   COMMENT ON COLUMN "P_ENROL_AFFL_TB"."P_AFFL_MCAID_ID" IS 'Affiliated Provider''s Medicaid Identifier'
   COMMENT ON COLUMN "P_ENROL_AFFL_TB"."P_AFFL_NAM" IS 'Affiliated Provider''s Name'
   COMMENT ON COLUMN "P_ENROL_AFFL_TB"."P_AFFL_BEG_DT" IS 'Begin date of a provider''s affiliation with a group, etc.'
   COMMENT ON COLUMN "P_ENROL_AFFL_TB"."P_AFFL_END_DT" IS 'End date of a provider''s affiliation with a group, etc.'
   COMMENT ON COLUMN "P_ENROL_AFFL_TB"."P_AFFL_TY_CD" IS 'The type of affiliation that links a provider with another provider.'
   COMMENT ON COLUMN "P_ENROL_AFFL_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_ENROL_AFFL_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_ENROL_AFFL_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_ENROL_AFFL_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_ENROL_AFFL_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_ENROL_AFFL_TB"  IS 'Provider Enrollment Affiliation Table to use during provider enrollment to contain information about the provider''s the enrolling provider is affiliated with.  Once the provider is approved, this data will be moved to the P-AFFL-TB.'
