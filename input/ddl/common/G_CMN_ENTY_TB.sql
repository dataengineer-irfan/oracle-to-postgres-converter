--------------------------------------------------------
--  DDL for Table G_CMN_ENTY_TB
--------------------------------------------------------

  CREATE TABLE "NDMMIS73E2"."G_CMN_ENTY_TB" 
   (	"G_CMN_ENTY_SK" NUMBER(10,0), 
	"G_PREFRD_COMMUN_MTHD_CD" VARCHAR2(2 BYTE), 
	"G_SEC_COMMUN_MTHD_CD" VARCHAR2(2 BYTE), 
	"G_CMN_ENTY_TY_CD" VARCHAR2(2 BYTE), 
	"G_VOID_IND" VARCHAR2(1 BYTE), 
	"G_NOTE_SET_SK" NUMBER(10,0), 
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
  TABLESPACE "G_M_D_NDMMIS73E2"  ENABLE ROW MOVEMENT ;

   COMMENT ON COLUMN "NDMMIS73E2"."G_CMN_ENTY_TB"."G_CMN_ENTY_SK" IS 'Surrogate Key for the Common Entity.  This value may be referred to as Payer ID on some UI screens.';
   COMMENT ON COLUMN "NDMMIS73E2"."G_CMN_ENTY_TB"."G_PREFRD_COMMUN_MTHD_CD" IS 'F    FAX
P    Phone
M    US Mail
E    Email';
   COMMENT ON COLUMN "NDMMIS73E2"."G_CMN_ENTY_TB"."G_SEC_COMMUN_MTHD_CD" IS 'F    FAX
P    Phone
M    US Mail
E    Email';
   COMMENT ON COLUMN "NDMMIS73E2"."G_CMN_ENTY_TB"."G_CMN_ENTY_TY_CD" IS 'e.g. Member, Provider, TPL, Contact Management, etc.';
   COMMENT ON COLUMN "NDMMIS73E2"."G_CMN_ENTY_TB"."G_VOID_IND" IS 'Void Indicator';
   COMMENT ON COLUMN "NDMMIS73E2"."G_CMN_ENTY_TB"."G_NOTE_SET_SK" IS 'Surrogate Key';
   COMMENT ON COLUMN "NDMMIS73E2"."G_CMN_ENTY_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism';
   COMMENT ON COLUMN "NDMMIS73E2"."G_CMN_ENTY_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.';
   COMMENT ON COLUMN "NDMMIS73E2"."G_CMN_ENTY_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.';
   COMMENT ON COLUMN "NDMMIS73E2"."G_CMN_ENTY_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.';
   COMMENT ON COLUMN "NDMMIS73E2"."G_CMN_ENTY_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.';
   COMMENT ON TABLE "NDMMIS73E2"."G_CMN_ENTY_TB"  IS 'The Common Entity Table is the primary portal into Contact Management and Common data.  Generally represents a Provider or Recipient.  Can be other types, such as Attorney or state government employee.  i.e. This is generally a person or place that possesses a Medicaid ID.

Common Entity types include (not limited to):
1. MMIS specific entity types
  a. Provider (entered)
  b. Member (enrolled)
  c. TPL Carrier
2. Specific Entity (Contact Management Entity)';
