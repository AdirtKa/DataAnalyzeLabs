"""
Модуль для работы со стилями и оформлением
"""

from config import CARD_BG_COLOR, PRIMARY_COLOR


def get_card_style():
    """Возвращает стиль карточки."""
    return {
        "backgroundColor": CARD_BG_COLOR,
        "border": "none"
    }


def get_kpi_card_body_style():
    """Возвращает стиль тела KPI карточки."""
    return {
        "padding": "15px",
        "border-radius": "5px"
    }


def get_dropdown_style():
    """Возвращает стиль для dropdown."""
    return {
        'color': 'black',
        'backgroundColor': 'white'
    }


def get_graph_layout_params():
    """Возвращает параметры layout для графиков."""
    return {
        'template': 'plotly_dark',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'margin': dict(l=10, r=10, t=10, b=10),
        'hovermode': 'x unified'
    }


def get_grid_color():
    """Возвращает цвет сетки графика."""
    return 'rgba(128,128,128,0.2)'
