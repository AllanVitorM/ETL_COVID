# src/ETL/transform_brazil.py
import pandas as pd
import numpy as np

class TransformCovidStates:
    def __init__(self, populacao=None):
        self.populacao = populacao

    def _safe_pct(self, numer, denom):
        denom_safe = denom.replace({0: np.nan})
        return (numer / denom_safe) * 100

    def transform_data(self, df):
        """
        Recebe DataFrame com colunas: date, total_casos, total_mortes, total_recuperados
        Retorna DataFrame com várias colunas diárias, médias móveis, taxas e tendências.
        """
        df = df.copy().sort_values('date').reset_index(drop=True)

        # garantir colunas inteiras
        for col in ['total_casos', 'total_mortes', 'total_recuperados']:
            if col not in df.columns:
                df[col] = 0
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

        # diffs diárias (primeiro dia = valor do dia)
        df['casos_diarios'] = df['total_casos'].diff().fillna(df['total_casos'])
        df['mortes_diarias'] = df['total_mortes'].diff().fillna(df['total_mortes'])
        df['recuperados_diarios'] = df['total_recuperados'].diff().fillna(df['total_recuperados'])

        for col in ['casos_diarios', 'mortes_diarias', 'recuperados_diarios']:
            df[col] = df[col].apply(lambda x: x if x>= 0 else 0)

        # taxas de crescimento (dia-a-dia) em %
        df['crescimento_casos_pct'] = self._safe_pct(df['casos_diarios'], df['total_casos'].shift(1))
        df['crescimento_mortes_pct'] = self._safe_pct(df['mortes_diarias'], df['total_mortes'].shift(1))
        df['crescimento_recuperacoes_pct'] = self._safe_pct(df['recuperados_diarios'], df['total_recuperados'].shift(1))

        # médias móveis (7 dias) com min_periods=1 para não gerar NaN no início
        df['casos_7d_ma'] = df['casos_diarios'].rolling(window=7, min_periods=1).mean()
        df['mortes_7d_ma'] = df['mortes_diarias'].rolling(window=7, min_periods=1).mean()
        df['recuperados_7d_ma'] = df['recuperados_diarios'].rolling(window=7, min_periods=1).mean()

        # tendência: diferença entre média móvel atual e média móvel 14 dias atrás dividida por 14
        df['casos_14d_change_avg'] = (df['casos_7d_ma'] - df['casos_7d_ma'].shift(14)) / 14
        df['mortes_14d_change_avg'] = (df['mortes_7d_ma'] - df['mortes_7d_ma'].shift(14)) / 14
        df['recuperados_14d_change_avg'] = (df['recuperados_7d_ma'] - df['recuperados_7d_ma'].shift(14)) / 14

        # rótulos de tendência simples
        def lbl(x):
            if pd.isna(x):
                return "indefinido"
            if x > 0:
                return "subindo"
            if x < 0:
                return "descendo"
            return "estavel"

        df['tendencia_casos_14d'] = df['casos_14d_change_avg'].apply(lbl)
        df['tendencia_mortes_14d'] = df['mortes_14d_change_avg'].apply(lbl)
        df['tendencia_recuperados_14d'] = df['recuperados_14d_change_avg'].apply(lbl)

        df['letalidade_pct'] = self._safe_pct(df['total_mortes'], df['total_casos'])
        df['recuperacao_pct'] = self._safe_pct(df['total_recuperados'], df['total_casos'])
        
        if self.populacao:
            df['casos_por_100k'] = (df['total_casos'] / self.populacao) * 100000
            df['mortes_por_1M'] = (df['total_mortes'] / self.populacao) * 1000000
        else:
            df['casos_por_100k'] = np.nan
            df['mortes_por_1M'] = np.nan
            
        # preencher NaNs nas taxas com "não informado"
        df[['crescimento_casos_pct', 'crescimento_mortes_pct', 'crescimento_recuperacoes_pct']] = \
            df[['crescimento_casos_pct', 'crescimento_mortes_pct', 'crescimento_recuperacoes_pct']].fillna("não informado")

        return df
