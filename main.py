import pandas
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import technical_analysis as ta
import os

df: pd.DataFrame = pd.read_csv('OCK-0172.csv')

df.drop(labels=df.loc[(df['Volume'] <= 0) | (df.isnull().any(axis=1))].index.tolist(), inplace=True)
df.reset_index(drop=True, inplace=True)
df['Date'] = pd.to_datetime(df['Date'])
df['Volume'] = df['Volume'].astype(np.float32)

df['21MA'] = df['Close'].rolling(window=21).mean()

macd, signal = ta.macd(close=df['Close'])
rsi = ta.rsi(close=df['Close'])
k, d = ta.stochastic(high=df['High'], low=df['Low'], close=df['Close'])
bb_upper, bb_middle, bb_lower = ta.bollinger_bands(close=df['Close'])
cci = ta.commodity_channel_index(high=df['High'], low=df['Low'], close=df['Close'])

df = pd.concat([df, macd, signal, rsi], axis=1)

PROJECT_DIR = os.path.dirname(__file__)
SOURCES_DIR = os.path.join(PROJECT_DIR, 'sources')

# if not os.path.exists(SOURCES_DIR):
#     os.mkdir(SOURCES_DIR)
#     print('Directory created successfully!')
# df.to_csv(os.path.join(SOURCES_DIR, 'PIE-5211.csv'), index=False)

# buy_called = df[(df['RSI_14'] < 30) & (df['Close'] < df['LOWER2']) & (df['%K_14'] < 20) & (df['MACD_12_26'] < -0.01)].copy()
# print(buy_called)
# sell_called = df[((df['RSI_14'] > 70) & (df['Close'] > df['UPPER2'])) | ((df['Close'] > df['UPPER2']) & (df['%K_14'] > 80))].copy()
# print(sell_called[50:])


# fig = go.Figure(data=[go.Candlestick(x=df.index,
#                                      open=df['Open'],
#                                      close=df['Close'],
#                                      high=df['High'],
#                                      low=df['Low'])
#                       ])

fig = make_subplots(specs=[[{'secondary_y': True}], [{'secondary_y': False}], [{'secondary_y': False}]],
                    rows=3,
                    cols=1,
                    shared_xaxes=True,
                    subplot_titles=['', '', ''],
                    row_heights=[0.6, 0.2, 0.2])

fig.add_trace(trace=go.Candlestick(x=df.index,
                                   open=df['Open'],
                                   close=df['Close'],
                                   high=df['High'],
                                   low=df['Low'],
                                   showlegend=False),
              secondary_y=True,
              row=1, col=1)

# fig.add_trace(trace=go.Scatter(x=df.index,
#                                y=df['21MA'],
#                                line=dict(color='#e0e0e0'),
#                                name='MA21'),
#               secondary_y=True,
#               row=1, col=1
#               )

volume_colors = ['green' if row['Open'] - row['Close'] >= 0 else 'red' for index, row in df.iterrows()]
fig.add_trace(trace=go.Bar(x=df.index,
                           y=df['Volume'],
                           name='Volume',
                           marker=dict(color=volume_colors),
                           showlegend=False),
              secondary_y=False,
              row=1, col=1
              )

fig.add_trace(trace=go.Scatter(x=[999, 1000],
                               y=[3.2, 3.2],
                               mode='markers',
                               marker=dict(symbol='triangle-down', size=10),
                               name='Signal called'),
              secondary_y=True,
              row=1, col=1
              )

fig.add_trace(trace=go.Scatter(x=df.index,
                               y=df['MACD_12_26'],
                               name='MACD'),
              row=2, col=1
              )

fig.add_trace(trace=go.Scatter(x=df.index,
                               y=df['SIGNAL_9'],
                               name='SIGNAL'),
              row=2, col=1
              )

fig.add_trace(trace=go.Scatter(x=df.index,
                               y=df['RSI_14'],
                               name='RSI'),
              row=3, col=1
              )

fig.update_layout(template='plotly_dark',
                  title='SUNWAY - 5211',
                  xaxis=dict(showgrid=False, title='Date', rangeslider=dict(visible=False)),
                  yaxis=dict(showgrid=True, range=[0, 50000000], title='Volume (RM) Million'),
                  xaxis2=dict(showgrid=False),
                  yaxis2=dict(showgrid=False, title='Price (RM)'),
                  yaxis3=dict(title='MACD'),
                  yaxis4=dict(title='RSI'),
                  legend=dict(orientation='h',
                              x=1,
                              y=1,
                              yanchor='bottom',
                              xanchor='right',
                              font=dict(size=10))
                  )
fig.show()
