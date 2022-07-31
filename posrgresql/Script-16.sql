select "locQcer"  from "NetflixDttLocQcSummary" ndlqs 

select * from "NetflixDttOriginationSummary" ndos 
where "submitDate" between '2022-05-01' and '2022-06-01'

# 1. OTD 
# on_time = 1 / 모든 task  * 100
# 1) origination
# 프리랜서 구분 컬럼 :

select author ,
	   count(*) as 전체 
 	   ,(select count(*) from "NetflixDttOriginationSummary" where "isOnTime" =true and ndos.author = author group by author ) as ontime_count
	   ,((select count(*) from "NetflixDttOriginationSummary" where "isOnTime" =true and ndos.author = author group by author )/count(*) )  * 100 as OTD
from "NetflixDttOriginationSummary" ndos 
group by author 

# 2)QC

select "locQcer"  ,
	   count(*) as 전체 
 	   ,(select count(*) from "NetflixDttLocQcSummary" where "isOnTime" =true and ndos."locQcer"  = "locQcer"  group by "locQcer"  ) as ontime_count
	   ,(select count(*) from "NetflixDttLocQcSummary" where "isOnTime" =true and ndos."locQcer"  = "locQcer"  group by "locQcer"  )/count(*)  * 100 as OTD
from "NetflixDttLocQcSummary" ndos 
group by "locQcer" 



