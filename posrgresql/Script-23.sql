select count(*) from "ContentTitles" ct where "workType"  = 'webnovel'and "createdAt" > '2022-06-17'
select * from "ContentTitles"
select distinct id,  "englishTitle" ,"koreanTitle" from "ContentTitles"  where "workType"  = 'webnovel' order by id 

select *  from "ContentTitles" ct where "workType"  = 'webnovel' and "createdAt" > '2022-06-17' order by id 
select * from "ContentTitles" ct 
select count(*) from "TranslationSentences" ts -- 3907514
select count(*) from "TranslationWorks" tw 


select  split_part("englishTitle",'WEBTOON ID>EN',2) from "ContentTitles" ct3 
where "englishTitle" like '%WEBTOON ID>EN%'

update "ContentTitles"
set "englishTitle" =  split_part("englishTitle",'WEBTOON ID>EN',2)
where "englishTitle" like '%WEBTOON ID>EN%'

select split_part("englishTitle",'WEBTOON KO>EN',2), * from "ContentTitles" ct3 
where "englishTitle" like '%WEBTOON KO>EN%'


update "ContentTitles"
set "englishTitle" =  split_part("englishTitle",'WEBTOON KO>EN',2)
where "englishTitle" like '%WEBTOON KO>EN%'


select split_part("englishTitle",'KO>EN',1), * from "ContentTitles" ct3 
where "englishTitle" like 'KO>EN%'

update "ContentTitles"
set "englishTitle" =  split_part("englishTitle",'KO>EN',1)
where "englishTitle" like '%KO>EN'

