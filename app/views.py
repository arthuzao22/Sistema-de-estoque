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
from datetime import datetime

from git import Repo

from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload

from app.db_connection import get_connection
from app.calculations import calcular_estoque_total_especifico, calcular_qtde_placas, calcular_qtde_caixas, calcular_qtde_bobinas, calcular_qtde_bobinas_ensacamento, calcular_contra_capa, calcular_granpeador, calcular_grampos,calcular_caixa_2, calcular_tintas_toners, calcular_espiral, calcular_Wireo, calcular_estoque_total

@login_required(login_url='/login/')
def home(request):
    tipo_de_material = request.GET.get('tipo_de_material')
    entrada_saida = request.GET.get('entrada_saida')
    data = request.GET.get('data')
    print("data", entrada_saida)

    try:
        conn = get_connection()
        query = "SELECT * FROM Estoque"
        estoques = pd.read_sql_query(query, conn)

        # Realiza os cálculos no DataFrame
        estoques['qtde_placas_unidades'] = estoques.apply(calcular_qtde_placas, axis=1)
        estoques['qtde_folhas_caixa'] = estoques.apply(calcular_qtde_caixas, axis=1)
        estoques['qtde_bobinas'] = estoques.apply(calcular_qtde_bobinas, axis=1)
        estoques['qtde_bobinas_ensacamento'] = estoques.apply(calcular_qtde_bobinas_ensacamento, axis=1)
        estoques['qtde_contra_capa'] = estoques.apply(calcular_contra_capa, axis=1)
        estoques['qtde_granpeador'] = estoques.apply(calcular_granpeador, axis=1)
        estoques['qtde_grampos'] = estoques.apply(calcular_grampos, axis=1)
        estoques['qtde_folhas_caixa_2'] = estoques.apply(calcular_caixa_2, axis=1)
        estoques['qtde_tintas_toners'] = estoques.apply(calcular_tintas_toners, axis=1)
        estoques['qtde_Wireo'] = estoques.apply(calcular_Wireo, axis=1)
        estoques['qtde_espiral'] = estoques.apply(calcular_espiral, axis=1)

        # Calcula a quantidade final
        estoques['qtde_final'] = estoques[['qtde_placas_unidades', 'qtde_folhas_caixa', 'qtde_bobinas',
                                           'qtde_bobinas_ensacamento', 'qtde_contra_capa',
                                           'qtde_granpeador', 'qtde_grampos', 'qtde_folhas_caixa_2',
                                           'qtde_tintas_toners', 'qtde_Wireo', 'qtde_espiral']].sum(axis=1, skipna=True)
        estoques['qtde_final'] = estoques['qtde_final'].astype(int)

        # Aplicar filtros
        if tipo_de_material:
            estoques = estoques[estoques['tipo_de_material'].str.contains(tipo_de_material, case=False, na=False)]
        if entrada_saida:
            estoques = estoques[estoques['entrada_saida'].str.contains(entrada_saida, case=False, na=False)]
        if data:
            estoques['data'] = datetime.now().strftime('%d/%m/%Y')
            data_filtrada = pd.to_datetime(data, errors='coerce').date()
            estoques = estoques[estoques['data'] == data_filtrada]

        estoques = estoques.sort_values(by='id', ascending=False)
        
        # Paginação
        paginator = Paginator(estoques.to_dict(orient='records'), 30)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'index.html', {'page_obj': page_obj})

    except Exception as e:
        messages.error(request, f"Erro ao carregar os dados do estoque: {e}")
        return render(request, 'index.html')

@login_required(login_url='/login/')  
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
    
@login_required(login_url='/login/')
def create(request):
    try:
        if request.method == "POST":
            conn = get_connection()
            data = request.POST.dict()
            query = """
                INSERT INTO Estoque (entrada_saida, data, qtde, tipo, formato, nome, tipo_de_material, formato_da_folha, folha)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            conn.execute(query, (
                data['entrada_saida'], data['data'], data['qtde'], data['tipo'], data['formato'],
                data['nome'], data['tipo_de_material'], data['formato_da_folha'], data['folha']
            ))
            conn.commit()
            messages.success(request, "Registro criado com sucesso!")
            return redirect('form')

        return render(request, 'form.html', {'form': EstoqueForm()})

    except Exception as e:
        messages.error(request, f"Erro ao salvar o registro: {e}")
        return redirect('form')

@login_required(login_url='/login/')  
def edit(request, pk):

    try:
        estoque = get_object_or_404(Estoque, pk=pk)
        data = {'form': EstoqueForm(instance=estoque)}
        return render(request, 'form.html', data)
    except Exception as e:
        messages.error(request, f"Erro ao editar o estoque: {e}")
        return redirect('home')
    
@login_required(login_url='/login/')
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

@login_required(login_url='/login/')  
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

@login_required(login_url='/login/')
def delete(request, pk):
    try:
        conn = get_connection()
        query = "DELETE FROM Estoque WHERE id = ?"
        conn.execute(query, (pk,))
        conn.commit()
        messages.success(request, "Registro excluído com sucesso!")
        return redirect('home')
    except Exception as e:
        messages.error(request, f"Erro ao excluir o registro: {e}")
        return redirect('home')


############################################################# CALCULOS DE ESTOQUE #############################################################

@login_required(login_url='/login/')  
def estoque(request):
    try:
        # Obtém os filtros da solicitação GET
        tipo_de_material = request.GET.get('tipo_de_material')
        tipo_material_geral = request.GET.get('tipo_material_geral')

        # Conecta ao SQLiteCloud e busca os dados da tabela Estoque
        conn = get_connection()
        query = "SELECT * FROM Estoque"
        df = pd.read_sql_query(query, conn)
        
        # Converte campos numéricos para Decimal
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

        # Converte os resultados para dicionário
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
        context = {
            'df_geral': df.to_dict(orient='records'),
            'estoque_total': estoque_total_dict,
            'estoque_total_geral': estoque_total_geral_dict
        }

        return render(request, 'estoque.html', context)

    except Exception as e:
        messages.error(request, f"Erro ao carregar a página de estoque: {e}")
        return render(request, 'estoque.html')

    
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

@login_required(login_url='/login/')  
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

########################################################## LOGIN ###############################################################

@login_required(login_url='/login/')
def dashboard(request):
    try:
        # Conecta ao SQLiteCloud e busca os dados da tabela Estoque
        conn = get_connection()
        query = "SELECT * FROM Estoque"
        df = pd.read_sql_query(query, conn)

        # Tratamento de dados
        df['qtde'] = pd.to_numeric(df['qtde'], errors='coerce').fillna(0).apply(Decimal)  # Garantir conversão numérica
        df['data'] = pd.to_datetime(df['data'], errors='coerce')  # Garantir conversão para datetime
        df['formato_da_folha'].fillna('Indefinido', inplace=True)  # Preencher valores nulos
        df['entrada_saida'] = df['entrada_saida'].str.lower()  # Padronizar strings

        # Total de Itens em Estoque
        total_itens = df['qtde'].count()

        # Itens em baixa (quantidade menor que 10)
        itens_baixa = df[df['qtde'] < 10]

        # Entradas e Saídas recentes
        entradas_recentes = df[df['entrada_saida'] == 'entrada']['qtde'].count()
        saidas_recentes = df[df['entrada_saida'] == 'saida']['qtde'].count()

        # Dados para o gráfico de entradas e saídas por data
        entradas_por_data = df[df['entrada_saida'] == 'entrada'].groupby('data')['qtde'].count().reset_index()
        saidas_por_data = df[df['entrada_saida'] == 'saida'].groupby('data')['qtde'].count().reset_index()
        
        # Preparar labels e datasets para o gráfico
        labels = entradas_por_data['data'].dt.strftime('%Y-%m-%d').tolist()
        entradas = entradas_por_data['qtde'].tolist()
        saidas = saidas_por_data['qtde'].tolist()
        print(entradas)
        
        # Dados para o gráfico de tipos de material
        tipos = df.groupby('formato')['qtde'].count().reset_index().sort_values(by='qtde', ascending=False)
        tipos_labels = tipos['formato'].tolist()
        tipos_quantidades = tipos['qtde'].tolist()

        # Contexto para o template      
        context = {
            'total_itens': total_itens,
            'itens_em_baixa': itens_baixa.to_dict(orient='records'),
            'entradas_recentes': entradas_recentes,
            'saidas_recentes': saidas_recentes,
            'labels': labels,
            'entradas': entradas,
            'saidas': saidas,
            'tipos': tipos_labels,
            'quantidades': tipos_quantidades,
        }

        return render(request, 'dashboard.html', context)

    except Exception as e:
        # Captura o erro detalhado e envia ao template
        error_message = traceback.format_exc()
        return render(request, 'dashboard.html', {'error': error_message})