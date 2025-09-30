# src/ETL/extract_brazil.py
import requests
import pandas as pd
from datetime import datetime

URL_BRAZIL = "https://disease.sh/v3/covid-19/historical/brazil?lastdays=all"

class ExtractCovidBrazil:
    def __init__(self, url=URL_BRAZIL, timeout=10):
        self.url = url
        self.timeout = timeout

    def _parse_timeline(self, timeline):
        """
        Recebe dict com 'cases','deaths','recovered' (format M/D/YY) e retorna DataFrame:
        date, total_casos, total_mortes, total_recuperados
        """
        cases = timeline.get("cases", {}) or {}
        deaths = timeline.get("deaths", {}) or {}
        recovered = timeline.get("recovered", {}) or {}

        # unir chaves e ordenar por data corretamente
        try:
            dates = sorted({d for d in cases.keys()} | {d for d in deaths.keys()} | {d for d in recovered.keys()},
                           key=lambda x: datetime.strptime(x, "%m/%d/%y"))
        except Exception:
            # fallback: ordenar lexical se parsing falhar
            dates = sorted({d for d in cases.keys()} | {d for d in deaths.keys()} | {d for d in recovered.keys()})

        rows = []
        for d in dates:
            rows.append({
                "date": d,
                "total_casos": int(cases.get(d, 0) or 0),
                "total_mortes": int(deaths.get(d, 0) or 0),
                "total_recuperados": int(recovered.get(d, 0) or 0)
            })

        df = pd.DataFrame(rows)
        df['date'] = pd.to_datetime(df['date'], format="%m/%d/%y", errors='coerce')
        df = df.dropna(subset=['date']).sort_values('date').reset_index(drop=True)
        return df

    def extract(self):
        """
        Faz GET no endpoint do Brasil e retorna DataFrame com totais por data.
        """
        try:
            resp = requests.get(self.url, timeout=self.timeout)
            resp.raise_for_status()
            payload = resp.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Erro ao acessar API {self.url}: {e}")

        # Payload esperado: {'country': 'Brazil', 'timeline': {...}}
        timeline = payload.get("timeline") or payload
        if isinstance(timeline, dict) and any(k in timeline for k in ("cases", "deaths", "recovered")):
            return self._parse_timeline(timeline)

        # fallback: tenta extrair campos no topo
        if all(k in payload for k in ('cases', 'deaths', 'recovered')) and isinstance(payload['cases'], dict):
            return self._parse_timeline({
                'cases': payload['cases'],
                'deaths': payload.get('deaths', {}),
                'recovered': payload.get('recovered', {})
            })

        raise RuntimeError("Resposta da API em formato inesperado. Esperado 'timeline' com 'cases','deaths','recovered'.")

if __name__ == "__main__":
    e = ExtractCovidBrazil()
    df = e.extract()
    print(df.head())
