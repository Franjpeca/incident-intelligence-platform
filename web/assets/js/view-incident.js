const searchBtn = document.getElementById("search-btn");
const loadBtn = document.getElementById("load-btn");

const incidentIdInput = document.getElementById("incident-id");

const searchFeedback = document.getElementById("search-feedback");
const searchResponse = document.getElementById("search-response");

const listFeedback = document.getElementById("list-feedback");
const incidentsList = document.getElementById("incidents-list");

function clearSearch() {
  searchFeedback.textContent = "";
  searchFeedback.className = "feedback";
  searchResponse.textContent = "";
}

function clearList() {
  listFeedback.textContent = "";
  listFeedback.className = "feedback";
  incidentsList.innerHTML = "";
}

function createCard(incident) {
  const card = document.createElement("div");
  card.className = "card";
  card.style.marginTop = "10px";

  card.innerHTML = `
    <h3>${incident.title || "Sin título"}</h3>
    <p><strong>ID:</strong> ${incident.id}</p>
    <p><strong>Descripcion:</strong> ${incident.description}</p>
    <p><strong>Estado:</strong> ${incident.status || "N/A"}</p>
  `;

  return card;
}

searchBtn.addEventListener("click", async () => {
  clearSearch();

  const id = incidentIdInput.value.trim();

  if (!id) {
    searchFeedback.textContent = "Introduce un ID valido";
    searchFeedback.classList.add("error");
    return;
  }

  try {
    const data = await apiRequest(`${CONFIG.API_BASE_URL}/incidents/${id}`, {
      method: "GET"
    });

    searchFeedback.textContent = "Incidencia encontrada";
    searchFeedback.classList.add("success");
    searchResponse.textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    searchFeedback.textContent = "Error al buscar incidencia";
    searchFeedback.classList.add("error");
    searchResponse.textContent = error.message;
  }
});

loadBtn.addEventListener("click", async () => {
  clearList();

  try {
    const data = await apiRequest(`${CONFIG.API_BASE_URL}/incidents`, {
      method: "GET"
    });

    if (!data.length) {
      listFeedback.textContent = "No hay incidencias";
      listFeedback.classList.add("error");
      return;
    }

    listFeedback.textContent = "Incidencias cargadas";
    listFeedback.classList.add("success");

    data.forEach(i => {
      incidentsList.appendChild(createCard(i));
    });

  } catch (error) {
    listFeedback.textContent = "Error al cargar incidencias";
    listFeedback.classList.add("error");
    incidentsList.textContent = error.message;
  }
});