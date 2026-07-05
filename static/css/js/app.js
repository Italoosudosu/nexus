/* ==========================================================================
   NEXUM — app.js
   Comportamento global do shell (sidebar + header), usado em todas as
   páginas autenticadas. Lógica específica de cada página fica em seu
   próprio arquivo (dashboard.js, clientes.js, etc.).
   ========================================================================== */

(function () {
  "use strict";

  const shell = document.querySelector(".app-shell");
  const toggleBtn = document.getElementById("sidebarToggle");
  const overlay = document.getElementById("sidebarOverlay");

  // Páginas sem sidebar (ex.: login) não possuem esses elementos.
  if (!shell || !toggleBtn || !overlay) {
    return;
  }

  function openSidebar() {
    shell.classList.add("sidebar-open");
    toggleBtn.setAttribute("aria-expanded", "true");
  }

  function closeSidebar() {
    shell.classList.remove("sidebar-open");
    toggleBtn.setAttribute("aria-expanded", "false");
  }

  function toggleSidebar() {
    if (shell.classList.contains("sidebar-open")) {
      closeSidebar();
    } else {
      openSidebar();
    }
  }

  toggleBtn.addEventListener("click", toggleSidebar);
  overlay.addEventListener("click", closeSidebar);

  // Fecha a gaveta automaticamente se a tela for redimensionada para desktop.
  window.addEventListener("resize", function () {
    if (window.innerWidth > 992) {
      closeSidebar();
    }
  });
})();
