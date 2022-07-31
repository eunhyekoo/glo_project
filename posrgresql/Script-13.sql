select * from "ContentTitles" ct 
select * from "TranslationSentences" ts 
select * from "TranslationWorks" tw 

select count(*) from "ContentTitles" ct # 66
select count(*) from "TranslationSentences" ts # 1,520,366
select count(*) from "TranslationWorks" tw  #1501

select * from "ContentTitles" ct order by id

# 전처리

select substring()"englishTitle"  from "ContentTitles" ct order by id

select * from "ContentTitles" ct2  where client = 'Naver'
select split_part("englishTitle",'(KO>EN)',1)from "ContentTitles" ct 
where client = 'Naver'

select  split_part("englishTitle",'WEBTOON ID>EN',2),* from "ContentTitles" ct3 
where "englishTitle" like 'WEBTOON ID>EN%'


#고객사명 분리 
update "ContentTitles"
set "englishTitle" = split_part("englishTitle",'[Naver]',2)
where "englishTitle" like '%Naver%'

# 소스 타겟 언어 제거 - NAVER
update "ContentTitles"
set "englishTitle" = split_part("englishTitle",'(KO>EN)',1)
where client = 'Naver'

select * from "ContentTitles" where client = 'Naver'
