import requests
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# ====== CONEXÃO COM O BANCO ======
conexao = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")
)

cursor = conexao.cursor()

cep = input ("Digite o seu CEP (apenas números): ")

while len (cep) != 8 or not cep.isdigit():
    print ("CEP incorreto, digite novamente apenas os números.")
    cep = input ("Digite o seu CEP: ")

url = f"https://viacep.com.br/ws/{cep}/json/"

resposta = requests.get(url)

dados = resposta.json()

cep_tratado = {
    "cep": dados.get("cep"),
    "logradouro": dados.get("logradouro"),
    "complemento": dados.get("complemento"),
    "bairro": dados.get("bairro"),
    "localidade": dados.get("localidade"),
    "uf": dados.get("uf")
}

print(cep_tratado)

# ====== INSERIR NO BANCO DE DADOS ======
sql = """
INSERT INTO enderecos (cep, logradouro, complemento, bairro, localidade, uf)
VALUES (%s, %s, %s, %s, %s, %s)
"""

valores = (
    cep_tratado["cep"],
    cep_tratado["logradouro"],
    cep_tratado["complemento"],
    cep_tratado["bairro"],
    cep_tratado["localidade"],
    cep_tratado["uf"]
)

cursor.execute(sql, valores)
conexao.commit()

print("\nDados inseridos no banco com sucesso!")

cursor.close()
conexao.close()