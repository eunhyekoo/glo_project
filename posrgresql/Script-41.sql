select * from "ContentTitles" ct 

CREATE view gloqual_sentences_view
as select ct.id as title_id ,tw.id as work_id, ts.id as sentence_id,ct."englishTitle" ,ct."koreanTitle" ,ct."workType" ,ct.client,ct."sourceLanguage" ,ct."targetLanguage" ,tw."episodeNumber",
tw."wordCount" ,ts.sentence  , ts."qcSentence" , ts."sourceSentence", tw."updatedAt" ,tw."createdAt" 
from "ContentTitles" ct 
left join "TranslationWorks" tw ON ct.id = tw."titleId" 
left join "TranslationSentences" ts on tw.id = ts."translationWorkId" 

select * from gloqual_sentences_view order by title_id asc
select count(*) from gloqual_sentences_view
CREATE VIEW mine
AS select * from it t , record r where t.sn = r.sn

출처: https://mine-it-record.tistory.com/396 [나만의 기록들:티스토리]

select count(*) from "ContentTitles" where "targetLanguage"  = 'en-US'
select count(*) from "ContentTitles"
select * from "ContentTitles" ct 
select count(*) from "TranslationSentences" ts 

delete "TranslationSentences"
update "ContentTitles"
set "targetLanguage"  = 'es'
where "targetLanguage"  = 'es-419'
select * from "ContentTitles" where "targetLanguage"  = 'es-419'

delete from "ContentTitles"
delete from "TranslationSentences"
delete from "TranslationWorks"