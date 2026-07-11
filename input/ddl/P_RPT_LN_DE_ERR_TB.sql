--------------------------------------------------------
--  DDL for Table P_RPT_LN_DE_ERR_TB
--------------------------------------------------------

  CREATE TABLE "P_RPT_LN_DE_ERR_TB" ("P_RPT_LN_DE_ERR_SK" NUMBER(10,0), "P_DE_PROV_ID" VARCHAR2(15), "P_DE_NAM" VARCHAR2(60), "P_DE_NUM" VARCHAR2(15), "P_DE_EXP_DT" DATE, "P_DE_ERROR_MSG" VARCHAR2(40), "P_DE_PRCS_DT" DATE, "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE)
