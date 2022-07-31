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