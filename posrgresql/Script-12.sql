- 요구사항 
- 생성된 모든 클라이언트 수
    - 각 입력란이 채워진 비율
- 생성된 모든 프로젝트 수
    - 각 입력란이 채워진 비율
- 생성된 모든 인보이스 수
    - 각 입력란이 채워진 비율
    
select count(*) from "Client"  c  # 103
select count(*) from "Project"
select count(*) from "Invoice"

select * from "Client" c 
select * from "Project" p 
select * from "Invoice" i2 

# client 기준 
# 1723


select c."id",p."clientId" ,p.id 
from "Client" c
left join "Project" p on c.id  = p."clientId" 
left join "Invoice" i on p.id = i."projectId" 
group by c."userId" ,i."projectId" ,p.id 



select c."userId",i."projectId" ,count(*)
from "Client" c
left join "Project" p on c.id  = p."clientId" 
left join "Invoice" i on p.id = i."projectId" 
group by c."userId" ,i."projectId" 

select count(*)
from "Client" c
left join "Project" p on c.id  = p."clientId" 
left join "Invoice" i on p.id = i."projectId" 
--group by c."userId" ,i."projectId" 


# 아예 카운트값으로 넘겨줄지, 데이터를 넘겨서 대시보드 에서 카운트할지 
select * from "Client" 
select * from "Project" p 
select "userId" , count(*) from "Project" group by "userId"  # 유저별 프로젝트
select "id" , count(*) from "Project" group by "id"  # 유저별 프로젝트
select "projectId",count(*) from "Invoice" group by "projectId" # 프로젝트별 invoice 



select * from "Client" c
left join "Project" as p 


select c."userId" ,count(*)
from "Client" c
left join "Project" p on c."userId"  = p."userId" 
group by c."userId" 



								  
select * from "Project"

select count(*) from "Project"
select * from "Project" 
select count(*) from "Project" p # 140

select distinct "userId"  from "Project" p 
select "userId",count(id)  from "Project" group by "userId" #유저 : 프로젝트 개수 

select count(*) from "Project" p 

select * from "Invoice" i 
select count(*) from "Invoice" # 115개 

select count(*) from "Project" p  
		 join "Invoice" i  on p.id  = i."projectId" 
		 
# 각 카운트 값 (클라이언트, 프로젝트, 인보이)
select (select count(*) from "Client") as clientcount,
	   (select count(*) from "Project") as Projcectcount,
	   (select count(*) from "Invoice") as Invoicecount
	   
# 유저별 프로젝트 개수 
select "userId",count(id)  from "Project" group by "userId"

# 프로젝트id  인보이스개수
select p.id ,count(i."projectId")  from "Project" p  
		 left join "Invoice" i  on p.id  = i."projectId" 
		 group by p.id
	   
select "userId",p.id as projectid ,count(i."projectId") as invoicecount
	from "Project" p
    left join "Invoice" i ON p.id = i."projectId" 
    group by p."userId" ,p.id
						

    
    