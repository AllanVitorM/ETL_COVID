# src/ETL/tranform_vaccine_brazil.py
import pandas as pd
import numpy as np

class TransformVaccineBrazil:
    def __init__(self):
        pass

    def _safe_pct(self, numer, denom):
        """
        Evita divisão por zero: denom == 0 -> NaN; retorna porcentagem (ex: 12.5)
        """
        denom_safe = denom.replace({0: np.nan})
        return (numer / denom_safe) * 100

    def transform(self, df):
        """
        Recebe DataFrame com colunas: date, total_vacinacoes (cumulativo)
        Retorna DataFrame com:
        - total_vacinacoes
        - vac_diarias
        - crescimento_vac_pct
        - vac_7d_ma
        - vac_14d_change_avg
        - tendencia_vac_14d
        """
        df = df.copy().sort_values('date').reset_index(drop=True)

        # garantir coluna numérica
        if 'total_vacinacoes' not in df.columns:
            df['total_vacinacoes'] = 0
        df['total_vacinacoes'] = pd.to_numeric(df['total_vacinacoes'], errors='coerce').fillna(0).astype(int)

        # diffs diárias: primeiro dia = total do dia
        df['vac_diarias'] = df['total_vacinacoes'].diff().fillna(df['total_vacinacoes'])
        # evitar valores negativos (correções históricas)
        df['vac_diarias'] = df['vac_diarias'].apply(lambda x: x if x >= 0 else 0)

        # taxa de crescimento diária relativa ao total do dia anterior
        df['crescimento_vac_pct'] = self._safe_pct(df['vac_diarias'], df['total_vacinacoes'].shift(1))

        # médias móveis (7 dias)
        df['vac_7d_ma'] = df['vac_diarias'].rolling(window=7, min_periods=1).mean()

        # tendência: variação média diária dos últimos 14 dias sobre média móvel 7d
        df['vac_14d_change_avg'] = (df['vac_7d_ma'] - df['vac_7d_ma'].shift(14)) / 14

        # rótulo de tendência simples
        def lbl(x):
            if pd.isna(x):
                return "indefinido"
            if x > 0:
                return "subindo"
            if x < 0:
                return "descendo"
            return "estavel"

        df['tendencia_vac_14d'] = df['vac_14d_change_avg'].apply(lbl)

        # Preencher NaNs em crescimento com "não informado" (segue sua preferência anterior)
        df['crescimento_vac_pct'] = df['crescimento_vac_pct'].fillna("não informado")

        return df
