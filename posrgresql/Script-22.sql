# title , requestid, packageid, duedate,submmiteddate, abandoneddate, target language, report type, assettype, content category, runtime, subtitle event, all erorors, obj erros, errorcode
select * from "NetflixDttOriginationSummary" ndos 

select count(*) from "NetflixDttLocQcSummary" ndlqs  --3510
select * from "NetflixDttLocQcError"
select count(*) from "NetflixDttLocQcResult" 

select count(*)
 from "NetflixDttLocQcSummary" as a 
 --left join "NetflixDttLocQcResult"  as b on a."requestId"  = b."requestId" 
  join "NetflixDttLocQcError"   as c on a."requestId"  = c."requestId"

select distinct count("titleId") from "NetflixDttLocQcSummary" 
select * from "NetflixDttLocQcSummary" where "locQcer"  = 'kucherjan@gmail.com'
select * from "NetflixDttLocQcResult" where author = 'kucherjan@gmail.com'

select * from "NetflixDttLocQcSummary" on a
left join "Netfl"

select a."locQcer",b.author ,b."titleId" ,b."titleId" ,a."dueDate"  from "NetflixDttLocQcSummary" as a
   left join "NetflixDttLocQcResult" as b on a."locQcer" = b.author and a."titleId" = b. "titleId"

select count(*) from "NetflixDttLocQcSummary" as a
  left join "NetflixDttLocQcResult" as b on a."locQcer" = b.author and a."titleId" = b. "titleId" 

select * fro
select count(*) from "NetflixDttLocQcError" ndlqe 

