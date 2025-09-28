# src/ETL/extract_vaccine_brazil.py
import requests
import pandas as pd
from datetime import datetime

URL_VACCINE_BRAZIL = "https://disease.sh/v3/covid-19/vaccine/coverage/countries/brazil?lastdays=all"

class ExtractVaccineBrazil:
    def __init__(self, url=URL_VACCINE_BRAZIL, timeout=10):
        self.url = url
        self.timeout = timeout

    def _parse_timeline(self, timeline):
        """
        Espera timeline: { 'MM/DD/YY': cumulative_value, ... }
        Retorna DataFrame com colunas: date, total_vacinacoes
        """
        if not isinstance(timeline, dict):
            raise RuntimeError("timeline inesperado para vacinação")

        # ordenar as chaves por data (formato M/D/YY)
        try:
            dates_sorted = sorted(timeline.keys(), key=lambda d: datetime.strptime(d, "%m/%d/%y"))
        except Exception:
            # fallback lexicográfico caso parsing falhe
            dates_sorted = sorted(timeline.keys())

        rows = []
        for d in dates_sorted:
            val = timeline.get(d, 0) or 0
            # tentar cast seguro para int
            try:
                val = int(val)
            except Exception:
                try:
                    val = int(float(val))
                except Exception:
                    val = 0
            rows.append({"date": d, "total_vacinacoes": val})

        df = pd.DataFrame(rows)
        df['date'] = pd.to_datetime(df['date'], format="%m/%d/%y", errors='coerce')
        df = df.dropna(subset=['date']).sort_values('date').reset_index(drop=True)
        return df

    def extract(self):
        """
        Faz a requisição e retorna DataFrame com totais diários (cumulativos) de vacinas.
        """
        try:
            resp = requests.get(self.url, timeout=self.timeout)
            resp.raise_for_status()
            payload = resp.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Erro ao acessar API {self.url}: {e}")

        # payload esperado: {'country': 'Brazil', 'timeline': {date: value}}
        timeline = payload.get("timeline")
        if timeline:
            return self._parse_timeline(timeline)

        # fallback: alguns endpoints podem devolver no topo
        if isinstance(payload, dict) and isinstance(payload.get('cases'), dict):
            # não aplicável normalmente, mas mantemos fallback
            raise RuntimeError("Formato inesperado: esperava 'timeline' com vacinação.")
        
        raise RuntimeError("Resposta da API sem campo 'timeline' com dados de vacinação.")

if __name__ == "__main__":
    e = ExtractVaccineBrazil()
    df = e.extract()
    print(df.head())
