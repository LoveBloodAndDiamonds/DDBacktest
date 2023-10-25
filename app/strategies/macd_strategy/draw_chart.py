import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_chart(df):
    # Создание подграфиков
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3])

    # График OHLC
    fig.add_trace(go.Candlestick(x=df['datetime'],
                                 open=df['open'],
                                 high=df['high'],
                                 low=df['low'],
                                 close=df['close'],
                                 name='OHLC',
                                 showlegend=False), row=1, col=1)

    # # Настраиваем цвет фона
    # fig.update_layout(
    #     plot_bgcolor='rgba(0, 0, 0, 0.7)',  # Задаем цвет фона (в данном случае темно-серый)
    #     paper_bgcolor='rgba(0, 0, 0, 0.7)'  # Задаем цвет фона области рисунка (в данном случае темно-серый)
    # )

    # Убираем решетку с осей
    fig.update_xaxes(showgrid=False)  # Убираем решетку с оси X
    fig.update_yaxes(showgrid=False)  # Убираем решетку с оси Y

    # График MACD
    fig.add_trace(go.Scatter(x=df['datetime'], y=df['macd'], name='MACD', line=dict(color='blue')), row=2, col=1)
    fig.add_trace(go.Scatter(x=df['datetime'], y=df['signal'], name='Signal', line=dict(color='orange')), row=2, col=1)
    fig.add_trace(go.Bar(x=df['datetime'], y=df['histogram'], name='Histogram'), row=2, col=1)

    # Отметка свечей с помощью синих точек
    pump_candles = df[df['is_pump']]
    fig.add_trace(go.Scatter(x=pump_candles['datetime'],
                             y=pump_candles['close'],
                             mode='markers',
                             marker=dict(color='blue', size=14),
                             name='Pump Candles'), row=1, col=1)

    hist_signal = df[df['hist_signal']]
    fig.add_trace(go.Scatter(x=hist_signal['datetime'],
                             y=hist_signal['close'],
                             mode='markers',
                             marker=dict(color='purple', size=15),
                             name='Hist sygnal'), row=1, col=1)

    # macd_signal_short = df[df['macd_signal_short']]
    # fig.add_trace(go.Scatter(x=macd_signal_short['datetime'],
    #                          y=macd_signal_short['close'],
    #                          mode='markers',
    #                          marker=dict(color='yellow', size=15),
    #                          name='MACD sygnal'), row=1, col=1)

    lines = list()
    for i, r in hist_signal.iterrows():
        close = r["close"]
        lines.append(
            go.Scatter(
                x=[df.iloc[0]["datetime"], df.iloc[-1]["datetime"]],
                y=[close, close],
                mode='lines',
                line=dict(color='white', width=2),
                name='Entry'
            )
        )
        lines.append(
            go.Scatter(
                x=[df.iloc[0]["datetime"], df.iloc[-1]["datetime"]],
                y=[close * 1.02, close * 1.02],
                mode='lines',
                line=dict(color='red', width=4),
                name='Stop'
            )
        )
        lines.append(
            go.Scatter(
                x=[df.iloc[0]["datetime"], df.iloc[-1]["datetime"]],
                y=[close * 0.98, close * 0.98],
                mode='lines',
                line=dict(color='green', width=4),
                name='Take'
            )
        )

    for line in lines:
        fig.add_trace(line, row=1, col=1)

    fig.update_layout(xaxis_rangeslider_visible=False)
    # Настройка оформления графика
    fig.update_layout(title='Combined Chart')

    # Отображение графика
    fig.show()
