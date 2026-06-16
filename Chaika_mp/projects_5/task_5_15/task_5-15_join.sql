select
	p.name as Название_товара,
	pr.price as Цена
from products as p
join prices as pr on p.id = pr.product_id 