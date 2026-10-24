const DATA_URL = "resources.json";

const listElement = document.getElementById("resource-list");
const template = document.getElementById("resource-card-template");
const formTemplate = document.getElementById("resource-form-template");
const menuButton = document.getElementById("menu-button");
const menuElement = document.getElementById("menu");
const importButton = document.getElementById("import-button");
const importInput = document.getElementById("import-input");
const exportButton = document.getElementById("export-button");
const statusElement = document.getElementById("status");

let resources = [];
let statusTimeout;

function setMenuOpen(open) {
  menuElement.classList.toggle("hidden", !open);
  menuButton.setAttribute("aria-expanded", String(open));
}

function closeMenu() {
  setMenuOpen(false);
}

function setStatus(message, type = "success") {
  clearTimeout(statusTimeout);
  statusElement.textContent = message;
  statusElement.className = "mt-4 rounded-lg px-4 py-3 text-sm " + (
    type === "error"
      ? "bg-rose-50 text-rose-700 ring-1 ring-rose-100"
      : "bg-emerald-50 text-emerald-700 ring-1 ring-emerald-100"
  );

  if (type === "success") {
    statusTimeout = setTimeout(() => {
      statusElement.classList.add("hidden");
    }, 5000);
  }
}

function normalizeResources(raw) {
  if (!Array.isArray(raw)) {
    throw new Error("Die JSON-Datei muss ein Array von Ressourcen enthalten.");
  }

  return raw.map((item, index) => {
    if (!item || typeof item !== "object" || Array.isArray(item)) {
      throw new Error(`Eintrag ${index + 1} ist kein gültiges Objekt.`);
    }

    const title = String(item.title ?? "").trim();
    const url = String(item.url ?? "").trim();

    if (!title) {
      throw new Error(`Eintrag ${index + 1}: Das Feld "title" fehlt.`);
    }

    let parsedUrl;
    try {
      parsedUrl = new URL(url, window.location.href);
    } catch {
      throw new Error(`Eintrag ${index + 1}: Die URL ist ungültig.`);
    }

    if (parsedUrl.protocol !== "http:" && parsedUrl.protocol !== "https:") {
      throw new Error(`Eintrag ${index + 1}: Nur HTTP- und HTTPS-Links sind erlaubt.`);
    }

    return {
      title,
      url: parsedUrl.href,
      description: String(item.description ?? "").trim(),
    };
  });
}

function createResourceCard(resource) {
  const card = template.content.firstElementChild.cloneNode(true);
  const description = card.querySelector("[data-description]");

  card.href = resource.url;
  card.querySelector("[data-title]").textContent = resource.title;

  if (resource.description) {
    description.textContent = resource.description;
  } else {
    description.remove();
  }

  return card;
}

function createResourceFormCard() {
  const form = formTemplate.content.firstElementChild.cloneNode(true);

  form.addEventListener("submit", (event) => {
    event.preventDefault();

    try {
      const formData = new FormData(form);
      const [resource] = normalizeResources([{
        title: formData.get("title"),
        url: formData.get("url"),
        description: formData.get("description"),
      }]);

      resources.push(resource);
      renderResources();
      setStatus("Ressource wurde hinzugefügt.");
    } catch (error) {
      setStatus(error.message, "error");
    }
  });

  return form;
}

function renderResources() {
  listElement.replaceChildren();

  if (resources.length === 0) {
    const empty = document.createElement("p");
    empty.className = "text-slate-500";
    empty.textContent = "Keine Ressourcen vorhanden.";
    listElement.append(empty);
  } else {
    resources.forEach((resource) => {
      listElement.append(createResourceCard(resource));
    });
  }

  listElement.append(createResourceFormCard());
}

async function loadDefaultResources() {
  const response = await fetch(DATA_URL, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Ressourcen konnten nicht geladen werden (HTTP ${response.status}).`);
  }
  return normalizeResources(await response.json());
}

function exportResources() {
  const blob = new Blob([JSON.stringify(resources, null, 2) + "\n"], {
    type: "application/json"
  });
  const downloadUrl = URL.createObjectURL(blob);
  const link = document.createElement("a");

  link.href = downloadUrl;
  link.download = "resources.json";
  document.body.append(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(downloadUrl);

  setStatus("Ressourcenliste wurde exportiert.");
}

async function importResources(file) {
  const raw = JSON.parse(await file.text());
  resources = normalizeResources(raw);
  renderResources();
  setStatus(`"${file.name}" wurde importiert.`);
}

async function init() {
  try {
    resources = await loadDefaultResources();
    renderResources();
  } catch (error) {
    setStatus(error.message, "error");
    listElement.replaceChildren();
  }
}

menuButton.addEventListener("click", () => {
  setMenuOpen(menuElement.classList.contains("hidden"));
});

document.addEventListener("click", (event) => {
  if (!menuElement.contains(event.target) && !menuButton.contains(event.target)) {
    closeMenu();
  }
});

importButton.addEventListener("click", () => {
  closeMenu();
  importInput.click();
});

importInput.addEventListener("change", async () => {
  const [file] = importInput.files;
  importInput.value = "";

  if (!file) {
    return;
  }

  try {
    await importResources(file);
  } catch (error) {
    const message = error instanceof SyntaxError
      ? "Die Datei enthält kein gültiges JSON."
      : error.message;
    setStatus(message, "error");
  }
});

exportButton.addEventListener("click", () => {
  closeMenu();
  exportResources();
});

init();
