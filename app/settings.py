# =======================================
# IMPORTAÇÃO DAS BIBLIOTECAS
# =======================================
from dotenv import load_dotenv
import os


# =======================================
# CONFIGURAÇÕES DA APLICAÇÃO
# =======================================

# Carrega as varáveis de ambiente definidas no arquivo .env
# Para o ambiente de execução da aplicação.
load_dotenv()

# Obtém a URL de conxão com o banco de dados.
# A variável DATABASE_URL deve estar definida no arquivo .env.
DATABASE_URL = os.getenv("DATABASE_URL") 
