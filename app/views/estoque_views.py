from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .calculos import (calcular_qtde_placas, calcular_qtde_placas_sem_tamanho,
                       calcular_qtde_caixas, calcular_qtde_bobinas, calcular_qtde_bobinas_ensacamento,
                       calcular_contra_capa, calcular_granpeador, calcular_grampos,
                       calcular_caixa_2, calcular_tintas_toners, calcular_Wireo, calcular_estoque_total)

