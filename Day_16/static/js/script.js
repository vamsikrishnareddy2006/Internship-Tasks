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
});
