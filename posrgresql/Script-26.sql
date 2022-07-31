select count(*) from "NetflixDttLocQcResult" as a -- 8962
select count(*) from "NetflixDttLocQcSummary" ndlqs  -- 13628
select count(*) from "NetflixDttLocQcError" ndlqe -- 46942


select * from "NetflixDttLocQcResult" as a where "requestId" = '015018ac-080f-48ab-8a5a-9553cc8b59bb' -- 8962
select * from "NetflixDttLocQcSummary" where "requestId"  = '015018ac-080f-48ab-8a5a-9553cc8b59bb' -- 13628
select * from "NetflixDttLocQcError" where "requestId" = 'a0cc0146-5794-4b13-91e6-42b8679f2f90' -- 46942
select cast(1 as text)

#locqc
select a."locQcSummarySheetId",a."locQcSummarySheetRowNumber",c."locQcErrorsSheetId" ,c."locQcErrorsSheetRowNumber",c."subtitleEvents" a."titleDesc",b.author ,a."requestId" ,a."packageId" ,a."dueDate" ,a."submitDate" ,a."targetLanguageCode" ,a."assetType" ,a."contentCategory" ,a."runtimeMinutes" 
,b."subtitleEvents" ,b."allErrors" ,b."objectiveMajorErrors" ,c."issues" 
from "NetflixDttLocQcSummary" as a 
left join "NetflixDttLocQcResult" as b on a."requestId"  = b."requestId" 
left join "NetflixDttLocQcError" as c on b."requestId"  = c."requestId" 
where issues = 0 and  a."requestId"  = '7360e8f3-4eef-4247-bdec-e3cb4464a886'


select a."locQcSummarySheetId",a."locQcSummarySheetRowNumber" ,b."locQcResultsSheetId" ,b."locQcResultsSheetRowNumber" ,c."locQcErrorsSheetId" ,c."locQcErrorsSheetRowNumber"  ,a."titleDesc",b.author ,a."requestId" ,a."packageId" ,a."dueDate" ,a."submitDate" ,a."targetLanguageCode" ,a."assetType" ,a."contentCategory" ,a."runtimeMinutes" 
,b."subtitleEvents" ,b."allErrors" ,b."objectiveMajorErrors" ,c."issues" ,c."errorCode" 
from "NetflixDttLocQcSummary" as a 
left join "NetflixDttLocQcResult" as b on a."requestId"  = b."requestId" 
left join "NetflixDttLocQcError" as c on b."requestId"  = c."requestId" 
where issues = 0 and  a."requestId"  = '7360e8f3-4eef-4247-bdec-e3cb4464a886'


select count(*)from "NetflixDttLocQcSummary" as a 
left join "NetflixDttLocQcResult" as b on a."requestId"  = b."requestId" 
left join "NetflixDttLocQcError" as c on b."requestId"  = c."requestId" 

select a."locQcSummarySheetId",a."locQcSummarySheetRowNumber" ,b."locQcResultsSheetId" ,b."locQcResultsSheetRowNumber" ,c."locQcErrorsSheetId" ,c."locQcErrorsSheetRowNumber" # ,a."titleDesc",a."requestId",c."issues" ,c."errorCode" 
from "NetflixDttLocQcSummary" as a 
left join "NetflixDttLocQcResult" as b on a."requestId"  = b."requestId" 
left join "NetflixDttLocQcError" as c on b."requestId"  = c."requestId" 
where issues = 0 and  a."requestId"  = '7360e8f3-4eef-4247-bdec-e3cb4464a886'

all_locqc_view
create view all_locqc_view
as select a."titleDesc",b.author ,a."requestId" ,a."packageId" ,a."dueDate" ,a."submitDate" ,a."targetLanguageCode" ,a."assetType" ,a."contentCategory" ,a."runtimeMinutes" 
,b."subtitleEvents" ,b."allErrors" ,b."objectiveMajorErrors" ,c."issues" 
from "NetflixDttLocQcSummary" as a 
left join "NetflixDttLocQcResult" as b on a."requestId"  = b."requestId" 
left join "NetflixDttLocQcError" as c on b."requestId"  = c."requestId" 
select * from all_locqc_view

SELECT * from public."NetflixDttLocQcError"

all_assetqc_view
# asset
select sub* from "NetflixDttAssetQcError" ndad 
sele
select a."titleDesc" ,a.author,  a."requestId" ,a."packageId" ,a."submitDate" ,a."targetLanguageCode" ,a."assetType" , a."contentCategory" ,b."runtimeMinutes" ,
b."issueCount",b.
from "NetflixDttAssetQcResult" as a
left join "NetflixDttAssetQcError" as b on a."requestId" = b."requestId" 

select * from "NetflixDttAssetQcResult"
create view all_assetqc_view
as select a."titleDesc" ,a.author,  a."requestId" ,a."packageId" ,a."submitDate" ,a."targetLanguageCode" ,a."assetType" , a."contentCategory" ,b."runtimeMinutes" ,
b."issueCount"
from "NetflixDttAssetQcResult" as a
left join "NetflixDttAssetQcError" as b on a."requestId" = b."requestId" 


select * from "NetflixDttAssetQcResult"
select count(*) from public."all_locqc_view"
select distinct count(*) from public."all_locqc_view"
select * from public."all_assetqc_view"

select "abandonmentDetailsSheetId" ,"abandonmentDetailsSheetRowNumber"  from "NetflixDttAbandonmentDetail" ndad2 
select abandonmentDetailSheetId,aban* from "NetflixDttAbandonmentDetail" ndad 