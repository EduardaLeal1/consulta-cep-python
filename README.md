Consulta e registro de CEP

Objetivo:
Este projeto permite consultar informações de endereço a partir de um CEP utilizando a API ViaCEP e registrar os dados em um banco MySQL local.


Estrutura do projeto:

- CEP.py → Script principal em Python que consulta a API e insere os dados no banco.  
- estrutura-banco.sql → Contém os comandos SQL para criar a tabela enderecos (apenas a estrutura, sem registros por enquanto).  
- .env → Arquivo para armazenar as credenciais do banco MySQL (não deve ser enviado ao GitHub).  
- .gitignore → Ignora arquivos sensíveis e caches do Python.


Pré-requisitos:

- Python 3.14 ou superior  
- MySQL instalado localmente  
- Bibliotecas Python: requests, mysql-connector-python, python-dotenv

Instalação das bibliotecas:

bash
pip install requests mysql-connector-python python-dotenv


Configuração do Banco de Dados:

1- Crie um banco MySQL local chamado consulta_cep;
2- Execute o arquivo estrutura-banco.sql para criar a tabela enderecos.

    CREATE TABLE enderecos (
      id INT AUTO_INCREMENT PRIMARY KEY,
      cep VARCHAR(9) NOT NULL,
      logradouro VARCHAR(255),
      complemento VARCHAR(255),
      bairro VARCHAR(255),
      localidade VARCHAR(255),
      uf CHAR(2)
      );


Configuração do .env: 

1- Crie um arquivo .env na raiz do projeto com as seguintes variáveis.

    DB_HOST=127.0.0.1
    DB_USER=root
    DB_PASS=sua_senha_mysql
    DB_NAME=consulta_cep

OBS: Nunca envie o .env para o GitHub. Ele contém informações sensíveis.

Como Executar:

1- Abra o terminal na pasta do projeto.
2- Execute o script:
    
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

3- Digite o CEP desejado (apenas números).
4- O script retornará os dados do endereço e registrará no banco MySQL.

Observações:

O projeto é para fins de aprendizado e demonstração.
O arquivo estrutura-banco.sql permite recriar a tabela enderecos sem expor dados sensíveis.




