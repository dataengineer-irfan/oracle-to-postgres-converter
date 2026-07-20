--------------------------------------------------------
--  DDL for Table G_ADR_USG_TB
--------------------------------------------------------

  CREATE TABLE "NDMMIS73E2"."G_ADR_USG_TB" 
   (	"G_CMN_ENTY_SK" NUMBER(10,0), 
	"G_ADR_USG_TY_CD" VARCHAR2(2 BYTE), 
	"G_ADR_SK" NUMBER(10,0), 
	"G_ADR_USG_SEQ_NUM" NUMBER(5,0), 
	"G_ADR_GLBL_SIG_CD" VARCHAR2(2 BYTE), 
	"G_ADR_USG_TY_SIG_CD" VARCHAR2(2 BYTE), 
	"G_ADR_USG_CHG_RSN_CD" VARCHAR2(2 BYTE), 
	"G_ADR_USG_STAT_CD" VARCHAR2(2 BYTE), 
	"G_ADR_USG_END_DT" DATE, 
	"G_ADR_USG_BEG_DT" DATE, 
	"G_ATTN_NAM" VARCHAR2(50 BYTE), 
	"L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, 
	"G_AUD_USER_ID" VARCHAR2(30 BYTE), 
	"G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, 
	"G_AUD_ADD_USER_ID" VARCHAR2(30 BYTE), 
	"G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE, 
	"G_DUMMY_IND" VARCHAR2(1 BYTE) DEFAULT 'N', 
	"G_DUMMY_TS" TIMESTAMP (6), 
	"G_DUMMY_USER_ID" VARCHAR2(30 BYTE)
   ) SEGMENT CREATION IMMEDIATE 
  PCTFREE 10 PCTUSED 0 INITRANS 1 MAXTRANS 255 
 ROW STORE COMPRESS ADVANCED LOGGING
  STORAGE(INITIAL 65536 NEXT 65536 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
  BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "G_M_D_NDMMIS73E2" ;

   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_USG_TB"."G_CMN_ENTY_SK" IS 'Surrogate Key for the Common Entity.  This value may be referred to as Payer ID on some UI screens.';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_USG_TB"."G_ADR_USG_TY_CD" IS 'Member
  Residential
  Mailing
Provider
  Service Location
  Billing
  Mailing
Carrier
  Corporate
  Billing
  Payment';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_USG_TB"."G_ADR_SK" IS 'Surrogate Key';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_USG_TB"."G_ADR_USG_SEQ_NUM" IS 'Sequence Number';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_USG_TB"."G_ADR_GLBL_SIG_CD" IS 'Primary, Secondary, Tertiary among all addresses for a CE.';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_USG_TB"."G_ADR_USG_TY_SIG_CD" IS 'P    Primary
S    Secondary
T    Tertiary
within Address Usage Type.';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_USG_TB"."G_ADR_USG_CHG_RSN_CD" IS 'Explains the reason for the Address Usage being changed.
R    Returned mail
I    Incorrect';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_USG_TB"."G_ADR_USG_STAT_CD" IS 'V    Void
P    Pending
A    Active
D    Deactivated
';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_USG_TB"."G_ADR_USG_END_DT" IS 'Initially set to ''12-31-9999''.
This column can be used to record when the current date ceases to be effective.  This can be used with or without the Address History table.';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_USG_TB"."G_ADR_USG_BEG_DT" IS 'By default, set to sysdate when the row is created.';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_USG_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_USG_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_USG_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_USG_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_USG_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_USG_TB"."G_DUMMY_IND" IS 'Global Indicator';
   COMMENT ON TABLE "NDMMIS73E2"."G_ADR_USG_TB"  IS 'Address Usage Table';
