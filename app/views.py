from django.shortcuts import render, redirect, get_object_or_404
from app.forms import EstoqueForm
from app.models import Estoque
import pandas as pd  # Certifique-se de que esta linha está presente
from decimal import Decimal
from app.forms import EstoqueForm
from django.contrib import messages


# Create your views here.
def home(request):
    try:
        estoques = Estoque.objects.all().values()
        df = pd.DataFrame(list(estoques))

        df['qtde_placas_unidades'] = df.apply(calcular_qtde_placas, axis=1)
        df['qtde_folhas_caixa'] = df.apply(calcular_qtde_caixas, axis=1)
        df['qtde_bobinas'] = df.apply(calcular_qtde_bobinas, axis=1)
        df['qtde_bobinas_ensacamento'] = df.apply(calcular_qtde_bobinas_ensacamento, axis=1)
        df['qtde_contra_capa'] = df.apply(calcular_contra_capa, axis=1)
        df['qtde_granpeador'] = df.apply(calcular_granpeador, axis=1)
        df['qtde_grampos'] = df.apply(calcular_grampos, axis=1)
        df['qtde_folhas_caixa_2'] = df.apply(calcular_caixa_2, axis=1)
        df['qtde_tintas_toners'] = df.apply(calcular_tintas_toners, axis=1)
        df['qtde_Wireo'] = df.apply(calcular_Wireo, axis=1)
        df['qtde_espiral'] = df.apply(calcular_espiral, axis=1)

        df['qtde_final'] = df[['qtde_placas_unidades', 'qtde_folhas_caixa', 'qtde_bobinas',
                               'qtde_bobinas_ensacamento', 'qtde_contra_capa', 
                               'qtde_granpeador', 'qtde_grampos', 'qtde_folhas_caixa_2', 
                               'qtde_tintas_toners', 'qtde_Wireo', 'qtde_espiral']].replace(0, pd.NA).sum(axis=1, skipna=True)

        context = {'db': df.to_dict(orient='records')}
        return render(request, 'index.html', context)
    except Exception as e:
        messages.error(request, f"Erro ao carregar os dados do estoque: {e}")
        return render(request, 'index.html')

def form(request):
    try:
        data = {'form': EstoqueForm()}
        return render(request, 'form.html', data)
    except Exception as e:
        messages.error(request, f"Erro ao carregar o formulário: {e}")
        return render(request, 'form.html')

# Create
def create(request):
    try:
        form = EstoqueForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'O estoque foi salvo com sucesso!')
            return redirect('form')
        else:
            messages.error(request, 'Erro ao salvar o estoque. Verifique os dados.')
        
        data = {'form': form}
        return render(request, 'form.html', data)
    except Exception as e:
        messages.error(request, f"Erro ao salvar o estoque: {e}")
        return render(request, 'form.html')

# Edit
def edit(request, pk):
    try:
        estoque = get_object_or_404(Estoque, pk=pk)
        data = {'form': EstoqueForm(instance=estoque)}
        return render(request, 'form.html', data)
    except Exception as e:
        messages.error(request, f"Erro ao editar o estoque: {e}")
        return redirect('home')

# Update
def update(request, pk):
    try:
        estoque = get_object_or_404(Estoque, pk=pk)
        form = EstoqueForm(request.POST or None, instance=estoque)
        if form.is_valid():
            form.save()
            messages.success(request, 'O estoque foi atualizado com sucesso!')
            return redirect('home')
        else:
            messages.error(request, 'Erro ao atualizar o estoque. Verifique os dados.')
        
        data = {'form': form}
        return render(request, 'form.html', data)
    except Exception as e:
        messages.error(request, f"Erro ao atualizar o estoque: {e}")
        return redirect('home')

# Delete
def delete(request, pk):
    try:
        estoque = get_object_or_404(Estoque, pk=pk)
        estoque.delete()
        messages.success(request, 'O estoque foi excluído com sucesso!')
        return redirect('home')
    except Exception as e:
        messages.error(request, f"Erro ao excluir o estoque: {e}")
        return redirect('home')


############################################################# CALCULOS DE ESTOQUE #############################################################


# Função para cálculo de quantidade de placas
def calcular_qtde_placas(row):
    if row['tipo'] == 'Placas' and row['qtde'] > 0:
        material = row['tipo_de_material']
        formato = row['formato']
        qtde = row['qtde']
        
        if material == "A4 OFFSSET 120g" and formato == "640x880":
            return qtde * 1500
        elif material == "A4 OFFSSET 120g" and formato == "660x960":
            return qtde * 2250
        elif material == "A3 OFFSSET 120g":
            return qtde * 1000
        elif material == "A4 OFFSSET 180g" and formato == "640x880":
            return qtde * 1500
        elif material == "A4 OFFSSET 180g" and formato == "660x960":
            return qtde * 2250
        elif material == "A3 OFFSSET 180g":
            return qtde * 1000
        elif material == "A4 OFFSSET 240g" and formato == "660x960":
            return qtde * 1350
        elif material == "A3 OFFSSET 240g":
            return qtde * 600
        elif material == "A4 COUCHÊ 90g" and formato == "660x960":
            return qtde * 2250
        elif material == "A3 COUCHÊ 90g":
            return qtde * 1000
        elif material == "A4 COUCHÊ 115g" and formato == "660x960":
            return qtde * 2250
        elif material == "A3 COUCHÊ 115g":
            return qtde * 1000
        elif material == "A4 COUCHÊ 170g" and formato == "660x960":
            return qtde * 2250
        elif material == "A3 COUCHÊ 170g":
            return qtde * 1000
        elif material == "A4 COUCHÊ 250g" and formato == "660x960":
            return qtde * 1125
        elif material == "A3 COUCHÊ 250g":
            return qtde * 500
        elif material == "A4 SUPREMO 300g" and formato == "660x960":
            return qtde * 1350
        elif material == "A3 SUPREMO 300g":
            return qtde * 600
        elif material == "ADESIVO FOSCO" and formato == "660x960":
            return qtde * 900
        
    return 0

def calcular_qtde_caixas(row):
    qtde = row['qtde']

    if row['tipo_de_material'][:2] == 'A4':
        if row['tipo'] == 'Cx' and row['formato'] == 'Impressão':
            return qtde * 5000
    elif row['tipo_de_material'][:2] == 'A3':
        if row['tipo'] == 'Cx' and row['formato'] == 'Impressão':
            return qtde * 5000
    return 0

def calcular_qtde_bobinas(row):
    qtde = row['qtde']

    if row['tipo_de_material'] in [
        'BOBINA DE LAMINAÇÃO BRILHO (MAIOR)',
        'BOBINA DE LAMINAÇÃO BRILHO (MENOR)',
        'BOBINA DE LAMINAÇÃO FOSCO',
        'BOBINA DE LAMINAÇÃO HOLOGRAFICA',
        'BOBINA PLASTICA (SHIRINK)'
    ]:
        return qtde

    return 0

def calcular_qtde_bobinas_ensacamento(row):
    qtde = row['qtde']
    
    if row['tipo_de_material'] == 'BOBINA PLASTICA A4 (ENSACAMENTO)':
        return qtde * 8
    elif row['tipo_de_material'] == 'BOBINA PLASTICA A3 (ENSACAMENTO)':
        return qtde * 6
    else:
        return 0

def calcular_contra_capa(row):
    qtde = row['qtde']
    
    if row['tipo_de_material'] == 'CAPA PLASTICA INCOLOR':
        return calcular_qtde_caixas(row) * 100
    if row['tipo_de_material'] == 'CONTRA CAPA PLASTICA AZUL':
        return calcular_qtde_caixas(row) * 100
    if row['tipo_de_material'] == 'CONTRA CAPA PLASTICA PRETO':
        return calcular_qtde_caixas(row) * 100
    return 0

def calcular_granpeador(row):
    qtde = row['qtde']

    if row['tipo_de_material'] == 'GRAMPEADOR':
        return qtde
    else:
        return 0
    
def calcular_grampos(row):
    qtde = row['qtde']

    if row['tipo_de_material'] == 'GRAMPO':
        return qtde * 5000
    else:
        return 0

def calcular_caixa_2(row):
    qtde = row['qtde']
    tipo = row['tipo']
    
    if tipo == 'Cx':
        if row['tipo_de_material'] == 'CX 2 - 25':
            return row['qtde'] * 25
        elif row['tipo_de_material'] == 'CX 2 - 20':
            return row['qtde'] * 20
        else:
            return 0
    else:
        return 0

def calcular_tintas_toners(row):
    qtde = row['qtde']

    if row['tipo_de_material'] in ['KONICA AMARELO'
                                  ,'KONICA AZUL'
                                  ,'KONICA MAGENTA'
                                  ,'PHASER 7800 AMARELO'
                                  ,'PHASER 7800 AZUL'
                                  ,'PHASER 7800 MAGENTA'
                                  ,'PHASER 7800 PRETO'
                                  ,'TINTA EPSON AMARELO (CORANTE)'
                                  ,'TINTA EPSON AMARELO (PIG)'
                                  ,'TINTA EPSON AZUL (CORANTE)'
                                  ,'TINTA EPSON AZUL (PIG)'
                                  ,'TINTA EPSON MAGENTA (CORANTE)'
                                  ,'TINTA EPSON MAGENTA (PIG)'
                                  ,'TINTA EPSON PRETO (CORANTE)'
                                  ,'TINTA EPSON PRETO (PIG)'
                                  ,'TINTA FOTOGRAFICA AMARELO'
                                  ,'TINTA FOTOGRAFICA AZUL'
                                  ,'TINTA FOTOGRAFICA AZUL CLAR0'
                                  ,'TINTA FOTOGRAFICA MAGENTA'
                                  ,'TINTA FOTOGRAFICA MAGENTA CLARO'
                                  ,'TINTA FOTOGRAFICA PRETO'
                                  ,'TINTA PLOTTER AMARELO'
                                  ,'TINTA PLOTTER AZUL'
                                  ,'TINTA PLOTTER MAGENTA'
                                  ,'TINTA PLOTTER PRETO'
                                  ,'TINTA RISO AMARELA'
                                  ,'TINTA RISO AZUL'
                                  ,'TINTA RISO MAGENTA'
                                  ,'TINTA RISO PRETO'
                                  ,'TONER C75 AMARELA'
                                  ,'TONER C75 AZUL'
                                  ,'TONER C75 MAGENTA'
                                  ,'TONER C75 PRETO'
                                  ,'TONNER ORIGINAL'
                                  ,'TONNER RW'
                                  ,'TONNER RW'
                                  ,'KONICA PRETO']:
        return qtde
    else:
        return 0
    
def calcular_espiral(row):
    qtde = row['qtde']
    tipo = row['tipo']

    if tipo == 'Cx':

        if row['tipo_de_material'] in ["ESPIRAL BRANCO 9 MM", "ESPIRAL INCOLOR 9 MM", "ESPIRAL PRETO 9 MM"]:
            pct = 20
            unidades = 100
            estoque_wireo = qtde * pct * unidades
            return estoque_wireo

        elif row['tipo_de_material'] in ["ESPIRAL INCOLOR 12 MM", "ESPIRAL BRANCO 12 MM", "ESPIRAL PRETO 12 MM"]:
            pct = 13
            unidades = 100
            estoque_wireo = qtde * pct * unidades
            return estoque_wireo

        elif row['tipo_de_material'] in ["ESPIRAL BRANCO 14 MM", "ESPIRAL INCOLOR 14 MM", "ESPIRAL PRETO 14 MM"]:
            pct = 14
            unidades = 100
            estoque_wireo = qtde * pct * unidades
            return estoque_wireo

        elif row['tipo_de_material'] in ["ESPIRAL BRANCO 17 MM", "ESPIRAL INCOLOR 17 MM", "ESPIRAL PRETO 17 MM"]:
            pct = 10
            unidades = 100
            estoque_wireo = qtde * pct * unidades
            return estoque_wireo

        elif row['tipo_de_material'] in ["ESPIRAL BRANCO 20 MM", "ESPIRAL INCOLOR 20 MM", "ESPIRAL PRETO 20 MM"]:
            pct = 11
            unidades = 70
            estoque_wireo = qtde * pct * unidades
            return estoque_wireo

        elif row['tipo_de_material'] in ["ESPIRAL BRANCO 23 MM", "ESPIRAL INCOLOR 23 MM", "ESPIRAL PRETO 23 MM"]:
            pct = 10
            unidades = 60
            estoque_wireo = qtde * pct * unidades
            return estoque_wireo

        elif row['tipo_de_material'] in ["ESPIRAL BRANCO 25 MM", "ESPIRAL INCOLOR 25 MM", "ESPIRAL PRETO 25 MM"]:
            pct = 12
            unidades = 45
            estoque_wireo = qtde * pct * unidades
            return estoque_wireo

        elif row['tipo_de_material'] in ["ESPIRAL BRANCO 29 MM", "ESPIRAL INCOLOR 29 MM", "ESPIRAL PRETO 29 MM"]:
            pct = 11
            unidades = 25
            estoque_wireo = qtde * pct * unidades
            return estoque_wireo

        elif row['tipo_de_material'] in ["ESPIRAL BRANCO 33 MM", "ESPIRAL INCOLOR 33 MM", "ESPIRAL PRETO 33 MM"]:
            pct = 12
            unidades = 25
            estoque_wireo = qtde * pct * unidades
            return estoque_wireo

        elif row['tipo_de_material'] in ["ESPIRAL BRANCO 40 MM", "ESPIRAL INCOLOR 40 MM", "ESPIRAL PRETO 40 MM"]:
            pct = 10
            unidades = 20
            estoque_wireo = qtde * pct * unidades
            return estoque_wireo

        elif row['tipo_de_material'] in ["ESPIRAL BRANCO 45 MM", "ESPIRAL INCOLOR 45 MM", "ESPIRAL PRETO 45 MM"]:
            pct = 8
            unidades = 16
            estoque_wireo = qtde * pct * unidades
            return estoque_wireo

        elif row['tipo_de_material'] in ["ESPIRAL BRANCO 50 MM", "ESPIRAL INCOLOR 50 MM", "ESPIRAL PRETO 50 MM"]:
            pct = 10
            unidades = 12
            estoque_wireo = qtde * pct * unidades
            return estoque_wireo
        else:
            return 0
    else:
        return 0

    
def calcular_Wireo(row):
    qtde = row['qtde']
    tipo = row['tipo']

    if tipo == 'Cx':
        if row['tipo_de_material'] == "WIRE-O BRANCO (1/2)" or row['tipo_de_material'] == "WIRE-O PRETO (1/2)":
            aneis = 26000
            estoque_wireo = qtde * aneis
            return estoque_wireo

        elif row['tipo_de_material'] == "WIRE-O BRANCO (1-1/4)" or row['tipo_de_material'] == "WIRE-O PRETO (1-1/4)":
            aneis = 2100
            estoque_wireo = qtde * aneis
            return estoque_wireo

        elif row['tipo_de_material'] == "WIRE-O BRANCO (3/4)" or row['tipo_de_material'] == "WIRE-O PRETO (3/4)":
            aneis = 8000
            estoque_wireo = qtde * aneis
            return estoque_wireo
        else:
            return 0
    else:
        return 0
    

def calcular_estoque_total(df):
    entradas = df[df['entrada_saida'] == 'Entrada'].groupby('tipo_de_material')['qtde_final'].sum()
    saidas = df[df['entrada_saida'] == 'Saida'].groupby('tipo_de_material')['qtde_final'].sum()
    estoque_total = entradas.subtract(saidas, fill_value=0)
    return estoque_total

def calcular_estoque_total_especifico(df):
    entradas = df[df['entrada_saida'] == 'Entrada'].groupby(['tipo_de_material', 'tipo'])['qtde'].sum()
    saidas = df[df['entrada_saida'] == 'Saida'].groupby(['tipo_de_material', 'tipo'])['qtde'].sum()
    
    estoque_total_geral = entradas.subtract(saidas, fill_value=0).reset_index(name='estoque_total')
    
    return estoque_total_geral


def estoque(request):
    estoque = Estoque.objects.all()
    data = {
        'entrada_saida': [f.entrada_saida for f in estoque],
        'data': [f.data for f in estoque],
        'qtde': [f.qtde for f in estoque],
        'tipo': [f.tipo for f in estoque],
        'formato': [f.formato for f in estoque],
        'nome': [f.nome for f in estoque],
        'tipo_de_material': [f.tipo_de_material for f in estoque],
        'formato_da_folha': [f.formato_da_folha for f in estoque],
        'folha': [f.folha for f in estoque],
    }

    df = pd.DataFrame(data)
    df['qtde'] = df['qtde'].apply(Decimal)

    # Aplicação das funções de cálculo
    df['qtde_placas_unidades'] = df.apply(calcular_qtde_placas, axis=1)
    df['qtde_folhas_caixa'] = df.apply(calcular_qtde_caixas, axis=1)
    df['qtde_bobinas'] = df.apply(calcular_qtde_bobinas, axis=1)
    df['qtde_bobinas_ensacamento'] = df.apply(calcular_qtde_bobinas_ensacamento, axis=1)
    df['qtde_contra_capa'] = df.apply(calcular_contra_capa, axis=1)
    df['qtde_granpeador'] = df.apply(calcular_granpeador, axis=1)
    df['qtde_grampos'] = df.apply(calcular_grampos, axis=1)
    df['qtde_folhas_caixa_2'] = df.apply(calcular_caixa_2, axis=1)
    df['qtde_tintas_toners'] = df.apply(calcular_tintas_toners, axis=1)
    df['qtde_Wireo'] = df.apply(calcular_Wireo, axis=1)
    df['qtde_espiral'] = df.apply(calcular_espiral, axis=1)

    # Cálculo de quantidade final
    df['qtde_final'] = df[['qtde_placas_unidades', 'qtde_folhas_caixa', 'qtde_bobinas',
                           'qtde_bobinas_ensacamento', 'qtde_contra_capa', 
                           'qtde_granpeador', 'qtde_grampos', 'qtde_folhas_caixa_2', 
                           'qtde_tintas_toners', 'qtde_Wireo', 'qtde_espiral']].sum(axis=1, skipna=True)

    # Cálculo do estoque total e total geral
    estoque_total = calcular_estoque_total(df)
    estoque_total_geral = calcular_estoque_total_especifico(df)

    # Converte o resultado para dicionário
    estoque_total_dict = estoque_total.to_dict()
    estoque_total_geral_dict = estoque_total_geral.to_dict()

    # Adiciona os dados ao contexto
    data['df'] = df.to_dict(orient='records')
    data['estoque_total'] = estoque_total_dict
    data['estoque_total_geral'] = estoque_total_geral.to_dict(orient='records')
    
    return render(request, 'estoque.html', {'df_geral': data['df'], 
                                            'estoque_total': data['estoque_total'], 
                                            'estoque_total_geral': data['estoque_total_geral']})


