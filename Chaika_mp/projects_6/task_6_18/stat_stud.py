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
        SELECT
            s.student_id,
            s.first_name || ' ' || s.last_name  AS student_name,
            s.enrollment_year,
            c.course_name,
            c.credits,
            e.grade
        FROM enrollments e
        JOIN students  s ON e.student_id  = s.student_id
        JOIN courses   c ON e.course_id   = c.course_id
        ORDER BY s.enrollment_year, s.student_id
    """

    df = pd.read_sql(query, connection)

    print(df.head(10))
    print(df.info())
    print(f"\nВсего записей: {len(df)}")
    print(f"Уникальных студентов: {df['student_id'].nunique()}")
    print(f"Уникальных курсов:   {df['course_name'].nunique()}")

    # Способ 1 — автоматический отчёт pandas
    print("\n=== describe() ===")
    print(df['grade'].describe().round(2))

    # Способ 2 — посчитать каждую метрику вручную
    print("\n=== Метрики вручную ===")
    metrics = {
        'Среднее (mean)'         : df['grade'].mean(),
        'Медиана (median)'       : df['grade'].median(),
        'Ст. отклонение (std)'   : df['grade'].std(),
        'Минимум (min)'          : df['grade'].min(),
        'Максимум (max)'         : df['grade'].max(),
    }

    for name, val in metrics.items():
        print(f"  {name:30s}: {val:.2f}")

    q1  = df['grade'].quantile(0.25)
    q2  = df['grade'].quantile(0.50)
    q3  = df['grade'].quantile(0.75)
    iqr = q3 - q1

    print(f"Q1  (25%): {q1}")
    print(f"Q2  (50%): {q2}")
    print(f"Q3  (75%): {q3}")
    print(f"IQR (Q3-Q1): {iqr}")

    # Процент студентов с оценкой 5 (отличников)
    pct_5 = (df['grade'] == 5).mean() * 100
    print(f"\nДоля оценок '5': {pct_5:.1f}%")

    # Частота каждой оценки
    print("\nРаспределение оценок:")
    print(df['grade'].value_counts().sort_index())

    # Средняя оценка и количество оценок по годам
    by_year = df.groupby('enrollment_year')['grade'].agg(
        count='count',
        mean='mean',
        median='median',
        std='std',
        min='min',
        max='max'
    ).round(2)

    print("\n=== Успеваемость по потокам ===")
    print(by_year)

    # Разница в средней оценке между 2023 и 2024
    m2023 = by_year.loc[2023, 'mean']
    m2024 = by_year.loc[2024, 'mean']
    print(f"\nРазница (2024 − 2023): {m2024 - m2023:+.2f}")

    by_course = df.groupby('course_name')['grade'].agg(
        enrollments='count',
        avg_grade='mean',
        std_grade='std'
    ).round(2).\
    sort_values('avg_grade', ascending=False)

    print("\n=== Рейтинг курсов по средней оценке ===")
    print(by_course.to_string())

    # Самый «лёгкий» и самый «сложный» курс
    print(f"\nЛучший результат: {by_course.index[0]}")
    print(f"Худший результат: {by_course.index[-1]}")

except Exception as error:
    print(f"Ошибка при подключении: {error}")