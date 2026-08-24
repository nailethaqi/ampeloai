const imageInput = document.getElementById("imageInput");
const imagePreview = document.getElementById("imagePreview");
const previewContainer = document.getElementById("previewContainer");
const analyzeButton = document.getElementById("analyzeButton");

const resultContainer = document.getElementById("resultContainer");
const predictionName = document.getElementById("predictionName");
const confidenceValue = document.getElementById("confidenceValue");
const confidenceBar = document.getElementById("confidenceBar");
const predictionStatus = document.getElementById("predictionStatus");
const recommendationText = document.getElementById("recommendationText");
const probabilitiesList = document.getElementById("probabilitiesList");
const newAnalysisButton = document.getElementById("newAnalysisButton");

const unsupportedWarning = document.getElementById("unsupportedWarning");
const unsupportedNewImageButton = document.getElementById(
    "unsupportedNewImageButton"
);

const historyList = document.getElementById("historyList");

const totalAnalyses = document.getElementById("totalAnalyses");
const healthyCount = document.getElementById("healthyCount");
const blackRotCount = document.getElementById("blackRotCount");
const escaCount = document.getElementById("escaCount");
const leafBlightCount = document.getElementById("leafBlightCount");

const blackRotPercent = document.getElementById("blackRotPercent");
const escaPercent = document.getElementById("escaPercent");
const healthyPercent = document.getElementById("healthyPercent");
const leafBlightPercent = document.getElementById("leafBlightPercent");

const blackRotBar = document.getElementById("blackRotBar");
const escaBar = document.getElementById("escaBar");
const healthyBar = document.getElementById("healthyBar");
const leafBlightBar = document.getElementById("leafBlightBar");

const languageButtons = document.querySelectorAll(".language-btn");

const HISTORY_STORAGE_KEY = "ampeloAIHistory";
const LANGUAGE_STORAGE_KEY = "ampeloAILanguage";
const MAX_HISTORY_ITEMS = 50;

const translations = {
    sq: {
        pageTitle: "AmpeloAI - Analiza e Gjethes së Rrushit",

        nav: {
            home: "Ballina",
            analyze: "Analizo",
            history: "Historia",
            statistics: "Statistikat",
            about: "Rreth sistemit"
        },

        hero: {
            badge: "Analizë e bimëve me Inteligjencë Artificiale",
            title: "Zbulimi i sëmundjeve të gjethes së rrushit me Inteligjencë Artificiale",
            description: "Ngarkoni një imazh të gjethes së rrushit dhe sistemi me Inteligjencë Artificiale do të analizojë gjendjen e saj dhe do të identifikojë sëmundjet e mundshme.",
            button: "Analizo gjethen"
        },

        analysis: {
            title: "Analiza e gjethes së rrushit",
            subtitle: "Ngarkoni një imazh për të filluar analizën.",
            requirementsTitle: "Kërkesat për imazhin:",
            requirementsText: "Për një analizë më të saktë, ngarkoni një fotografi të qartë dhe nga afër të një gjethjeje rrushi. Imazhet e frutave të rrushit, kërcellit, bimëve të tjera ose objekteve të palidhura nuk mbështeten.",
            uploadTitle: "Ngarko imazhin e gjethes së rrushit",
            uploadText: "Klikoni këtu për të zgjedhur një imazh",
            fileTypes: "JPG, JPEG ose PNG",
            selectedImage: "Imazhi i zgjedhur",
            analyzeButton: "Analizo imazhin",
            analyzing: "Duke analizuar..."
        },

        result: {
            label: "Rezultati i analizës me AI",
            confidence: "Besueshmëria",
            status: "Statusi",
            recommendation: "Rekomandimi",
            probabilities: "Probabilitetet e parashikimit",
            anotherImage: "Analizo një imazh tjetër",
            analysisCompleted: "Analiza u përfundua",
            reviewResult: "Rishikoni rezultatin e analizës."
        },

        unsupported: {
            title: "Imazh i papërshtatshëm",
            description: "Imazhi i ngarkuar nuk është identifikuar si gjethe rrushi. Ju lutem ngarkoni një fotografi të qartë dhe nga afër të një gjethjeje rrushi.",
            button: "Zgjidh një imazh tjetër",
            className: "Imazh i pambështetur"
        },

        history: {
            badge: "Regjistrimet e analizave",
            title: "Analizat e fundit",
            description: "Shikoni analizat e fundit të realizuara në këtë pajisje me sistemin AmpeloAI.",
            result: "Rezultati",
            confidence: "Besueshmëria",
            date: "Data",
            loading: "Duke ngarkuar analizat...",
            empty: "Ende nuk është regjistruar asnjë analizë në këtë pajisje."
        },

        statistics: {
            badge: "Statistikat e sistemit",
            title: "Statistikat e analizave",
            description: "Përmbledhje e analizave të realizuara në këtë pajisje me sistemin AmpeloAI.",
            total: "Gjithsej analiza",
            healthy: "E shëndetshme",
            blackRot: "Kalbëzimi i zi",
            esca: "Esca",
            escaFull: "Esca (njollat e zeza)",
            healthyLeaf: "Gjethe e shëndetshme",
            leafBlight: "Djegia e gjethes",
            distribution: "Shpërndarja e parashikimeve"
        },

        about: {
            title: "Si funksionon AmpeloAI?",
            step1Title: "Ngarko",
            step1Text: "Ngarkoni një fotografi të qartë dhe nga afër të një gjethjeje rrushi.",
            step2Title: "Analiza me AI",
            step2Text: "Modeli i Inteligjencës Artificiale analizon karakteristikat vizuale të imazhit të ngarkuar.",
            step3Title: "Rezultati",
            step3Text: "Shikoni gjendjen e parashikuar, nivelin e besueshmërisë dhe rekomandimin përkatës."
        },

        footer: {
            text: "© 2026 AmpeloAI. Të gjitha të drejtat e rezervuara."
        },

        alerts: {
            invalidType: "Ju lutem zgjidhni një imazh në formatin JPG, JPEG ose PNG.",
            selectImage: "Ju lutem zgjidhni fillimisht një imazh.",
            analysisError: "Ndodhi një gabim gjatë analizimit të imazhit. Ju lutem provoni përsëri."
        }
    },

    en: {
        pageTitle: "AmpeloAI - Grape Leaf Analysis",

        nav: {
            home: "Home",
            analyze: "Analyze",
            history: "History",
            statistics: "Statistics",
            about: "About"
        },

        hero: {
            badge: "AI-Powered Plant Analysis",
            title: "Detect Grape Leaf Diseases Using Artificial Intelligence",
            description: "Upload an image of a grape leaf and the Artificial Intelligence system will analyze its condition and identify possible diseases.",
            button: "Analyze Leaf"
        },

        analysis: {
            title: "Grape Leaf Analysis",
            subtitle: "Upload an image to begin the analysis.",
            requirementsTitle: "Image requirements:",
            requirementsText: "For accurate analysis, upload a clear close-up image of a grape leaf. Images of grapes, stems, other plants or unrelated objects are not supported.",
            uploadTitle: "Upload grape leaf image",
            uploadText: "Click here to choose an image",
            fileTypes: "JPG, JPEG or PNG",
            selectedImage: "Selected Image",
            analyzeButton: "Analyze Image",
            analyzing: "Analyzing..."
        },

        result: {
            label: "AI Analysis Result",
            confidence: "Confidence",
            status: "Status",
            recommendation: "Recommendation",
            probabilities: "Prediction Probabilities",
            anotherImage: "Analyze Another Image",
            analysisCompleted: "Analysis Completed",
            reviewResult: "Review the analysis result."
        },

        unsupported: {
            title: "Unsupported Image",
            description: "The uploaded image was not identified as a grape leaf. Please upload a clear close-up image of a grape leaf.",
            button: "Choose Another Image",
            className: "Unsupported Image"
        },

        history: {
            badge: "Analysis Records",
            title: "Recent Analyses",
            description: "View the most recent analyses performed on this device using the AmpeloAI system.",
            result: "Result",
            confidence: "Confidence",
            date: "Date",
            loading: "Loading analyses...",
            empty: "No analyses have been recorded on this device yet."
        },

        statistics: {
            badge: "System Statistics",
            title: "Analysis Statistics",
            description: "Summary of the analyses performed on this device using the AmpeloAI system.",
            total: "Total Analyses",
            healthy: "Healthy",
            blackRot: "Black Rot",
            esca: "Esca",
            escaFull: "Esca (Black Measles)",
            healthyLeaf: "Healthy Leaf",
            leafBlight: "Leaf Blight",
            distribution: "Prediction Distribution"
        },

        about: {
            title: "How does AmpeloAI work?",
            step1Title: "Upload",
            step1Text: "Upload a clear close-up photograph of a grape leaf.",
            step2Title: "AI Analysis",
            step2Text: "The Artificial Intelligence model analyzes the visual characteristics of the uploaded image.",
            step3Title: "Result",
            step3Text: "View the predicted condition, confidence score and corresponding recommendation."
        },

        footer: {
            text: "© 2026 AmpeloAI. All rights reserved."
        },

        alerts: {
            invalidType: "Please select an image in JPG, JPEG or PNG format.",
            selectImage: "Please select an image first.",
            analysisError: "An error occurred while analyzing the image. Please try again."
        }
    }
};

const diseaseInformation = {
    Healthy: {
        sq: {
            name: "Gjethe e shëndetshme",
            status: "E shëndetshme",
            recommendation: "Nuk janë identifikuar shenja të sëmundjeve të mbështetura nga sistemi. Vazhdoni monitorimin e rregullt dhe praktikat e mira të menaxhimit të vreshtit."
        },

        en: {
            name: "Healthy Leaf",
            status: "Healthy",
            recommendation: "No signs of the grape leaf diseases supported by the system were detected. Continue regular monitoring and good vineyard management practices."
        }
    },

    Black_Rot: {
        sq: {
            name: "Kalbëzimi i zi",
            status: "Sëmundje e identifikuar",
            recommendation: "Imazhi paraqet karakteristika që lidhen me kalbëzimin e zi. Kontrolloni gjethet dhe materialin bimor përreth dhe, sipas nevojës, konsultohuni me një specialist të bujqësisë."
        },

        en: {
            name: "Black Rot",
            status: "Disease Detected",
            recommendation: "The image shows characteristics associated with Black Rot. Inspect nearby leaves and affected plant material and, when necessary, consider consultation with an agricultural specialist."
        }
    },

    Esca: {
        sq: {
            name: "Esca (njollat e zeza)",
            status: "Sëmundje e identifikuar",
            recommendation: "Gjethja paraqet karakteristika që lidhen me sëmundjen Esca. Monitoroni me kujdes hardhinë e prekur dhe konsideroni një vlerësim profesional për masat e përshtatshme të menaxhimit."
        },

        en: {
            name: "Esca (Black Measles)",
            status: "Disease Detected",
            recommendation: "The leaf shows characteristics associated with Esca. Monitor the affected vine carefully and consider professional assessment for appropriate disease-management measures."
        }
    },

    Leaf_Blight: {
        sq: {
            name: "Djegia e gjethes",
            status: "Sëmundje e identifikuar",
            recommendation: "Imazhi paraqet karakteristika që lidhen me djegien e gjethes. Kontrolloni gjethet përreth, mirëmbani higjienën e vreshtit dhe konsideroni këshillimin me një specialist të bujqësisë."
        },

        en: {
            name: "Leaf Blight",
            status: "Disease Detected",
            recommendation: "The image shows characteristics associated with Leaf Blight. Inspect surrounding leaves, maintain appropriate vineyard hygiene and consider guidance from an agricultural specialist."
        }
    },

    Other: {
        sq: {
            name: "Imazh i pambështetur"
        },

        en: {
            name: "Unsupported Image"
        }
    }
};

const savedLanguage = localStorage.getItem(LANGUAGE_STORAGE_KEY);

let currentLanguage = savedLanguage === "en" ? "en" : "sq";
let lastPrediction = null;
let lastHistory = [];
let isAnalyzing = false;

function translate(key) {
    const keys = key.split(".");
    let value = translations[currentLanguage];

    for (const currentKey of keys) {
        if (
            value &&
            Object.prototype.hasOwnProperty.call(value, currentKey)
        ) {
            value = value[currentKey];
        } else {
            return key;
        }
    }

    return value;
}

function getLocalHistory() {
    try {
        const storedHistory = localStorage.getItem(HISTORY_STORAGE_KEY);

        if (!storedHistory) {
            return [];
        }

        const parsedHistory = JSON.parse(storedHistory);

        if (!Array.isArray(parsedHistory)) {
            return [];
        }

        return parsedHistory.filter(item => {
            return (
                item &&
                typeof item.predicted_class === "string" &&
                item.predicted_class !== "Other" &&
                item.created_at
            );
        });
    } catch (error) {
        console.error("Local history error:", error);
        return [];
    }
}

function saveLocalHistory(history) {
    try {
        localStorage.setItem(
            HISTORY_STORAGE_KEY,
            JSON.stringify(history)
        );
    } catch (error) {
        console.error("Could not save local history:", error);
    }
}

function createAnalysisId() {
    if (
        window.crypto &&
        typeof window.crypto.randomUUID === "function"
    ) {
        return window.crypto.randomUUID();
    }

    return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function saveAnalysisLocally(prediction) {
    if (
        prediction.predicted_class === "Other" ||
        prediction.is_supported === false
    ) {
        return;
    }

    const history = getLocalHistory();

    const analysis = {
        id: createAnalysisId(),
        predicted_class: prediction.predicted_class,
        confidence: Math.min(
            Math.max(
                Number(prediction.confidence) || 0,
                0
            ),
            100
        ),
        created_at: new Date().toISOString()
    };

    history.unshift(analysis);

    const limitedHistory = history.slice(
        0,
        MAX_HISTORY_ITEMS
    );

    saveLocalHistory(limitedHistory);

    refreshLocalHistoryAndStatistics();
}

function applyLanguage(language) {
    currentLanguage = language === "en" ? "en" : "sq";

    localStorage.setItem(
        LANGUAGE_STORAGE_KEY,
        currentLanguage
    );

    document.documentElement.lang = currentLanguage;

    document.title =
        translations[currentLanguage].pageTitle;

    document
        .querySelectorAll("[data-i18n]")
        .forEach(element => {
            const key =
                element.getAttribute("data-i18n");

            element.textContent =
                translate(key);
        });

    languageButtons.forEach(button => {
        button.classList.toggle(
            "active",
            button.dataset.lang === currentLanguage
        );
    });

    if (isAnalyzing) {
        analyzeButton.textContent =
            translate("analysis.analyzing");
    }

    if (lastPrediction) {
        displayPrediction(
            lastPrediction,
            false
        );
    }

    refreshLocalHistoryAndStatistics();

    if (window.lucide) {
        window.lucide.createIcons();
    }
}

languageButtons.forEach(button => {
    button.addEventListener(
        "click",
        function () {
            applyLanguage(
                this.dataset.lang
            );
        }
    );
});

imageInput.addEventListener(
    "change",
    function () {
        const file = this.files[0];

        if (!file) {
            return;
        }

        const allowedTypes = [
            "image/jpeg",
            "image/png"
        ];

        if (!allowedTypes.includes(file.type)) {
            alert(
                translate(
                    "alerts.invalidType"
                )
            );

            imageInput.value = "";
            return;
        }

        const reader =
            new FileReader();

        reader.onload =
            function (event) {
                imagePreview.src =
                    event.target.result;

                previewContainer.hidden =
                    false;

                resultContainer.hidden =
                    true;

                unsupportedWarning.hidden =
                    true;

                lastPrediction = null;

                resetResultValues();
            };

        reader.readAsDataURL(file);
    }
);

analyzeButton.addEventListener(
    "click",
    async function () {
        const file =
            imageInput.files[0];

        if (!file) {
            alert(
                translate(
                    "alerts.selectImage"
                )
            );

            return;
        }

        isAnalyzing = true;

        analyzeButton.disabled = true;

        analyzeButton.textContent =
            translate(
                "analysis.analyzing"
            );

        resultContainer.hidden = true;
        unsupportedWarning.hidden = true;

        const formData =
            new FormData();

        formData.append(
            "file",
            file
        );

        try {
            const response =
                await fetch(
                    "/api/predict",
                    {
                        method: "POST",
                        body: formData
                    }
                );

            const data =
                await response.json();

            if (!response.ok) {
                throw new Error(
                    data.detail ||
                    "Image analysis failed."
                );
            }

            if (
                !data.prediction ||
                !data.prediction.predicted_class
            ) {
                throw new Error(
                    "Invalid prediction response."
                );
            }

            const prediction =
                data.prediction;

            const unsupported =
                prediction.predicted_class === "Other" ||
                prediction.is_supported === false;

            if (unsupported) {
                lastPrediction = null;

                showUnsupportedWarning();

                return;
            }

            lastPrediction =
                prediction;

            displayPrediction(
                prediction
            );

            saveAnalysisLocally(
                prediction
            );

        } catch (error) {
            console.error(
                "Prediction error:",
                error
            );

            alert(
                translate(
                    "alerts.analysisError"
                )
            );

        } finally {
            isAnalyzing = false;

            analyzeButton.disabled =
                false;

            analyzeButton.textContent =
                translate(
                    "analysis.analyzeButton"
                );
        }
    }
);

function showUnsupportedWarning() {
    resultContainer.hidden = true;

    unsupportedWarning.hidden = false;

    resetResultValues();

    if (window.lucide) {
        window.lucide.createIcons();
    }

    unsupportedWarning.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
}

function displayPrediction(
    prediction,
    shouldScroll = true
) {
    const className =
        prediction.predicted_class;

    const information =
        diseaseInformation[
            className
        ]?.[currentLanguage] || null;

    predictionName.textContent =
        information?.name ||
        className;

    const confidence =
        Math.min(
            Math.max(
                Number(
                    prediction.confidence
                ) || 0,
                0
            ),
            100
        );

    confidenceValue.textContent =
        `${confidence.toFixed(2)}%`;

    confidenceBar.style.width =
        `${confidence}%`;

    predictionStatus.textContent =
        information?.status ||
        translate(
            "result.analysisCompleted"
        );

    recommendationText.textContent =
        information?.recommendation ||
        translate(
            "result.reviewResult"
        );

    predictionStatus.className =
        className === "Healthy"
            ? "status-healthy"
            : "status-disease";

    displayProbabilities(
        prediction.probabilities || {}
    );

    unsupportedWarning.hidden = true;
    resultContainer.hidden = false;

    if (shouldScroll) {
        resultContainer.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }
}

function displayProbabilities(
    probabilities
) {
    probabilitiesList.innerHTML = "";

    Object.entries(
        probabilities
    ).forEach(
        ([className, value]) => {
            const probability =
                Math.min(
                    Math.max(
                        Number(value) || 0,
                        0
                    ),
                    100
                );

            const information =
                diseaseInformation[
                    className
                ]?.[currentLanguage] || null;

            const readableName =
                information?.name ||
                className;

            const item =
                document.createElement(
                    "div"
                );

            item.className =
                "probability-item";

            const info =
                document.createElement(
                    "div"
                );

            info.className =
                "probability-info";

            const name =
                document.createElement(
                    "span"
                );

            name.textContent =
                readableName;

            const percentage =
                document.createElement(
                    "strong"
                );

            percentage.textContent =
                `${probability.toFixed(2)}%`;

            info.appendChild(name);

            info.appendChild(
                percentage
            );

            const track =
                document.createElement(
                    "div"
                );

            track.className =
                "probability-track";

            const bar =
                document.createElement(
                    "div"
                );

            bar.className =
                "probability-bar";

            bar.style.width =
                `${probability}%`;

            track.appendChild(bar);

            item.appendChild(info);

            item.appendChild(
                track
            );

            probabilitiesList.appendChild(
                item
            );
        }
    );
}

function resetAnalysis() {
    imageInput.value = "";
    imagePreview.src = "";

    previewContainer.hidden = true;
    resultContainer.hidden = true;
    unsupportedWarning.hidden = true;

    lastPrediction = null;

    resetResultValues();

    document
        .getElementById("analysis")
        .scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
}

newAnalysisButton.addEventListener(
    "click",
    resetAnalysis
);

unsupportedNewImageButton.addEventListener(
    "click",
    resetAnalysis
);

function resetResultValues() {
    predictionName.textContent = "-";
    confidenceValue.textContent = "0%";
    confidenceBar.style.width = "0%";
    predictionStatus.textContent = "-";
    predictionStatus.className = "";
    recommendationText.textContent = "";
    probabilitiesList.innerHTML = "";
}

function refreshLocalHistoryAndStatistics() {
    lastHistory =
        getLocalHistory();

    displayHistory(
        lastHistory
    );

    displayStatistics(
        calculateStatistics(
            lastHistory
        )
    );
}

function displayHistory(history) {
    historyList.innerHTML = "";

    if (
        !Array.isArray(history) ||
        history.length === 0
    ) {
        const emptyMessage =
            document.createElement(
                "p"
            );

        emptyMessage.className =
            "empty-message";

        emptyMessage.textContent =
            translate(
                "history.empty"
            );

        historyList.appendChild(
            emptyMessage
        );

        return;
    }

    history.forEach(
        (item, index) => {
            const row =
                document.createElement(
                    "div"
                );

            row.className =
                "history-row";

            const information =
                diseaseInformation[
                    item.predicted_class
                ]?.[currentLanguage] || null;

            const readableName =
                information?.name ||
                item.predicted_class;

            const date =
                new Date(
                    item.created_at
                );

            const locale =
                currentLanguage === "sq"
                    ? "sq-AL"
                    : "en-GB";

            const formattedDate =
                Number.isNaN(
                    date.getTime()
                )
                    ? "-"
                    : date.toLocaleString(
                        locale,
                        {
                            day: "2-digit",
                            month: "2-digit",
                            year: "numeric",
                            hour: "2-digit",
                            minute: "2-digit"
                        }
                    );

            const confidence =
                Math.min(
                    Math.max(
                        Number(
                            item.confidence
                        ) || 0,
                        0
                    ),
                    100
                );

            const result =
                document.createElement(
                    "div"
                );

            result.className =
                "history-result";

            const number =
                document.createElement(
                    "span"
                );

            number.className =
                "history-number";

            number.textContent =
                `#${history.length - index}`;

            const resultName =
                document.createElement(
                    "strong"
                );

            resultName.textContent =
                readableName;

            result.appendChild(
                number
            );

            result.appendChild(
                resultName
            );

            const confidenceElement =
                document.createElement(
                    "div"
                );

            confidenceElement.className =
                "history-confidence";

            confidenceElement.textContent =
                `${confidence.toFixed(2)}%`;

            const dateElement =
                document.createElement(
                    "div"
                );

            dateElement.className =
                "history-date";

            dateElement.textContent =
                formattedDate;

            row.appendChild(
                result
            );

            row.appendChild(
                confidenceElement
            );

            row.appendChild(
                dateElement
            );

            historyList.appendChild(
                row
            );
        }
    );
}

function calculateStatistics(history) {
    const classes = {
        Black_Rot: 0,
        Esca: 0,
        Healthy: 0,
        Leaf_Blight: 0
    };

    history.forEach(item => {
        if (
            Object.prototype.hasOwnProperty.call(
                classes,
                item.predicted_class
            )
        ) {
            classes[
                item.predicted_class
            ] += 1;
        }
    });

    return {
        total_analyses:
            Object.values(classes)
                .reduce(
                    (sum, count) =>
                        sum + count,
                    0
                ),
        classes
    };
}

function displayStatistics(data) {
    const total =
        Number(
            data?.total_analyses
        ) || 0;

    const classes =
        data?.classes || {};

    const blackRot =
        Number(
            classes.Black_Rot
        ) || 0;

    const esca =
        Number(
            classes.Esca
        ) || 0;

    const healthy =
        Number(
            classes.Healthy
        ) || 0;

    const leafBlight =
        Number(
            classes.Leaf_Blight
        ) || 0;

    totalAnalyses.textContent =
        total;

    healthyCount.textContent =
        healthy;

    blackRotCount.textContent =
        blackRot;

    escaCount.textContent =
        esca;

    leafBlightCount.textContent =
        leafBlight;

    const calculatePercentage =
        value => {
            if (total <= 0) {
                return 0;
            }

            return Math.min(
                Math.max(
                    (value / total) *
                        100,
                    0
                ),
                100
            );
        };

    const blackRotPercentage =
        calculatePercentage(
            blackRot
        );

    const escaPercentage =
        calculatePercentage(
            esca
        );

    const healthyPercentage =
        calculatePercentage(
            healthy
        );

    const leafBlightPercentage =
        calculatePercentage(
            leafBlight
        );

    blackRotPercent.textContent =
        `${blackRotPercentage.toFixed(1)}%`;

    escaPercent.textContent =
        `${escaPercentage.toFixed(1)}%`;

    healthyPercent.textContent =
        `${healthyPercentage.toFixed(1)}%`;

    leafBlightPercent.textContent =
        `${leafBlightPercentage.toFixed(1)}%`;

    blackRotBar.style.width =
        `${blackRotPercentage}%`;

    escaBar.style.width =
        `${escaPercentage}%`;

    healthyBar.style.width =
        `${healthyPercentage}%`;

    leafBlightBar.style.width =
        `${leafBlightPercentage}%`;
}

applyLanguage(currentLanguage);
refreshLocalHistoryAndStatistics();

if (window.lucide) {
    window.lucide.createIcons();
}