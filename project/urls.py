from django.urls import path
from app import views  # Ajuste conforme o nome da sua aplicação

urlpatterns = [
    path('home/', views.home, name='home'),
    path('form/', views.form, name='form'),
    path('create/', views.create, name='create'),
    path('home/edit/<int:pk>/', views.edit, name='edit'),
    path('update/<int:pk>/', views.update, name='update'),
    path('home/delete/<int:pk>/', views.delete, name='delete'),
    path('estoque/', views.estoque, name='estoque'),
    path('', views.index_btn, name='index_btn'),
    path('download-db/', views.download_database, name='download_database'),
    path('login/', views.login_view, name='login'),  # Certifique-se de que esta URL está correta
    path('register/', views.register_view, name='register_view'),
    path('subir/', views.subir_para_base_de_dados, name='subir_para_base_de_dados'),
]
