/* ==========================================================================
   NEXUM — login.js
   Comportamento da tela de autenticação.
   Sem regra de negócio: apenas UI + chamada à API de autenticação.
   ========================================================================== */

(function () {
  "use strict";

  const form = document.getElementById("loginForm");
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("senha");
  const togglePasswordBtn = document.getElementById("togglePassword");
  const submitBtn = document.getElementById("loginSubmit");
  const errorBox = document.getElementById("loginError");

  /**
   * Alterna a visibilidade do campo de senha.
   */
  function togglePasswordVisibility() {
    const isHidden = passwordInput.type === "password";
    passwordInput.type = isHidden ? "text" : "password";
    togglePasswordBtn.setAttribute(
      "aria-label",
      isHidden ? "Ocultar senha" : "Mostrar senha",
    );
    togglePasswordBtn.classList.toggle("is-visible", isHidden);
  }

  /**
   * Exibe uma mensagem de erro no formulário.
   * @param {string} message
   */
  function showError(message) {
    errorBox.textContent = message;
    errorBox.classList.add("visible");
  }

  function hideError() {
    errorBox.classList.remove("visible");
    errorBox.textContent = "";
  }

  /**
   * Alterna o estado de carregamento do botão de envio.
   * @param {boolean} isLoading
   */
  function setLoading(isLoading) {
    submitBtn.disabled = isLoading;
    submitBtn.classList.toggle("is-loading", isLoading);
  }

  /**
   * Validação simples de e-mail no client-side.
   * A validação definitiva sempre acontece no backend (Flask).
   * @param {string} value
   */
  function isValidEmail(value) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
  }

  async function handleSubmit(event) {
    event.preventDefault();
    hideError();

    const email = emailInput.value.trim();
    const senha = passwordInput.value;
    const lembrar = document.getElementById("lembrar").checked;

    if (!email || !isValidEmail(email)) {
      showError("Informe um e-mail válido.");
      emailInput.focus();
      return;
    }

    if (!senha) {
      showError("Informe sua senha.");
      passwordInput.focus();
      return;
    }

    setLoading(true);

    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, senha, lembrar }),
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        showError(data.mensagem || "E-mail ou senha inválidos.");
        setLoading(false);
        return;
      }

      window.location.href = data.redirect || "/dashboard";
    } catch (err) {
      showError("Não foi possível conectar ao servidor. Tente novamente.");
      setLoading(false);
    }
  }

  form.addEventListener("submit", handleSubmit);
  togglePasswordBtn.addEventListener("click", togglePasswordVisibility);
})();
