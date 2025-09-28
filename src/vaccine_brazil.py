# src/vaccine_brazil.py
from src.ETL.extract_vaccine_brazil import ExtractVaccineBrazil
from src.ETL.transform_vaccine_brazil import TransformVaccineBrazil
from src.ETL.load_vaccine_brazil import LoadVaccineBrazil

def run_vaccine_brazil_etl():
    extractor = ExtractVaccineBrazil()
    print("Extraindo dados de vacinação do Brasil...")
    df_raw = extractor.extract()
    print(f"Linhas extraídas: {len(df_raw)} | primeira data: {df_raw['date'].min()} | última: {df_raw['date'].max()}")

    transformer = TransformVaccineBrazil()
    print("Transformando dados de vacinação...")
    df_transformed = transformer.transform(df_raw)

    loader = LoadVaccineBrazil(output_dir="output")
    out_csv = loader.save_csv(df_transformed, "vaccine_brazil.csv")

    print("ETL Vacinação Brasil concluída.")
    print(df_transformed.head(15))
    return out_csv

if __name__ == "__main__":
    run_vaccine_brazil_etl()
