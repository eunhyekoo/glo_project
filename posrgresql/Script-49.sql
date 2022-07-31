-- public.all_locqc_view source

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
     
    
    
    -- public.all_assetqc_view source

CREATE OR REPLACE VIEW public.all_assetqc_view
AS SELECT a."assetQcResultsSheetId",
    a."assetQcResultsSheetRowNumber",
    b."assetQcErrorsSheetId",
    b."assetQcErrorsSheetRowNumber",
    a."titleDesc",
    a.author,
    a."requestId",
    a."packageId",
    a."submitDate",
    a."targetLanguageCode",
    a."assetType",
    a."contentCategory",
    b."runtimeMinutes",
    b."issueCount",
    b."issueCode"
   FROM "NetflixDttAssetQcResult" a
     LEFT JOIN "NetflixDttAssetQcError" b ON a."requestId"::text = b."requestId"::text;