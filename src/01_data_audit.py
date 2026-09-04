import pandas as pd
from pathlib import Path


# Localiza a pasta principal do projeto
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Define o caminho da base original
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "dados_piwi.xlsx"


# Carrega a primeira aba do Excel
df = pd.read_excel(RAW_FILE, sheet_name=0)


print("\nBASE CARREGADA COM SUCESSO")
print(f"Número de linhas: {df.shape[0]}")
print(f"Número de colunas: {df.shape[1]}")