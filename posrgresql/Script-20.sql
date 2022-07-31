DELETE FROM "ContentTitles"

DELETE FROM 
"TranslationSentences"  a 
USING "TranslationWorks"  b
USING "ContentTitles"  c
where a."translationWorkId" = b.id
and b.titleId = c.id
and a.client =  'NAVER'

DELETE



select * from "ContentTitles" as a where client = 'NAVER'
	left join "TranslationWorks"   as b on a.id = b."titleId" 
--left join "TranslationSentences" as c on b.id = c."translationWorkId"
where a.client = 'NAVER'

DELETE FROM "TranslationWorks"

select count(*) from "ContentTitles" ct 
select count(*) from "TranslationSentences" ts # 3923631
select count(*) from "TranslationWorks" tw #920

select * from "ContentTitles"
where "englishTitle" =  'WEBTOON ID>EN, MAYA'S WORLD'
select distinct "englishTitle"  from "ContentTitles" ct 
select * from "TranslationSentences" ts 
select * from "TranslationWorks" tw 