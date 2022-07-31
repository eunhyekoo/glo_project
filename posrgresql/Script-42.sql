select * from "ContentTitles" ct where "workType"  = 'webnovel'
select * from "TranslationWorks" tw 
select * from "TranslationSentences" ts 

select ct.id,tw.id, ts.id,"englishTitle" ,"koreanTitle" ,"workType" ,client,"sourceLanguage" ,"targetLanguage" ,tw."episodeNumber",
tw."wordCount" ,ts.sentence  , ts."qcSentence" , ts."sourceSentence", tw."updatedAt" ,tw."createdAt" 
from "ContentTitles" ct 
left join "TranslationWorks" tw ON ct.id = tw."titleId" 
left join "TranslationSentences" ts on tw.id = ts."translationWorkId" 

CREATE view gloqual_sentences_view
as select ct.id as title_id ,tw.id as work_id, ts.id as sentence_id,ct."englishTitle" ,ct."koreanTitle" ,ct."workType" ,ct.client,ct."sourceLanguage" ,ct."targetLanguage" ,tw."episodeNumber",
tw."wordCount" ,ts.sentence  , ts."qcSentence" , ts."sourceSentence", tw."updatedAt" ,tw."createdAt" 
from "ContentTitles" ct 
left join "TranslationWorks" tw ON ct.id = tw."titleId" 
left join "TranslationSentences" ts on tw.id = ts."translationWorkId"  
id 


select distinct  "workType"  from gloqual_sentences_view gsv 

select count(*) from gloqual_sentences_view gsv  where "workType"  = 'webtoon'
select count(*) from gloqual_sentences_view gsv  where "workType"  = 'webnovel'

select * from gloqual_sentences_view gsv
select count(*) from "TranslationWorks" tw 
select sum("wordCount") from gloqual_works_view
select * from gloqual_works_view gwv 

select count(*) from gloqual_works_view gwv 
select * from "TranslationWorks" tw2 
select count(*) from "ContentTitles" ct 
left join "TranslationWorks" tw ON  ct.id = tw."titleId" 


title_id 

SELECT "workId", "createdAt", "updatedAt", "episodeNumber", "wordCount", "sourceText", "targetText",
"targetTextAfterQc", "englishTitle", "workType", client, genre, "sourceLanguage",
"targetLanguage", "koreanTitle", "isRrated", pm, poc, translator, qcer
FROM gloqual_works_view;


CREATE view gloqual_works_view
as
select ct.id as title_id, tw.id as work_id, tw."createdAt" ,tw."updatedAt" ,tw."episodeNumber",tw."wordCount" ,tw."sourceText" ,tw."targetText" 
,tw."targetTextAfterQc" ,ct."englishTitle" ,ct."koreanTitle" ,ct."workType" ,ct.client ,ct.genre ,ct."sourceLanguage" ,ct."targetLanguage" 
,ct."isRrated" 
from "ContentTitles" ct  
left join "TranslationWorks" tw ON ct.id = tw."titleId" 



select length("sourceText"),* from "TranslationWorks" tw2 
select ct.id as title_id, tw.id as work_id, tw."createdAt" ,tw."updatedAt" ,tw."episodeNumber",tw."wordCount" ,tw."sourceText" ,tw."targetText" 
,tw."targetTextAfterQc" ,ct."englishTitle" ,ct."koreanTitle" ,ct."workType" ,ct.client ,ct.genre ,ct."sourceLanguage" ,ct."targetLanguage" 
,ct."isRrated" 
from "ContentTitles" ct  
left join "TranslationWorks" tw ON ct.id = tw."titleId" 
left join "TranslationSentences" ts ON tw."id" = ts."translationWorkId" 

select ct.id, tw.id,count(*)
from "ContentTitles" ct  
left join "TranslationWorks" tw ON ct.id = tw."titleId" 
left join "TranslationSentences" ts ON tw."id" = ts."translationWorkId" 
group by ct.id,tw.id 






