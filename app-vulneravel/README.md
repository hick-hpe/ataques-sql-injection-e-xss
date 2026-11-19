# App Vulnerável — SQL Injection e XSS

Aplicação desenvolvida com Flask e MySQL para demonstrar vulnerabilidades comuns em aplicações web, especialmente **SQL Injection (SQLi)** e **Cross-Site Scripting (XSS)**.

O projeto simula um sistema de autenticação e gerenciamento de publicações, permitindo observar como a ausência de validação e de mecanismos adequados de proteção pode comprometer a segurança da aplicação.

> **Atenção:** esta aplicação é intencionalmente vulnerável e deve ser utilizada exclusivamente em ambiente local e controlado, para fins educacionais.

## Funcionalidades

- Autenticação de usuários;
- Listagem de publicações;
- Criação de publicações com título e conteúdo;
- Encerramento de sessão;
- Endpoint para verificação de disponibilidade da aplicação.

## Vulnerabilidades demonstradas

### SQL Injection (SQLi)

A aplicação utiliza concatenação direta de valores fornecidos pelo usuário na construção de consultas SQL.

**1. Login**

A consulta de autenticação utiliza uma f-string para inserir diretamente os dados recebidos do formulário:

```python
query = f"""
    SELECT * FROM usuarios
    WHERE usuario = '{usuario}'
    AND senha = '{senha}'
"""
```

Isso permite que entradas especialmente construídas alterem a lógica da consulta SQL.

**2. Criação de publicações**

O mesmo problema ocorre na inserção de publicações:

```python
query = f"""
    INSERT INTO posts (titulo, conteudo, usuario_id)
    VALUES ('{titulo}', '{conteudo}', '{usuario_id}')
"""
```

Como os valores são concatenados diretamente à instrução, a aplicação fica suscetível à manipulação da consulta.

### Cross-Site Scripting (XSS)

A vulnerabilidade de XSS está presente na renderização do conteúdo das publicações.

No template `posts.html`, é utilizado o filtro `safe` do Jinja:

```jinja2
{{ post.conteudo | safe }}
```

Esse filtro desativa o escape automático para o conteúdo renderizado, fazendo com que marcações HTML e scripts fornecidos pelo usuário possam ser interpretados pelo navegador.

Nesse cenário, temos um exemplo de **XSS armazenado (Stored XSS)**, pois o conteúdo malicioso pode ser salvo no banco de dados e executado posteriormente quando outro usuário visualizar a publicação.

## Tecnologias utilizadas

- Python 3.12
- Flask
- MySQL 8.4
- mysql-connector-python
- Jinja2
- Bootstrap 5.2.3
- Docker
- Docker Compose

## Estrutura do projeto

```text
app-vulneravel/
├── src/
│   ├── main.py
│   └── templates/
│       ├── criar_post.html
│       ├── login.html
│       └── posts.html
└── README.md
```

## Execução

A aplicação faz parte de um ambiente Docker Compose compartilhado com a versão segura e o banco de dados MySQL.

Para iniciar os serviços, execute o comando na raiz do projeto:

```bash
docker compose up -d --build
```

A aplicação estará disponível em:

**http://localhost:5000**

### Credenciais iniciais

| Usuário | Senha |
|---|---|
| admin | admin123 |

### Endpoint de saúde

```http
GET /health
```

Retorna uma mensagem indicando que a aplicação está online.

## Observações

- As senhas são armazenadas em texto puro nesta versão.
- A aplicação utiliza `debug=True`.
- Não há consultas SQL parametrizadas nas operações vulneráveis.
- O escape automático do Jinja é desativado para o conteúdo das publicações por meio do filtro `safe`.
- O link de cadastro presente na tela de login não possui uma rota implementada.

## Objetivo educacional

O objetivo desta aplicação é demonstrar, de maneira prática, como vulnerabilidades de SQL Injection e XSS podem surgir durante o desenvolvimento de aplicações web, permitindo analisar seus impactos e comparar posteriormente com uma implementação que utiliza mecanismos de proteção.