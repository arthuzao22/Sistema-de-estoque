const qtdeElements = document.getElementsByClassName('qtde');

for (let i = 0; i < qtdeElements.length; i++) {
    console.log(qtdeElements[i].value); // Exemplo: imprime o valor de cada elemento
}

        // Função para abrir/fechar o menu lateral no mobile
        const menuToggle = document.getElementById('menuToggle');
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('overlay');

        menuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('show');
            overlay.classList.toggle('show');
        });

        overlay.addEventListener('click', () => {
            sidebar.classList.remove('show');
            overlay.classList.remove('show');
        });