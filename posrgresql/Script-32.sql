select count(*) from "ContentTitles" ct 
select count(*) from "TranslationSentences" ts 
select count(*) from "TranslationWorks" tw 

select * from "ContentTitles" ct 

select * from "TranslationWorks" ts 

select * from ContentTitles

select "englishTitle",split_part("englishTitle",'(KO>EN',1) from "ContentTitles" ct3 
where "englishTitle" like '%(KO>EN)'

update "ContentTitles"
set "englishTitle" =  split_part("englishTitle",'(KO>EN',1)
where "englishTitle" like '%(KO>EN)'