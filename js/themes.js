/* BOKASAFN_THEME_SYSTEM */

const BOKASAFN_THEMES = [
    "light",
    "green",
    "dark",
    "purple",
    "orange"
];

function setBokasafnTheme(theme) {
    if (!BOKASAFN_THEMES.includes(theme)) {
        theme = "light";
    }

    document.body.dataset.theme = theme;

    localStorage.setItem("bokasafn-theme", theme);

    document.querySelectorAll(".theme-option").forEach(button => {
        button.classList.toggle(
            "active",
            button.dataset.theme === theme
        );
    });
}

function loadBokasafnTheme() {
    const saved =
        localStorage.getItem("bokasafn-theme") || "light";

    setBokasafnTheme(saved);
}

document.addEventListener("DOMContentLoaded", loadBokasafnTheme);
