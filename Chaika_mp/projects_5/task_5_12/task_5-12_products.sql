select category, count (*)
from products 
group by category;

select category, count (*)
from products 
group by category
order by count desc;