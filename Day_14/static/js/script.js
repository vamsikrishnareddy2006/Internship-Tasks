const toggleBtn = document.getElementById("theme-toggle");
const root = document.documentElement;

function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    toggleBtn.textContent = theme === "dark" ? "☀️" : "🌙";
}

const saved = localStorage.getItem("devpulse-theme") || "light";
applyTheme(saved);

toggleBtn.addEventListener("click", () => {
    const current = root.getAttribute("data-theme");
    const next = current === "dark" ? "light" : "dark";
    localStorage.setItem("devpulse-theme", next);
    applyTheme(next);
});
