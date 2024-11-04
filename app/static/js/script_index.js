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