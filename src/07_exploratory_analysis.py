import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns



PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DIR = (
    PROJECT_ROOT /
    "data" /
    "processed"
)

REPORTS_DIR = PROJECT_ROOT / "reports"

FIGURES_DIR = REPORTS_DIR / "figures"


RESPONDENTS_FILE = (
    PROCESSED_DIR /
    "respondents_analytical.csv"
)

PURCHASE_FACTORS_FILE = (
    REPORTS_DIR /
    "purchase_factor_ranking.csv"
)

SUSTAINABLE_ATTRIBUTES_FILE = (
    REPORTS_DIR /
    "sustainable_attribute_ranking.csv"
)

STRATEGIC_SEGMENTS_FILE = (
    REPORTS_DIR /
    "strategic_segments.csv"
)


# Cria a pasta dos gráficos
FIGURES_DIR.mkdir(
    parents=True,
    exist_ok=True
)



required_files = [
    RESPONDENTS_FILE,
    PURCHASE_FACTORS_FILE,
    SUSTAINABLE_ATTRIBUTES_FILE,
    STRATEGIC_SEGMENTS_FILE
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
        "da análise exploratória."
    )


df = pd.read_csv(
    RESPONDENTS_FILE,
    encoding="utf-8-sig"
)

purchase_factors = pd.read_csv(
    PURCHASE_FACTORS_FILE,
    encoding="utf-8-sig"
)

sustainable_attributes = pd.read_csv(
    SUSTAINABLE_ATTRIBUTES_FILE,
    encoding="utf-8-sig"
)

strategic_segments = pd.read_csv(
    STRATEGIC_SEGMENTS_FILE,
    encoding="utf-8-sig"
)


print("\n" + "=" * 60)
print("ANÁLISE EXPLORATÓRIA")
print("=" * 60)

print(f"\nParticipantes analisados: {len(df)}")



sns.set_theme(
    style="whitegrid",
    font_scale=1.0
)


WINE_COLOR = "#722F37"

ROSE_COLOR = "#C98A83"

GREEN_COLOR = "#526B58"

LIGHT_GREEN = "#A8B9A5"

TEXT_COLOR = "#302A2B"

GRID_COLOR = "#E5DDDA"


plt.rcParams["figure.facecolor"] = "white"

plt.rcParams["axes.facecolor"] = "white"

plt.rcParams["text.color"] = TEXT_COLOR

plt.rcParams["axes.labelcolor"] = TEXT_COLOR

plt.rcParams["xtick.color"] = TEXT_COLOR

plt.rcParams["ytick.color"] = TEXT_COLOR




def format_percentage(value):
    """
    Formata um número utilizando vírgula decimal.
    """

    return (
        f"{value:.1f}%"
        .replace(".", ",")
    )


def wrap_labels(labels, width=38):
    """
    Quebra rótulos longos em mais de uma linha.
    """

    return [
        textwrap.fill(
            str(label),
            width=width
        )
        for label in labels
    ]


def remove_chart_borders(axis):
    """
    Remove bordas que não contribuem para a leitura.
    """

    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.spines["left"].set_visible(False)



# GRÁFICO DOS FATORES DE COMPRA


purchase_plot = (
    purchase_factors
    .sort_values(
        "selection_pct",
        ascending=True
    )
    .copy()
)


purchase_plot["wrapped_label"] = wrap_labels(
    purchase_plot["purchase_factor"]
)


figure, axis = plt.subplots(
    figsize=(11, 7)
)


axis.barh(
    purchase_plot["wrapped_label"],
    purchase_plot["selection_pct"],
    color=WINE_COLOR
)


axis.set_title(
    "Fatores considerados na compra de vinho",
    loc="left",
    fontsize=17,
    fontweight="bold",
    pad=18
)


axis.set_xlabel(
    "Percentual dos participantes"
)

axis.set_ylabel("")

axis.set_xlim(
    0,
    purchase_plot["selection_pct"].max() + 12
)


axis.grid(
    axis="x",
    color=GRID_COLOR,
    alpha=0.7
)

axis.grid(
    axis="y",
    visible=False
)


for position, value in enumerate(
    purchase_plot["selection_pct"]
):

    axis.text(
        value + 1,
        position,
        format_percentage(value),
        va="center",
        fontsize=10,
        fontweight="bold"
    )


remove_chart_borders(axis)

figure.tight_layout()


purchase_chart_file = (
    FIGURES_DIR /
    "01_purchase_factors.png"
)


figure.savefig(
    purchase_chart_file,
    dpi=200,
    bbox_inches="tight"
)

plt.close(figure)



#  ATRIBUTOS DOS VINHOS SUSTENTÁVEIS


sustainable_plot = (
    sustainable_attributes
    .sort_values(
        "selection_pct",
        ascending=True
    )
    .copy()
)


sustainable_plot["wrapped_label"] = wrap_labels(
    sustainable_plot["sustainable_attribute"]
)


figure, axis = plt.subplots(
    figsize=(11, 6)
)


axis.barh(
    sustainable_plot["wrapped_label"],
    sustainable_plot["selection_pct"],
    color=GREEN_COLOR
)


axis.set_title(
    "Atributos valorizados em vinhos sustentáveis",
    loc="left",
    fontsize=17,
    fontweight="bold",
    pad=18
)


axis.set_xlabel(
    "Percentual dos participantes"
)

axis.set_ylabel("")

axis.set_xlim(
    0,
    sustainable_plot["selection_pct"].max() + 12
)


axis.grid(
    axis="x",
    color=GRID_COLOR,
    alpha=0.7
)

axis.grid(
    axis="y",
    visible=False
)


for position, value in enumerate(
    sustainable_plot["selection_pct"]
):

    axis.text(
        value + 1,
        position,
        format_percentage(value),
        va="center",
        fontsize=10,
        fontweight="bold"
    )


remove_chart_borders(axis)

figure.tight_layout()


sustainable_chart_file = (
    FIGURES_DIR /
    "02_sustainable_attributes.png"
)


figure.savefig(
    sustainable_chart_file,
    dpi=200,
    bbox_inches="tight"
)

plt.close(figure)



importance_order = [
    "Pouco importante",
    "Moderadamente importante",
    "Muito importante",
    "Extremamente importante"
]


importance_distribution = (
    df["label_importance"]
    .value_counts()
    .reindex(
        importance_order,
        fill_value=0
    )
    .reset_index()
)


importance_distribution.columns = [
    "label_importance",
    "respondents"
]


importance_distribution["percentage"] = (
    100 *
    importance_distribution["respondents"] /
    len(df)
)


figure, axis = plt.subplots(
    figsize=(10, 5.5)
)


bars = axis.bar(
    importance_distribution["label_importance"],
    importance_distribution["percentage"],
    color=[
        "#DFC0B6",
        ROSE_COLOR,
        "#A44A5A",
        WINE_COLOR
    ]
)


axis.set_title(
    "Importância da sustentabilidade no rótulo",
    loc="left",
    fontsize=17,
    fontweight="bold",
    pad=18
)


axis.set_xlabel("")

axis.set_ylabel(
    "Percentual dos participantes"
)

axis.set_ylim(
    0,
    importance_distribution["percentage"].max() + 10
)


axis.grid(
    axis="y",
    color=GRID_COLOR,
    alpha=0.7
)

axis.grid(
    axis="x",
    visible=False
)


axis.tick_params(
    axis="x",
    rotation=10
)


for bar, value in zip(
    bars,
    importance_distribution["percentage"]
):

    axis.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        format_percentage(value),
        ha="center",
        fontweight="bold"
    )


axis.spines["top"].set_visible(False)
axis.spines["right"].set_visible(False)

figure.tight_layout()


importance_chart_file = (
    FIGURES_DIR /
    "03_label_importance.png"
)


figure.savefig(
    importance_chart_file,
    dpi=200,
    bbox_inches="tight"
)

plt.close(figure)



segments_plot = (
    strategic_segments
    .sort_values(
        "respondents_pct",
        ascending=True
    )
    .copy()
)


segments_plot["wrapped_label"] = wrap_labels(
    segments_plot["strategic_segment"],
    width=28
)


segment_colors = []


for segment in segments_plot["strategic_segment"]:

    if segment == "Alta prioridade":
        segment_colors.append(WINE_COLOR)

    elif segment == "Potencial sustentável":
        segment_colors.append(GREEN_COLOR)

    elif segment == "Consumidor frequente tradicional":
        segment_colors.append(ROSE_COLOR)

    else:
        segment_colors.append(LIGHT_GREEN)


figure, axis = plt.subplots(
    figsize=(10, 5.5)
)


axis.barh(
    segments_plot["wrapped_label"],
    segments_plot["respondents_pct"],
    color=segment_colors
)


axis.set_title(
    "Distribuição dos segmentos estratégicos",
    loc="left",
    fontsize=17,
    fontweight="bold",
    pad=18
)


axis.set_xlabel(
    "Percentual dos participantes"
)

axis.set_ylabel("")

axis.set_xlim(
    0,
    segments_plot["respondents_pct"].max() + 10
)


axis.grid(
    axis="x",
    color=GRID_COLOR,
    alpha=0.7
)

axis.grid(
    axis="y",
    visible=False
)


for position, value in enumerate(
    segments_plot["respondents_pct"]
):

    axis.text(
        value + 0.8,
        position,
        format_percentage(value),
        va="center",
        fontsize=10,
        fontweight="bold"
    )


remove_chart_borders(axis)

figure.tight_layout()


segments_chart_file = (
    FIGURES_DIR /
    "04_strategic_segments.png"
)


figure.savefig(
    segments_chart_file,
    dpi=200,
    bbox_inches="tight"
)

plt.close(figure)



respondents = len(df)


high_importance_pct = (
    100 *
    df["high_label_importance"].mean()
)


average_importance = (
    df["label_importance_score"].mean()
)


average_monthly_consumption = (
    df["monthly_consumption_estimate"].mean()
)


south_region_pct = (
    100 *
    df["region"]
    .eq("Região Sul")
    .mean()
)


postgraduate_pct = (
    100 *
    df["education"]
    .eq("Pós-graduação completa")
    .mean()
)


urban_zone_pct = (
    100 *
    df["residence_zone"]
    .eq("Zona urbana")
    .mean()
)


top_purchase_factor = (
    purchase_factors.iloc[0]
)


top_sustainable_attribute = (
    sustainable_attributes.iloc[0]
)



summary = f"""
PIWI CONSUMER INSIGHTS
SUMÁRIO EXECUTIVO

Participantes analisados: {respondents}

PRINCIPAIS RESULTADOS

1. {format_percentage(high_importance_pct)} dos participantes
consideram muito ou extremamente importante comunicar
sustentabilidade no rótulo.

2. O principal fator geral de compra foi:
{top_purchase_factor["purchase_factor"]}
({format_percentage(top_purchase_factor["selection_pct"])}).

3. O principal atributo valorizado em vinhos sustentáveis foi:
{top_sustainable_attribute["sustainable_attribute"]}
({format_percentage(top_sustainable_attribute["selection_pct"])}).

4. A importância média da sustentabilidade no rótulo foi
{average_importance:.2f} em uma escala de 1 a 4.

5. A frequência média estimada de consumo foi
{average_monthly_consumption:.1f} vezes por mês.

RECOMENDAÇÃO DE NEGÓCIO

A estratégia de posicionamento dos vinhos PIWI deve combinar:

- qualidade sensorial;
- preço competitivo;
- clareza das informações no rótulo;
- benefícios ambientais comprovados.

A sustentabilidade deve complementar a proposta de valor,
e não substituir atributos tradicionais como qualidade e preço.

LIMITAÇÕES DA ANÁLISE

A amostra é de conveniência e apresenta concentração:

- Região Sul: {format_percentage(south_region_pct)};
- Pós-graduação completa: {format_percentage(postgraduate_pct)};
- Zona urbana: {format_percentage(urban_zone_pct)}.

Os resultados descrevem os participantes da pesquisa e não
devem ser generalizados automaticamente para toda a população
brasileira.
""".strip()


SUMMARY_FILE = (
    REPORTS_DIR /
    "executive_summary.txt"
)


SUMMARY_FILE.write_text(
    summary,
    encoding="utf-8"
)



print("\nGráficos criados:")

print(f"- {purchase_chart_file.name}")
print(f"- {sustainable_chart_file.name}")
print(f"- {importance_chart_file.name}")
print(f"- {segments_chart_file.name}")


print("\n" + "-" * 60)
print("PRINCIPAIS RESULTADOS")
print("-" * 60)

print(
    "Alta importância do rótulo: "
    f"{format_percentage(high_importance_pct)}"
)

print(
    "Importância média: "
    f"{average_importance:.2f}"
)

print(
    "Consumo mensal estimado: "
    f"{average_monthly_consumption:.1f}"
)


print("\nSumário executivo criado:")
print(SUMMARY_FILE)


print("\n" + "=" * 60)
print("ANÁLISE EXPLORATÓRIA FINALIZADA")
print("=" * 60)