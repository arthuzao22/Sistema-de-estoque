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

    try:
        estoques = Estoque.objects.all().values()
        df = pd.DataFrame(list(estoques))

        df['qtde_placas_unidades'] = df.apply(calcular_qtde_placas, axis=1)
        df['qtde_placas_unidades_sem_tamanho'] = df.apply(calcular_qtde_placas_sem_tamanho, axis=1)
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
        df['qtde_final'] = df[['qtde_placas_unidades', 'qtde_placas_unidades_sem_tamanho', 'qtde_folhas_caixa', 'qtde_bobinas',
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
