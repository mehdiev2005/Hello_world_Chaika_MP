import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np


# -----------------------------------------------------------------------------
# БЛОК 1: ПОДКЛЮЧЕНИЕ И ИЗВЛЕЧЕНИЕ ДАННЫХ
# -----------------------------------------------------------------------------

try:
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        user="postgres",
        password="example",
        database="testdb"
    )
    print("✓ Подключение установлено")

    # --- Запрос 1: цены по категориям (для boxplot) ---
    df_categories = pd.read_sql("""
        SELECT p.category, pr.price
        FROM prices pr
        JOIN products p ON pr.product_id = p.id
        ORDER BY p.category, pr.price
    """, connection)

    # --- Запрос 2: все цены (для гистограммы) ---
    df_all_prices = pd.read_sql("SELECT price FROM prices", connection)

    # --- Запрос 3: для scatter plot — две цены каждого продукта ---
    # Так как у каждого продукта ровно 2 цены, используем MIN и MAX.
    df_product_prices = pd.read_sql("""
        SELECT 
            p.id,
            p.name,
            MIN(pr.price) AS price1,
            MAX(pr.price) AS price2
        FROM products p
        JOIN prices pr ON p.id = pr.product_id
        GROUP BY p.id, p.name
        ORDER BY p.id
    """, connection)

    # --- Дополнительный запрос: информация о продуктах для аномалий ---
    df_products = pd.read_sql("SELECT id, name, category FROM products", connection)

    print(f"Категорий в выборке:         {df_categories['category'].nunique()}")
    print(f"Всего записей о ценах:       {len(df_all_prices)}")
    print(f"Продуктов с двумя ценами:    {len(df_product_prices)}")

except Exception as error:
    print(f"Ошибка подключения: {error}")
    raise SystemExit

finally:
    connection.close()
    print("✓ Соединение закрыто\n")

# -----------------------------------------------------------------------------
# БЛОК 2: ПОДГОТОВКА ДАННЫХ ДЛЯ ГРАФИКОВ И РАСЧЁТ СТАТИСТИК
# -----------------------------------------------------------------------------

# Статистики для гистограммы
mean_price = df_all_prices['price'].mean()
median_price = df_all_prices['price'].median()
std_price = df_all_prices['price'].std()
q1 = df_all_prices['price'].quantile(0.25)
q3 = df_all_prices['price'].quantile(0.75)
iqr = q3 - q1

# Корреляция между двумя ценами продуктов (для scatter plot)
corr = df_product_prices['price1'].corr(df_product_prices['price2'])

# Порог для аномального расхождения цен (например, 30% от средней цены)
price_diff_threshold = 0.3 * mean_price
df_product_prices['price_diff'] = abs(df_product_prices['price1'] - df_product_prices['price2'])
anomaly_products = df_product_prices[df_product_prices['price_diff'] > price_diff_threshold]

# Выбросы цен по методу IQR (для отдельных цен)
outliers_iqr = df_all_prices[
    (df_all_prices['price'] < q1 - 1.5 * iqr) | 
    (df_all_prices['price'] > q3 + 1.5 * iqr)
]

# -----------------------------------------------------------------------------
# БЛОК 3: ПОСТРОЕНИЕ ГРАФИКОВ (сетка 2×2, последняя ячейка — текст)
# -----------------------------------------------------------------------------

plt.rcParams.update({
    "font.family":       "DejaVu Sans",
    "font.size":         10,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":         True,
    "grid.alpha":        0.3,
    "grid.linestyle":    "--",
    "figure.dpi":        130,
})

fig = plt.figure(figsize=(14, 10))
fig.suptitle("Анализ товарной базы данных", fontsize=15, fontweight="bold", y=0.98)

# Сетка 2×2
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.35)

ax1 = fig.add_subplot(gs[0, 0])  # Boxplot по категориям
ax2 = fig.add_subplot(gs[0, 1])  # Гистограмма распределения цен
ax3 = fig.add_subplot(gs[1, 0])  # Scatter plot (две цены продукта)
ax4 = fig.add_subplot(gs[1, 1])  # Текстовый блок с аномалиями
ax4.axis('off')  # Убираем оси, оставляем только текст

# ── ГРАФИК 1: Boxplot — распределение цен по категориям ──
# Группируем данные для boxplot
categories = df_categories.groupby('category')['price'].apply(list).to_dict()
category_names = list(categories.keys())
category_prices = [categories[cat] for cat in category_names]

bp = ax1.boxplot(category_prices, labels=category_names, patch_artist=True,
                 showmeans=True, meanline=True, meanprops={'color': 'red', 'linestyle': '--'})

# Закрашиваем коробки
for box in bp['boxes']:
    box.set_facecolor('#66c2a5')
    box.set_edgecolor('black')
ax1.set_ylabel("Цена")
ax1.set_title("Распределение цен по категориям\n(медиана, квартили, выбросы)", fontweight="bold")
ax1.grid(axis='y', linestyle='--', alpha=0.7)

# Добавляем подпись с IQR
ax1.text(0.95, 0.95, f"Общий IQR = {iqr:.2f}", transform=ax1.transAxes,
         ha='right', va='top', fontsize=8, bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

# ── ГРАФИК 2: Гистограмма распределения всех цен ──
n_bins = 15
counts, bins, patches = ax2.hist(df_all_prices['price'], bins=n_bins, color='#8da0cb',
                                 edgecolor='white', alpha=0.8, label='Все цены')
# Вертикальные линии среднего и медианы
ax2.axvline(mean_price, color='red', linestyle='-', linewidth=2, label=f'Среднее = {mean_price:.2f}')
ax2.axvline(median_price, color='blue', linestyle='--', linewidth=2, label=f'Медиана = {median_price:.2f}')
ax2.set_xlabel("Цена")
ax2.set_ylabel("Количество товаров")
ax2.set_title("Гистограмма распределения цен", fontweight="bold")
ax2.legend()

# Текст со статистикой на поле графика
stats_text = (f"Всего цен: {len(df_all_prices)}\n"
              f"Среднее: {mean_price:.2f}\n"
              f"Медиана: {median_price:.2f}\n"
              f"Ст. откл.: {std_price:.2f}\n"
              f"IQR: {iqr:.2f}")
ax2.text(0.95, 0.95, stats_text, transform=ax2.transAxes,
         va='top', ha='right', fontsize=8,
         bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='gray', alpha=0.8))

# ── ГРАФИК 3: Scatter plot — сравнение двух цен каждого продукта ──
ax3.scatter(df_product_prices['price1'], df_product_prices['price2'],
            c='#fc8d62', edgecolor='white', s=60, alpha=0.8)

# Линия y = x
min_price = min(df_product_prices['price1'].min(), df_product_prices['price2'].min())
max_price = max(df_product_prices['price1'].max(), df_product_prices['price2'].max())
ax3.plot([min_price, max_price], [min_price, max_price], 'k--', alpha=0.5, label='y = x')

# Выделяем аномальные продукты (большая разница в ценах)
if not anomaly_products.empty:
    ax3.scatter(anomaly_products['price1'], anomaly_products['price2'],
                c='red', edgecolor='black', s=80, marker='o', label='Аномальное расхождение')
    # Добавляем подписи для нескольких самых больших расхождений
    top_anomalies = anomaly_products.nlargest(5, 'price_diff')
    for _, row in top_anomalies.iterrows():
        ax3.annotate(row['name'], (row['price1'], row['price2']),
                     xytext=(5, 5), textcoords='offset points', fontsize=7, alpha=0.8)

ax3.set_xlabel("Первая цена (MIN)")
ax3.set_ylabel("Вторая цена (MAX)")
ax3.set_title("Сравнение двух цен одного продукта", fontweight="bold")
ax3.legend(loc='lower right')
ax3.grid(True, alpha=0.3)

# ── ТЕКСТОВЫЙ БЛОК С АНОМАЛИЯМИ (ax4) ──
anomaly_text = "⚠️ ОБНАРУЖЕННЫЕ АНОМАЛИИ ⚠️\n\n"
anomaly_text += f"1. Ценовые выбросы по методу IQR: {len(outliers_iqr)} шт.\n"
if not outliers_iqr.empty:
    anomaly_text += f"   Примеры: {', '.join(map(str, outliers_iqr['price'].head(3).values))}\n"
anomaly_text += f"\n2. Продукты с аномальной разницей между двумя ценами (>30% от средней цены):\n"
if not anomaly_products.empty:
    for _, row in anomaly_products.iterrows():
        anomaly_text += f"   - {row['name']}: {row['price1']:.2f} vs {row['price2']:.2f} "
        anomaly_text += f"(разница = {row['price_diff']:.2f})\n"
else:
    anomaly_text += "   не обнаружено\n"

anomaly_text += "\n3. Дополнительно:\n"
anomaly_text += f"   - Всего продуктов: {len(df_products)}\n"
anomaly_text += f"   - У всех продуктов есть ровно 2 цены и 2 поставщика (по условию)\n"
anomaly_text += f"   - Корреляция между двумя ценами: {corr:.2f} "

if corr > 0.7:
    anomaly_text += "(сильная положительная связь)\n"
elif corr > 0.3:
    anomaly_text += "(умеренная связь)\n"
else:
    anomaly_text += "(слабая или отсутствует)\n"

ax4.text(0.05, 0.95, anomaly_text, transform=ax4.transAxes,
         va='top', ha='left', fontsize=9, fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='#fff3f3', edgecolor='#d9534f'))

# -----------------------------------------------------------------------------
# БЛОК 5: СОХРАНЕНИЕ
# -----------------------------------------------------------------------------
OUTPUT_FILE = "product_analysis.png"
plt.savefig(OUTPUT_FILE, bbox_inches="tight", dpi=150)
print(f"\n✓ График сохранён: {OUTPUT_FILE}")
plt.show()