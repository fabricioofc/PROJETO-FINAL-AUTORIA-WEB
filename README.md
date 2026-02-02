# Sistema de Gestão de Conteúdo para Blog de Negócios

Este projeto consiste em uma plataforma de gerenciamento de conteúdo (CMS) desenvolvida para a publicação e administração de artigos técnicos sobre empreendedorismo e gestão. A aplicação utiliza o framework Flask para o processamento de rotas e lógica de backend, integrando-se a um banco de dados relacional MySQL para o armazenamento persistente de dados. O sistema oferece uma interface pública para leitores e um painel administrativo restrito para a gestão de posts, categorias e autores.

## Configuração e Execução do Projeto

Para reproduzir o ambiente de execução deste projeto em uma estação de trabalho Windows, siga os procedimentos técnicos descritos abaixo.

## 1. Preparação do Ambiente
Certifique-se de possuir o Python 3 e o MySQL Server instalados em seu sistema.

## 2. Instalação de Dependências
Abra o terminal no diretório raiz do projeto e execute o comando abaixo para instalar as bibliotecas necessárias:
pip install -r requirements.txt
## 3. Configuração do Banco de Dados
1. Crie um banco de dados no MySQL chamado `blog_db`.
2. Execute a importação do arquivo `database.sql` presente na raiz do projeto para estruturar as tabelas e dados iniciais.
3. Caso as credenciais do seu servidor MySQL local sejam diferentes das predefinidas, atualize as configurações no arquivo `app.py` (linhas 18 a 21):
   - `app.config['MYSQL_USER']`
   - `app.config['MYSQL_PASSWORD']`

## 4. Inicialização da Aplicação
Para iniciar o servidor de desenvolvimento, execute o seguinte comando:
python app.py

A aplicação estará acessível através do endereço: http://127.0.0.1:5000

## 5.Credenciais Administrativas
O acesso ao painel de controle pode ser realizado com as seguintes credenciais:
Usuário: admin
Senha: negocios2026

Projeto desenvolvido por Alec e Fabricio, alunos de Informática do IFRN.
