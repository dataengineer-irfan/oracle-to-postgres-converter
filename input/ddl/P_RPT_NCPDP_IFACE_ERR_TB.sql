--------------------------------------------------------
--  DDL for Table P_RPT_NCPDP_IFACE_ERR_TB
--------------------------------------------------------

  CREATE TABLE "P_RPT_NCPDP_IFACE_ERR_TB" ("P_NCPDP_IFACE_ERR_SK" NUMBER(10,0), "P_ALT_ID" VARCHAR2(15), "P_ERR_FLD_NAM" VARCHAR2(10), "P_ERR_FLD_DATA" VARCHAR2(50), "P_NCPDP_ID" VARCHAR2(15), "G_RPT_ERR_MSG_TEXT" VARCHAR2(100), "R_LOB_CD" VARCHAR2(3), "G_RPT_PRCS_DT" DATE, "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE) 

   COMMENT ON COLUMN "P_RPT_NCPDP_IFACE_ERR_TB"."P_NCPDP_IFACE_ERR_SK" IS 'Provider National Council for Prescription Drug Program (NCPDP) Interface Error Surrogate Key'
   COMMENT ON COLUMN "P_RPT_NCPDP_IFACE_ERR_TB"."P_ALT_ID" IS 'An alternate identifier for a Provider.  This may be used when a Provider is assigned an ID different than their primary ID (i.e. NABP Number, DEA Number) by a Customer or has multiple identifiers it can be recognized by.'
   COMMENT ON COLUMN "P_RPT_NCPDP_IFACE_ERR_TB"."P_ERR_FLD_NAM" IS 'Error field name'
   COMMENT ON COLUMN "P_RPT_NCPDP_IFACE_ERR_TB"."P_ERR_FLD_DATA" IS 'Error Value'
   COMMENT ON COLUMN "P_RPT_NCPDP_IFACE_ERR_TB"."P_NCPDP_ID" IS 'A unique number the system assigns to the provider for NHMMIS claims processing.'
   COMMENT ON COLUMN "P_RPT_NCPDP_IFACE_ERR_TB"."G_RPT_ERR_MSG_TEXT" IS 'Error Message'
   COMMENT ON COLUMN "P_RPT_NCPDP_IFACE_ERR_TB"."R_LOB_CD" IS 'This field indicates a line of business code to be used for system processing. The line of business is used to identify the entities that have fiscal responsibility for payment of insurance claims on behalf of their respective members.'
   COMMENT ON COLUMN "P_RPT_NCPDP_IFACE_ERR_TB"."G_RPT_PRCS_DT" IS 'Report Process Date'
   COMMENT ON COLUMN "P_RPT_NCPDP_IFACE_ERR_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_RPT_NCPDP_IFACE_ERR_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_RPT_NCPDP_IFACE_ERR_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON TABLE "P_RPT_NCPDP_IFACE_ERR_TB"  IS 'Provider Report NCPDP Interface Error Table'
