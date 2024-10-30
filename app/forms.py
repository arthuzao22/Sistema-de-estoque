from django.forms import ModelForm
from app.models import Estoque 

class EstoqueForm(ModelForm):
    
    class Meta:
        model = Estoque
        fields = ['entrada_saida', 'data', 'qtde', 'tipo', 'formato', 'nome', 'tipo_de_material', 'formato_da_folha', 'folha']
