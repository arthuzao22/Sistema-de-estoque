from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import FileResponse
from django.conf import settings
import os
import time
import pandas as pd
from decimal import Decimal
from app.forms import EstoqueForm
from app.models import Estoque

from git import Repo

from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload


@login_required(login_url='/login/')  # Redireciona para a página de login se não estiver logado
def home(request):
    tipo_de_material = request.GET.get('tipo_de_material')
    entrada_saida = request.GET.get('entrada_saida')
    data = request.GET.get('data')
    
    print(data)

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

        # Cálculo de quantidade final
        df['qtde_final'] = df[['qtde_placas_unidades', 'qtde_folhas_caixa', 'qtde_bobinas',
                               'qtde_bobinas_ensacamento', 'qtde_contra_capa', 
                               'qtde_granpeador', 'qtde_grampos', 'qtde_folhas_caixa_2', 
                               'qtde_tintas_toners', 'qtde_Wireo', 'qtde_espiral']].sum(axis=1, skipna=True)

        df['qtde_final'] = df['qtde_final'].astype(int)

        # Filtra pelo tipo de material, se fornecido
        if tipo_de_material:
            df = df[df['tipo_de_material'].str.contains(tipo_de_material, case=False, na=False)]

        # Filtra pela entrada ou saída, se fornecido
        if entrada_saida:
            df = df[df['entrada_saida'].str.contains(entrada_saida, case=False, na=False)]
            
        # Filtra pela data, se fornecido
        if data:
            df['data'] = pd.to_datetime(df['data'], errors='coerce').dt.date
            data_filtrada = pd.to_datetime(data, errors='coerce').date()
            df = df[df['data'] == data_filtrada]


        # Ordena os resultados pelo 'id' em ordem decrescente
        df = df.sort_values(by='id', ascending=False)

        paginator = Paginator(df.to_dict(orient='records'), 30)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Passa os dados para o contexto
        context = {'page_obj': page_obj}
        return render(request, 'index.html', context)

    except Exception as e:
        messages.error(request, f"Erro ao carregar os dados do estoque: {e}")
        return render(request, 'index.html')

@login_required(login_url='/login/')  # Redireciona para a página de login se não estiver logado
def form(request):
    try:
        if request.user.is_authenticated:
            nome_usuario = request.user.first_name
        else:
            nome_usuario = "Visitante"  # Caso o usuário não esteja logado

        data = {
            'form': EstoqueForm(),
            'nome_usuario': nome_usuario
        }

        return render(request, 'form.html', data)
    except Exception as e:
        messages.error(request, f"Erro ao carregar o formulário: {e}")
        
        data = {'nome_usuario': nome_usuario}
        return render(request, 'form.html', data)

@login_required(login_url='/login/')  # Redireciona para a página de login se não estiver logado
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

@login_required(login_url='/login/')  # Redireciona para a página de login se não estiver logado
def edit(request, pk):

    try:
        estoque = get_object_or_404(Estoque, pk=pk)
        data = {'form': EstoqueForm(instance=estoque)}
        return render(request, 'form.html', data)
    except Exception as e:
        messages.error(request, f"Erro ao editar o estoque: {e}")
        return redirect('home')
    
@login_required(login_url='/login/')  # Apontando para a URL correta de login
def index_btn(request):
    if request.user.is_authenticated:
        nome_usuario = request.user.first_name
        id = request.user.id
    else:
        nome_usuario = "Visitante"  # Caso o usuário não esteja logado
    context = {
    'nome_usuario': nome_usuario,
    'id': id  # Certifique-se de que 'id' está definido em algum lugar no código
    }
    return render(request, 'index_btn.html', context)


@login_required(login_url='/login/')  # Redireciona para a página de login se não estiver logado
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

@login_required(login_url='/login/')  # Redireciona para a página de login se não estiver logado
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
    if row['formato_da_folha'] != 'null' and row['tipo'] == 'Placas':
        material = row['tipo_de_material']
        formato = row['formato_da_folha']
        qtde = int(row['qtde'])
        
        if material == 'OFFSSET 120g' and formato == '640x880':
            return (250 * 8) * qtde
        elif material == "OFFSSET 120g" and formato == "660x960":
            return (250 * 9) * qtde
        
        elif material == "OFFSSET 180g" and formato == "640x880":
            return (250 * 8) * qtde
        
        elif material == "COUCHÊ 90g" and formato == "660x960":
            return (250 * 9) * qtde
        
        elif material == "COUCHÊ 115g" and formato == "660x960":
            return (250 * 9) * qtde
        
        elif material == "COUCHÊ 170g" and formato == "660x960":
            return (250 * 9) * qtde
        
        elif material == "COUCHÊ 240g" and formato == "660x960":
            return (150 * 9) * qtde
        
        elif material == "COUCHÊ 250g" and formato == "660x960":
            return (125 * 9) * qtde
        
        elif material == "Adesivo Colacril 173g" and formato == "660x960":
            return (100 * 9) * qtde
        elif material == "Adesivo Colacril 190g" and formato == "660x960":
            return (100 * 9) * qtde
        elif material == "Cartão Triplex 300g" and formato == "660x960":
            return (100 * 9) * qtde
        elif material == "Duo Design 300g" and formato == "660x960":
            return (150 * 9) * qtde
    return 0

def calcular_qtde_caixas(row):
    qtde = row['qtde']
    if row['tipo'] == 'Cx':
        
        if row['tipo_de_material'][:2] == 'A4':
            if row['tipo'] == 'Cx' and row['formato'] == 'Impressão':
                return qtde * 5000
        elif row['tipo_de_material'][:2] == 'A3':
            if row['tipo'] == 'Cx' and row['formato'] == 'Impressão':
                return qtde * 2500
        return 0
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
    
    if row['tipo']=='Cx':
        if row['tipo_de_material'] == 'CAPA PLASTICA INCOLOR':
            return qtde * 10 * 100
        if row['tipo_de_material'] == 'CONTRA CAPA PLASTICA AZUL':
            return qtde * 10 * 100
        if row['tipo_de_material'] == 'CONTRA CAPA PLASTICA PRETO':
            return qtde* 10 * 100
        return 0
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

#serve para calcular a qtde de espiral
def calcular_espiral(row):
    qtde = row['qtde']
    tipo = row['tipo']

    if tipo == 'Pacotes':

        if row['tipo_de_material'] in ["ESPIRAL BRANCO 9 MM", "ESPIRAL INCOLOR 9 MM", "ESPIRAL PRETO 9 MM"]:
            unidades = 100
            estoque_wireo = qtde * unidades
            return estoque_wireo

        elif row['tipo_de_material'] in ["ESPIRAL INCOLOR 12 MM", "ESPIRAL BRANCO 12 MM", "ESPIRAL PRETO 12 MM"]:
            unidades = 100
            estoque_wireo = qtde * unidades
            return estoque_wireo

        elif row['tipo_de_material'] in ["ESPIRAL BRANCO 14 MM", "ESPIRAL INCOLOR 14 MM", "ESPIRAL PRETO 14 MM"]:
            unidades = 100
            estoque_wireo = qtde * unidades
            return estoque_wireo

        elif row['tipo_de_material'] in ["ESPIRAL BRANCO 17 MM", "ESPIRAL INCOLOR 17 MM", "ESPIRAL PRETO 17 MM"]:
            unidades = 100
            estoque_wireo = qtde * unidades
            return estoque_wireo

        elif row['tipo_de_material'] in ["ESPIRAL BRANCO 20 MM", "ESPIRAL INCOLOR 20 MM", "ESPIRAL PRETO 20 MM"]:
            unidades = 70
            estoque_wireo = qtde * unidades
            return estoque_wireo

        elif row['tipo_de_material'] in ["ESPIRAL BRANCO 23 MM", "ESPIRAL INCOLOR 23 MM", "ESPIRAL PRETO 23 MM"]:
            unidades = 60
            estoque_wireo = qtde * unidades
            return estoque_wireo

        elif row['tipo_de_material'] in ["ESPIRAL BRANCO 25 MM", "ESPIRAL INCOLOR 25 MM", "ESPIRAL PRETO 25 MM"]:
            unidades = 45
            estoque_wireo = qtde * unidades
            return estoque_wireo

        elif row['tipo_de_material'] in ["ESPIRAL BRANCO 29 MM", "ESPIRAL INCOLOR 29 MM", "ESPIRAL PRETO 29 MM"]:
            unidades = 25
            estoque_wireo = qtde * unidades
            return estoque_wireo

        elif row['tipo_de_material'] in ["ESPIRAL BRANCO 33 MM", "ESPIRAL INCOLOR 33 MM", "ESPIRAL PRETO 33 MM"]:
            unidades = 25
            estoque_wireo = qtde * unidades
            return estoque_wireo

        elif row['tipo_de_material'] in ["ESPIRAL BRANCO 40 MM", "ESPIRAL INCOLOR 40 MM", "ESPIRAL PRETO 40 MM"]:
            unidades = 20
            estoque_wireo = qtde * unidades
            return estoque_wireo

        elif row['tipo_de_material'] in ["ESPIRAL BRANCO 45 MM", "ESPIRAL INCOLOR 45 MM", "ESPIRAL PRETO 45 MM"]:
            unidades = 16
            estoque_wireo = qtde * unidades
            return estoque_wireo

        elif row['tipo_de_material'] in ["ESPIRAL BRANCO 50 MM", "ESPIRAL INCOLOR 50 MM", "ESPIRAL PRETO 50 MM"]:
            unidades = 12
            estoque_wireo = qtde * unidades
            return estoque_wireo
        else:
            return 0
    
    elif tipo == 'Cx':

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

import pandas as pd

def calcular_estoque_total_especifico(df):
    # Ajusta as quantidades para o tipo de material específico
    for index, row in df.iterrows():
        if row['tipo'] == 'Pacotes':
            if row['tipo_de_material'] in ["ESPIRAL BRANCO 9 MM", "ESPIRAL INCOLOR 9 MM", "ESPIRAL PRETO 9 MM"]:
                df.at[index, 'qtde'] = (row['qtde'] * 100) / (20 * 100)
                
            elif row['tipo_de_material'] in ["ESPIRAL INCOLOR 12 MM", "ESPIRAL BRANCO 12 MM", "ESPIRAL PRETO 12 MM"]:
                df.at[index, 'qtde'] = (row['qtde'] * 100) / (13 * 100)
    
            elif row['tipo_de_material'] in ["ESPIRAL BRANCO 14 MM", "ESPIRAL INCOLOR 14 MM", "ESPIRAL PRETO 14 MM"]:
                df.at[index, 'qtde'] = (row['qtde'] * 100) / (14 * 100)
    
    
            elif row['tipo_de_material'] in ["ESPIRAL BRANCO 17 MM", "ESPIRAL INCOLOR 17 MM", "ESPIRAL PRETO 17 MM"]:
                df.at[index, 'qtde'] = (row['qtde'] * 100) / (10 * 100)
    
    
            elif row['tipo_de_material'] in ["ESPIRAL BRANCO 20 MM", "ESPIRAL INCOLOR 20 MM", "ESPIRAL PRETO 20 MM"]:
                df.at[index, 'qtde'] = (row['qtde'] * 100) / (11 * 70)
    
    
            elif row['tipo_de_material'] in ["ESPIRAL BRANCO 23 MM", "ESPIRAL INCOLOR 23 MM", "ESPIRAL PRETO 23 MM"]:
                df.at[index, 'qtde'] = (row['qtde'] * 100) / (10 * 60)
    
    
            elif row['tipo_de_material'] in ["ESPIRAL BRANCO 25 MM", "ESPIRAL INCOLOR 25 MM", "ESPIRAL PRETO 25 MM"]:
                df.at[index, 'qtde'] = (row['qtde'] * 100) / (12 * 45)
    
    
            elif row['tipo_de_material'] in ["ESPIRAL BRANCO 29 MM", "ESPIRAL INCOLOR 29 MM", "ESPIRAL PRETO 29 MM"]:
                df.at[index, 'qtde'] = (row['qtde'] * 100) / (11 * 35)
    
    
            elif row['tipo_de_material'] in ["ESPIRAL BRANCO 33 MM", "ESPIRAL INCOLOR 33 MM", "ESPIRAL PRETO 33 MM"]:
                df.at[index, 'qtde'] = (row['qtde'] * 100) / (12 * 25)
    
    
            elif row['tipo_de_material'] in ["ESPIRAL BRANCO 40 MM", "ESPIRAL INCOLOR 40 MM", "ESPIRAL PRETO 40 MM"]:
                df.at[index, 'qtde'] = (row['qtde'] * 100) / (10 * 20)
    
    
            elif row['tipo_de_material'] in ["ESPIRAL BRANCO 45 MM", "ESPIRAL INCOLOR 45 MM", "ESPIRAL PRETO 45 MM"]:
                df.at[index, 'qtde'] = (row['qtde'] * 100) / (9 * 16)
    
    
            elif row['tipo_de_material'] in ["ESPIRAL BRANCO 50 MM", "ESPIRAL INCOLOR 50 MM", "ESPIRAL PRETO 50 MM"]:
                df.at[index, 'qtde'] = (row['qtde'] * 100) / (10 * 12)

    
    # Muda o tipo de 'Pacotes' para 'Cx'
    df.loc[df['tipo'] == 'Pacotes', 'tipo'] = 'Cx'
        
    # Agrupa as quantidades por tipo de material e tipo
    entradas = df[df['entrada_saida'] == 'Entrada'].groupby(['tipo_de_material', 'tipo'])['qtde'].sum()
    saidas = df[df['entrada_saida'] == 'Saida'].groupby(['tipo_de_material', 'tipo'])['qtde'].sum()
    
    # Calcula o estoque total
    estoque_total_geral = entradas.subtract(saidas, fill_value=0).reset_index(name='estoque_total') 
    
    return estoque_total_geral

@login_required(login_url='/login/')  # Redireciona para a página de login se não estiver logado
def estoque(request):
    try:
        # Obtém o tipo de material a partir da solicitação GET
        tipo_de_material = request.GET.get('tipo_de_material')
        tipo_material_geral = request.GET.get('tipo_material_geral')

        # Consulta todos os itens no queryset
        estoque = Estoque.objects.all()

        # Monta o dicionário de dados com as informações do queryset
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
        df['qtde_final'] = df[['qtde_placas_unidades',  'qtde_folhas_caixa', 'qtde_bobinas',
                               'qtde_bobinas_ensacamento', 'qtde_contra_capa', 
                               'qtde_granpeador', 'qtde_grampos', 'qtde_folhas_caixa_2', 
                               'qtde_tintas_toners', 'qtde_Wireo', 'qtde_espiral']].sum(axis=1, skipna=True)

        # Cálculo do estoque total e total geral
        estoque_total = calcular_estoque_total(df)
        estoque_total_geral = calcular_estoque_total_especifico(df)

        # Converte o resultado para dicionário
        estoque_total_dict = estoque_total.to_dict()
        estoque_total_geral_dict = estoque_total_geral.to_dict(orient='records')

        # Filtra o estoque_total pelo tipo de material, se fornecido
        if tipo_de_material:
            estoque_total_dict = {tipo: qtd for tipo, qtd in estoque_total_dict.items()
                                  if tipo_de_material.lower() in tipo.lower()}
        # Filtra o estoque_total pelo tipo_material_geral, se fornecido
        if tipo_material_geral:
            estoque_total_geral_dict = [item for item in estoque_total_geral_dict
                                        if tipo_material_geral.lower() in item['tipo_de_material'].lower()]

        # Adiciona os dados ao contexto
        data['df'] = df.to_dict(orient='records')
        data['estoque_total'] = estoque_total_dict
        data['estoque_total_geral'] = estoque_total_geral_dict

        return render(request, 'estoque.html', {
            'df_geral': data['df'], 
            'estoque_total': data['estoque_total'], 
            'estoque_total_geral': data['estoque_total_geral']
        })
    except Exception as e:
        messages.error(request, f"Erro ao carregar a página de estoque: {e}")
        return render(request, 'estoque.html')
    
def download_database(request):
    # Caminho completo para o arquivo `db.sqlite3`
    database_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    # Retorna o arquivo como uma resposta de download
    return FileResponse(open(database_path, 'rb'), as_attachment=True, filename='db.sqlite3')

########################################################## LOGIN ###############################################################

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        
        user = authenticate(request, username=email, password=senha)
        if user is not None:
            login(request, user)
            return redirect('index_btn')  # Redireciona para a página inicial após login bem-sucedido
        else:
            # Exibir uma mensagem de erro caso o login falhe
            messages.error(request, "Credenciais inválidas. Tente novamente.")
            return render(request, 'login.html')

    return render(request, 'login.html')

@login_required(login_url='/login/')  # Redireciona para a página de login se não estiver logado
def register_view(request):
    if request.user.id == 1:
        if request.method == 'POST':
            email = request.POST['email']
            nome = request.POST['nome']
            senha = request.POST['senha']
            cargo = request.POST['cargo']

            # Verificar se o email já está registrado
            if User.objects.filter(email=email).exists():
                messages.error(request, "Este email já está registrado.")
                return redirect('register')

            try:
                # Criar o novo usuário
                user = User.objects.create_user(username=email, email=email, password=senha)
                user.first_name = nome
                user.last_name = cargo  # Armazene o cargo no campo last_name ou em outro modelo se necessário.
                user.save()

                # Mensagem de sucesso
                messages.success(request, "Cadastro realizado com sucesso!")
                return redirect('login')  # Redireciona para a página de login após o registro.

            except IntegrityError:
                messages.error(request, "Erro ao registrar o usuário. Tente novamente.")
                return redirect('register')
            except Exception as e:
                messages.error(request, f"Ocorreu um erro inesperado: {e}")
                return redirect('register')

        return render(request, 'register.html')  # Renderiza o formulário de registro
    else:
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return render(request, 'index_btn.html')  # Renderiza a página inicial caso não tenha permissão
    
    
def subir_para_base_de_dados(request):
    if request.method == "POST" and request.FILES.get('excelFile'):
        excel_file = request.FILES['excelFile']
        
        # Carregar o arquivo Excel
        sheet_informacoes = pd.read_excel(excel_file)

        # Iterar sobre as linhas do arquivo e salvar no banco de dados
        for i in range(len(sheet_informacoes)):
            registro = Estoque(
                entrada_saida=sheet_informacoes.loc[i, "entrada_saida"],
                data=sheet_informacoes.loc[i, "data"],
                qtde=sheet_informacoes.loc[i, "qtde"],
                tipo=sheet_informacoes.loc[i, "tipo"],
                formato=sheet_informacoes.loc[i, "formato"],
                nome=sheet_informacoes.loc[i, "nome"],
                tipo_de_material=sheet_informacoes.loc[i, "tipo_de_material"],
                formato_da_folha=sheet_informacoes.loc[i, "formato_da_folha"],
                folha=sheet_informacoes.loc[i, "folha"]
            )
            registro.save()

        # Redirecionar ou exibir uma mensagem de sucesso
        return render(request, 'register.html')

    return render(request, 'upload_excel.html')
        
