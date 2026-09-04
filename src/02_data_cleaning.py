import re
from pathlib import Path

import pandas as pd


# ==========================================================
# 1. CONFIGURAÇÃO DOS CAMINHOS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_FILE = PROJECT_ROOT / "data" / "raw" / "dados_piwi.xlsx"

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_FILE = PROCESSED_DIR / "respondents_clean.csv"


# Cria a pasta processed caso ela ainda não exista
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================================
# 2. CARREGAMENTO DA BASE ORIGINAL
# ==========================================================

df = pd.read_excel(RAW_FILE, sheet_name=0)

initial_rows = len(df)

print("\n" + "=" * 60)
print("LIMPEZA E PADRONIZAÇÃO DOS DADOS")
print("=" * 60)

print(f"\nRegistros carregados: {initial_rows}")


# ==========================================================
# 3. PADRONIZAÇÃO DOS NOMES ORIGINAIS
# ==========================================================

def normalize_header(column_name):
    """
    Remove espaços no início e no final e substitui
    sequências de espaços por apenas um espaço.
    """

    column_name = str(column_name).strip()

    column_name = re.sub(
        r"\s+",
        " ",
        column_name
    )

    return column_name


df.columns = [
    normalize_header(column)
    for column in df.columns
]


# ==========================================================
# 4. RENOMEAÇÃO DAS COLUNAS
# ==========================================================

column_names = [
    "submitted_at",
    "consent",
    "region",
    "residence_zone",
    "age_group",
    "gender",
    "race_color",
    "income_group",
    "education",
    "consumption_frequency",
    "consumer_profile_raw",
    "wine_types_raw",
    "purchase_channels_raw",
    "purchase_factors_raw",
    "sustainable_attributes_raw",
    "label_importance"
]


# Validação da quantidade de colunas antes da renomeação
if len(df.columns) != len(column_names):
    raise ValueError(
        "A quantidade de colunas da base é diferente da esperada. "
        f"Esperado: {len(column_names)}. "
        f"Encontrado: {len(df.columns)}."
    )


df.columns = column_names

print(f"Colunas padronizadas: {len(df.columns)}")


# ==========================================================
# 5. TRATAMENTO DA DATA
# ==========================================================

df["submitted_at"] = pd.to_datetime(
    df["submitted_at"],
    errors="coerce"
)

invalid_dates = df["submitted_at"].isna().sum()

print(f"Datas inválidas encontradas: {invalid_dates}")


# ==========================================================
# 6. REMOÇÃO DE ESPAÇOS NOS TEXTOS
# ==========================================================

text_columns = df.select_dtypes(
    include="object"
).columns


for column in text_columns:

    df[column] = df[column].apply(
        lambda value: value.strip()
        if isinstance(value, str)
        else value
    )


# ==========================================================
# 7. VALIDAÇÃO DO CONSENTIMENTO
# ==========================================================

accepted_consent = "Sim, aceito participar"

rows_without_consent = (
    df["consent"] != accepted_consent
).sum()


df = df[
    df["consent"] == accepted_consent
].copy()


print(
    "Registros removidos por ausência de consentimento: "
    f"{rows_without_consent}"
)


# ==========================================================
# 8. REMOÇÃO DE DUPLICATAS
# ==========================================================

duplicate_rows = df.duplicated().sum()

df = df.drop_duplicates().reset_index(drop=True)

print(f"Registros duplicados removidos: {duplicate_rows}")


# ==========================================================
# 9. PADRONIZAÇÃO DA ZONA DE RESIDÊNCIA
# ==========================================================

residence_zone_map = {
    "Zona urbana": "Zona urbana",
    "Zona Rural": "Zona rural",
    "Zona rural": "Zona rural"
}


df["residence_zone"] = (
    df["residence_zone"]
    .replace(residence_zone_map)
)


# ==========================================================
# 10. PADRONIZAÇÃO DO PERFIL DO CONSUMIDOR
# ==========================================================

def standardize_consumer_profile(value):
    """
    Agrupa respostas equivalentes em categorias padronizadas.
    As respostas originais continuam preservadas na coluna
    consumer_profile_raw.
    """

    normalized_value = str(value).strip().casefold()

    if (
        "profissional da área" in normalized_value
        or "professora de restaurante" in normalized_value
        or "maitre" in normalized_value
    ):
        return "Profissional do setor"

    if "conhecimentos técnicos" in normalized_value:
        return "Apreciador técnico"

    if (
        "interesse pelo tema" in normalized_value
        or "algum conhecimento" in normalized_value
    ):
        return "Apreciador interessado"

    if "não consumidor" in normalized_value:
        return "Não consumidor"

    if "consumidor ocasional" in normalized_value:
        return "Consumidor ocasional"

    return "Não classificado"


df["consumer_profile"] = (
    df["consumer_profile_raw"]
    .apply(standardize_consumer_profile)
)


# ==========================================================
# 11. CRIAÇÃO DO IDENTIFICADOR ANÔNIMO
# ==========================================================

df.insert(
    0,
    "respondent_id",
    range(1, len(df) + 1)
)


# ==========================================================
# 12. ORGANIZAÇÃO DAS COLUNAS
# ==========================================================

column_order = [
    "respondent_id",
    "submitted_at",
    "consent",
    "region",
    "residence_zone",
    "age_group",
    "gender",
    "race_color",
    "income_group",
    "education",
    "consumption_frequency",
    "consumer_profile",
    "consumer_profile_raw",
    "wine_types_raw",
    "purchase_channels_raw",
    "purchase_factors_raw",
    "sustainable_attributes_raw",
    "label_importance"
]


df = df[column_order]


# ==========================================================
# 13. VALIDAÇÕES FINAIS
# ==========================================================

final_rows = len(df)

remaining_nulls = df.isna().sum().sum()

duplicate_ids = df["respondent_id"].duplicated().sum()

unclassified_profiles = (
    df["consumer_profile"] == "Não classificado"
).sum()


print("\n" + "-" * 60)
print("RESULTADO DA LIMPEZA")
print("-" * 60)

print(f"Registros iniciais: {initial_rows}")
print(f"Registros finais: {final_rows}")
print(f"Valores nulos restantes: {remaining_nulls}")
print(f"IDs duplicados: {duplicate_ids}")
print(
    "Perfis não classificados: "
    f"{unclassified_profiles}"
)


# Impede a exportação se houver IDs duplicados
if duplicate_ids > 0:
    raise ValueError(
        "Foram encontrados IDs duplicados."
    )


# ==========================================================
# 14. EXPORTAÇÃO DA BASE TRATADA
# ==========================================================

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


print("\nBase tratada exportada com sucesso:")
print(OUTPUT_FILE)

print("\n" + "=" * 60)
print("LIMPEZA FINALIZADA")
print("=" * 60)