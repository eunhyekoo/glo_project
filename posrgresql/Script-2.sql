select * from dummy_table2
select count(*) from dummy_table2

select count(*) from (
select * from dummy_table
union all
select * from dummy_table2) as a