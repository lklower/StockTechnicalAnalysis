import pandas


def rsi(close: pandas.Series,
        period: int = 14,
        decimal: int = 5) -> pandas.DataFrame:
    price_chaged: str = 'price_changed'
    gain: str = 'is_gain'
    loss: str = 'is_loss'
    avg_gain: str = 'avg_gain'
    avg_loss: str = 'avg_loss'
    rs: str = 'rs'

    df: pandas.DataFrame = pandas.DataFrame(data=close)

    df[price_chaged] = df[close.name].diff()
    df[gain] = df[price_chaged].apply(lambda x: x if x > 0 else 0)
    df[loss] = df[price_chaged].apply(lambda x: abs(x) if x < 0 else 0)
    df[avg_gain] = df[gain].ewm(com=period - 1, min_periods=period, adjust=False).mean()
    df[avg_loss] = df[loss].ewm(com=period - 1, min_periods=period, adjust=False).mean()
    df[rs] = df[avg_gain] / df[avg_loss]
    df[f'RSI_{period}'] = df['rs'].apply(lambda x: 100 - (100 / (x + 1)))

    df[f'RSI_{period}'] = df[f'RSI_{period}'].apply(lambda x: round(x, decimal))

    return df[f'RSI_{period}']


def macd(close: pandas.Series,
         fast_length: int = 12,
         slow_length: int = 26,
         signal_length: int = 9,
         decimal: int = 5) -> tuple[pandas.Series, pandas.Series]:
    short_ema: str = 'short_ema'
    long_ema: str = 'long_ema'
    df = pandas.DataFrame(data=close)
    df[short_ema] = close.ewm(span=fast_length, min_periods=fast_length, adjust=False).mean()
    df[long_ema] = close.ewm(span=slow_length, min_periods=slow_length, adjust=False).mean()
    df[f'MACD_{fast_length}_{slow_length}'] = df[short_ema] - df[long_ema]
    df[f'SIGNAL_{signal_length}'] = df[f'MACD_{fast_length}_{slow_length}'].ewm(span=9, adjust=False).mean()

    df[f'MACD_{fast_length}_{slow_length}'] = df[f'MACD_{fast_length}_{slow_length}'].apply(lambda x: round(x, decimal))
    df[f'SIGNAL_{signal_length}'] = df[f'SIGNAL_{signal_length}'].apply(lambda x: round(x, decimal))

    return df[f'MACD_{fast_length}_{slow_length}'], df[f'SIGNAL_{signal_length}']


def stochastic(high: pandas.Series,
               low: pandas.Series,
               close: pandas.Series,
               k_period: int = 14,
               d_period: int = 3,
               decimal: int = 5) -> tuple[pandas.Series, pandas.Series]:
    highest: str = f'high_{k_period}'
    lowest: str = f'low_{k_period}'
    k_str: str = f'%K_{k_period}'
    d_str: str = f'%D_{d_period}'

    df: pandas.DataFrame = pandas.concat([high, low, close], axis=1)

    df[highest] = df[high.name].rolling(k_period, min_periods=k_period).max()
    df[lowest] = df[low.name].rolling(k_period, min_periods=k_period).min()
    df[k_str] = ((df[close.name] - df[lowest]) / (df[highest] - df[lowest])) * 100
    df[d_str] = df[k_str].rolling(d_period, min_periods=d_period).mean()

    df[k_str] = df[k_str].apply(lambda x: round(x, decimal))
    df[d_str] = df[d_str].apply(lambda x: round(x, decimal))

    return df[k_str], df[d_str]


def bollinger_bands(close: pandas.Series,
                    periods: int = 20,
                    sigma_width: int = 2,
                    decimal: int = 5) -> tuple[pandas.Series, pandas.Series, pandas.Series]:
    middle: str = f'MIDDLE{periods}'
    lower: str = f'LOWER{sigma_width}'
    upper: str = f'UPPER{sigma_width}'
    sigma: str = 'sigma'

    df: pandas.DataFrame = pandas.DataFrame(data=close)

    df[middle] = df[close.name].rolling(periods, min_periods=periods).mean()
    df[sigma] = df[close.name].rolling(periods, min_periods=periods).std()
    df[upper] = df[middle] + df[sigma] * sigma_width
    df[lower] = df[middle] - df[sigma] * sigma_width

    df[middle] = df[middle].apply(lambda x: round(x, decimal))
    df[upper] = df[upper].apply(lambda x: round(x, decimal))
    df[lower] = df[lower].apply(lambda x: round(x, decimal))

    return df[upper], df[middle], df[lower]


def commodity_channel_index(high: pandas.Series,
                            low: pandas.Series,
                            close: pandas.Series,
                            periods: int = 20) -> pandas.Series:
    typical_price: str = 'typical_price'
    sma: str = 'sma'
    mad: str = 'mad'

    df: pandas.DataFrame = pandas.concat([high, low, close], axis=1)

    df[typical_price] = (df[high.name] + df[low.name] + df[close.name]) / 3
    df[sma] = df[typical_price].rolling(periods, min_periods=periods).mean()
    df[mad] = df[typical_price].rolling(periods, min_periods=periods).apply(lambda x: pandas.Series(x).mad())
    df[f'CCI{periods}'] = (df[typical_price] - df[sma]) / (.015 * df[mad])

    return df[f'CCI{periods}']
