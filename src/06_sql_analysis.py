import sqlite3
from pathlib import Path

import pandas as pd



PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATABASE_FILE = (
    PROJECT_ROOT /
    "data" /
    "processed" /
    "piwi_consumer_insights.db"
)

SQL_DIR = PROJECT_ROOT / "sql"

REPORTS_DIR = PROJECT_ROOT / "reports"

VIEWS_FILE = SQL_DIR / "01_create_views.sql"


# Garante que a pasta reports exista
REPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)



if not DATABASE_FILE.exists():

    raise FileNotFoundError(
        "Banco de dados não encontrado. "
        "Execute primeiro o arquivo "
        "src/05_database_load.py."
    )


if not VIEWS_FILE.exists():

    raise FileNotFoundError(
        "O arquivo sql/01_create_views.sql "
        "não foi encontrado."
    )


print("\n" + "=" * 60)
print("ANÁLISE SQL")
print("=" * 60)



connection = sqlite3.connect(
    DATABASE_FILE
)


try:

   

    views_script = VIEWS_FILE.read_text(
        encoding="utf-8"
    )

    connection.executescript(
        views_script
    )

    connection.commit()

    print("\nViews criadas com sucesso.")


    

    views = pd.read_sql_query(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'view'
        ORDER BY name;
        """,
        connection
    )


    print("\nViews disponíveis:")

    for view_name in views["name"]:
        print(f"- {view_name}")


   

    analytical_queries = {

        "executive_kpis": """
            SELECT *
            FROM vw_executive_kpis;
        """,

        "importance_by_profile": """
            SELECT *
            FROM vw_importance_by_profile;
        """,

        "purchase_factor_ranking": """
            SELECT *
            FROM vw_purchase_factor_ranking;
        """,

        "sustainable_attribute_ranking": """
            SELECT *
            FROM vw_sustainable_attribute_ranking;
        """,

        "purchase_channel_ranking": """
            SELECT *
            FROM vw_purchase_channel_ranking;
        """,

        "strategic_segments": """
            SELECT *
            FROM vw_strategic_segments;
        """
    }


  

    query_results = {}


    for report_name, query in analytical_queries.items():

        result = pd.read_sql_query(
            query,
            connection
        )

        query_results[report_name] = result

        output_file = (
            REPORTS_DIR /
            f"{report_name}.csv"
        )

        result.to_csv(
            output_file,
            index=False,
            encoding="utf-8-sig"
        )

        print(
            f"Relatório criado: "
            f"{output_file.name}"
        )


  

    print("\n" + "-" * 60)
    print("INDICADORES EXECUTIVOS")
    print("-" * 60)

    print(
        query_results["executive_kpis"]
        .to_string(index=False)
    )


    
    print("\n" + "-" * 60)
    print("PRINCIPAIS FATORES DE COMPRA")
    print("-" * 60)

    print(
        query_results["purchase_factor_ranking"]
        .head(5)
        .to_string(index=False)
    )


   

    print("\n" + "-" * 60)
    print("ATRIBUTOS DE VINHOS SUSTENTÁVEIS")
    print("-" * 60)

    print(
        query_results[
            "sustainable_attribute_ranking"
        ]
        .head(5)
        .to_string(index=False)
    )


   

    quality_queries = {

        "duplicate_ids": """
            SELECT COUNT(*) AS total
            FROM (
                SELECT respondent_id
                FROM fact_respondents
                GROUP BY respondent_id
                HAVING COUNT(*) > 1
            );
        """,

        "invalid_importance_scores": """
            SELECT COUNT(*) AS total
            FROM fact_respondents
            WHERE label_importance_score
                  NOT BETWEEN 1 AND 4
               OR label_importance_score IS NULL;
        """,

        "invalid_binary_values": """
            SELECT COUNT(*) AS total
            FROM fact_respondents
            WHERE high_label_importance
                  NOT IN (0, 1)
               OR high_label_importance IS NULL;
        """
    }


    print("\n" + "-" * 60)
    print("TESTES DE QUALIDADE")
    print("-" * 60)


    quality_errors = 0


    for check_name, query in quality_queries.items():

        result = pd.read_sql_query(
            query,
            connection
        )

        total = result.loc[0, "total"]

        quality_errors += total

        print(f"{check_name}: {total}")


    if quality_errors > 0:

        raise ValueError(
            "O banco possui problemas de qualidade."
        )


    print("\nTodos os testes de qualidade passaram.")


    print("\n" + "=" * 60)
    print("ANÁLISE SQL FINALIZADA COM SUCESSO")
    print("=" * 60)


finally:

    connection.close()

    print("\nConexão com o banco encerrada.")