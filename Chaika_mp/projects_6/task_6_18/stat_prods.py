import psycopg2
import pandas as pd

try:
    # Устанавливаем соединение
    connection = psycopg2.connect(
        host="localhost",          # База в контейнере, но доступна через localhost
        port="5432",               # Порт из секции ports
        user="postgres",           # POSTGRES_USER
        password="example",        # POSTGRES_PASSWORD
        database="testdb"          # POSTGRES_DB
    )
    print("✓ Подключение установлено")

    query = """
        select
        	prices.price,
            p.id,
            p.name,
            p.category 
        FROM products p 
        JOIN prices ON p.id  = prices.product_id
    """

    df = pd.read_sql(query, connection)


    print("\n=== Метрики вручную ===")
    metrics = {
        'Среднее (mean) (руб.)'         : df['price'].mean(),
        'Медиана (median) (руб.)'       : df['price'].median(),
        'Ст. отклонение (std) (руб.)'   : df['price'].std(),
        'Минимум (min) (руб.)'          : df['price'].min(),
        'Максимум (max) (руб.)'         : df['price'].max(),
    }

    for name, val in metrics.items():
        print(f"  {name:30s}: {val:.2f}")

    q1  = df['price'].quantile(0.25).round(2)
    q2  = df['price'].quantile(0.50).round(2)
    q3  = df['price'].quantile(0.75).round(2)
    iqr = q3 - q1

    print(f"Q1  (25%): {q1}")
    print(f"Q2  (50%): {q2}")
    print(f"Q3  (75%): {q3}")
    print(f"IQR (Q3-Q1): {iqr}")

    filtered_df = df[df['price'] > q3]
    print(filtered_df)








    by_category = df.groupby('category')['price'].agg(
        count='count',
        mean='mean',
        median='median',
        std='std'
    ).round(2).sort_values('mean', ascending=False)

    print("\n=== Цены по категориям ===")
    print(by_category)

    result = df.groupby('id').agg(
        name=('name', 'first'),
        category=('category', 'first'),
        min_price=('price', 'min'),
        max_price=('price', 'max')
    )
    result['price_range'] = result['max_price'] - result['min_price']

    top5 = result.sort_values('price_range', ascending=False).head(5)

    print(top5[['name', 'category', 'min_price', 'max_price', 'price_range']])

except Exception as error:
    print(f"Ошибка при подключении: {error}")