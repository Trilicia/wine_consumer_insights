import re
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

INPUT_FILE = PROCESSED_DIR / "respondents_clean.csv"



df = pd.read_csv(
    INPUT_FILE,
    encoding="utf-8-sig"
)


print("\n" + "=" * 60)
print("TRATAMENTO DAS PERGUNTAS DE MÚLTIPLA ESCOLHA")
print("=" * 60)

print(f"\nParticipantes carregados: {len(df)}")



controlled_options = {

    "wine_types": [
        "Vinho tinto seco",
        "Vinho branco seco",
        "Vinho rosé",
        "Vinho espumante",
        "Vinho suave",
        "Vinho demi-sec",
        "Vinho licoroso e/ou fortificado",
        "Não tenho preferência definida"
    ],

    "purchase_channels": [
        "Supermercados",
        "Lojas físicas especializadas",
        "Lojas online especializadas",
        "Diretamente em vinícolas",
        "Restaurantes e bares",
        "Aplicativos de delivery de bebidas"
    ],

    "purchase_factors": [
        "Preço",
        "Região de origem",
        "Variedade",
        "Vinícola / Produtor",
        "Recomendação (amigos, especialistas, avaliações)",
        "Descrição sensorial (aroma, sabor estilo)",
        "Promoções ou descontos",
        "Design e informação do rótulo",
        "Práticas sustentáveis e/ou impacto ambiental",
        "Curiosidade ou interesse por novos produtos"
    ],

    "sustainable_attributes": [
        "Qualidade sensorial (sabor, aroma, equilíbrio)",
        "Sustentabilidade ambiental (menor impacto no cultivo)",
        "Origem das uvas (região/procedência)",
        "Clareza e transparência das informações no rótulo",
        "Presença de certificações ou selos ambientais",
        "Preço",
        "Grau de inovação do produto"
    ]
}



multiselect_columns = {
    "wine_types": "wine_types_raw",
    "purchase_channels": "purchase_channels_raw",
    "purchase_factors": "purchase_factors_raw",
    "sustainable_attributes": "sustainable_attributes_raw"
}




def extract_selected_options(raw_value, options):
    """
    Identifica as alternativas oficiais dentro da resposta.

    A função não utiliza split(",") porque algumas alternativas
    possuem vírgulas dentro do próprio texto.
    """

    if pd.isna(raw_value):
        return [], ""

    original_value = str(raw_value).strip()

    selected_options = []

    for option in options:

        if option.casefold() in original_value.casefold():
            selected_options.append(option)

    # Começa com o texto original
    residual_text = original_value

    # Remove do texto todas as alternativas reconhecidas
    for option in sorted(
        selected_options,
        key=len,
        reverse=True
    ):

        residual_text = re.sub(
            re.escape(option),
            " ",
            residual_text,
            flags=re.IGNORECASE
        )

    # Remove vírgulas, ponto e vírgula e espaços nas extremidades
    residual_text = re.sub(
        r"^[\s,;]+|[\s,;]+$",
        "",
        residual_text
    )

    # Corrige separadores repetidos
    residual_text = re.sub(
        r"\s*[,;]\s*[,;]+\s*",
        ", ",
        residual_text
    )

    residual_text = residual_text.strip()

    return selected_options, residual_text


bridge_tables = {}

unclassified_answers = []


for topic, source_column in multiselect_columns.items():

    bridge_rows = []

    for _, row in df.iterrows():

        respondent_id = row["respondent_id"]

        raw_value = row[source_column]

        selected_options, residual_text = (
            extract_selected_options(
                raw_value,
                controlled_options[topic]
            )
        )

        # Cria uma linha para cada alternativa selecionada
        for option in selected_options:

            bridge_rows.append({
                "respondent_id": respondent_id,
                "option": option
            })

        # Preserva respostas livres ou não reconhecidas
        if residual_text:

            unclassified_answers.append({
                "respondent_id": respondent_id,
                "topic": topic,
                "original_answer": raw_value,
                "unclassified_text": residual_text
            })

    bridge_df = pd.DataFrame(
        bridge_rows,
        columns=[
            "respondent_id",
            "option"
        ]
    )

    bridge_tables[topic] = bridge_df



unclassified_df = pd.DataFrame(
    unclassified_answers,
    columns=[
        "respondent_id",
        "topic",
        "original_answer",
        "unclassified_text"
    ]
)



print("\n" + "-" * 60)
print("RESULTADO DO PROCESSAMENTO")
print("-" * 60)


for topic, bridge_df in bridge_tables.items():

    duplicated_pairs = bridge_df.duplicated(
        subset=[
            "respondent_id",
            "option"
        ]
    ).sum()

    participants_with_options = (
        bridge_df["respondent_id"]
        .nunique()
    )

    print(f"\nTema: {topic}")
    print(f"Seleções identificadas: {len(bridge_df)}")

    print(
        "Participantes com alternativas oficiais: "
        f"{participants_with_options}"
    )

    print(
        "Combinações duplicadas: "
        f"{duplicated_pairs}"
    )

    if duplicated_pairs > 0:

        raise ValueError(
            f"Foram encontradas duplicatas em {topic}."
        )


print(
    "\nRespostas com conteúdo não classificado: "
    f"{len(unclassified_df)}"
)



for topic, bridge_df in bridge_tables.items():

    output_file = (
        PROCESSED_DIR /
        f"bridge_{topic}.csv"
    )

    bridge_df.to_csv(
        output_file,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"Arquivo criado: {output_file.name}")


unclassified_output = (
    PROCESSED_DIR /
    "unclassified_answers.csv"
)


unclassified_df.to_csv(
    unclassified_output,
    index=False,
    encoding="utf-8-sig"
)


print(
    f"Arquivo criado: "
    f"{unclassified_output.name}"
)


print("\n" + "=" * 60)
print("PROCESSAMENTO FINALIZADO COM SUCESSO")
print("=" * 60)