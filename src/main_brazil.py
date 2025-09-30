# src/main_brazil.py
from src.ETL.extract_brazil import ExtractCovidBrazil
from src.ETL.transform_brazil import TransformCovidBrazil
from src.ETL.load_brazil import LoadCovidBrazil

def run_brazil_etl():
    extractor = ExtractCovidBrazil()
    print("Extraindo dados do Brasil...")
    df_raw = extractor.extract()
    print(f"Linhas extraídas: {len(df_raw)} | primeira data: {df_raw['date'].min()} | última: {df_raw['date'].max()}")

    transformer = TransformCovidBrazil()
    print("Transformando dados...")
    df_transformed = transformer.transform(df_raw)

    loader = LoadCovidBrazil()
    out_csv = loader.save_csv(df_transformed, "covid_brazil_daily.csv")
    # opcional: loader.save_parquet(df_transformed)

    print("ETL Brasil concluída.")
    print(df_transformed.head(15))
    return out_csv

if __name__ == "__main__":
    run_brazil_etl()
