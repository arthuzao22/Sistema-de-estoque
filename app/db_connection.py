import sqlitecloud

# URL de conexão do SQLiteCloud
connection_url = "sqlitecloud://cby0ni6znk.sqlite.cloud:8860/Sistema-de-estoque?apikey=7f61CyMIbBwy4rxeMLdJtrUFaYu44AJ8LoARGrHeHS8"

# Função para obter a conexão com o SQLiteCloud
def get_connection():
    return sqlitecloud.connect(connection_url)
