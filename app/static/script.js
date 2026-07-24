const popup = document.getElementById("pop");

//Abrir POP-UP (Modal) de vendas
function abrirPopup(open) {
  if (open) popup.classList.add("opened");
  else popup.classList.remove("opened");
}

//Formatar valores floats do banco de dados em valores monetarios no front-end
const celulas = document.querySelectorAll(".moeda");
const formatar = new Intl.NumberFormat("pt-BR", {
    //Define a moeda utilizada
    style: "currency",
    currency: "BRL",
});
celulas.forEach((celula) => {
  const valor = parseFloat(celula.textContent);
  if (!isNaN(valor)) {
    celula.textContent = formatar.format(valor);
  }
});

const customData = `${day}/${month}/${year}`;


async function deletarRegistro(id) {
  const url = `/vendas/${id}`;

  try {
    const response = await fetch(url, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    if (response === 204) {
      console.log("Registro deletado!");
      window.location.reload();
      return;
    }

    const data = await response.json();
    window.location.reload();
    console.log("Registro deletado!", data);
  } catch (error) {
    // Captura erros de rede ou lançados manualmente acima
    console.error("Failed to delete resource:", error);
  }
}

const dateInput = document.getElementById("Data-Registro");
const formulario = document.getElementById("forms");

formulario.addEventListener("submit", function (evento) {
  evento.preventDefault();

  const dataSelecionada = new Date(dateInput.value);
  const hoje = new Date();
  const dataMinima = new Date();

  dataMinima.setFullYear(hoje.getFullYear() - 120);

  dateInput.setCustomValidity("");

  if (dataSelecionada > hoje) {
    dateInput.setCustomValidity("A data não pode ser no futuro.");
  } else if (dataSelecionada < dataMinima) {
    dateInput.setCustomValidity("Por favor, insira uma data válida.");
  }

  if (formulario.checkValidity()) {
    alert("Enviado!");
    formulario.submit();
  } else {
    formulario.reportValidity();
  }
});

const input = document.getElementById("valor");
const displayFormatted = document.getElementById("displayFormatted");
const displayNumeric = document.getElementById("displayNumeric");

// Formata um número (em centavos, inteiro) para o padrão monetário brasileiro
function formatFromCents(cents) {
  const value = cents / 100;
  return value.toLocaleString("pt-BR", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}

function onlyDigits(str) {
  return str.replace(/\D/g, "");
}

function updateDisplay(cents) {
  const numericValue = cents / 100;
  displayFormatted.textContent = "R$ " + formatFromCents(cents);
  displayNumeric.textContent = numericValue.toFixed(2);
}

input.addEventListener("input", (e) => {
  let digits = onlyDigits(e.target.value);

  // Remove zeros à esquerda desnecessários, mas mantém ao menos "0"
  digits = digits.replace(/^0+(?=\d)/, "");

  if (digits === "") {
    digits = "0";
  }

  const cents = parseInt(digits, 10);

  e.target.value = formatFromCents(cents);
  updateDisplay(cents);

  // Guarda o valor numérico no dataset, útil para pegar o valor via JS externamente
  e.target.dataset.rawValue = (cents / 100).toFixed(2);
});

input.value = formatFromCents(0);
updateDisplay(0);
input.dataset.rawValue = "0.00";

input.addEventListener("focus", () => {
  const val = input.value;
  input.setSelectionRange(val.length, val.length);
});


