import os
import pandas as pd

class LoadCovidGlobal:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def save_df(self, df, filename="covid_global.csv"):
        path = os.path.join(self.output_dir, filename)
        df.to_csv(path, index=False)
        print(f"Arquivo salvo em: {path}")
        