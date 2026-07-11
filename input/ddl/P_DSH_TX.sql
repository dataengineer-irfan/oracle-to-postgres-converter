--------------------------------------------------------
--  DDL for Table P_DSH_TX
--------------------------------------------------------

  CREATE TABLE "P_DSH_TX" ("P_SYS_ID" NUMBER(10,0), "P_DSH_SK" NUMBER(10,0), "P_DSH_PCT" NUMBER(6,2), "L_HIBERNATE_VER_NUM" NUMBER(9,0) DEFAULT 0, "G_AUD_ADD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_ADD_USER_ID" VARCHAR2(30), "G_AUD_TS" TIMESTAMP (6) DEFAULT SYSDATE, "G_AUD_USER_ID" VARCHAR2(30))
