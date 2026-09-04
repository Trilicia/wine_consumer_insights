"use strict";



const data = window.PIWI_DATA || [];


if (data.length === 0) {

    throw new Error(
        "Nenhum dado foi encontrado em data.js."
    );

}


console.log(
    `Dashboard carregado com ${data.length} participantes.`
);




const filterElements = {

    region: document.getElementById(
        "filterRegion"
    ),

    age_group: document.getElementById(
        "filterAge"
    ),

    consumer_profile: document.getElementById(
        "filterProfile"
    ),

    consumption_frequency: document.getElementById(
        "filterFrequency"
    ),

    education: document.getElementById(
        "filterEducation"
    )

};


const clearFiltersButton = document.getElementById(
    "clearFilters"
);




const sampleCountElement = document.getElementById(
    "sampleCount"
);

const filteredCountElement = document.getElementById(
    "filteredCount"
);

const respondentsElement = document.getElementById(
    "kpiRespondents"
);

const highImportanceElement = document.getElementById(
    "kpiHighImportance"
);

const averageImportanceElement = document.getElementById(
    "kpiAverageImportance"
);

const frequencyElement = document.getElementById(
    "kpiFrequency"
);

const insightTextElement = document.getElementById(
    "insightText"
);



const COLORS = {

    wine: "#722F37",

    wineDark: "#421D23",

    wineLight: "#A44A5A",

    rose: "#C98A83",

    roseLight: "#DFC0B6",

    green: "#45634C",

    greenLight: "#A8B9A5",

    grid: "#E5DDDA",

    text: "#302A2B"

};



const indicatorLabels = {

    purchase_factors: {

        preco:
            "Preço",

        regiao_de_origem:
            "Região de origem",

        variedade:
            "Variedade",

        vinicola_produtor:
            "Vinícola / Produtor",

        recomendacao_amigos_especialistas_avaliacoes:
            "Recomendação",

        descricao_sensorial_aroma_sabor_estilo:
            "Descrição sensorial",

        promocoes_ou_descontos:
            "Promoções ou descontos",

        design_e_informacao_do_rotulo:
            "Design e informação do rótulo",

        praticas_sustentaveis_e_ou_impacto_ambiental:
            "Práticas sustentáveis",

        curiosidade_ou_interesse_por_novos_produtos:
            "Interesse por novidades"

    },


    sustainable_attributes: {

        qualidade_sensorial_sabor_aroma_equilibrio:
            "Qualidade sensorial",

        sustentabilidade_ambiental_menor_impacto_no_cultivo:
            "Sustentabilidade ambiental",

        origem_das_uvas_regiao_procedencia:
            "Origem das uvas",

        clareza_e_transparencia_das_informacoes_no_rotulo:
            "Clareza no rótulo",

        presenca_de_certificacoes_ou_selos_ambientais:
            "Certificações ambientais",

        preco:
            "Preço",

        grau_de_inovacao_do_produto:
            "Grau de inovação"

    },


    purchase_channels: {

        supermercados:
            "Supermercados",

        lojas_fisicas_especializadas:
            "Lojas físicas especializadas",

        lojas_online_especializadas:
            "Lojas online especializadas",

        diretamente_em_vinicolas:
            "Diretamente em vinícolas",

        restaurantes_e_bares:
            "Restaurantes e bares",

        aplicativos_de_delivery_de_bebidas:
            "Aplicativos de delivery"

    }

};



const filterOrders = {

    age_group: [
        "Entre 18 e 25 anos",
        "Entre 26 e 35 anos",
        "Entre 36 e 45 anos",
        "Entre 46 e 55 anos",
        "Acima de 55 anos"
    ],


    consumption_frequency: [
        "Não consumo vinho",
        "Raramente",
        "1 vez por mês",
        "1 vez a cada 15 dias",
        "1 vez por semana",
        "De 2 a 3 vezes por semana",
        "De 4 a 6 vezes por semana",
        "Diariamente"
    ]

};



let purchaseFactorsChart = null;

let importanceChart = null;

let sustainableAttributesChart = null;

let purchaseChannelsChart = null;




function formatPercentage(value) {

    return new Intl.NumberFormat(
        "pt-BR",
        {
            minimumFractionDigits: 1,
            maximumFractionDigits: 1
        }
    ).format(value) + "%";

}


function formatDecimal(value, decimalPlaces = 2) {

    return new Intl.NumberFormat(
        "pt-BR",
        {
            minimumFractionDigits: decimalPlaces,
            maximumFractionDigits: decimalPlaces
        }
    ).format(value);

}



function populateFilter(fieldName, selectElement) {

    let values = [
        ...new Set(
            data
                .map(row => row[fieldName])
                .filter(value => value)
        )
    ];


    if (filterOrders[fieldName]) {

        values = filterOrders[fieldName].filter(
            value => values.includes(value)
        );

    } else {

        values.sort(
            (firstValue, secondValue) =>
                firstValue.localeCompare(
                    secondValue,
                    "pt-BR"
                )
        );

    }


    values.forEach(value => {

        const option = document.createElement(
            "option"
        );

        option.value = value;

        option.textContent = value;

        selectElement.appendChild(option);

    });

}



function getFilteredData() {

    return data.filter(row => {

        return Object.entries(
            filterElements
        ).every(([fieldName, selectElement]) => {

            const selectedValue =
                selectElement.value;

            return (
                selectedValue === ""
                || row[fieldName] === selectedValue
            );

        });

    });

}



function calculateIndicatorRanking(
    filteredData,
    prefix
) {

    const indicatorColumns = Object.keys(
        data[0]
    ).filter(column => {

        return column.startsWith(
            `${prefix}__`
        );

    });


    const ranking = indicatorColumns.map(column => {

        const selectedTotal = filteredData.reduce(
            (total, row) => {

                return (
                    total
                    + Number(row[column] || 0)
                );

            },
            0
        );


        const percentage = (
            filteredData.length > 0
                ? (
                    selectedTotal
                    / filteredData.length
                ) * 100
                : 0
        );


        const indicatorName = column.replace(
            `${prefix}__`,
            ""
        );


        const friendlyLabel = (
            indicatorLabels[prefix]?.[indicatorName]
            || indicatorName
        );


        return {

            label: friendlyLabel,

            percentage: percentage,

            total: selectedTotal

        };

    });


    ranking.sort(
        (firstItem, secondItem) =>
            secondItem.percentage
            - firstItem.percentage
    );


    return ranking;

}



function createBarChartOptions() {

    return {

        responsive: true,

        maintainAspectRatio: false,

        indexAxis: "y",

        animation: {
            duration: 450
        },

        plugins: {

            legend: {
                display: false
            },

            tooltip: {

                callbacks: {

                    label: function(context) {

                        return (
                            formatPercentage(
                                context.raw
                            )
                        );

                    }

                }

            }

        },

        scales: {

            x: {

                beginAtZero: true,

                max: 100,

                ticks: {

                    callback: function(value) {

                        return value + "%";

                    },

                    color: COLORS.text

                },

                grid: {
                    color: COLORS.grid
                }

            },


            y: {

                ticks: {

                    color: COLORS.text,

                    font: {
                        size: 12
                    }

                },

                grid: {
                    display: false
                }

            }

        }

    };

}



function renderPurchaseFactorsChart(
    filteredData
) {

    const ranking = calculateIndicatorRanking(
        filteredData,
        "purchase_factors"
    );


    if (purchaseFactorsChart) {

        purchaseFactorsChart.destroy();

    }


    const chartContext = document
        .getElementById(
            "purchaseFactorsChart"
        )
        .getContext("2d");


    purchaseFactorsChart = new Chart(
        chartContext,
        {

            type: "bar",

            data: {

                labels: ranking.map(
                    item => item.label
                ),

                datasets: [{

                    data: ranking.map(
                        item => item.percentage
                    ),

                    backgroundColor:
                        COLORS.wine,

                    borderRadius: 6,

                    barThickness: 16

                }]

            },

            options: createBarChartOptions()

        }
    );

}



function renderSustainableAttributesChart(
    filteredData
) {

    const ranking = calculateIndicatorRanking(
        filteredData,
        "sustainable_attributes"
    );


    if (sustainableAttributesChart) {

        sustainableAttributesChart.destroy();

    }


    const chartContext = document
        .getElementById(
            "sustainableAttributesChart"
        )
        .getContext("2d");


    sustainableAttributesChart = new Chart(
        chartContext,
        {

            type: "bar",

            data: {

                labels: ranking.map(
                    item => item.label
                ),

                datasets: [{

                    data: ranking.map(
                        item => item.percentage
                    ),

                    backgroundColor:
                        COLORS.green,

                    borderRadius: 6,

                    barThickness: 18

                }]

            },

            options: createBarChartOptions()

        }
    );

}


function renderPurchaseChannelsChart(
    filteredData
) {

    const ranking = calculateIndicatorRanking(
        filteredData,
        "purchase_channels"
    );


    if (purchaseChannelsChart) {

        purchaseChannelsChart.destroy();

    }


    const chartContext = document
        .getElementById(
            "purchaseChannelsChart"
        )
        .getContext("2d");


    purchaseChannelsChart = new Chart(
        chartContext,
        {

            type: "bar",

            data: {

                labels: ranking.map(
                    item => item.label
                ),

                datasets: [{

                    data: ranking.map(
                        item => item.percentage
                    ),

                    backgroundColor:
                        COLORS.rose,

                    borderRadius: 6,

                    barThickness: 18

                }]

            },

            options: createBarChartOptions()

        }
    );

}



function renderImportanceChart(
    filteredData
) {

    const importanceOrder = [
        "Extremamente importante",
        "Muito importante",
        "Moderadamente importante",
        "Pouco importante"
    ];


    const importanceValues = importanceOrder.map(
        importanceLevel => {

            return filteredData.filter(row => {

                return (
                    row.label_importance
                    === importanceLevel
                );

            }).length;

        }
    );


    if (importanceChart) {

        importanceChart.destroy();

    }


    const chartContext = document
        .getElementById(
            "importanceChart"
        )
        .getContext("2d");


    importanceChart = new Chart(
        chartContext,
        {

            type: "doughnut",

            data: {

                labels: importanceOrder,

                datasets: [{

                    data: importanceValues,

                    backgroundColor: [
                        COLORS.wine,
                        COLORS.wineLight,
                        COLORS.rose,
                        COLORS.roseLight
                    ],

                    borderColor: "#FFFDFB",

                    borderWidth: 3,

                    hoverOffset: 8

                }]

            },


            options: {

                responsive: true,

                maintainAspectRatio: false,

                cutout: "63%",

                plugins: {

                    legend: {

                        position: "bottom",

                        labels: {

                            color: COLORS.text,

                            boxWidth: 13,

                            padding: 16,

                            font: {
                                size: 11
                            }

                        }

                    },


                    tooltip: {

                        callbacks: {

                            label: function(context) {

                                const total = (
                                    context.dataset.data
                                    .reduce(
                                        (
                                            accumulated,
                                            value
                                        ) =>
                                            accumulated
                                            + value,
                                        0
                                    )
                                );


                                const percentage = (
                                    total > 0
                                        ? (
                                            context.raw
                                            / total
                                        ) * 100
                                        : 0
                                );


                                return (
                                    `${context.label}: `
                                    + formatPercentage(
                                        percentage
                                    )
                                );

                            }

                        }

                    }

                }

            }

        }
    );

}



function updateKpis(filteredData) {

    const respondents =
        filteredData.length;


    const highImportanceTotal =
        filteredData.reduce(
            (total, row) => {

                return (
                    total
                    + Number(
                        row.high_label_importance
                    )
                );

            },
            0
        );


    const importanceTotal =
        filteredData.reduce(
            (total, row) => {

                return (
                    total
                    + Number(
                        row.label_importance_score
                    )
                );

            },
            0
        );


    const frequencyTotal =
        filteredData.reduce(
            (total, row) => {

                return (
                    total
                    + Number(
                        row.monthly_consumption_estimate
                    )
                );

            },
            0
        );


    const highImportancePercentage = (
        respondents > 0
            ? (
                highImportanceTotal
                / respondents
            ) * 100
            : 0
    );


    const averageImportance = (
        respondents > 0
            ? importanceTotal / respondents
            : 0
    );


    const averageFrequency = (
        respondents > 0
            ? frequencyTotal / respondents
            : 0
    );


    respondentsElement.textContent =
        respondents.toLocaleString("pt-BR");


    filteredCountElement.textContent =
        respondents.toLocaleString("pt-BR");


    highImportanceElement.textContent =
        formatPercentage(
            highImportancePercentage
        );


    averageImportanceElement.textContent =
        formatDecimal(
            averageImportance,
            2
        );


    frequencyElement.textContent =
        formatDecimal(
            averageFrequency,
            1
        );

}



function updateInsight(filteredData) {

    if (filteredData.length === 0) {

        insightTextElement.textContent =
            "Nenhum participante corresponde aos filtros selecionados.";

        return;

    }


    const purchaseRanking =
        calculateIndicatorRanking(
            filteredData,
            "purchase_factors"
        );


    const sustainableRanking =
        calculateIndicatorRanking(
            filteredData,
            "sustainable_attributes"
        );


    const topPurchaseFactor =
        purchaseRanking[0];


    const topSustainableAttribute =
        sustainableRanking[0];


    insightTextElement.textContent =
        `Neste recorte, ${topPurchaseFactor.label.toLowerCase()} `
        + `é o principal fator de compra `
        + `(${formatPercentage(topPurchaseFactor.percentage)}), `
        + `enquanto ${topSustainableAttribute.label.toLowerCase()} `
        + `lidera entre os atributos sustentáveis `
        + `(${formatPercentage(topSustainableAttribute.percentage)}).`;

}



function updateDashboard() {

    const filteredData =
        getFilteredData();


    updateKpis(
        filteredData
    );


    updateInsight(
        filteredData
    );


    renderPurchaseFactorsChart(
        filteredData
    );


    renderImportanceChart(
        filteredData
    );


    renderSustainableAttributesChart(
        filteredData
    );


    renderPurchaseChannelsChart(
        filteredData
    );

}



function clearFilters() {

    Object.values(
        filterElements
    ).forEach(selectElement => {

        selectElement.value = "";

    });


    updateDashboard();

}



function initializeDashboard() {

    sampleCountElement.textContent =
        data.length.toLocaleString("pt-BR");


    Object.entries(
        filterElements
    ).forEach(([fieldName, selectElement]) => {

        populateFilter(
            fieldName,
            selectElement
        );


        selectElement.addEventListener(
            "change",
            updateDashboard
        );

    });


    clearFiltersButton.addEventListener(
        "click",
        clearFilters
    );


    updateDashboard();

}



initializeDashboard();