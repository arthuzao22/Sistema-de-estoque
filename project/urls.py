from django.contrib import admin
from django.urls import path
from app import views
from app.views import home, form, create, edit, update, delete, estoque, index_btn, download_database, login_view  # Adicionei o login_view aqui

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'),
    path('form/', form, name='form'),
    path('create/', create, name='create'),
    path('home/edit/<int:pk>/', edit, name='edit'),
    path('update/<int:pk>/', update, name='update'),
    path('home/delete/<int:pk>/', delete, name='delete'),
    path('estoque/', estoque, name='estoque'),
    path('', index_btn, name='index_btn'),
    path('download-db/', download_database, name='download_database'),
    path('login/', login_view, name='login'),
    path('register/', views.register_view, name='register_view'),  # Corrigido para utilizar views
]
