--------------------------------------------------------
--  DDL for Table G_ADR_TB
--------------------------------------------------------

  CREATE TABLE "NDMMIS73E2"."G_ADR_TB" 
   (	"G_ADR_SK" NUMBER(10,0), 
	"G_LINE1_ADR" VARCHAR2(64 BYTE), 
	"G_LINE2_ADR" VARCHAR2(64 BYTE), 
	"G_LINE3_ADR" VARCHAR2(64 BYTE), 
	"G_LINE4_ADR" VARCHAR2(64 BYTE), 
	"G_CITY_NAM" VARCHAR2(30 BYTE), 
	"G_TOWN_CD" VARCHAR2(3 BYTE), 
	"G_US_STATE_CD" VARCHAR2(2 BYTE), 
	"G_ZIP5_CD" VARCHAR2(5 BYTE), 
	"G_ZIP4_CD" VARCHAR2(4 BYTE), 
	"G_CNTRY_CD" VARCHAR2(3 BYTE), 
	"G_CNTY_CD" VARCHAR2(5 BYTE), 
	"G_USPS_ADR_VRFY_CD" VARCHAR2(2 BYTE), 
	"G_USPS_LINE1_ADR" VARCHAR2(64 BYTE), 
	"G_USPS_LINE2_ADR" VARCHAR2(64 BYTE), 
	"G_LAT_NUM" NUMBER(7,4), 
	"G_LON_NUM" NUMBER(7,4), 
	"G_CMN_ENTY_TY_CD" VARCHAR2(2 BYTE), 
	"G_DSTCT_OFC_CD" VARCHAR2(3 BYTE), 
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

   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_TB"."G_ADR_SK" IS 'Integer value that uniquely identifies each address row.';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_TB"."G_LINE1_ADR" IS 'Address line 1.';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_TB"."G_LINE2_ADR" IS 'Address line 2. ';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_TB"."G_LINE3_ADR" IS 'Address line 3.';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_TB"."G_LINE4_ADR" IS 'Address line 4.';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_TB"."G_CITY_NAM" IS 'City Name';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_TB"."G_TOWN_CD" IS 'e.g.

Code    Code Description

000    Out of State

001    Acworth

002    Charlestown

003    Claremont

004    Cornish';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_TB"."G_US_STATE_CD" IS 'USPS State Code.';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_TB"."G_ZIP5_CD" IS 'Zip5 Code (Length of 5)';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_TB"."G_ZIP4_CD" IS 'Zip4 Code (Length of 4)';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_TB"."G_CNTRY_CD" IS 'Code designating country.  If this is an international address, this code value should be anything but US.



Enterprise is a Medicaid application.  Being a domestic government program, the assumption is that the percentage of international addresses stored will be quite small.  Thus, little benefit is expected from designing an elegant and encompassing solution, which would be complicated.  For international addresses, the Data Architecture recommendation is that we use address lines 1-4 (add more if necessary) to capture the international address.  At the same time, the user needs to make sure that the Country Code is changed to something besides US.  Whatever is entered in the free-form address lines will be the international address.  If further QC is required, Enterprise can parse the address lines and apply formatting/editing rules. ';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_TB"."G_CNTY_CD" IS 'On 5/11/06, Mac Wansley said: For County Code I would vote for defining it as 5 characters for Enterprise, recognizing that in some states the leading positions may be zeros or blanks.   We can then choose to suppress the leading positions (zeros or blank) for UI display and reports, although UI and reports would need to account for 5 positions.



On 5/11/06, Madhu Krish said: This standard defines for most of the countries and dependent areas in the world:

a two letter (ISO 3166-1 alpha-2) 

a three-letter (ISO 3166-1 alpha-3), and 

a three-digit numeric (ISO 3166-1 numeric) code. 

http://en.wikipedia.org/wiki/Country_codes#Lists_of_country_codes_by_country';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_TB"."G_USPS_ADR_VRFY_CD" IS '00 - perfect match, here is the address; 

01 - only one match, but had to make a few changes (such as change LN to Lane, etc.), or 

02 - couldn''t find address but here are some possible matches.   

P.S. There is no guarantee that a GeoStan-like product will be used.';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_TB"."G_USPS_LINE1_ADR" IS 'Verfified USPS address.  Will conform to the output parameters of the call to Geostan.';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_TB"."G_USPS_LINE2_ADR" IS 'Verfified USPS address.  Will conform to the output parameters of the call to Geostan.';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_TB"."G_LAT_NUM" IS 'Latitude of the address.  The value will be null if the address cannot be validated (per GeoStan as per 12/13/06).';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_TB"."G_LON_NUM" IS 'Latitude of the address.  The value will be null if the address cannot be validated (per GeoStan as per 12/13/06).';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_TB"."G_CMN_ENTY_TY_CD" IS 'e.g. Member, Provider, TPL, Contact Management, etc.

There is a requirement to search addresses filtered by subsystem (e.g. TPL).  An index placed over this column allows for a subsystem level search with relative efficiency.  If the value of this column in the base table is NULL, then the row does not participate in  the index.  Thus, addresses that don''t need to be searched won''t pose a performance hit when they are inserted.';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_TB"."G_DSTCT_OFC_CD" IS 'In the Address Table, the District Office is only stored for Service Location addresses.

e.g. 01 Keene District Office, 02 Claremont, 03 Locana, 04 Conway, 05 Concord, 

06 Portsmouth, 07 Rochester, 08 Littleton, 09 Berlin, 10 Manchester, 11 Nashua

16 Salem, 17 Rochester, 78 Central Health Kids, 99 Division of Human Services';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_TB"."G_AUD_USER_ID" IS 'The user ID or process that last modified the row.';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_TB"."G_AUD_TS" IS 'The timestamp when the row was last modified.';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.';
   COMMENT ON COLUMN "NDMMIS73E2"."G_ADR_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.';
   COMMENT ON TABLE "NDMMIS73E2"."G_ADR_TB"  IS 'The General Address Table is used to store addresses for all types of entties throughout the Enterprise system.';
