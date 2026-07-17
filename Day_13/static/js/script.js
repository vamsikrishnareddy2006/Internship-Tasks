document.addEventListener("DOMContentLoaded", function () {
    // Mobile nav toggle
    const navToggle = document.getElementById("navToggle");
    const navLinks = document.getElementById("navLinks");
    if (navToggle && navLinks) {
        navToggle.addEventListener("click", function () {
            navLinks.classList.toggle("open");
        });
    }

    // Dark mode toggle
    const darkToggle = document.getElementById("darkModeToggle");
    const root = document.documentElement;

    const savedTheme = localStorageSafeGet("theme");
    if (savedTheme === "dark") {
        root.setAttribute("data-theme", "dark");
        if (darkToggle) darkToggle.textContent = "☀️";
    }

    if (darkToggle) {
        darkToggle.addEventListener("click", function () {
            const isDark = root.getAttribute("data-theme") === "dark";
            if (isDark) {
                root.removeAttribute("data-theme");
                darkToggle.textContent = "🌙";
                localStorageSafeSet("theme", "light");
            } else {
                root.setAttribute("data-theme", "dark");
                darkToggle.textContent = "☀️";
                localStorageSafeSet("theme", "dark");
            }
        });
    }
});

// Wrap localStorage access safely (works fine in a real browser deployment)
function localStorageSafeGet(key) {
    try {
        return window.localStorage.getItem(key);
    } catch (e) {
        return null;
    }
}

function localStorageSafeSet(key, value) {
    try {
        window.localStorage.setItem(key, value);
    } catch (e) {
        /* no-op if storage unavailable */
    }
}
