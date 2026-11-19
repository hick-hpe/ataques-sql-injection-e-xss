# App Segura — Proteção contra SQL Injection e XSS

Aplicação desenvolvida com Flask e MySQL para demonstrar mecanismos de proteção contra vulnerabilidades comuns em aplicações web, especialmente **SQL Injection (SQLi)** e **Cross-Site Scripting (XSS)**.

O projeto possui funcionalidades equivalentes às da versão vulnerável, permitindo comparar as implementações e compreender como determinadas práticas de desenvolvimento contribuem para a segurança da aplicação.

## Funcionalidades

- Autenticação de usuários;
- Verificação de senhas utilizando hash;
- Listagem de publicações;
- Criação de publicações com título e conteúdo;
- Encerramento de sessão;
- Validação de campos obrigatórios;
- Endpoint para verificação de disponibilidade da aplicação.

## Medidas de segurança implementadas

### SQL Injection (SQLi)

A aplicação utiliza consultas SQL parametrizadas, separando os comandos SQL dos valores fornecidos pelo usuário.

**1. Login**

```python
query = """
    SELECT id, usuario, senha
    FROM usuarios
    WHERE usuario = %s
"""

cursor.execute(query, (usuario,))
```

Os valores são enviados separadamente da instrução SQL, impedindo que entradas fornecidas pelo usuário sejam interpretadas como parte do comando.

**2. Criação de publicações**

O mesmo mecanismo é utilizado na inserção de dados:

```python
query = """
    INSERT INTO posts (titulo, conteudo, usuario_id)
    VALUES (%s, %s, %s)
"""

cursor.execute(
    query,
    (titulo, conteudo, usuario_id)
)
```

Dessa maneira, os dados são tratados como parâmetros, reduzindo o risco de manipulação das consultas SQL.

### Armazenamento seguro de senhas

A aplicação utiliza funções do módulo `werkzeug.security` para trabalhar com senhas.

- `generate_password_hash()`: gera um hash da senha.
- `check_password_hash()`: verifica se a senha informada corresponde ao hash armazenado.

Exemplo:

```python
senha_hash = generate_password_hash(senha)
```

Durante a autenticação:

```python
check_password_hash(resultado['senha'], senha)
```

Assim, a senha não precisa ser armazenada em texto puro no banco de dados.

### Cross-Site Scripting (XSS)

Para evitar a execução de conteúdo HTML ou JavaScript fornecido pelo usuário, a aplicação mantém o escape automático do Jinja.

No template `posts.html`, o conteúdo é renderizado sem utilizar o filtro `safe`:

```jinja2
{{ post.conteudo }}
```

Dessa forma, caracteres especiais são convertidos em suas representações HTML, fazendo com que o conteúdo seja exibido como texto em vez de ser interpretado como código pelo navegador.

Essa medida ajuda a prevenir ataques de **XSS armazenado (Stored XSS)**.

### Gerenciamento de sessão

Após uma autenticação bem-sucedida, a aplicação executa:

```python
session.clear()
```

Isso limpa os dados anteriores da sessão antes de registrar as informações do usuário autenticado.

### Validação de campos

Na criação de publicações, a aplicação verifica se o título e o conteúdo foram preenchidos antes de realizar a inserção no banco de dados.

Também utiliza tratamento de exceções e rollback em caso de falha na operação de inserção.

## Tecnologias utilizadas

- Python 3.12
- Flask
- MySQL 8.4
- mysql-connector-python
- Werkzeug
- Jinja2
- Bootstrap 5.2.3
- Docker
- Docker Compose

## Estrutura do projeto

```text
app-seguro/
├── src/
│   ├── main.py
│   └── templates/
│       ├── criar_post.html
│       ├── login.html
│       └── posts.html
└── README.md
```

## Execução

A aplicação faz parte de um ambiente Docker Compose compartilhado com a versão vulnerável e o banco de dados MySQL.

Para iniciar os serviços, execute o comando na raiz do projeto:

```bash
docker compose up -d --build
```

A aplicação estará disponível em:

**http://localhost:5001**

### Credenciais iniciais

| Usuário | Senha |
|---|---|
| admin | admin123 |

A senha inicial do administrador é convertida para hash quando a aplicação é iniciada.

### Endpoint de saúde

```http
GET /health
```

Retorna uma mensagem indicando que a aplicação está online.

## Observações

- A aplicação utiliza um banco de dados separado da versão vulnerável.
- O hash da senha do administrador é atualizado durante a inicialização da aplicação.
- O modo de depuração do Flask está desativado (`debug=False`).
- O link de cadastro presente na tela de login não possui uma rota implementada.
- A implementação demonstra proteções específicas contra SQL Injection e XSS, mas não contempla todos os mecanismos necessários para uma aplicação em produção.

## Objetivo educacional

O objetivo desta aplicação é demonstrar como práticas de desenvolvimento seguro podem reduzir vulnerabilidades em aplicações web.

Sua implementação permite comparar diretamente os mecanismos de proteção com aqueles utilizados na versão vulnerável, facilitando o entendimento das diferenças entre desenvolvimento vulnerável e desenvolvimento seguro.