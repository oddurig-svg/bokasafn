(() => {
    function applySystemTheme() {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        document.body.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
    }

    applySystemTheme();

    const themeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    themeMediaQuery.addEventListener('change', applySystemTheme);
})();
