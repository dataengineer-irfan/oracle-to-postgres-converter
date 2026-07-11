--------------------------------------------------------
--  DDL for Table P_RPT_CMS_UPD_TB
--------------------------------------------------------

  CREATE TABLE "P_RPT_CMS_UPD_TB" ("P_RPT_CMS_UPD_SK" NUMBER(10,0), "P_REC_TYPE" VARCHAR2(3), "P_IFACE_PRCS_DT" DATE, "P_MMIS_ID" VARCHAR2(15), "P_PROV_NAM" VARCHAR2(60), "P_ERR_MSG_TEXT" VARCHAR2(40), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE)
