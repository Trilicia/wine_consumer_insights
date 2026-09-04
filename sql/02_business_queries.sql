
-- ---------------------------------------------------------
-- 1. Quais são os principais indicadores do projeto?
-- ---------------------------------------------------------

SELECT *
FROM vw_executive_kpis;


-- ---------------------------------------------------------
-- 2. Quais fatores são mais considerados na compra?
-- ---------------------------------------------------------

SELECT
    purchase_factor,
    respondents,
    selection_pct

FROM vw_purchase_factor_ranking

ORDER BY
    selection_pct DESC;


-- ---------------------------------------------------------
-- 3. Quais atributos são mais valorizados em vinhos
-- sustentáveis?
-- ---------------------------------------------------------

SELECT
    sustainable_attribute,
    respondents,
    selection_pct

FROM vw_sustainable_attribute_ranking

ORDER BY
    selection_pct DESC;


-- ---------------------------------------------------------
-- 4. Quais são os principais canais de aquisição?
-- ---------------------------------------------------------

SELECT
    purchase_channel,
    respondents,
    selection_pct

FROM vw_purchase_channel_ranking

ORDER BY
    selection_pct DESC;


-- ---------------------------------------------------------
-- 5. Como a importância do rótulo varia por perfil?
-- ---------------------------------------------------------

SELECT
    consumer_profile,
    respondents,
    average_importance,
    high_importance_pct

FROM vw_importance_by_profile

WHERE respondents >= 5

ORDER BY
    high_importance_pct DESC;


-- ---------------------------------------------------------
-- 6. Qual é a distribuição dos segmentos estratégicos?
-- ---------------------------------------------------------

SELECT *
FROM vw_strategic_segments;


-- ---------------------------------------------------------
-- 7. Quais canais são utilizados pelo público que atribui
-- alta importância à sustentabilidade no rótulo?
-- ---------------------------------------------------------

SELECT
    channel.option AS purchase_channel,

    COUNT(
        DISTINCT channel.respondent_id
    ) AS respondents,

    ROUND(
        100.0 *
        COUNT(DISTINCT channel.respondent_id) /
        (
            SELECT COUNT(*)
            FROM fact_respondents
            WHERE high_label_importance = 1
        ),
        1
    ) AS high_interest_audience_pct

FROM bridge_purchase_channels AS channel

INNER JOIN fact_respondents AS respondent
    ON channel.respondent_id =
       respondent.respondent_id

WHERE
    respondent.high_label_importance = 1

GROUP BY
    channel.option

ORDER BY
    respondents DESC;


-- ---------------------------------------------------------
-- 8. Quais perfis combinam alta frequência de consumo
-- e alta importância da sustentabilidade?
-- ---------------------------------------------------------

SELECT
    consumer_profile,
    COUNT(*) AS respondents,

    ROUND(
        AVG(monthly_consumption_estimate),
        1
    ) AS average_monthly_consumption,

    ROUND(
        100.0 * AVG(high_label_importance),
        1
    ) AS high_importance_pct

FROM fact_respondents

WHERE
    consumption_intensity = 'Alta frequência'

GROUP BY
    consumer_profile

HAVING
    COUNT(*) >= 5

ORDER BY
    high_importance_pct DESC,
    respondents DESC;