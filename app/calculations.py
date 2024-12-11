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
        elif material == "ADESIVO FOSCO" and formato == "660x960":
            return qtde * 900
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
    # Agrupa as entradas por tipo_de_material e formato_da_folha
    entradas = df[df['entrada_saida'] == 'Entrada'].groupby(['tipo_de_material', 'formato_da_folha'])['qtde_final'].sum()
    # Agrupa as saídas por tipo_de_material e formato_da_folha
    saidas = df[df['entrada_saida'] == 'Saida'].groupby(['tipo_de_material', 'formato_da_folha'])['qtde_final'].sum()
    # Calcula o estoque total considerando as entradas e saídas
    estoque_total = entradas.subtract(saidas, fill_value=0).reset_index(name='estoque_total')
    return estoque_total


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
    entradas = df[df['entrada_saida'] == 'Entrada'].groupby(['tipo_de_material', 'tipo', 'formato_da_folha'])['qtde'].sum()
    saidas = df[df['entrada_saida'] == 'Saida'].groupby(['tipo_de_material', 'tipo', 'formato_da_folha'])['qtde'].sum()
    
    # Calcula o estoque total
    estoque_total_geral = entradas.subtract(saidas, fill_value=0).reset_index(name='estoque_total') 
    
    return estoque_total_geral