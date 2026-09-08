function toggleAppearancePanel() {
    const panel = document.getElementById("appearance-panel");

    if (!panel) return;

    panel.classList.toggle("hidden");
}
