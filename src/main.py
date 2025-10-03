from src.ETL.extract import ExtractCovidStates
from src.ETL.transform import TransformCovidStates
from src.ETL.load import LoadCovidStates

class Main:
    def __init__(self):
        pass
    
    def run(self):
        e = ExtractCovidStates("China")
        df = e.extract_data()
        populacao = e.get_population()
        
        t = TransformCovidStates(populacao=populacao)
        df_t = t.transform_data(df)
        
        l = LoadCovidStates()
        l.save_csv(df_t, "covid_China.csv")
        
        
        print(df_t.head(15))
        
if __name__ == "__main__":
    main = Main()
    main.run()