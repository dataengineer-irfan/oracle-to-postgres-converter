--------------------------------------------------------
--  Ref Constraints for Table G_ADR_USG_TB
--------------------------------------------------------

  ALTER TABLE "NDMMIS73E2"."G_ADR_USG_TB" ADD CONSTRAINT "G_ADR_USG_F1" FOREIGN KEY ("G_CMN_ENTY_SK")
	  REFERENCES "NDMMIS73E2"."G_CMN_ENTY_TB" ("G_CMN_ENTY_SK") ENABLE;
  ALTER TABLE "NDMMIS73E2"."G_ADR_USG_TB" ADD CONSTRAINT "G_ADR_USG_F2" FOREIGN KEY ("G_ADR_SK")
	  REFERENCES "NDMMIS73E2"."G_ADR_TB" ("G_ADR_SK") ENABLE;
