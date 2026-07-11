--------------------------------------------------------
--  DDL for Table P_RPT_TERM_LCKN_LCKT_TB
--------------------------------------------------------

  CREATE TABLE "P_RPT_TERM_LCKN_LCKT_TB" ("P_RPT_TERM_LCKN_LCKT_SK" NUMBER(10,0), "R_LOB_CD" VARCHAR2(3), "P_ALT_ID" VARCHAR2(15), "P_ALT_ID_TY_CD" VARCHAR2(3), "P_TY_CD" VARCHAR2(3), "B_FULL_NAM" VARCHAR2(100), "B_ALT_ID" VARCHAR2(15), "B_LCKN_BEG_DT" DATE, "B_LCKN_END_DT" DATE, "B_LTC_REVW_TY_CD" VARCHAR2(1), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_RPT_PRCS_DT" DATE) 

   COMMENT ON COLUMN "P_RPT_TERM_LCKN_LCKT_TB"."P_RPT_TERM_LCKN_LCKT_SK" IS 'Uniquely identifies the record'
   COMMENT ON COLUMN "P_RPT_TERM_LCKN_LCKT_TB"."R_LOB_CD" IS 'This field indicates a line of business code to be used for system processing. The line of business is used to identify the entities that have fiscal responsibility for payment of insurance claims on behalf of their respective members.'
   COMMENT ON COLUMN "P_RPT_TERM_LCKN_LCKT_TB"."P_ALT_ID" IS 'An alternate identifier for a Provider.  This may be used when a Provider is assigned an ID different than their primary ID (i.e. NABP Number, DEA Number) by a Customer or has multiple identifiers it can be recognized by.'
   COMMENT ON COLUMN "P_RPT_TERM_LCKN_LCKT_TB"."P_ALT_ID_TY_CD" IS 'The Provider Alternate Identifier Type Code identifies the source of the identifier.'
   COMMENT ON COLUMN "P_RPT_TERM_LCKN_LCKT_TB"."P_TY_CD" IS 'A code that designates the State''s classification of providers.'
   COMMENT ON COLUMN "P_RPT_TERM_LCKN_LCKT_TB"."B_FULL_NAM" IS 'Network Name'
   COMMENT ON COLUMN "P_RPT_TERM_LCKN_LCKT_TB"."B_ALT_ID" IS 'This is a user assigned ID by which the member is known to the State.  Each state/federal agency that determines member eligibility for medical services has its own identification number for a member.  From time to time one agency may change the identific'
   COMMENT ON COLUMN "P_RPT_TERM_LCKN_LCKT_TB"."B_LCKN_BEG_DT" IS 'Global Date Data'
   COMMENT ON COLUMN "P_RPT_TERM_LCKN_LCKT_TB"."B_LCKN_END_DT" IS 'Global Date Data'
   COMMENT ON COLUMN "P_RPT_TERM_LCKN_LCKT_TB"."B_LTC_REVW_TY_CD" IS 'The review type code identifies the results of a review conducted and authorized by the utilization review contractors to approve a member''s stay in a long-term care facility.'
   COMMENT ON COLUMN "P_RPT_TERM_LCKN_LCKT_TB"."L_HIBERNATE_VER_NUM" IS 'This supports hibernate caching mechanism and also supports the pessimistic Locking mechanism'
   COMMENT ON COLUMN "P_RPT_TERM_LCKN_LCKT_TB"."G_AUD_ADD_USER_ID" IS 'The user ID or process that added the row.'
   COMMENT ON COLUMN "P_RPT_TERM_LCKN_LCKT_TB"."G_AUD_ADD_TS" IS 'The timestamp when the row was added.'
   COMMENT ON COLUMN "P_RPT_TERM_LCKN_LCKT_TB"."G_RPT_PRCS_DT" IS 'Process date.'
