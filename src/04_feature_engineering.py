from pathlib import Path

import pandas as pd



PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

INPUT_FILE = (
    PROCESSED_DIR /
    "respondents_clean.csv"
)

OUTPUT_FILE = (
    PROCESSED_DIR /
    "respondents_analytical.csv"
)



df = pd.read_csv(
    INPUT_FILE,
    encoding="utf-8-sig",
    parse_dates=["submitted_at"]
)


print("\n" + "=" * 60)
print("ENGENHARIA DE VARIÁVEIS")
print("=" * 60)

print(f"\nParticipantes carregados: {len(df)}")



frequency_monthly_map = {
    "Não consumo vinho": 0.0,
    "Raramente": 0.5,
    "1 vez por mês": 1.0,
    "1 vez a cada 15 dias": 2.0,
    "1 vez por semana": 4.3,
    "De 2 a 3 vezes por semana": 10.8,
    "De 4 a 6 vezes por semana": 21.5,
    "Diariamente": 30.4
}


df["monthly_consumption_estimate"] = (
    df["consumption_frequency"]
    .map(frequency_monthly_map)
)




unmapped_frequency = df.loc[
    df["monthly_consumption_estimate"].isna(),
    "consumption_frequency"
].unique()


if len(unmapped_frequency) > 0:

    raise ValueError(
        "Foram encontradas frequências não mapeadas: "
        f"{unmapped_frequency}"
    )




def classify_consumption_intensity(monthly_frequency):
    """
    Classifica o participante de acordo com a
    frequência mensal estimada de consumo.
    """

    if monthly_frequency == 0:
        return "Não consumidor"

    if monthly_frequency < 1:
        return "Baixa frequência"

    if monthly_frequency < 4.3:
        return "Frequência moderada"

    return "Alta frequência"


df["consumption_intensity"] = (
    df["monthly_consumption_estimate"]
    .apply(classify_consumption_intensity)
)


importance_score_map = {
    "Pouco importante": 1,
    "Moderadamente importante": 2,
    "Muito importante": 3,
    "Extremamente importante": 4
}


df["label_importance_score"] = (
    df["label_importance"]
    .map(importance_score_map)
)




unmapped_importance = df.loc[
    df["label_importance_score"].isna(),
    "label_importance"
].unique()


if len(unmapped_importance) > 0:

    raise ValueError(
        "Foram encontradas respostas de importância "
        f"não mapeadas: {unmapped_importance}"
    )




df["high_label_importance"] = (
    df["label_importance_score"]
    .ge(3)
    .astype(int)
)



knowledge_score_map = {
    "Não consumidor": 0,
    "Consumidor ocasional": 1,
    "Apreciador interessado": 2,
    "Apreciador técnico": 3,
    "Profissional do setor": 4
}


df["consumer_knowledge_score"] = (
    df["consumer_profile"]
    .map(knowledge_score_map)
)



unmapped_profiles = df.loc[
    df["consumer_knowledge_score"].isna(),
    "consumer_profile"
].unique()


if len(unmapped_profiles) > 0:

    raise ValueError(
        "Foram encontrados perfis não mapeados: "
        f"{unmapped_profiles}"
    )



def create_strategic_segment(row):
    """
    Segmenta o público combinando frequência de consumo
    e importância atribuída à sustentabilidade no rótulo.
    """

    high_importance = (
        row["high_label_importance"] == 1
    )

    frequent_consumer = (
        row["monthly_consumption_estimate"] >= 4.3
    )

    if high_importance and frequent_consumer:
        return "Alta prioridade"

    if high_importance and not frequent_consumer:
        return "Potencial sustentável"

    if not high_importance and frequent_consumer:
        return "Consumidor frequente tradicional"

    return "Baixa prioridade"


df["strategic_segment"] = df.apply(
    create_strategic_segment,
    axis=1
)



analytical_columns = [
    "monthly_consumption_estimate",
    "consumption_intensity",
    "label_importance_score",
    "high_label_importance",
    "consumer_knowledge_score",
    "strategic_segment"
]


null_values = (
    df[analytical_columns]
    .isna()
    .sum()
    .sum()
)


invalid_importance_scores = (
    ~df["label_importance_score"]
    .between(1, 4)
).sum()


invalid_binary_values = (
    ~df["high_label_importance"]
    .isin([0, 1])
).sum()


print("\n" + "-" * 60)
print("VALIDAÇÃO DAS VARIÁVEIS")
print("-" * 60)

print(
    "Valores nulos nas variáveis analíticas: "
    f"{null_values}"
)

print(
    "Pontuações de importância inválidas: "
    f"{invalid_importance_scores}"
)

print(
    "Indicadores binários inválidos: "
    f"{invalid_binary_values}"
)


if null_values > 0:
    raise ValueError(
        "Existem valores nulos nas variáveis analíticas."
    )


if invalid_importance_scores > 0:
    raise ValueError(
        "Existem pontuações de importância inválidas."
    )


if invalid_binary_values > 0:
    raise ValueError(
        "Existem valores diferentes de 0 ou 1 no indicador."
    )



print("\n" + "-" * 60)
print("DISTRIBUIÇÃO POR INTENSIDADE DE CONSUMO")
print("-" * 60)

print(
    df["consumption_intensity"]
    .value_counts()
)


print("\n" + "-" * 60)
print("DISTRIBUIÇÃO DOS SEGMENTOS ESTRATÉGICOS")
print("-" * 60)

print(
    df["strategic_segment"]
    .value_counts()
)



df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


print("\nBase analítica exportada com sucesso:")
print(OUTPUT_FILE)

print("\n" + "=" * 60)
print("ENGENHARIA DE VARIÁVEIS FINALIZADA")
print("=" * 60)