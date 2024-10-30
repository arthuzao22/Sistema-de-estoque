from django.db import models

# Create your models here.
class Estoque(models.Model):
    entrada_saida = models.CharField(max_length=50)
    data = models.DateField()
    qtde = models.IntegerField()
    tipo = models.CharField(max_length=100)
    formato = models.CharField(max_length=100)
    nome = models.CharField(max_length=150)
    tipo_de_material = models.CharField(max_length=100)
    formato_da_folha = models.CharField(max_length=100)
    folha = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
