select product_id, count (*)
from prices;

select product_id, avg(price)
from prices 
group by product_id;

select product_id, min(price)
from prices 
group by product_id;

select product_id, max(price)
from prices 
group by product_id;