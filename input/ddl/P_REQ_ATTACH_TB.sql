--------------------------------------------------------
--  DDL for Table P_REQ_ATTACH_TB
--------------------------------------------------------

  CREATE TABLE "P_REQ_ATTACH_TB" ("P_SYS_ID" NUMBER(10,0), "P_REQ_ATTACH_SK" NUMBER(10,0), "P_ATTACH_TY_CD" VARCHAR2(3), "P_ATTACH_RECD_IND" VARCHAR2(1), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_REQ_ATTACH_TB"."P_SYS_ID" IS 'Provider Internal System Identifier.'
   COMMENT ON COLUMN "P_REQ_ATTACH_TB"."P_REQ_ATTACH_SK" IS 'Provider Required Attachment Surrogate Key'
   COMMENT ON COLUMN "P_REQ_ATTACH_TB"."P_ATTACH_TY_CD" IS 'Provider Attachment Type Code..'
   COMMENT ON COLUMN "P_REQ_ATTACH_TB"."P_ATTACH_RECD_IND" IS 'Provider Attachment received Indicator.'
   COMMENT ON COLUMN "P_REQ_ATTACH_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_REQ_ATTACH_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.'
   COMMENT ON COLUMN "P_REQ_ATTACH_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.'
   COMMENT ON COLUMN "P_REQ_ATTACH_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_REQ_ATTACH_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_REQ_ATTACH_TB"  IS 'The Provider Required Attachments Table indicates which appropriate forms need to be attached to a provider''s DHHS enrollment application.'
