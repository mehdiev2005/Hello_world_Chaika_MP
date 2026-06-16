select * from prices order by price desc limit 5;

select * from prices order by created_at desc limit 10;

select distinct price from prices order by price limit 10;

select * from prices order by price desc offset 20;