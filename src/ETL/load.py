# src/ETL/load_brazil.py
import os
import pandas as pd

class LoadCovidStates:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save_csv(self, df, filename="covid_states.csv"):
        path = os.path.join(self.output_dir, filename)
        df.to_csv(path, index=False)
        print(f"[LoadCovidStates] Arquivo salvo em: {path}")
        return path
