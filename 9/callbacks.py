"""
Модуль с callback функциями для обновления графиков
"""

from dash import callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from components import create_kpi_card
from styles import get_graph_layout_params, get_grid_color


def get_filtered_data(df, year_range, region, model, fuel_type, classification):
    """
    Фильтрует данные по параметрам.

    Args:
        df (pd.DataFrame): Исходный DataFrame
        year_range (list): Диапазон лет [начало, конец]
        region (str): Выбранный регион
        model (str): Выбранная модель
        fuel_type (str): Выбранный тип топлива
        classification (str): Выбранная классификация

    Returns:
        pd.DataFrame: Отфильтрованный DataFrame
    """
    filtered_df = df[
        (df['Year'] >= year_range[0]) &
        (df['Year'] <= year_range[1])
        ]

    if region != 'all':
        filtered_df = filtered_df[filtered_df['Region'] == region]
    if model != 'all':
        filtered_df = filtered_df[filtered_df['Model'] == model]
    if fuel_type != 'all':
        filtered_df = filtered_df[filtered_df['Fuel_Type'] == fuel_type]
    if classification != 'all':
        filtered_df = filtered_df[filtered_df['Sales_Classification'] == classification]

    return filtered_df


def register_callbacks(app, df):
    """
    Регистрирует все callback функции приложения.

    Args:
        app: Dash приложение
        df (pd.DataFrame): DataFrame с данными
    """

    @callback(
        [Output('kpi-total-sales', 'children'),
         Output('kpi-total-revenue', 'children'),
         Output('kpi-avg-price', 'children'),
         Output('kpi-top-model', 'children')],
        [Input('year-slider', 'value'),
         Input('region-dropdown', 'value'),
         Input('model-dropdown', 'value'),
         Input('fuel-dropdown', 'value'),
         Input('classification-dropdown', 'value')]
    )
    def update_kpis(year_range, region, model, fuel_type, classification):
        """Обновляет KPI метрики."""
        filtered_df = get_filtered_data(df, year_range, region, model, fuel_type, classification)

        total_sales = filtered_df['Sales_Volume'].sum()
        total_revenue = (filtered_df['Sales_Volume'] * filtered_df['Price_USD']).sum()
        avg_price = filtered_df['Price_USD'].mean()
        top_model = filtered_df.groupby('Model')['Sales_Volume'].sum().idxmax() if len(filtered_df) > 0 else "N/A"

        sales_str = f"{int(total_sales):,}"
        revenue_str = f"${total_revenue / 1e9:.2f}B" if total_revenue >= 1e9 else f"${total_revenue / 1e6:.1f}M"
        avg_price_str = f"${avg_price:,.0f}"

        return (
            create_kpi_card("Всего продаж", sales_str),
            create_kpi_card("Общая выручка", revenue_str),
            create_kpi_card("Средняя цена", avg_price_str),
            create_kpi_card("Топ модель", top_model)
        )

    @callback(
        Output('sales-trend-graph', 'figure'),
        [Input('year-slider', 'value'),
         Input('region-dropdown', 'value'),
         Input('model-dropdown', 'value'),
         Input('fuel-dropdown', 'value'),
         Input('classification-dropdown', 'value')]
    )
    def update_sales_trend(year_range, region, model, fuel_type, classification):
        """Обновляет график динамики продаж по годам."""
        filtered_df = get_filtered_data(df, year_range, region, model, fuel_type, classification)

        yearly_sales = filtered_df.groupby('Year').agg({
            'Sales_Volume': 'sum',
            'Price_USD': 'mean'
        }).reset_index()
        yearly_sales['Revenue'] = yearly_sales['Sales_Volume'] * yearly_sales['Price_USD']

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=yearly_sales['Year'],
            y=yearly_sales['Sales_Volume'],
            mode='lines+markers',
            name='Продажи',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8),
            hovertemplate='<b>Год:</b> %{x}<br><b>Продажи:</b> %{y:,}<extra></extra>'
        ))

        layout_params = get_graph_layout_params()
        layout_params['xaxis'] = dict(title='Год', showgrid=True, gridcolor=get_grid_color())
        layout_params['yaxis'] = dict(title='Объём продаж', showgrid=True, gridcolor=get_grid_color())

        fig.update_layout(**layout_params)
        return fig

    @callback(
        Output('top-models-graph', 'figure'),
        [Input('year-slider', 'value'),
         Input('region-dropdown', 'value'),
         Input('fuel-dropdown', 'value'),
         Input('classification-dropdown', 'value')]
    )
    def update_top_models(year_range, region, fuel_type, classification):
        """Обновляет график топ-5 моделей по продажам."""
        filtered_df = get_filtered_data(df, year_range, region, 'all', fuel_type, classification)

        top_models = filtered_df.groupby('Model')['Sales_Volume'].sum().nlargest(5).reset_index()

        fig = px.bar(
            top_models,
            x='Sales_Volume',
            y='Model',
            orientation='h',
            color='Sales_Volume',
            color_continuous_scale='Blues',
            text='Sales_Volume'
        )

        fig.update_traces(
            texttemplate='%{text:,.0f}',
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Продажи: %{x:,}<extra></extra>'
        )

        layout_params = get_graph_layout_params()
        layout_params['xaxis'] = dict(title='', showgrid=False)
        layout_params['yaxis'] = dict(title='', showgrid=False)
        layout_params['showlegend'] = False
        layout_params['coloraxis_showscale'] = False

        fig.update_layout(**layout_params)
        return fig

    @callback(
        Output('region-distribution-graph', 'figure'),
        [Input('year-slider', 'value'),
         Input('model-dropdown', 'value'),
         Input('fuel-dropdown', 'value'),
         Input('classification-dropdown', 'value')]
    )
    def update_region_distribution(year_range, model, fuel_type, classification):
        """Обновляет график распределения продаж по регионам."""
        filtered_df = get_filtered_data(df, year_range, 'all', model, fuel_type, classification)

        region_sales = filtered_df.groupby('Region')['Sales_Volume'].sum().reset_index()

        fig = px.pie(
            region_sales,
            values='Sales_Volume',
            names='Region',
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Blues_r
        )

        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Продажи: %{value:,}<br>Доля: %{percent}<extra></extra>'
        )

        layout_params = get_graph_layout_params()
        layout_params['showlegend'] = True
        layout_params['legend'] = dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05)

        fig.update_layout(**layout_params)
        return fig

    @callback(
        Output('fuel-type-graph', 'figure'),
        [Input('year-slider', 'value'),
         Input('region-dropdown', 'value'),
         Input('model-dropdown', 'value'),
         Input('classification-dropdown', 'value')]
    )
    def update_fuel_type_distribution(year_range, region, model, classification):
        """Обновляет график распределения по типам топлива."""
        filtered_df = get_filtered_data(df, year_range, region, model, 'all', classification)

        fuel_sales = filtered_df.groupby('Fuel_Type')['Sales_Volume'].sum().reset_index()
        fuel_sales = fuel_sales.sort_values('Sales_Volume', ascending=False)

        fig = px.bar(
            fuel_sales,
            x='Fuel_Type',
            y='Sales_Volume',
            color='Fuel_Type',
            color_discrete_sequence=px.colors.qualitative.Set2,
            text='Sales_Volume'
        )

        fig.update_traces(
            texttemplate='%{text:,.0f}',
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Продажи: %{y:,}<extra></extra>'
        )

        layout_params = get_graph_layout_params()
        layout_params['xaxis'] = dict(title='', showgrid=False)
        layout_params['yaxis'] = dict(title='Объём продаж', showgrid=True, gridcolor=get_grid_color())
        layout_params['showlegend'] = False

        fig.update_layout(**layout_params)
        return fig

    @callback(
        Output('color-distribution-graph', 'figure'),
        [Input('year-slider', 'value'),
         Input('region-dropdown', 'value'),
         Input('model-dropdown', 'value'),
         Input('fuel-dropdown', 'value')]
    )
    def update_color_distribution(year_range, region, model, fuel_type):
        """Обновляет график распределения по цветам автомобилей."""
        filtered_df = get_filtered_data(df, year_range, region, model, fuel_type, 'all')

        color_sales = filtered_df.groupby('Color')['Sales_Volume'].sum().reset_index()
        color_sales = color_sales.sort_values('Sales_Volume', ascending=False)

        fig = px.bar(
            color_sales,
            x='Sales_Volume',
            y='Color',
            orientation='h',
            color='Sales_Volume',
            color_continuous_scale='Viridis',
            text='Sales_Volume'
        )

        fig.update_traces(
            texttemplate='%{text:,.0f}',
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Продажи: %{x:,}<extra></extra>'
        )

        layout_params = get_graph_layout_params()
        layout_params['xaxis'] = dict(title='Объём продаж', showgrid=True, gridcolor=get_grid_color())
        layout_params['yaxis'] = dict(title='', showgrid=False)
        layout_params['showlegend'] = False
        layout_params['coloraxis_showscale'] = False

        fig.update_layout(**layout_params)
        return fig

    @callback(
        Output('classification-graph', 'figure'),
        [Input('year-slider', 'value'),
         Input('region-dropdown', 'value'),
         Input('model-dropdown', 'value'),
         Input('fuel-dropdown', 'value')]
    )
    def update_classification_graph(year_range, region, model, fuel_type):
        """Обновляет график классификации продаж."""
        filtered_df = get_filtered_data(df, year_range, region, model, fuel_type, 'all')

        classification_sales = filtered_df.groupby('Sales_Classification')['Sales_Volume'].sum().reset_index()

        fig = px.pie(
            classification_sales,
            values='Sales_Volume',
            names='Sales_Classification',
            color_discrete_sequence=['#FF6B6B', '#FFA500', '#4ECDC4']
        )

        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Продажи: %{value:,}<br>Доля: %{percent}<extra></extra>'
        )

        layout_params = get_graph_layout_params()
        layout_params['showlegend'] = True

        fig.update_layout(**layout_params)
        return fig

    @callback(
        Output('engine-price-scatter', 'figure'),
        [Input('year-slider', 'value'),
         Input('region-dropdown', 'value'),
         Input('model-dropdown', 'value'),
         Input('fuel-dropdown', 'value'),
         Input('classification-dropdown', 'value')]
    )
    def update_engine_price_scatter(year_range, region, model, fuel_type, classification):
        """Обновляет график зависимости между объёмом двигателя и ценой."""
        filtered_df = get_filtered_data(df, year_range, region, model, fuel_type, classification)

        fig = px.scatter(
            filtered_df,
            x='Engine_Size_L',
            y='Price_USD',
            color='Model',
            size='Sales_Volume',
            hover_data=['Transmission', 'Fuel_Type'],
            title='',
            color_discrete_sequence=px.colors.qualitative.Plotly
        )

        fig.update_traces(
            hovertemplate='<b>%{customdata[0]}</b><br>Объём: %{x}L<br>Цена: $%{y:,.0f}<br>Трансмиссия: %{customdata[1]}<br>Топливо: %{customdata[2]}<extra></extra>'
        )

        layout_params = get_graph_layout_params()
        layout_params['xaxis'] = dict(title='Объём двигателя (литры)', showgrid=True, gridcolor=get_grid_color())
        layout_params['yaxis'] = dict(title='Цена (USD)', showgrid=True, gridcolor=get_grid_color())
        layout_params['height'] = 500
        layout_params['hovermode'] = 'closest'

        fig.update_layout(**layout_params)
        return fig
