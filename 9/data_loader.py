"""
Модуль для загрузки и обработки данных
"""

import pandas as pd
import numpy as np
from config import DATA_PATH


def load_data():
    """
    Загружает данные о продажах BMW из CSV файла.

    Returns:
        pd.DataFrame: DataFrame с данными о продажах

    Raises:
        FileNotFoundError: Если файл данных не найден
    """
    try:
        df = pd.read_csv(DATA_PATH)
        df = _process_data(df)
        return df
    except FileNotFoundError:
        print(f"Файл {DATA_PATH} не найден. Используются демонстрационные данные.")
        return create_demo_data()


def _process_data(df):
    """
    Обрабатывает загруженные данные (преобразование типов).

    Args:
        df (pd.DataFrame): Исходный DataFrame

    Returns:
        pd.DataFrame: Обработанный DataFrame
    """
    if 'Year' in df.columns:
        df['Year'] = df['Year'].astype(int)
    if 'Price_USD' in df.columns:
        df['Price_USD'] = pd.to_numeric(df['Price_USD'], errors='coerce')
    if 'Sales_Volume' in df.columns:
        df['Sales_Volume'] = pd.to_numeric(df['Sales_Volume'], errors='coerce')
    if 'Engine_Size_L' in df.columns:
        df['Engine_Size_L'] = pd.to_numeric(df['Engine_Size_L'], errors='coerce')
    if 'Mileage_KM' in df.columns:
        df['Mileage_KM'] = pd.to_numeric(df['Mileage_KM'], errors='coerce')

    return df


def create_demo_data():
    """
    Создаёт демонстрационные данные для тестирования дашборда.

    Returns:
        pd.DataFrame: DataFrame с демонстрационными данными
    """
    years = list(range(2010, 2025))
    models = ['3 Series', '5 Series', '7 Series', 'X3', 'X5', 'X7', 'i4', 'iX']
    regions = ['Europe', 'North America', 'Asia', 'Middle East', 'Africa']
    colors = ['Black', 'White', 'Silver', 'Gray', 'Blue', 'Red']
    fuel_types = ['Petrol', 'Diesel', 'Hybrid', 'Electric']
    transmissions = ['Automatic', 'Manual']
    sales_classifications = ['Low', 'Medium', 'High']

    data = []
    for year in years:
        for _ in range(150):
            engine_size = np.random.choice([1.5, 2.0, 2.5, 3.0, 3.5, 4.0])
            price = np.random.randint(30000, 150000)
            sales_vol = np.random.randint(10, 500)

            data.append({
                'Model': np.random.choice(models),
                'Year': year,
                'Region': np.random.choice(regions),
                'Color': np.random.choice(colors),
                'Fuel_Type': np.random.choice(fuel_types),
                'Transmission': np.random.choice(transmissions),
                'Engine_Size_L': engine_size,
                'Mileage_KM': np.random.randint(5000, 300000),
                'Price_USD': price,
                'Sales_Volume': sales_vol,
                'Sales_Classification': np.random.choice(sales_classifications)
            })

    return pd.DataFrame(data)


def get_unique_values(df, column):
    """
    Возвращает отсортированные уникальные значения столбца.

    Args:
        df (pd.DataFrame): DataFrame
        column (str): Название столбца

    Returns:
        list: Отсортированный список уникальных значений
    """
    return sorted(df[column].unique())
