# src/ETL/load_vaccine_brazil.py
import os
import pandas as pd

class LoadVaccineBrazil:
    def __init__(self, output_dir="output"):
        # como pediu, salva em output/vaccine_brazil.csv (mesma pasta output da ETL original)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save_csv(self, df, filename="vaccine_brazil.csv"):
        path = os.path.join(self.output_dir, filename)
        # garantir que o dataframe seja salvo corretamente; se houver colunas com strings/NA, ok
        df.to_csv(path, index=False)
        print(f"[LoadVaccineBrazil] Arquivo salvo em: {path}")
        return path

    def save_parquet(self, df, filename="vaccine_brazil.parquet"):
        path = os.path.join(self.output_dir, filename)
        df.to_parquet(path, index=False)
        print(f"[LoadVaccineBrazil] Parquet salvo em: {path}")
        return path
