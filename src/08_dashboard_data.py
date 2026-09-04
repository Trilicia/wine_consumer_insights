import json
import re
import unicodedata
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DIR = (
    PROJECT_ROOT /
    "data" /
    "processed"
)

DASHBOARD_DIR = (
    PROJECT_ROOT /
    "dashboard"
)


RESPONDENTS_FILE = (
    PROCESSED_DIR /
    "respondents_analytical.csv"
)


DASHBOARD_CSV_FILE = (
    PROCESSED_DIR /
    "dashboard_data.csv"
)


DASHBOARD_JS_FILE = (
    DASHBOARD_DIR /
    "data.js"
)


# Garante que a pasta dashboard exista
DASHBOARD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


bridge_files = {
    "wine_types": (
        PROCESSED_DIR /
        "bridge_wine_types.csv"
    ),

    "purchase_channels": (
        PROCESSED_DIR /
        "bridge_purchase_channels.csv"
    ),

    "purchase_factors": (
        PROCESSED_DIR /
        "bridge_purchase_factors.csv"
    ),

    "sustainable_attributes": (
        PROCESSED_DIR /
        "bridge_sustainable_attributes.csv"
    )
}



required_files = [
    RESPONDENTS_FILE,
    *bridge_files.values()
]


missing_files = [
    str(file_path)
    for file_path in required_files
    if not file_path.exists()
]


if missing_files:

    print("\nArquivos não encontrados:")

    for file_path in missing_files:
        print(f"- {file_path}")

    raise FileNotFoundError(
        "Execute as etapas anteriores antes "
        "de preparar os dados do dashboard."
    )


print("\n" + "=" * 60)
print("PREPARAÇÃO DOS DADOS DO DASHBOARD")
print("=" * 60)



def slugify(value):
    """
    Converte um texto para um formato adequado
    para o nome de uma coluna.

    Exemplo:
    'Região de origem' se torna 'regiao_de_origem'.
    """

    value = str(value)

    # Remove acentos
    value = unicodedata.normalize(
        "NFKD",
        value
    )

    value = (
        value
        .encode("ascii", "ignore")
        .decode("utf-8")
    )

    # Converte para letras minúsculas
    value = value.lower()

    # Substitui caracteres especiais por underline
    value = re.sub(
        r"[^a-z0-9]+",
        "_",
        value
    )

    # Remove underline das extremidades
    value = value.strip("_")

    return value



respondents = pd.read_csv(
    RESPONDENTS_FILE,
    encoding="utf-8-sig"
)


print(
    f"\nParticipantes carregados: "
    f"{len(respondents)}"
)



dashboard_columns = [
    "respondent_id",
    "region",
    "residence_zone",
    "age_group",
    "gender",
    "income_group",
    "education",
    "consumption_frequency",
    "consumer_profile",
    "monthly_consumption_estimate",
    "consumption_intensity",
    "label_importance",
    "label_importance_score",
    "high_label_importance",
    "consumer_knowledge_score",
    "strategic_segment"
]


dashboard_df = respondents[
    dashboard_columns
].copy()



for topic, file_path in bridge_files.items():

    bridge_df = pd.read_csv(
        file_path,
        encoding="utf-8-sig"
    )


    # Cria uma tabela com uma linha por participante
    # e uma coluna para cada alternativa
    pivot_table = pd.crosstab(
        bridge_df["respondent_id"],
        bridge_df["option"]
    )


    # Garante que os indicadores sejam apenas 0 ou 1
    pivot_table = pivot_table.clip(
        upper=1
    )


    # Renomeia as colunas
    renamed_columns = {
        option: (
            f"{topic}__{slugify(option)}"
        )
        for option in pivot_table.columns
    }


    pivot_table = pivot_table.rename(
        columns=renamed_columns
    )


    # Transforma respondent_id novamente em coluna
    pivot_table = pivot_table.reset_index()


    # Junta com a tabela principal
    dashboard_df = dashboard_df.merge(
        pivot_table,
        on="respondent_id",
        how="left"
    )


    print(
        f"Tema processado: {topic} — "
        f"{len(renamed_columns)} indicadores"
    )



indicator_columns = [
    column
    for column in dashboard_df.columns
    if "__" in column
]


dashboard_df[indicator_columns] = (
    dashboard_df[indicator_columns]
    .fillna(0)
    .astype(int)
)



duplicate_ids = (
    dashboard_df["respondent_id"]
    .duplicated()
    .sum()
)


invalid_indicators = (
    ~dashboard_df[indicator_columns]
    .isin([0, 1])
).sum().sum()


missing_values = (
    dashboard_df
    .isna()
    .sum()
    .sum()
)


print("\n" + "-" * 60)
print("VALIDAÇÃO DA FONTE DO DASHBOARD")
print("-" * 60)

print(
    f"Linhas: "
    f"{len(dashboard_df)}"
)

print(
    f"Colunas: "
    f"{len(dashboard_df.columns)}"
)

print(
    f"Identificadores duplicados: "
    f"{duplicate_ids}"
)

print(
    f"Indicadores inválidos: "
    f"{invalid_indicators}"
)

print(
    f"Valores nulos: "
    f"{missing_values}"
)


if duplicate_ids > 0:

    raise ValueError(
        "A fonte do dashboard possui "
        "identificadores duplicados."
    )


if invalid_indicators > 0:

    raise ValueError(
        "A fonte do dashboard possui "
        "indicadores diferentes de 0 ou 1."
    )


if missing_values > 0:

    raise ValueError(
        "A fonte do dashboard possui valores nulos."
    )



dashboard_df.to_csv(
    DASHBOARD_CSV_FILE,
    index=False,
    encoding="utf-8-sig"
)


print(
    "\nCSV do dashboard criado: "
    f"{DASHBOARD_CSV_FILE.name}"
)



# Converte o DataFrame para registros JSON
dashboard_records = json.loads(
    dashboard_df.to_json(
        orient="records",
        force_ascii=False
    )
)


javascript_content = (
    "window.PIWI_DATA = "
    + json.dumps(
        dashboard_records,
        ensure_ascii=False,
        separators=(",", ":")
    )
    + ";\n"
)


DASHBOARD_JS_FILE.write_text(
    javascript_content,
    encoding="utf-8"
)


print(
    "Arquivo JavaScript criado: "
    f"{DASHBOARD_JS_FILE.name}"
)


print("\n" + "=" * 60)
print("DADOS DO DASHBOARD PREPARADOS COM SUCESSO")
print("=" * 60)

print(
    f"\nParticipantes: "
    f"{len(dashboard_df)}"
)

print(
    f"Variáveis disponíveis: "
    f"{len(dashboard_df.columns)}"
)

print(
    f"Indicadores de múltipla escolha: "
    f"{len(indicator_columns)}"
)