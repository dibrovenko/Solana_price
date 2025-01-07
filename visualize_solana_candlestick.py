import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def visualize_solana_candlestick(data):
    # Преобразуем данные в DataFrame
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'], unit='s')  # Преобразуем время в читаемый формат

    # Рассчитаем среднюю цену (Open + Close) / 2
    df['average_price'] = (df['open'] + df['close']) / 2

    # Создаем график
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.03, row_heights=[0.7, 0.3])

    # Добавляем свечной график
    fig.add_trace(go.Candlestick(x=df['time'],
                                 open=df['open'], high=df['high'],
                                 low=df['low'], close=df['close'],
                                 name='Candlesticks'), row=1, col=1)

    # Добавляем линию средней цены
    fig.add_trace(go.Scatter(x=df['time'], y=df['average_price'], mode='lines', line=dict(color='blue'), name='Average Price'), row=1, col=1)

    # Добавляем гистограмму объема
    fig.add_trace(go.Bar(x=df['time'], y=df['volume'], name='Volume'), row=2, col=1)

    # Настройки оформления
    fig.update_layout(title='Solana Price Chart with Average Price',
                      xaxis_rangeslider_visible=False,  # Скрываем ползунок
                      xaxis=dict(type='category'),
                      yaxis_title='Price (USD)',
                      yaxis2_title='Volume',
                      template='plotly_dark')  # Темная тема

    # Отображаем график
    fig.show()