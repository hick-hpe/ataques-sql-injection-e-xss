# Laboratório de SQL Injection e XSS

Projeto educacional para demonstrar, em ambiente local e controlado, vulnerabilidades de **SQL Injection (SQLi)** e **Cross-Site Scripting (XSS)**. O repositório contém duas versões de uma pequena aplicação de publicações: uma vulnerável e outra com medidas de proteção.

## Aplicações

| Aplicação | Endereço local | Objetivo |
|---|---|---|
| [App vulnerável](app-vulneravel/README.md) | http://localhost:5000 | Demonstrar falhas de SQL Injection e XSS |
| [App segura](app-seguro/README.md) | http://localhost:5001 | Comparar as falhas com implementações de proteção |

As duas aplicações usam Flask, MySQL e templates Jinja. O banco é executado em um contêiner separado.

## Requisitos

- Docker
- Docker Compose (plugin `docker compose`)
- Git, caso queira clonar o repositório

Não é necessário instalar Python ou MySQL diretamente na máquina: as dependências e o banco são executados pelos contêineres.

## Como executar

Na raiz do projeto, onde está o arquivo `docker-compose.yml`:

```bash
docker compose up -d --build
```

Aguarde o banco MySQL ficar saudável e as aplicações iniciarem. Depois, acesse:

- App vulnerável: http://localhost:5000
- App segura: http://localhost:5001
- Verificação de saúde da app vulnerável: http://localhost:5000/health
- Verificação de saúde da app segura: http://localhost:5001/health

As duas aplicações compartilham o mesmo servidor MySQL, mas utilizam bancos separados: `app_posts_vulneravel` e `app_posts_seguro`.

## Credenciais iniciais

O script `mysql/init.sql` cria o usuário de demonstração abaixo em ambos os bancos:

| Usuário | Senha inicial |
|---|---|
| `admin` | `admin123` |

Na aplicação segura, a senha é convertida para hash quando a aplicação inicia. Na aplicação vulnerável, a senha permanece armazenada em texto puro, conforme o propósito didático do exemplo.

> Essas credenciais são públicas e servem somente para o laboratório. Não reutilize esse padrão em aplicações reais.

## O que observar

### SQL Injection

- **App vulnerável:** a consulta de login e a inserção de publicações são montadas por interpolação direta dos dados recebidos do formulário.
- **App segura:** utiliza parâmetros (`%s`) nas consultas SQL, separando os dados fornecidos pelo usuário da instrução SQL.

### Cross-Site Scripting (XSS)

- **App vulnerável:** o conteúdo da publicação é renderizado com o filtro Jinja `safe`, desativando o escape automático naquele campo.
- **App segura:** o conteúdo é renderizado sem o filtro `safe`, mantendo o escape automático do Jinja.

### Outras diferenças

- A aplicação segura armazena a senha usando `generate_password_hash` e valida com `check_password_hash`.
- A aplicação segura limpa a sessão antes de definir os dados da autenticação.
- A aplicação vulnerável utiliza `debug=True`; a segura utiliza `debug=False`.

## Comandos úteis

Os comandos abaixo estão disponíveis no `Makefile`:

| Comando | Descrição |
|---|---|
| `make build` | Constrói as imagens e inicia os contêineres |
| `make up` | Inicia os contêineres em segundo plano |
| `make down` | Para e remove os contêineres, preservando o volume do banco |
| `make downv` | Para e remove os contêineres e também os volumes |
| `make ps` | Exibe o estado dos contêineres |
| `make logs` | Acompanha os logs dos serviços |
| `make db-root` | Abre o cliente MySQL como `root` |
| `make db` | Abre o cliente MySQL como `app_user` |

Também é possível usar diretamente:

```bash
docker compose logs -f
docker compose ps
docker compose down
```

Para apagar os dados persistidos do MySQL e recriar o ambiente do zero:

```bash
docker compose down -v
docker compose up -d --build
```

**Atenção:** `down -v` remove o volume `mysql_data` e, consequentemente, os dados dos dois bancos.

## Estrutura do projeto

```text
.
├── app-vulneravel/
│   ├── README.md
│   └── src/
│       ├── main.py
│       └── templates/
├── app-seguro/
│   ├── README.md
│   └── src/
│       ├── main.py
│       └── templates/
├── mysql/
│   └── init.sql
├── docker-compose.yml
├── Dockerfile
├── Makefile
└── requirements.txt
```

## Limitações conhecidas


- O laboratório utiliza credenciais e chaves fixas no `docker-compose.yml` como conveniência didática.
- O serviço Flask é iniciado com o servidor de desenvolvimento integrado; não é uma configuração de produção.
- A aplicação segura demonstra proteções específicas para SQLi e XSS, mas não deve ser considerada uma aplicação completamente protegida ou pronta para produção.

## Uso responsável

Utilize este projeto somente em sua própria máquina ou em ambiente para o qual você tenha autorização explícita. Não exponha a versão vulnerável à internet nem teste os exemplos contra sistemas de terceiros.

## Tecnologias

- Python 3.12
- Flask
- MySQL 8.4
- mysql-connector-python
- Jinja
- Bootstrap 5.2.3
- Docker e Docker Compose
""",
"app-vulneravel/README.md": """# App vulnerável

Aplicação Flask criada para demonstrar, de forma controlada, exemplos de **SQL Injection (SQLi)** e **Cross-Site Scripting (XSS)**. Ela simula um sistema simples de login e publicação de conteúdo.

> Execute somente em ambiente local e isolado. Não utilize esta aplicação em produção nem a exponha à internet.

## Executar

A aplicação é iniciada junto com o banco MySQL pelo Compose da raiz do repositório. Consulte o [README geral](../README.md) para os requisitos e comandos.

Depois de iniciar os serviços, acesse:

**http://localhost:5000**

Credenciais iniciais:

- Usuário: `admin`
- Senha: `admin123`

## Funcionalidades

- Login de usuário.
- Listagem de publicações.
- Criação de publicações com título e conteúdo.
- Encerramento da sessão.
- Endpoint `/health` para verificar se a aplicação está online.

## Vulnerabilidades demonstradas

### 1. SQL Injection no login

Em `src/main.py`, os valores recebidos do formulário são inseridos diretamente na string SQL por meio de uma f-string:

```python
query = f"""
    SELECT * FROM usuarios
    WHERE usuario = '{usuario}'
    AND senha = '{senha}'
"""
```

Como os dados são concatenados à instrução, entradas especialmente construídas podem alterar a lógica da consulta.

### 2. SQL Injection na criação de publicações

A rota de criação também monta o `INSERT` por concatenação direta:

```python
query = f"""
    INSERT INTO posts (titulo, conteudo, usuario_id)
    VALUES ('{titulo}', '{conteudo}', '{usuario_id}')
"""
```

Os campos recebidos do formulário não são enviados como parâmetros separados.

### 3. XSS armazenado

No template `src/templates/posts.html`, o conteúdo da publicação é renderizado assim:

```jinja2
{{ post.conteudo | safe }}
```

O filtro `safe` informa ao Jinja que o valor deve ser tratado como HTML seguro, impedindo o escape automático nesse ponto. Se um usuário armazenar marcação ou código HTML/JavaScript no conteúdo, ele poderá ser interpretado pelo navegador de quem visualizar a publicação.

## Como analisar

1. Inicie o ambiente pela raiz do projeto.
2. Entre com as credenciais de demonstração.
3. Observe no código de `src/main.py` como as consultas SQL são construídas.
4. Compare a renderização de `post.conteudo` com a versão segura.
5. Faça testes somente no laboratório local e observe o comportamento do navegador e da aplicação.

## Estrutura

```text
app-vulneravel/
├── README.md
└── src/
    ├── main.py
    └── templates/
        ├── criar_post.html
        ├── login.html
        └── posts.html
```

## Observações

- A senha inicial é armazenada em texto puro no banco desta versão.
- A aplicação é iniciada com `debug=True`.
- Esta aplicação é intencionalmente vulnerável: não reutilize seu código como base de um sistema real.
""",
"app-seguro/README.md": """# App segura

Aplicação Flask que apresenta medidas de proteção contra **SQL Injection (SQLi)** e **Cross-Site Scripting (XSS)**. Ela possui as mesmas funcionalidades básicas da versão vulnerável, permitindo comparar as implementações.

> Esta versão demonstra algumas práticas de segurança, mas não representa, por si só, uma aplicação completa ou pronta para produção.

## Executar

A aplicação é iniciada junto com o banco MySQL pelo Compose da raiz do repositório. Consulte o [README geral](../README.md) para os requisitos e comandos.

Depois de iniciar os serviços, acesse:

**http://localhost:5001**

Credenciais iniciais:

- Usuário: `admin`
- Senha: `admin123`

A senha inicial é atualizada para um hash quando a aplicação inicia.

## Funcionalidades

- Login de usuário.
- Listagem de publicações.
- Criação de publicações com título e conteúdo.
- Encerramento da sessão.
- Endpoint `/health` para verificar se a aplicação está online.

## Proteções implementadas

### 1. Consultas SQL parametrizadas

As consultas que recebem dados do usuário utilizam placeholders `%s` e passam os valores separadamente:

```python
query = """
    SELECT id, usuario, senha
    FROM usuarios
    WHERE usuario = %s
"""

cursor.execute(query, (usuario,))
```

Na criação de publicações, os valores também são enviados como parâmetros:

```python
query = """
    INSERT INTO posts (titulo, conteudo, usuario_id)
    VALUES (%s, %s, %s)
"""

cursor.execute(query, (titulo, conteudo, usuario_id))
```

Dessa forma, os dados são tratados como valores da consulta, em vez de serem concatenados à instrução SQL.

### 2. Hash de senha

A aplicação utiliza funções do `werkzeug.security`:

- `generate_password_hash()` para gerar o hash da senha.
- `check_password_hash()` para verificar a senha informada no login.

A senha não é comparada diretamente com um valor em texto puro durante a autenticação.

### 3. Escape automático contra XSS

No template `src/templates/posts.html`, o conteúdo é renderizado sem o filtro `safe`:

```jinja2
{{ post.conteudo }}
```

O Jinja aplica o escape automático no contexto HTML, fazendo com que marcações fornecidas pelo usuário sejam exibidas como texto, em vez de serem interpretadas como HTML executável.

## Como analisar

1. Inicie o ambiente pela raiz do projeto.
2. Entre com as credenciais de demonstração.
3. Compare as consultas SQL desta versão com as de `app-vulneravel`.
4. Compare a renderização de `post.conteudo` nos dois templates.
5. Observe como o armazenamento e a verificação da senha diferem entre as versões.

## Estrutura

```text
app-seguro/
├── README.md
└── src/
    ├── main.py
    └── templates/
        ├── criar_post.html
        ├── login.html
        └── posts.html
```

## Observações e limitações

- A função `iniciar_banco()` define a senha do usuário `admin` como `admin123` e grava seu hash sempre que a aplicação inicia. Isso é adequado apenas à demonstração e deve ser substituído por um fluxo apropriado de criação/gerenciamento de usuários em um sistema real.
- A aplicação é iniciada com `debug=False`, mas ainda utiliza o servidor de desenvolvimento do Flask.
- O projeto não implementa todas as proteções necessárias para uma aplicação web em produção; por exemplo, não há proteção CSRF explícita nos formulários.