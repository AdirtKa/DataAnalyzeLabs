"""
BMW Sales Dashboard
===================
Интерактивный дашборд для анализа продаж BMW (2010-2024)

Структурированная версия с разделением на модули.
"""

import dash
from dash import html
import dash_bootstrap_components as dbc

from config import APP_TITLE, APP_DESCRIPTION, MAIN_BG_COLOR, HOST, PORT, DEBUG
from data_loader import load_data
from components import create_kpi_card, create_filter_section, create_graph_card
from callbacks import register_callbacks


# ========== ИНИЦИАЛИЗАЦИЯ ПРИЛОЖЕНИЯ ==========
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)
app.title = APP_TITLE

# ========== ЗАГРУЗКА ДАННЫХ ==========
df = load_data()

# ========== LAYOUT ПРИЛОЖЕНИЯ ==========
app.layout = dbc.Container([
    # Заголовок
    dbc.Row([
        dbc.Col([
            html.H1(f"🚗 {APP_TITLE}", className="text-center mb-1 mt-4"),
            html.P(APP_DESCRIPTION, className="text-center text-muted mb-4"),
        ], width=12)
    ]),

    # KPI метрики
    dbc.Row([
        dbc.Col(html.Div(id='kpi-total-sales'), width=3),
        dbc.Col(html.Div(id='kpi-total-revenue'), width=3),
        dbc.Col(html.Div(id='kpi-avg-price'), width=3),
        dbc.Col(html.Div(id='kpi-top-model'), width=3),
    ], className="mb-4"),

    # Основной контент
    dbc.Row([
        # Левая колонка - фильтры
        dbc.Col([
            create_filter_section(df)
        ], width=3),

        # Правая колонка - графики
        dbc.Col([
            # Первый ряд графиков
            dbc.Row([
                dbc.Col([
                    create_graph_card('sales-trend-graph', 'Динамика продаж по годам')
                ], width=8),

                dbc.Col([
                    create_graph_card('top-models-graph', 'Топ-5 моделей')
                ], width=4),
            ], className="mb-3"),

            # Второй ряд графиков
            dbc.Row([
                dbc.Col([
                    create_graph_card('region-distribution-graph', 'Распределение по регионам')
                ], width=6),

                dbc.Col([
                    create_graph_card('fuel-type-graph', 'Предпочтения по типу топлива')
                ], width=6),
            ], className="mb-3"),

            # Третий ряд графиков
            dbc.Row([
                dbc.Col([
                    create_graph_card('color-distribution-graph', 'Распределение по цветам')
                ], width=6),

                dbc.Col([
                    create_graph_card('classification-graph', 'Классификация продаж')
                ], width=6),
            ], className="mb-3"),

            # Четвёртый ряд графиков
            dbc.Row([
                dbc.Col([
                    create_graph_card('engine-price-scatter', 'Соотношение объёма двигателя и цены')
                ], width=12),
            ], className="mb-3"),
        ], width=9),
    ]),

    # Подвал
    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.P("© 2024 BMW Sales Analytics Dashboard | Данные: 2010-2024",
                   className="text-center text-muted small")
        ], width=12)
    ])
], fluid=True, style={"backgroundColor": MAIN_BG_COLOR})

# ========== РЕГИСТРАЦИЯ CALLBACKS ==========
register_callbacks(app, df)

# ========== ЗАПУСК ПРИЛОЖЕНИЯ ==========
if __name__ == '__main__':
    app.run(
        debug=DEBUG,
        host=HOST,
        port=PORT
    )
