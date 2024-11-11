  // Função para exibir o spinner ao enviar o formulário
  function showLoadingSpinner() {
    document.getElementById('loading-spinner').style.display = 'block';
    document.querySelector('.card').style.display = 'none';  // Esconde o card de login
    document.querySelector('button[type="submit"]').disabled = true;  // Desabilita o botão de submit
}