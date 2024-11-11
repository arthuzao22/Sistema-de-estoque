  // Função para exibir o spinner ao enviar o formulário
  function showLoadingSpinner() {
    document.getElementById('loading-spinner').style.display = 'block';
    document.querySelector('.card').style.display = 'none';  // Esconde o card de login
    document.querySelector('button[type="submit"]').disabled = true;  // Desabilita o botão de submit
}


function atualizaTipo() {
    // Captura os elementos "formato" e "tipo"
    var formato = document.getElementById("formato").value;
    var tipo = document.getElementById("tipo");

    // Limpa as opções existentes no campo "tipo"
    tipo.innerHTML = '<option value="">Selecione um tipo</option>';

    // Adiciona as opções de acordo com o valor selecionado em "formato"
    if (formato === "Impressão") {
        tipo.innerHTML += '<option value="Placas">Placas</option>';
        tipo.innerHTML += '<option value="Cx">Cx</option>';
    } else if (formato === "Acabamento") {
        tipo.innerHTML += '<option value="Cx">Cx</option>';
        tipo.innerHTML += '<option value="Unidade">Unidade</option>';
        tipo.innerHTML += '<option value="Pacotes">Pacotes</option>';
    } else if (formato === "TintaTonner") {
        tipo.innerHTML += '<option value="Unidade">Unidade</option>';
    }
}


function checkConnection() {
    inicial = document.getElementById('inicial')
    if (!navigator.onLine) {
        inicial.display.none
        alert("Sem conexão com a Internet. Verifique sua conexão e tente novamente.");
    }
}

// Verifica a conexão ao carregar a página e ao alterar o status da conexão
window.addEventListener('load', checkConnection);
window.addEventListener('offline', checkConnection);

function checkConnection() {
    if (!navigator.onLine) {
        alert("Sem conexão com a Internet. Verifique sua conexão e tente novamente.");
    }
}

// Verifica a conexão ao carregar a página e ao alterar o status da conexão
window.addEventListener('load', checkConnection);
window.addEventListener('offline', checkConnection);

function toggleEspecificacoes(tipo) {
    const especificacoes = document.getElementById('especificacoes');
    if (tipo === "Placas") {
        especificacoes.classList.remove('hidden');
    } else {
        especificacoes.classList.add('hidden');
        document.getElementById('folha').value = 'null'; // Limpa o campo se não for "Placas"
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const tipo = document.getElementById('tipo').value;
    toggleEspecificacoes(tipo);
});

// Chama a função no carregamento para definir o estado inicial
document.addEventListener('DOMContentLoaded', () => {
    const tipo = document.getElementById('tipo').value;
    toggleEspecificacoes(tipo);
});

const subcategorias = {
    Acabamento: [
        'ESPIRAL BRANCO 9 MM', 'ESPIRAL BRANCO 12 MM', 'ESPIRAL BRANCO 14 MM', 'ESPIRAL BRANCO 17 MM', 'ESPIRAL BRANCO 20 MM',
        'ESPIRAL BRANCO 23 MM', 'ESPIRAL BRANCO 25 MM', 'ESPIRAL BRANCO 29 MM', 'ESPIRAL BRANCO 33 MM', 'ESPIRAL BRANCO 40 MM',
        'ESPIRAL BRANCO 45 MM', 'ESPIRAL BRANCO 50 MM', 'ESPIRAL INCOLOR 9 MM', 'ESPIRAL INCOLOR 12 MM', 'ESPIRAL INCOLOR 14 MM',
        'ESPIRAL INCOLOR 17 MM', 'ESPIRAL INCOLOR 20 MM', 'ESPIRAL INCOLOR 23 MM', 'ESPIRAL INCOLOR 25 MM', 'ESPIRAL INCOLOR 29 MM',
        'ESPIRAL INCOLOR 33 MM', 'ESPIRAL INCOLOR 40 MM', 'ESPIRAL INCOLOR 45 MM', 'ESPIRAL INCOLOR 50 MM', 'ESPIRAL PRETO 9 MM',
        'ESPIRAL PRETO 12 MM', 'ESPIRAL PRETO 14 MM', 'ESPIRAL PRETO 17 MM', 'ESPIRAL PRETO 20 MM', 'ESPIRAL PRETO 23 MM',
        'ESPIRAL PRETO 25 MM', 'ESPIRAL PRETO 29 MM', 'ESPIRAL PRETO 33 MM', 'ESPIRAL PRETO 40 MM', 'ESPIRAL PRETO 45 MM',
        'ESPIRAL PRETO 50 MM', 'WIRE-O BRANCO (1/2)', 'WIRE-O BRANCO (1-1/4)', 'WIRE-O BRANCO (3/4)', 'WIRE-O PRETO (1/2)',
        'WIRE-O PRETO (1-1/4)', 'WIRE-O PRETO (3/4)', 'BOBINA DE LAMINAÇÃO BRILHO (MAIOR)', 'BOBINA DE LAMINAÇÃO BRILHO (MENOR)',
        'BOBINA DE LAMINAÇÃO FOSCO', 'BOBINA DE LAMINAÇÃO HOLOGRAFICA', 'BOBINA PLASTICA (SHIRINK)', 'BOBINA PLASTICA A3 (ENSACAMENTO)',
        'BOBINA PLASTICA A4 (ENSACAMENTO)', 'CAPA PLASTICA INCOLOR', 'CONTRA CAPA PLASTICA AZUL', 'CONTRA CAPA PLASTICA PRETO',
        'GRAMPEADOR', 'GRAMPO', 'CX 2 - 20', 'CX 2 - 25'
    ],
    Impressão: [
        'A4 OFFSSET 120g', 'A3 OFFSSET 120g', 'A4 OFFSSET 180g', 'A3 OFFSSET 180g', 
        'A4 COUCHÊ 90g', 'A3 COUCHÊ 90g', 'A4 COUCHÊ 115g', 'A3 COUCHÊ 115g', 
        'A4 COUCHÊ 170g', 'A3 COUCHÊ 170g', 'A4 COUCHÊ 240g', 'A3 COUCHÊ 240g', 
        'A4 COUCHÊ 250g', 'A3 COUCHÊ 250g', 'A3 Adesivo Colacril 173g', 
        'A3 Adesivo Colacril 190g', 'A3 Cartão Triplex 300g', 'A3 Duo Design 300g', 
        'ADESIVO FOSCO'
    ],
    TintaTonner: [
        'KONICA AMARELO', 'KONICA AZUL', 'KONICA MAGENTA', 'KONICA PRETO', 'PHASER 7800 AMARELO', 'PHASER 7800 AZUL',
        'PHASER 7800 MAGENTA', 'PHASER 7800 PRETO', 'TINTA EPSON AMARELO (CORANTE)', 'TINTA EPSON AMARELO (PIG)',
        'TINTA EPSON AZUL (CORANTE)', 'TINTA EPSON AZUL (PIG)', 'TINTA EPSON MAGENTA (CORANTE)', 'TINTA EPSON MAGENTA (PIG)',
        'TINTA EPSON PRETO (CORANTE)', 'TINTA EPSON PRETO (PIG)', 'TINTA FOTOGRAFICA AMARELO', 'TINTA FOTOGRAFICA AZUL',
        'TINTA FOTOGRAFICA AZUL CLARO', 'TINTA FOTOGRAFICA MAGENTA', 'TINTA FOTOGRAFICA MAGENTA CLARO', 'TINTA FOTOGRAFICA PRETO',
        'TINTA PLOTTER AMARELO', 'TINTA PLOTTER AZUL', 'TINTA PLOTTER MAGENTA', 'TINTA PLOTTER PRETO', 'TINTA RISO AMARELA',
        'TINTA RISO AZUL', 'TINTA RISO MAGENTA', 'TINTA RISO PRETO', 'TONER C75 AMARELA', 'TONER C75 AZUL', 'TONER C75 MAGENTA',
        'TONER C75 PRETO', 'TONNER ORIGINAL', 'TONNER RW'
    ]
    // Expedição: ['Caixas', 'Paletes'],
    // Limpeza: ['Detergentes', 'Desinfetantes'],
    // Escritório: ['Papelaria', 'Mobiliário'],
    // Mercado: ['Alimentos', 'Bebidas']
};

// Função para atualizar as subcategorias com base no formato selecionado
function atualizaSubcategoria() {
    var formato = document.getElementById("formato").value;
    var subcategoria = document.getElementById("tipo_de_material");

    // Limpa as opções apenas se houver subcategorias correspondentes ao valor do formato
    if (subcategorias[formato]) {
        // Limpa as opções atuais do campo "Subcategoria"
        subcategoria.innerHTML = '<option value="">Selecione uma subcategoria</option>';

        // Adiciona as opções de subcategorias disponíveis
        subcategorias[formato].forEach(function (item) {
            var option = document.createElement("option");
            option.value = item;
            option.textContent = item;
            subcategoria.appendChild(option);
        });
    } else {
        // Caso não haja subcategorias, restaura a opção padrão
        subcategoria.innerHTML = '<option value="">Selecione uma subcategoria</option>';
    }
}