import sqlite3
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DIR = (
    PROJECT_ROOT /
    "data" /
    "processed"
)

DATABASE_FILE = (
    PROCESSED_DIR /
    "piwi_consumer_insights.db"
)


# Arquivos que serão carregados no banco
data_files = {
    "fact_respondents": (
        PROCESSED_DIR /
        "respondents_analytical.csv"
    ),

    "bridge_wine_types": (
        PROCESSED_DIR /
        "bridge_wine_types.csv"
    ),

    "bridge_purchase_channels": (
        PROCESSED_DIR /
        "bridge_purchase_channels.csv"
    ),

    "bridge_purchase_factors": (
        PROCESSED_DIR /
        "bridge_purchase_factors.csv"
    ),

    "bridge_sustainable_attributes": (
        PROCESSED_DIR /
        "bridge_sustainable_attributes.csv"
    ),

    "unclassified_answers": (
        PROCESSED_DIR /
        "unclassified_answers.csv"
    )
}


print("\n" + "=" * 60)
print("CARREGAMENTO DO BANCO DE DADOS")
print("=" * 60)



missing_files = []


for table_name, file_path in data_files.items():

    if not file_path.exists():
        missing_files.append(
            str(file_path)
        )


if missing_files:

    print("\nArquivos não encontrados:")

    for file_path in missing_files:
        print(f"- {file_path}")

    raise FileNotFoundError(
        "Execute as etapas anteriores antes de criar o banco."
    )


print("\nTodos os arquivos necessários foram encontrados.")



connection = sqlite3.connect(
    DATABASE_FILE
)


# Ativa verificações de chave estrangeira
connection.execute(
    "PRAGMA foreign_keys = ON;"
)


print("\nConexão com o SQLite criada com sucesso.")



try:

    for table_name, file_path in data_files.items():

        dataframe = pd.read_csv(
            file_path,
            encoding="utf-8-sig"
        )

        dataframe.to_sql(
            table_name,
            connection,
            if_exists="replace",
            index=False
        )

        print(
            f"Tabela {table_name}: "
            f"{len(dataframe)} registros"
        )


    # Confirma as alterações no banco
    connection.commit()



    connection.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS
        idx_fact_respondents_id
        ON fact_respondents (respondent_id);
        """
    )

    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS
        idx_wine_types_respondent
        ON bridge_wine_types (respondent_id);
        """
    )

    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS
        idx_purchase_channels_respondent
        ON bridge_purchase_channels (respondent_id);
        """
    )

    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS
        idx_purchase_factors_respondent
        ON bridge_purchase_factors (respondent_id);
        """
    )

    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS
        idx_sustainable_attributes_respondent
        ON bridge_sustainable_attributes (respondent_id);
        """
    )

    connection.commit()

    print("\nÍndices criados com sucesso.")


    print("\n" + "-" * 60)
    print("VALIDAÇÃO DAS TABELAS")
    print("-" * 60)


    database_tables = pd.read_sql_query(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name;
        """,
        connection
    )


    print("\nTabelas disponíveis no banco:")

    for table_name in database_tables["name"]:
        print(f"- {table_name}")



    print("\nQuantidade de registros:")


    for table_name in data_files:

        query = (
            f"SELECT COUNT(*) AS total "
            f"FROM {table_name};"
        )

        result = pd.read_sql_query(
            query,
            connection
        )

        total = result.loc[0, "total"]

        print(
            f"{table_name}: {total}"
        )



    duplicate_ids_query = """
        SELECT
            respondent_id,
            COUNT(*) AS occurrences
        FROM fact_respondents
        GROUP BY respondent_id
        HAVING COUNT(*) > 1;
    """


    duplicate_ids = pd.read_sql_query(
        duplicate_ids_query,
        connection
    )


    print(
        "\nIDs duplicados na tabela principal: "
        f"{len(duplicate_ids)}"
    )


    if not duplicate_ids.empty:

        raise ValueError(
            "Foram encontrados IDs duplicados "
            "na tabela fact_respondents."
        )



    bridge_tables = [
        "bridge_wine_types",
        "bridge_purchase_channels",
        "bridge_purchase_factors",
        "bridge_sustainable_attributes"
    ]


    total_orphan_records = 0


    for bridge_table in bridge_tables:

        orphan_query = f"""
            SELECT COUNT(*) AS total
            FROM {bridge_table} AS bridge

            LEFT JOIN fact_respondents AS respondent
                ON bridge.respondent_id =
                   respondent.respondent_id

            WHERE respondent.respondent_id IS NULL;
        """


        orphan_result = pd.read_sql_query(
            orphan_query,
            connection
        )


        orphan_records = (
            orphan_result.loc[0, "total"]
        )


        total_orphan_records += orphan_records


        print(
            f"Registros órfãos em {bridge_table}: "
            f"{orphan_records}"
        )


    if total_orphan_records > 0:

        raise ValueError(
            "Foram encontrados registros órfãos "
            "nas tabelas ponte."
        )

    sample_query = """
        SELECT
            respondent_id,
            region,
            age_group,
            consumer_profile,
            strategic_segment
        FROM fact_respondents
        LIMIT 5;
    """


    sample = pd.read_sql_query(
        sample_query,
        connection
    )


    print("\nExemplo de registros da tabela principal:")
    print(sample)


    print("\n" + "=" * 60)
    print("BANCO CRIADO E VALIDADO COM SUCESSO")
    print("=" * 60)

    print(f"\nBanco salvo em:\n{DATABASE_FILE}")



finally:

    connection.close()

    print("\nConexão com o banco encerrada.")