import requests
from src.utils.constant import URL
import pandas as pd


class ExtractCovid:
    def __init__(self):
        pass
    
    def ExtractDataCovid(self):
        response = requests.get(URL)
        data = response.json()

        
        df_cases = pd.DataFrame(data['cases'].items(), columns=['date', 'total_casos'])
        df_deaths = pd.DataFrame(data['deaths'].items(), columns=['date', 'total_mortes'])
        df_recovered = pd.DataFrame(data['recovered'].items(), columns=['date', 'total_recuperados'])
        
        df = df_cases.merge(df_deaths, on='date').merge(df_recovered, on='date')
        df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y', errors='coerce')
        
        return df