const incidentAnalysisForm = document.getElementById("incident-analysis-form");
const getIncidentAnalysisForm = document.getElementById("get-incident-analysis-form");
const useModelForm = document.getElementById("use-model-form");

const incidentAnalysisFeedback = document.getElementById("incident-analysis-feedback");
const incidentAnalysisResponse = document.getElementById("incident-analysis-response");

const getIncidentAnalysisFeedback = document.getElementById("get-incident-analysis-feedback");
const getIncidentAnalysisResponse = document.getElementById("get-incident-analysis-response");

const useModelFeedback = document.getElementById("use-model-feedback");
const useModelResponse = document.getElementById("use-model-response");

function clearIncidentAnalysis() {
  incidentAnalysisFeedback.textContent = "";
  incidentAnalysisFeedback.className = "feedback";
  incidentAnalysisResponse.textContent = "";
}

function clearGetIncidentAnalysis() {
  getIncidentAnalysisFeedback.textContent = "";
  getIncidentAnalysisFeedback.className = "feedback";
  getIncidentAnalysisResponse.textContent = "";
}

function clearUseModel() {
  useModelFeedback.textContent = "";
  useModelFeedback.className = "feedback";
  useModelResponse.textContent = "";
}

incidentAnalysisForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  clearIncidentAnalysis();

  const id = document.getElementById("incident-analysis-id").value.trim();

  try {
    const data = await apiRequest(`${CONFIG.API_BASE_URL}/incidents/${id}/analysis`, {
      method: "POST"
    });

    incidentAnalysisFeedback.textContent = "Analisis lanzado correctamente";
    incidentAnalysisFeedback.classList.add("success");
    incidentAnalysisResponse.textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    incidentAnalysisFeedback.textContent = "Error al analizar la incidencia";
    incidentAnalysisFeedback.classList.add("error");
    incidentAnalysisResponse.textContent = error.message;
  }
});

getIncidentAnalysisForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  clearGetIncidentAnalysis();

  const id = document.getElementById("get-incident-analysis-id").value.trim();

  try {
    const data = await apiRequest(`${CONFIG.API_BASE_URL}/incidents/${id}/analysis`, {
      method: "GET"
    });

    getIncidentAnalysisFeedback.textContent = "Analisis obtenido correctamente";
    getIncidentAnalysisFeedback.classList.add("success");
    getIncidentAnalysisResponse.textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    getIncidentAnalysisFeedback.textContent = "Error al obtener el analisis";
    getIncidentAnalysisFeedback.classList.add("error");
    getIncidentAnalysisResponse.textContent = error.message;
  }
});

useModelForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  clearUseModel();

  const text = document.getElementById("model-text").value.trim();
  const analysisType = document.getElementById("analysis-type").value.trim();

  const payload = {
    text: text
  };

  if (analysisType) {
    payload.analysis_type = analysisType;
  }

  try {
    const data = await apiRequest(`${CONFIG.LLM_API_BASE_URL}/analysis/text`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    useModelFeedback.textContent = "Texto analizado correctamente";
    useModelFeedback.classList.add("success");
    useModelResponse.textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    useModelFeedback.textContent = "Error al usar el modelo";
    useModelFeedback.classList.add("error");
    useModelResponse.textContent = error.message;
  }
});