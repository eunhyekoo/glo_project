SELECT "startedAt", "endedAt", "targetLangCode", ranking, "failRate", denominator, "originationRequestIds", "qcRequestIds"
FROM "NetflixAssetQcRankings"order by "startedAt"  desc


SELECT "startedAt", "endedAt", count("targetLangCode")
FROM "NetflixAssetQcRankings" group by "startedAt" ,"endedAt" order by "startedAt" desc



select * from "NetflixAbandonments" na 

select * from "NetflixAssetQcResults" naqr 
select * from "NetflixOriginationSummaries" nos2 

select * from "NetflixL10nQcResultsReportView" nlnqrrv 
select * from "NetflixOriginationSummaryView" nosv 


# summary

SELECT email, "requestId", "titleId", "packageId", "titleDesc", "assetType", "contentCategory", "reasonCode", "paymentCode", "sourceLangCode", "targetLangCode", "runtimeMins", "currentState", "submittedAt", "dueAt", "startedAt", "isOnTime"
FROM "NetflixOriginationSummaries" where email = 'aguilar.mlaura@gmail.com'

SELECT email, "requestId", "titleId", "packageId", "titleDesc", "assetType", "contentCategory", "reasonCode", "paymentCode", "targetLangCode", "runtimeMins", "currentState", "submittedAt", "dueAt", "startedAt", "isOnTime"
FROM "NetflixL10nQcSummaries"where email = 'aguilar.mlaura@gmail.com'

# resulllllt

SELECT email, "requestId", "titleId", "packageId", "titleDesc", "assetType", "contentCategory", "reasonCode", "sourceLangCode", "targetLangCode", "submittedAt", "qcSubmittedAt", "assetQcTaskType", "netNeutral", "assetQcResult"
FROM "NetflixAssetQcResults" where email = 'aguilar.mlaura@gmail.com'


select 
