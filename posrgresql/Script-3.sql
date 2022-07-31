select "translateBox" 
FROM "WebtoonEpisodeTask" 

select "translateBox" 
FROM "WebtoonEpisodeTask"  where "translateBox" ->> 'text'='ss';

select "translateBox"->> 'text'
from "WebtoonEpisodeTask"

select "translateBox"-> ''->>'id' as testcolumn
from "WebtoonEpisodeTask"

select "translateBox"
from "WebtoonEpisodeTask"
where "translateBox"  @> '[{"heigth":100}]'

select jsonb_array_elements("translateBox")
from "WebtoonEpisodeTask" wet 


select id,json_Agg( "translateBox" ->>'text')
from (
	select id, jsonb_array_elements("translateBox") as "translateBox" 
	from "WebtoonEpisodeTask" w
	) t
where "translateBox"->>'text' != ''
group by id;


select id, json_agg("translateBox") as tranlsateBox
from (
	select id, jsonb_array_elements("translateBox") as "translateBox" 
	from "WebtoonEpisodeTask" w
	) t
where "translateBox"->>'text' != ''
group by id;

select *
from "WebtoonEpisodeTask" wet 

/* 1. jsonb 데이터를 다루는 방법 확인 
 * 2. 소스 텍스트랑 타겟 텍스트를 비교해보
 * 
 * */

select id,
	   json_agg( "translateBox" ->>'text')  as "sourcetext",
	   words as "targettext"
from (
	select id, jsonb_array_elements("translateBox") as "translateBox", words 
	from "WebtoonEpisodeTask" w
	) t
where "translateBox"->>'text' != ''
group by id,words;

