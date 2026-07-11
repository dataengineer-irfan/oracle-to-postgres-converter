--------------------------------------------------------
--  DDL for Table P_EVENT_TB
--------------------------------------------------------

  CREATE TABLE "P_EVENT_TB" ("P_SYS_ID" NUMBER(10,0), "P_EVENT_SK" NUMBER(10,0), "P_EVENT_TS" TIMESTAMP (6), "P_EVENT_CD" VARCHAR2(4), "P_EVENT_USER_ID" VARCHAR2(30), "P_EVENT_NOTE_TEXT" VARCHAR2(128), "P_EVENT_PRCS_IND" VARCHAR2(1), "P_EVENT_TY_CD" VARCHAR2(3), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_EVENT_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_EVENT_TB"."P_EVENT_SK" IS 'Provider Event Surrogate Key'
   COMMENT ON COLUMN "P_EVENT_TB"."P_EVENT_TS" IS 'The date and time a provider enrollment tracking event occured.'
   COMMENT ON COLUMN "P_EVENT_TB"."P_EVENT_CD" IS 'A code used to identify an event that occurred during provider enrollment tracking.'
   COMMENT ON COLUMN "P_EVENT_TB"."P_EVENT_USER_ID" IS 'The user ID associated with a provider enrollment tracking event. The event may have been entereed manually or by the system'
   COMMENT ON COLUMN "P_EVENT_TB"."P_EVENT_NOTE_TEXT" IS 'Note or comment text associated with a provider enrollment tracking event.'
   COMMENT ON COLUMN "P_EVENT_TB"."P_EVENT_PRCS_IND" IS 'Provider Enrollment Tracking Event Process Indicator'
   COMMENT ON COLUMN "P_EVENT_TB"."P_EVENT_TY_CD" IS 'Provider Enrollment Tracking Event Type Code. '
   COMMENT ON COLUMN "P_EVENT_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_EVENT_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_EVENT_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_EVENT_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_EVENT_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_EVENT_TB"  IS 'The Provider Event Table contains date and time stamp of changes.'
