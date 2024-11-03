document.querySelectorAll('#qtde_alert').forEach(td => {
    if (td.innerText == "0") { // Verifica se o conteúdo do td é "0"
        td.style.background = 'red'; // Altera o background para vermelho
    }
});