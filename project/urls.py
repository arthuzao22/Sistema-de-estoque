from django.contrib import admin
from django.urls import path
from app.views import home, form, create, edit, update, delete, estoque, index_btn

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
]