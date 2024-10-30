# Generated by Django 5.1.2 on 2024-10-28 13:20

from django.db import migrations, models


class Migration(migrations.Migration):
    operations = [
        migrations.CreateModel(
            name='Estoque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entrada_saida', models.CharField(max_length=50)),
                ('data', models.CharField(max_length=100)),
                ('qtde', models.IntegerField()),
                ('tipo', models.CharField(max_length=100)),
                ('formato', models.CharField(max_length=100)),
                ('nome', models.CharField(max_length=150)),
                ('tipo_de_material', models.CharField(max_length=100)),
                ('formato_da_folha', models.CharField(max_length=100)),
                ('folha', models.CharField(max_length=100)),
            ],
        ),

    ]
