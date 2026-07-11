--------------------------------------------------------
--  DDL for Table P_RA_MEDM_TB
--------------------------------------------------------

  CREATE TABLE "P_RA_MEDM_TB" ("P_SYS_ID" NUMBER(10,0), "P_RA_MEDM_SK" NUMBER(10,0), "P_RA_MEDM_CD" VARCHAR2(1), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_RA_MEDM_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_RA_MEDM_TB"."P_RA_MEDM_SK" IS 'Provider Remittance Advice Medium Surrogate Key'
   COMMENT ON COLUMN "P_RA_MEDM_TB"."P_RA_MEDM_CD" IS 'This code indicates the medium that the State uses to send remittance advices to the provider.'
   COMMENT ON COLUMN "P_RA_MEDM_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_RA_MEDM_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_RA_MEDM_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_RA_MEDM_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_RA_MEDM_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_RA_MEDM_TB"  IS 'The table contains information about the type of medium we should use for Remittance Advices that we send a provider.'
