from src.ETL.extract import ExtractCovid
from src.ETL.transform import TransformCovid
from src.ETL.load import LoadCovidGlobal

class Main:
    def __init__(self):
        pass
    
    def run(self):
        e = ExtractCovid()
        df = e.ExtractDataCovid()
        
        t = TransformCovid()
        df_t = t.transform_data(df)
        
        l = LoadCovidGlobal()
        l.save_df(df_t, "covid_global.csv")
        
        
        print(df_t.head(15))
        
if __name__ == "__main__":
    main = Main()
    main.run()