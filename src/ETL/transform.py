import pandas as pd

class TransformCovid:
    def __init__(self):
        pass

    def transform_data(self, df):
        df = df.sort_values('date')
        
        df['casos_diarios'] = df['total_casos'].diff().fillna(0)
        df['mortes_diarias'] = df['total_mortes'].diff().fillna(0)
        df['casos_recuperados'] = df['total_recuperados'].diff().fillna(0)
        
        df['crescimento_casos'] = df['casos_diarios'] / df['total_casos'].shift(1) * 100
        df['crescimento_mortes'] = df['mortes_diarias'] / df['total_mortes'].shift(1) * 100
        df['crescimento_recuperacoes'] = df['casos_recuperados'] / df['total_recuperados'].shift(1) * 100
        
        df['casos_7d'] = df['casos_diarios'].rolling(window=7).mean()
        df['mortes_7d'] = df['mortes_diarias'].rolling(window=7).mean()
        df['recuperacao_7d'] = df['casos_recuperados'].rolling(window=7).mean()
        
        df.fillna(0, inplace=True)
        
        return df