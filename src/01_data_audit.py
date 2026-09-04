import pandas as pd
from pathlib import Path



# Localiza a pasta principal do projeto
PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_FILE = PROJECT_ROOT / "data" / "raw" / "dados_piwi.xlsx"


df = pd.read_excel(RAW_FILE, sheet_name=0)


print("\n" + "=" * 60)
print("1. DIMENSÕES DA BASE")
print("=" * 60)

print(f"Número de linhas: {df.shape[0]}")
print(f"Número de colunas: {df.shape[1]}")



print("\n" + "=" * 60)
print("2. PRIMEIROS REGISTROS")
print("=" * 60)

print(df.head())



print("\n" + "=" * 60)
print("3. NOMES DAS COLUNAS")
print("=" * 60)

for position, column in enumerate(df.columns, start=1):
    print(f"{position}. {column}")



print("\n" + "=" * 60)
print("4. TIPOS DOS DADOS")
print("=" * 60)

print(df.dtypes)


print("\n" + "=" * 60)
print("5. VALORES NULOS POR COLUNA")
print("=" * 60)

null_values = df.isna().sum()

print(null_values)
print(f"\nTotal de valores nulos: {null_values.sum()}")


print("\n" + "=" * 60)
print("6. REGISTROS DUPLICADOS")
print("=" * 60)

duplicate_rows = df.duplicated().sum()

print(f"Quantidade de registros duplicados: {duplicate_rows}")


print("\n" + "=" * 60)
print("7. PERÍODO DA COLETA")
print("=" * 60)

date_column = "Carimbo de data/hora"

timestamps = pd.to_datetime(
    df[date_column],
    errors="coerce"
)

invalid_dates = timestamps.isna().sum()

print(f"Data inicial: {timestamps.min()}")
print(f"Data final: {timestamps.max()}")
print(f"Datas inválidas: {invalid_dates}")



print("\n" + "=" * 60)
print("8. CONSENTIMENTO DOS PARTICIPANTES")
print("=" * 60)

consent_column = "Pergunta Obrigatória"

print(df[consent_column].value_counts(dropna=False))



print("\n" + "=" * 60)
print("9. QUANTIDADE DE VALORES ÚNICOS")
print("=" * 60)

print(df.nunique())


print("\n" + "=" * 60)
print("AUDITORIA FINALIZADA COM SUCESSO")
print("=" * 60)