
-- Testes de qualidade do banco de dados

-- O resultado deve ser zero
SELECT
    COUNT(*) AS duplicate_ids

FROM (
    SELECT
        respondent_id

    FROM fact_respondents

    GROUP BY
        respondent_id

    HAVING
        COUNT(*) > 1
);


-- O resultado deve ser zero
SELECT
    COUNT(*) AS invalid_importance_scores

FROM fact_respondents

WHERE
    label_importance_score NOT BETWEEN 1 AND 4

    OR label_importance_score IS NULL;


-- O resultado deve ser zero
SELECT
    COUNT(*) AS invalid_binary_values

FROM fact_respondents

WHERE
    high_label_importance NOT IN (0, 1)

    OR high_label_importance IS NULL;


-- O resultado deve ser zero
SELECT
    COUNT(*) AS orphan_purchase_factors

FROM bridge_purchase_factors AS bridge

LEFT JOIN fact_respondents AS respondent
    ON bridge.respondent_id =
       respondent.respondent_id

WHERE
    respondent.respondent_id IS NULL;


-- O resultado deve ser zero
SELECT
    COUNT(*) AS orphan_purchase_channels

FROM bridge_purchase_channels AS bridge

LEFT JOIN fact_respondents AS respondent
    ON bridge.respondent_id =
       respondent.respondent_id

WHERE
    respondent.respondent_id IS NULL;


-- O resultado deve ser zero
SELECT
    COUNT(*) AS orphan_sustainable_attributes

FROM bridge_sustainable_attributes AS bridge

LEFT JOIN fact_respondents AS respondent
    ON bridge.respondent_id =
       respondent.respondent_id

WHERE
    respondent.respondent_id IS NULL;