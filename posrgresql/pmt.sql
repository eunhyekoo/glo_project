select * from "Client" 
select count(*) from "Client" c  # 103

select * from "Project" 
select count(*) from "Project" p # 140

select distinct "userId"  from "Project" p 
select "userId",count(id)  from "Project" group by "userId" #유저 : 프로젝트 개수 


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
						
