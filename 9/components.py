"""
Модуль для создания переиспользуемых компонентов интерфейса
"""

from dash import dcc, html
import dash_bootstrap_components as dbc
from config import CARD_BG_COLOR
from styles import get_dropdown_style


def create_kpi_card(title, value, icon=""):
    """
    Создаёт карточку с KPI метрикой.

    Args:
        title (str): Название метрики
        value (str): Значение метрики
        icon (str): Иконка (опционально)

    Returns:
        dbc.Card: Карточка с метрикой
    """
    return dbc.Card(
        dbc.CardBody([
            html.H6(title, className="text-muted mb-2"),
            html.H3(value, className="mb-0 text-white font-weight-bold"),
        ]),
        className="mb-3",
        style={"backgroundColor": CARD_BG_COLOR, "border": "none"}
    )


def create_filter_section(df):
    """
    Создаёт секцию с фильтрами для дашборда.

    Args:
        df (pd.DataFrame): DataFrame с данными

    Returns:
        dbc.Card: Карточка с фильтрами
    """
    dropdown_style = get_dropdown_style()

    return dbc.Card(
        dbc.CardBody([
            html.H5("Фильтры", className="mb-3"),

            # Фильтр по годам
            html.Label("Период:", className="fw-bold mt-2"),
            dcc.RangeSlider(
                id='year-slider',
                min=int(df['Year'].min()),
                max=int(df['Year'].max()),
                value=[int(df['Year'].min()), int(df['Year'].max())],
                marks={str(year): str(year) for year in range(int(df['Year'].min()), int(df['Year'].max()) + 1, 2)},
                step=1,
                tooltip={"placement": "bottom", "always_visible": True}
            ),

            html.Br(),

            # Фильтр по регионам
            html.Label("Регион:", className="fw-bold mt-3"),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': 'Все регионы', 'value': 'all'}] +
                        [{'label': region, 'value': region} for region in sorted(df['Region'].unique())],
                value='all',
                clearable=False,
                className="mb-3",
                style=dropdown_style
            ),

            # Фильтр по моделям
            html.Label("Модель:", className="fw-bold"),
            dcc.Dropdown(
                id='model-dropdown',
                options=[{'label': 'Все модели', 'value': 'all'}] +
                        [{'label': model, 'value': model} for model in sorted(df['Model'].unique())],
                value='all',
                clearable=False,
                className="mb-3",
                style=dropdown_style
            ),

            # Фильтр по типу топлива
            html.Label("Тип топлива:", className="fw-bold"),
            dcc.Dropdown(
                id='fuel-dropdown',
                options=[{'label': 'Все типы', 'value': 'all'}] +
                        [{'label': fuel, 'value': fuel} for fuel in sorted(df['Fuel_Type'].unique())],
                value='all',
                clearable=False,
                className="mb-3",
                style=dropdown_style
            ),

            # Фильтр по классификации продаж
            html.Label("Классификация продаж:", className="fw-bold"),
            dcc.Dropdown(
                id='classification-dropdown',
                options=[{'label': 'Все классификации', 'value': 'all'}] +
                        [{'label': cls, 'value': cls} for cls in sorted(df['Sales_Classification'].unique())],
                value='all',
                clearable=False,
                className="mb-3",
                style=dropdown_style
            ),
        ]),
        className="mb-3",
        style={"backgroundColor": CARD_BG_COLOR, "border": "none"}
    )


def create_graph_card(graph_id, title):
    """
    Создаёт карточку с графиком.

    Args:
        graph_id (str): ID графика
        title (str): Название графика

    Returns:
        dbc.Card: Карточка с графиком
    """
    return dbc.Card(
        dbc.CardBody([
            html.H5(title, className="mb-3"),
            dcc.Graph(id=graph_id)
        ]),
        style={"backgroundColor": CARD_BG_COLOR, "border": "none"}
    )
