// SSOT Domain: ui
const apiBase = "http://localhost:8080";

const repoPath = document.getElementById("repoPath");
const openRepo = document.getElementById("openRepo");
const repoStatus = document.getElementById("repoStatus");
const agentsInput = document.getElementById("agentsInput");
const saveAgents = document.getElementById("saveAgents");
const agentsStatus = document.getElementById("agentsStatus");
const taskPrompt = document.getElementById("taskPrompt");
const runTask = document.getElementById("runTask");
const taskStatus = document.getElementById("taskStatus");
const refreshRuns = document.getElementById("refreshRuns");
const runsList = document.getElementById("runsList");
const runDetail = document.getElementById("runDetail");
const apiStatus = document.getElementById("apiStatus");

const showStatus = (node, payload) => {
  node.textContent = JSON.stringify(payload, null, 2);
};

const apiRequest = async (path, options = {}) => {
  const response = await fetch(`${apiBase}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Request failed");
  }
  return response.json();
};

const updateApiStatus = async () => {
  try {
    const payload = await apiRequest("/health");
    apiStatus.textContent = `API online • ${payload.time}`;
  } catch (error) {
    apiStatus.textContent = "API not connected";
  }
};

openRepo.addEventListener("click", async () => {
  try {
    repoStatus.textContent = "Opening repo...";
    const payload = await apiRequest("/open_repo_path", {
      method: "POST",
      body: JSON.stringify({ path: repoPath.value.trim() }),
    });
    showStatus(repoStatus, payload);
  } catch (error) {
    repoStatus.textContent = error.message;
  }
});

saveAgents.addEventListener("click", async () => {
  try {
    agentsStatus.textContent = "Saving agents...";
    const agents = JSON.parse(agentsInput.value);
    const payload = await apiRequest("/agents", {
      method: "POST",
      body: JSON.stringify({ agents }),
    });
    showStatus(agentsStatus, payload);
  } catch (error) {
    agentsStatus.textContent = error.message;
  }
});

runTask.addEventListener("click", async () => {
  try {
    taskStatus.textContent = "Dispatching task...";
    const payload = await apiRequest("/tasks/run", {
      method: "POST",
      body: JSON.stringify({ prompt: taskPrompt.value }),
    });
    showStatus(taskStatus, payload);
  } catch (error) {
    taskStatus.textContent = error.message;
  }
});

refreshRuns.addEventListener("click", async () => {
  try {
    runDetail.textContent = "Loading runs...";
    const payload = await apiRequest("/runs");
    runsList.innerHTML = "";
    payload.runs.forEach((runId) => {
      const item = document.createElement("li");
      const button = document.createElement("button");
      button.textContent = runId;
      button.addEventListener("click", async () => {
        runDetail.textContent = "Loading run...";
        const run = await apiRequest(`/runs/${runId}`);
        runDetail.textContent = JSON.stringify(run, null, 2);
      });
      item.appendChild(button);
      runsList.appendChild(item);
    });
  } catch (error) {
    runDetail.textContent = error.message;
  }
});

updateApiStatus();
setInterval(updateApiStatus, 10000);
