const form = document.getElementById("create-form");
const feedback = document.getElementById("feedback");
const responseBox = document.getElementById("response");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  feedback.textContent = "";
  responseBox.textContent = "";

  const payload = {
  title: document.getElementById("title").value,
  description: document.getElementById("description").value
  };

  try {
    const data = await apiRequest(`${CONFIG.API_BASE_URL}/incidents`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    feedback.textContent = "Incidencia creada correctamente";
    responseBox.textContent = JSON.stringify(data, null, 2);

    form.reset();
  } catch (error) {
    feedback.textContent = "Error al crear incidencia";
    responseBox.textContent = error.message;
  }
});