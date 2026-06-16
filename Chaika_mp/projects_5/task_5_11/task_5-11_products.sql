select * from PRODUCTS where category = 'Электроника';

select * from products where category = 'Одежда' and name like '%женские%';

select * from PRODUCTS where category in ('Продукты', 'Книги');

select * from PRODUCTS where not category = 'Бытовая техника';

select * from PRODUCTS where category in ('Электроника', 'Одежда', 'Книги');

select * from PRODUCTS where (category = 'Электроника' and name like '%Samsung%') or category = 'Бытовая техника';

select * from PRODUCTS where (category in ('Электроника', '', '') and id between 1 and 15 and not name like '%Samsung%') or category = 'Книги';

