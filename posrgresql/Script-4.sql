create table public.dummy_table(
	no	integer 	not null primary key
,	title varchar(300) not null
, 	content text	null
, 	create_dt timestamp(0) not null default current_timestamp
,	update_dt timestamp(0) null
);

select * from dummy_table 

insert into public.dummy_table(no,title, content)
select series as no
     , md5(trunc(random() * 40)::varchar) as title
     , substr('가나다라마바사아자차카타파하ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', trunc(random() * 40)::integer + 1, trunc(random() * 10)::integer) as content
  from generate_series(1, 10000) series;
  
 
 select count(*)
 	from public.dummy_table
 	
 select * from public.dummy_table limit 100;