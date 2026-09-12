"use strict";

document.addEventListener("DOMContentLoaded", () => {
  const root = document.documentElement;
  const themeToggle = document.getElementById("theme-toggle");
  const navbar = document.getElementById("navbar");
  const storageKey = "theme";

  const updateThemeToggle = (theme) => {
    if (!themeToggle) return;
    themeToggle.textContent = theme === "dark" ? "☀️ Light" : "🌙 Dark";
    themeToggle.setAttribute(
      "aria-label",
      theme === "dark" ? "Switch to light theme" : "Switch to dark theme",
    );
  };

  const applyTheme = (theme) => {
    const nextTheme = theme === "light" ? "light" : "dark";
    root.setAttribute("data-theme", nextTheme);
    updateThemeToggle(nextTheme);
    try {
      localStorage.setItem(storageKey, nextTheme);
    } catch (_error) {
      // Ignore storage access errors (private mode / blocked storage)
    }
  };

  let savedTheme = null;
  try {
    savedTheme = localStorage.getItem(storageKey);
  } catch (_error) {
    savedTheme = null;
  }

  const initialTheme = savedTheme || root.getAttribute("data-theme") || "dark";
  applyTheme(initialTheme);

  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      const currentTheme = root.getAttribute("data-theme") || "dark";
      const nextTheme = currentTheme === "dark" ? "light" : "dark";
      applyTheme(nextTheme);
      if (typeof window.reRenderCanvasCharts === "function") {
        window.reRenderCanvasCharts();
      }
    });
  }

  if (navbar) {
    const updateNavbarScrollState = () => {
      navbar.classList.toggle("scrolled", window.scrollY > 50);
    };
    updateNavbarScrollState();
    window.addEventListener("scroll", updateNavbarScrollState, { passive: true });
  }
});
