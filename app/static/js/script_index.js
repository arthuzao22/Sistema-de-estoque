function confirmarExclusao(itemId) {
    // Defina a senha fixa
    const senhaCorreta = "cdg12345";  // Altere para a senha desejada
    const senhaUsuario = prompt("Digite a senha para confirmar a exclusão:");

    // Verifica se a senha está correta
    if (senhaUsuario === senhaCorreta) {
        // Redireciona para o link de exclusão se a senha estiver correta
        window.location.href = `delete/${itemId}`;
    } else {
        // Mensagem de senha incorreta
        alert("Senha incorreta. A exclusão foi cancelada.");
    }
}

document.querySelectorAll('#qtde_alert').forEach(td => {
    if (td.innerText == "0") { // Verifica se o conteúdo do td é "0"
        td.style.background = '#FF6666'; // Altera o background para vermelho
    }
});

document.querySelectorAll('#entrada_saida_alert').forEach(td => {
    if (td.innerText == "Saida") { // Verifica se o conteúdo do td é "0"
        td.style.background = '#ff666665'; // Altera o background para vermelho
    }
});

document.querySelectorAll('#entrada_saida_alert').forEach(td => {
    if (td.innerText == "Entrada") { // Verifica se o conteúdo do td é "0"
        td.style.background = 'rgba(153, 255, 0, 0.197)'; // Altera o background para vermelho
    }
});

const formatter = new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
});

document.querySelectorAll("td[id^='data-']").forEach(td => {
    const rawDate = td.textContent.trim();
    const date = new Date(rawDate);
    if (!isNaN(date)) {
        td.textContent = formatter.format(date);
    }
});

// Função para abrir/fechar o menu lateral no mobile
const menuToggle = document.getElementById('menuToggle');
const sidebar = document.getElementById('sidebar');
const overlay = document.getElementById('overlay')
menuToggle.addEventListener('click', () => {
    sidebar.classList.toggle('show');
    overlay.classList.toggle('show');
})
overlay.addEventListener('click', () => {
    sidebar.classList.remove('show');
    overlay.classList.remove('show');
});