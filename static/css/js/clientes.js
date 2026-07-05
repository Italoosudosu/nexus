/* ==========================================================================
   NEXUM — clientes.js
   Comportamento das páginas de Clientes (listagem e formulário).
   Sem regra de negócio: apenas UI + chamadas à API REST /api/clientes.
   ========================================================================== */

(function () {
  "use strict";

  /* ------------------------------------------------------------------------
     Listagem — busca em tempo real e exclusão
     ------------------------------------------------------------------------ */
  const searchInput = document.getElementById("buscaClientes");
  const tableBody = document.getElementById("clientesTableBody");

  function formatarStatus(status) {
    const label = status === "ativo" ? "Ativo" : "Inativo";
    return `<span class="status-badge status-badge--${status}">${label}</span>`;
  }

  function linhaCliente(cliente) {
    const cidade = cliente.endereco
      ? [cliente.endereco.cidade, cliente.endereco.estado].filter(Boolean).join("/")
      : "—";

    return `
      <tr data-id="${cliente.id}">
        <td>${cliente.nome}</td>
        <td class="is-muted">${cliente.cpf}</td>
        <td class="is-muted">${cliente.telefone || "—"}</td>
        <td class="is-muted">${cidade}</td>
        <td>${formatarStatus(cliente.status)}</td>
        <td>
          <div class="row-actions">
            <a class="row-action-btn" href="/clientes/${cliente.id}/editar" aria-label="Editar">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <path d="M4 20h4l10-10-4-4L4 16v4Z"/>
              </svg>
            </a>
            <button class="row-action-btn row-action-btn--danger" data-action="excluir" data-id="${cliente.id}" aria-label="Excluir">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <path d="M5 7h14M9 7V5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2m-8 0 1 12a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1l1-12"/>
              </svg>
            </button>
          </div>
        </td>
      </tr>`;
  }

  function renderTabela(clientes) {
    if (!clientes.length) {
      tableBody.innerHTML =
        '<tr class="data-table__empty"><td colspan="6">Nenhum cliente encontrado.</td></tr>';
      return;
    }
    tableBody.innerHTML = clientes.map(linhaCliente).join("");
  }

  let debounceTimer = null;

  async function buscarClientes(termo) {
    const url = termo ? `/api/clientes?busca=${encodeURIComponent(termo)}` : "/api/clientes";
    const response = await fetch(url);
    const clientes = await response.json();
    renderTabela(clientes);
  }

  async function excluirCliente(id, linha) {
    const confirmado = window.confirm("Tem certeza que deseja excluir este cliente?");
    if (!confirmado) return;

    const response = await fetch(`/api/clientes/${id}`, { method: "DELETE" });

    if (response.status === 204) {
      linha.remove();
      if (!tableBody.querySelector("tr")) {
        renderTabela([]);
      }
    } else {
      window.alert("Não foi possível excluir o cliente.");
    }
  }

  if (searchInput && tableBody) {
    searchInput.addEventListener("input", function () {
      clearTimeout(debounceTimer);
      const termo = searchInput.value.trim();
      debounceTimer = setTimeout(() => buscarClientes(termo), 300);
    });

    tableBody.addEventListener("click", function (event) {
      const btn = event.target.closest('[data-action="excluir"]');
      if (!btn) return;
      const linha = btn.closest("tr");
      excluirCliente(btn.dataset.id, linha);
    });
  }

  /* ------------------------------------------------------------------------
     Formulário — cadastro e edição
     ------------------------------------------------------------------------ */
  const form = document.getElementById("clienteForm");

  if (form) {
    const errorBox = document.getElementById("clienteFormError");
    const submitBtn = document.getElementById("clienteFormSubmit");

    function showError(message) {
      errorBox.textContent = message;
      errorBox.classList.add("visible");
    }

    function hideError() {
      errorBox.classList.remove("visible");
      errorBox.textContent = "";
    }

    function setLoading(isLoading) {
      submitBtn.disabled = isLoading;
      submitBtn.classList.toggle("is-loading", isLoading);
    }

    async function handleSubmit(event) {
      event.preventDefault();
      hideError();
      setLoading(true);

      const modo = form.dataset.modo;
      const clienteId = form.dataset.clienteId;

      const payload = {
        nome: document.getElementById("nome").value.trim(),
        cpf: document.getElementById("cpf").value.trim(),
        telefone: document.getElementById("telefone").value.trim(),
        email: document.getElementById("email").value.trim(),
        data_nascimento: document.getElementById("data_nascimento").value || null,
        status: document.getElementById("status").value,
        endereco: {
          cep: document.getElementById("cep").value.trim(),
          logradouro: document.getElementById("logradouro").value.trim(),
          numero: document.getElementById("numero").value.trim(),
          complemento: document.getElementById("complemento").value.trim(),
          bairro: document.getElementById("bairro").value.trim(),
          cidade: document.getElementById("cidade").value.trim(),
          estado: document.getElementById("estado").value.trim(),
        },
      };

      const url = modo === "editar" ? `/api/clientes/${clienteId}` : "/api/clientes";
      const method = modo === "editar" ? "PUT" : "POST";

      try {
        const response = await fetch(url, {
          method,
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
          showError(data.mensagem || "Não foi possível salvar o cliente.");
          setLoading(false);
          return;
        }

        window.location.href = "/clientes";
      } catch (err) {
        showError("Não foi possível conectar ao servidor. Tente novamente.");
        setLoading(false);
      }
    }

    form.addEventListener("submit", handleSubmit);
  }
})();
