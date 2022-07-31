
select "submitDate",* from "all_locqc_view" where author = 'susannehoyersten@glocalizeinc.com'


select "submitDate" ,* from "NetflixDttLocQcSummary" where "locQcer"  = 'susannehoyersten@glocalizeinc.com'
select "submitDate" ,* from "NetflixDttLocQcResult" where "author"  = 'susannehoyersten@glocalizeinc.com' 
select "submitDate" ,* from "NetflixDttLocQcError" where "author" = 'susannehoyersten@glocalizeinc.com' 
select "submitDate","locQcSummarySheetId" ,origiantionSummaryfrom "NetflixDttOriginationSummary" ndos where "author"  = 'susannehoyersten@glocalizeinc.com' 

SELECT "originationSummarySheetId", "originationSummarySheetRowNumber", "partnerId", partner, author, "requestId", "xfrRequestId", "titleId", "packageId", "titleDesc", "assetType", "contentCategory", "reasonCode", "paymentCode", "originalAudioLanguageCode", "sourceLanguageCode", "targetLanguageCode", "runtimeMinutes", "currentState", "submitDate", "dueDate", "startDate", "isOnTime", "billingEvents"
FROM "NetflixDttOriginationSummary";

select * from "NetflixDttLocQcResult" where author  = 'susannehoyersten@glocalizeinc.com'
select * from "NetflixDttLocQcError" where author  = 'susannehoyersten@glocalizeinc.com'
SELECT "locQcResultsSheetId", "locQcResultsSheetRowNumber", "partnerId", partner, author, "requestId", "qcRequestId", "titleId", "packageId", "titleDesc", "assetType", "contentCategory", "reasonCode", "originalAudioLanguageCode", "sourceLanguageCode", "targetLanguageCode", "runtimeMinutes", "subtitleEvents", "submitDate", "qcSubmitDate", "qcReasonCode", "isNetNeutral", "allErrors", "objectiveErrors", "objectiveMajorErrors", "objectiveMinorErrors", "objectiveErrorsPerRtm", "objectiveErrorsPerEvent"
FROM "NetflixDttLocQcResult";

SELECT "locQcErrorsSheetId", "locQcErrorsSheetRowNumber", "partnerId", partner, author, "requestId", "titleId", "packageId", "titleDesc", "assetType", "contentCategory", "reasonCode", "originalAudioLanguageCode", "sourceLanguageCode", "targetLanguageCode", "runtimeMinutes", "subtitleEvents", "submitDate", "qcSubmitDate", "qcReasonCode", "isNetNeutral", "errorCode", objective, issues
FROM "NetflixDttLocQcError";

select a."locQcResultsSheetId" ,a."locQcResultsSheetRowNumber",b."locQcErrorsSheetId" ,b."locQcErrorsSheetRowNumber" ,
	   a."titleDesc",
    a.author,
    a."requestId",
    a."packageId",
    a."submitDate",
    a."targetLanguageCode",
    a."assetType",
    a."contentCategory",
    a."runtimeMinutes",
    a."subtitleEvents",
    a."allErrors",
    a."objectiveMajorErrors",
    b.issues,
    b."errorCode"
from "NetflixDttLocQcResult"  as a 
left join "NetflixDttLocQcError" as b on a."requestId" = b."requestId"
where a.author  = 'susannehoyersten@glocalizeinc.com'
"locQcResultsSheetId" 

select * from all_assetqc_view where "issueCode"isnull
netflix_locqc_view
select count(*) from netflix_locqc_view
create view netflix_locqc_view
as select a."locQcResultsSheetId" ,a."locQcResultsSheetRowNumber",b."locQcErrorsSheetId" ,b."locQcErrorsSheetRowNumber" ,
	   a."titleDesc",
    a.author,
    a."requestId",
    a."packageId",
    a."submitDate",
    a."targetLanguageCode",
    a."assetType",
    a."contentCategory",
    a."runtimeMinutes",
    a."subtitleEvents",
    a."allErrors",
    a."objectiveMajorErrors",
    b.issues,
    b."errorCode"
from "NetflixDttLocQcResult"  as a 
left join "NetflixDttLocQcError" as b on a."requestId" = b."requestId"


select * from all_locqc_view alv 
select * from "netflix_locqc_view"
SELECT a."originationSummarySheedId",
    a."",
    b."locQcResultsSheetId",
    b."locQcResultsSheetRowNumber",
    c."locQcErrorsSheetId",
    c."locQcErrorsSheetRowNumber",
    a."titleDesc",
    b.author,
    a."requestId",
    a."packageId",
    a."dueDate",
    a."submitDate",
    a."targetLanguageCode",
    a."assetType",
    a."contentCategory",
    a."runtimeMinutes",
    b."subtitleEvents",
    b."allErrors",
    b."objectiveMajorErrors",
    c.issues,
    c."errorCode"
   FROM "NetflixDttOriginationSummary" a
     LEFT JOIN "NetflixDttLocQcResult" b ON a."requestId"::text = b."requestId"::text
     LEFT JOIN "NetflixDttLocQcError" c ON b."requestId"::text = c."requestId"::text
    where b.author  = 'susannehoyersten@glocalizeinc.com'
    
    
    
    
CREATE OR REPLACE VIEW public.all_locqc_view
AS SELECT a."locQcSummarySheetId",
    a."locQcSummarySheetRowNumber",
    b."locQcResultsSheetId",
    b."locQcResultsSheetRowNumber",
    c."locQcErrorsSheetId",
    c."locQcErrorsSheetRowNumber",
    a."titleDesc",
    b.author,
    a."requestId",
    a."packageId",
    a."dueDate",
    a."submitDate",
    a."targetLanguageCode",
    a."assetType",
    a."contentCategory",
    a."runtimeMinutes",
    b."subtitleEvents",
    b."allErrors",
    b."objectiveMajorErrors",
    c.issues,
    c."errorCode"
   FROM "NetflixDttLocQcSummary" a
     LEFT JOIN "NetflixDttLocQcResult" b ON a."requestId"::text = b."requestId"::text
     LEFT JOIN "NetflixDttLocQcError" c ON b."requestId"::text = c."requestId"::text;