######################################################## 
# Faculdade: Cesar School                              #
# Curso: Segurança da Informação                       #
# Período: 2025.1                                      #
# Disciplina: Projeto 1                                #
# Professor de Projeto 1: Humberto Caetano             #
# Professora de Fundamentos de Programação: Carol Melo #
# Projeto: App Denúncia de Bullying Anônima            #
# Descrição: Utilidades                                #
# Equipe:                                              #
#           Artur Cavalcanti                           #
#           Eduardo Henrique Ferreira Fonseca Barbosa  #
#           Evandro José Rodrigues Torres Zacarias     #
#           Gabriel de Medeiros Almeida                #
#           Maria Clara Miranda                        #
#           Mauro Sérgio Rezende da Silva              #
#           Silvio Barros Tenório                      #
# Versão: 1.6                                          #
# Data: 24/05/2025                                     #
######################################################## 

import hashlib
import bcrypt
import random
import string
import requests
from dotenv import load_dotenv
import os

# Gerar MD5
def gerar_md5(senha: str) -> str:
    return hashlib.md5(senha.encode('utf-8')).hexdigest()

# Gerar Hash BCrypt
def gerar_hash_bcrypt(senha: str) -> str:
    return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Verifica Hash BCrypt
def verificar_hash_bcrypt(senha: str, hashed: str) -> bool:
    return bcrypt.checkpw(senha.encode('utf-8'), hashed.encode('utf-8'))

# Gerar Senha Forte
def gerar_senha_forte(tamanho=8):
    # Definindo os conjuntos de caracteres
    letras_minusculas = string.ascii_lowercase
    letras_maiusculas = string.ascii_uppercase
    numeros = string.digits
    # simbolos = string.punctuation
    # simbolos = '[!@#$%^&*(),.?":{}|<>]'
    simbolos = '[!@#$%^&*(),.?":{}|]'

    # Garantindo pelo menos um caractere de cada categoria
    senha = [
        random.choice(letras_minusculas),
        random.choice(letras_maiusculas),
        random.choice(numeros),
        random.choice(simbolos)
    ]

    # Preenchendo o restante da senha com caracteres aleatórios de todas as categorias
    todos_caracteres = letras_minusculas + letras_maiusculas + numeros + simbolos
    senha.extend(random.choice(todos_caracteres) for _ in range(tamanho - 4))

    # Embaralhando os caracteres para maior aleatoriedade
    random.shuffle(senha)

    # Convertendo a lista em string
    return ''.join(senha)

# Enviar Email com a Senha para o Usuário
def envia_email(nome, email_destinatario, senha):
    try:
        # Carrega as variáveis do arquivo .env
        load_dotenv()

        # Acessa as variáveis
        chave_api = os.getenv('CHAVE_API')

        # Configurações
        API_KEY = chave_api
        URL = "https://api.brevo.com/v3/smtp/email"

        # Cabeçalhos da requisição
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "api-key": API_KEY
        }

        # Corpo do e-mail (JSON)
        payload = {
            "sender": {
                "name": "App Denúncia de Bullying",
                "email": "denuncia.bullying.anonima@gmail.com"  # Domínio verificado na Brevo
            },
            "to": [{"email": f"{email_destinatario}"}],
            "subject": "Assunto do E-mail",
            "htmlContent": f"<h1>Olá! {nome}</h1><p>Segue a senha para acessar o App Denúncia de Bullying Anônima - Módulo Gerencial:<p>Email: <strong>{email_destinatario}</strong><p>Senha: <strong>{senha}</strong><p>",
            "textContent": "Senha App Denúncia de Bullying Anônima"
        }

        # Enviar e-mail
        response = requests.post(URL, headers=headers, json=payload)

        if response.status_code == 201:
            print("E-mail enviado com sucesso!")
            return True
        else:
            print(f"Erro: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(e)
        return False