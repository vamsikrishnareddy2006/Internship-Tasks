// DevPulse — small UX touches. No dark-mode toggle needed:
// this is a dark-only "terminal" identity by design.

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".field input").forEach((input) => {
        input.addEventListener("focus", () => {
            input.closest(".field").classList.add("is-active");
        });
        input.addEventListener("blur", () => {
            input.closest(".field").classList.remove("is-active");
        });
    });

    // Mobile nav toggle
    const navToggle = document.getElementById("navToggle");
    const navLinks = document.querySelector(".nav-links");
    if (navToggle && navLinks) {
        navToggle.addEventListener("click", () => {
            navLinks.classList.toggle("open");
        });
    }

    // Auto-dismiss flash messages after a few seconds
    document.querySelectorAll(".flash").forEach((el, i) => {
        setTimeout(() => {
            el.style.transition = "opacity 0.4s, transform 0.4s";
            el.style.opacity = "0";
            el.style.transform = "translateY(-6px)";
            setTimeout(() => el.remove(), 400);
        }, 5000 + i * 300);
    });
});
