
-- Criação das views analíticas

DROP VIEW IF EXISTS vw_executive_kpis;


CREATE VIEW vw_executive_kpis AS

SELECT
    COUNT(*) AS respondents,

    ROUND(
        AVG(label_importance_score),
        2
    ) AS average_label_importance,

    ROUND(
        100.0 * AVG(high_label_importance),
        1
    ) AS high_label_importance_pct,

    ROUND(
        AVG(monthly_consumption_estimate),
        1
    ) AS average_monthly_consumption,

    ROUND(
        100.0 * AVG(
            CASE
                WHEN consumer_profile IN (
                    'Apreciador técnico',
                    'Profissional do setor'
                )
                THEN 1.0
                ELSE 0.0
            END
        ),
        1
    ) AS technical_audience_pct

FROM fact_respondents;


DROP VIEW IF EXISTS vw_importance_by_profile;


CREATE VIEW vw_importance_by_profile AS

SELECT
    consumer_profile,

    COUNT(*) AS respondents,

    ROUND(
        AVG(label_importance_score),
        2
    ) AS average_importance,

    ROUND(
        100.0 * AVG(high_label_importance),
        1
    ) AS high_importance_pct

FROM fact_respondents

GROUP BY
    consumer_profile

ORDER BY
    high_importance_pct DESC,
    respondents DESC;

DROP VIEW IF EXISTS vw_purchase_factor_ranking;


CREATE VIEW vw_purchase_factor_ranking AS

SELECT
    bridge.option AS purchase_factor,

    COUNT(
        DISTINCT bridge.respondent_id
    ) AS respondents,

    ROUND(
        100.0 *
        COUNT(DISTINCT bridge.respondent_id) /
        (
            SELECT COUNT(*)
            FROM fact_respondents
        ),
        1
    ) AS selection_pct

FROM bridge_purchase_factors AS bridge

GROUP BY
    bridge.option

ORDER BY
    respondents DESC;



DROP VIEW IF EXISTS vw_sustainable_attribute_ranking;


CREATE VIEW vw_sustainable_attribute_ranking AS

SELECT
    bridge.option AS sustainable_attribute,

    COUNT(
        DISTINCT bridge.respondent_id
    ) AS respondents,

    ROUND(
        100.0 *
        COUNT(DISTINCT bridge.respondent_id) /
        (
            SELECT COUNT(*)
            FROM fact_respondents
        ),
        1
    ) AS selection_pct

FROM bridge_sustainable_attributes AS bridge

GROUP BY
    bridge.option

ORDER BY
    respondents DESC;


DROP VIEW IF EXISTS vw_purchase_channel_ranking;


CREATE VIEW vw_purchase_channel_ranking AS

SELECT
    bridge.option AS purchase_channel,

    COUNT(
        DISTINCT bridge.respondent_id
    ) AS respondents,

    ROUND(
        100.0 *
        COUNT(DISTINCT bridge.respondent_id) /
        (
            SELECT COUNT(*)
            FROM fact_respondents
        ),
        1
    ) AS selection_pct

FROM bridge_purchase_channels AS bridge

GROUP BY
    bridge.option

ORDER BY
    respondents DESC;



DROP VIEW IF EXISTS vw_strategic_segments;


CREATE VIEW vw_strategic_segments AS

SELECT
    strategic_segment,

    COUNT(*) AS respondents,

    ROUND(
        100.0 * COUNT(*) /
        (
            SELECT COUNT(*)
            FROM fact_respondents
        ),
        1
    ) AS respondents_pct,

    ROUND(
        AVG(monthly_consumption_estimate),
        1
    ) AS average_monthly_consumption,

    ROUND(
        AVG(label_importance_score),
        2
    ) AS average_label_importance

FROM fact_respondents

GROUP BY
    strategic_segment

ORDER BY
    respondents DESC;