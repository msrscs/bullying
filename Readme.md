# Faculdade 
    Cesar School

# Curso
    Segurança da Informação

# Período
    2025.1

# Disciplina
    Projeto 1

# Professor de Projeto 1
    Humberto Caetano

# Professora de Fundamentos de Programação
    Carol Melo

# Equipe
    Artur Cavalcanti
    Eduardo Henrique Ferreira Fonseca Barbosa
    Evandro José Rodrigues Torres Zacarias
    Gabriel de Medeiros Almeida
    Maria Clara Miranda
    Mauro Sérgio Rezende da Silva
    Silvio Barros Tenório

# Projeto
    App de Denúncia de Bullying Anônima

    - Módulo Denunciante
    - Módulo Gerencial

# Comandos
    - Cria ambiente virtual
        python -m venv venv

    - Ativar ambiente virtual
        * Linux/Mac:
            source venv/bin/activate
        * Windows:
            venv/Scripts/activate

    - Lista os pacotes instalados
        pip freeze

    - Gerar arquivo requirements.txt
        pip freeze > requirements.txt

    - Recuperar venv com requirements.txt
        pip install -r ./requirements.txt
    
    - Atualizar o pip
        python.exe -m pip install --upgrade pip

    - Instalar o Flet
        pip install flet[all]
    
    - Instalar o BCrypt:
        pip install bcrypt

# Paleta de Cores
    - paleta_cores.jpg

# Arquivos Python
    - denunciante.py    => App de Denúncia de Bullying Anônima - Módulo Denunciante
    - gerencial.py      => App de Denúncia de Bullying Anônima - Módulo Gerencial
    - dados.py          => Biblioteca de Manipulação do Banco de Dados (utilizado nos dois módulos)
    - utilidades.py     => Biblioteca de Utilidades (utilizado nos dois módulos)
    - teste.py          => Programa de Testes da Biblioteca de Manipulação do Banco de Dados (utilizado apenas para testes)

# Arquivo Banco de Dados SQLite3
    - bullying.db       => Banco de Dados do App de Denúncia de Bullying Anônima

# Utilizado o Serviço de API da Brevo para o envio de e-mail  
    - https://app.brevo.com/
    - Necessário criar o arquivo .env e colocar a chave da API
