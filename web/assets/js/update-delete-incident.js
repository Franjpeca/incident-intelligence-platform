const updateForm = document.getElementById("update-form");
const statusForm = document.getElementById("status-form");
const deleteForm = document.getElementById("delete-form");

const updateFeedback = document.getElementById("update-feedback");
const updateResponse = document.getElementById("update-response");

const statusFeedback = document.getElementById("status-feedback");
const statusResponse = document.getElementById("status-response");

const deleteFeedback = document.getElementById("delete-feedback");
const deleteResponse = document.getElementById("delete-response");

function clearUpdate() {
  updateFeedback.textContent = "";
  updateFeedback.className = "feedback";
  updateResponse.textContent = "";
}

function clearStatus() {
  statusFeedback.textContent = "";
  statusFeedback.className = "feedback";
  statusResponse.textContent = "";
}

function clearDelete() {
  deleteFeedback.textContent = "";
  deleteFeedback.className = "feedback";
  deleteResponse.textContent = "";
}

updateForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  clearUpdate();

  const id = document.getElementById("update-id").value.trim();
  const title = document.getElementById("update-title").value.trim();
  const description = document.getElementById("update-description").value.trim();
  const status = document.getElementById("update-status").value;

  const payload = {};

  if (title) payload.title = title;
  if (description) payload.description = description;
  if (status) payload.status = status;

  if (Object.keys(payload).length === 0) {
    updateFeedback.textContent = "Debes rellenar al menos un campo";
    updateFeedback.classList.add("error");
    return;
  }

  try {
    const data = await apiRequest(`${CONFIG.API_BASE_URL}/incidents/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    updateFeedback.textContent = "Incidencia actualizada correctamente";
    updateFeedback.classList.add("success");
    updateResponse.textContent = JSON.stringify(data, null, 2);

  } catch (error) {
    updateFeedback.textContent = "Error al actualizar incidencia";
    updateFeedback.classList.add("error");
    updateResponse.textContent = error.message;
  }
});

statusForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  clearStatus();

  const id = document.getElementById("status-id").value.trim();
  const status = document.getElementById("status-only").value;

  const payload = {
    status: status
  };

  try {
    const data = await apiRequest(`${CONFIG.API_BASE_URL}/incidents/${id}/status`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    statusFeedback.textContent = "Estado actualizado correctamente";
    statusFeedback.classList.add("success");
    statusResponse.textContent = JSON.stringify(data, null, 2);

  } catch (error) {
    statusFeedback.textContent = "Error al actualizar estado";
    statusFeedback.classList.add("error");
    statusResponse.textContent = error.message;
  }
});

deleteForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  clearDelete();

  const id = document.getElementById("delete-id").value.trim();

  try {
    const data = await apiRequest(`${CONFIG.API_BASE_URL}/incidents/${id}`, {
      method: "DELETE"
    });

    deleteFeedback.textContent = "Incidencia borrada correctamente";
    deleteFeedback.classList.add("success");
    deleteResponse.textContent = JSON.stringify(data, null, 2);

  } catch (error) {
    deleteFeedback.textContent = "Error al borrar incidencia";
    deleteFeedback.classList.add("error");
    deleteResponse.textContent = error.message;
  }
});