# Task Manager Application Backend

Este repositório contém uma aplicação **FastAPI** para gerenciamento de tarefas, integrada com **PostgreSQL** e utilizando **Alembic** para migrações de banco de dados. A aplicação também faz uso do **Poetry** para gerenciamento de dependências.

## Requisitos

Antes de iniciar, certifique-se de ter as seguintes ferramentas instaladas em seu sistema:

- **Docker**: Para criar containers e orquestrar a aplicação e o banco de dados.
- **Docker Compose**: Para facilitar o gerenciamento dos serviços.
- **Poetry**: Para gerenciar as dependências do projeto.

## Configurações Iniciais

### 1. Variáveis de Ambiente

A aplicação usa variáveis de ambiente para configurar a conexão com o banco de dados e outros parâmetros de execução. Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
# .env

# Configurações do Banco de Dados
DATABASE_URL=postgresql+asyncpg://<username>:<password>@db:5432/taskmanager
DATABASE_URL_TEST=postgresql+asyncpg://<username>:<password>@db:5433/taskmanager_test

# Configurações do JWT
SECRET_KEY=your-secret-key

# Outros parâmetros
ENVIRONMENT=dev
```

A variável `ENVIRONMENT` deve ser configurada como `dev`, `test` ou `prd`, dependendo do ambiente de execução.
Ao executar os testes com `pytest` automáticamente será atualizado para `test`.

### 2. Instalar Dependências Localmente

Se você pretende rodar a aplicação localmente, use o **Poetry** para instalar as dependências.

```bash
poetry install
```

### 3. Executando com Docker e Docker Compose

A maneira mais simples de iniciar a aplicação é usando **Docker** e **Docker Compose**.

#### Passos:

1. **Build da Aplicação**:

   Execute o seguinte comando para construir a imagem Docker da aplicação:

   ```bash
   docker-compose build
   ```

2. **Iniciar os Containers**:

   Inicie a aplicação e o banco de dados:

   ```bash
   docker-compose up
   ```

3. **Aplicar Migrações**:

   O script de inicialização do container irá automaticamente aguardar o PostgreSQL estar pronto e, em seguida, aplicar as migrações:

   ```bash
   # O script de inicialização já cuida disso, mas você pode aplicar manualmente se necessário:
   docker-compose exec web alembic upgrade head
   ```

4. **Acessar a Aplicação**:

   A aplicação estará disponível em [http://localhost:8000](http://localhost:8000).

   Você também pode acessar a documentação interativa **Swagger UI** em [http://localhost:8000/docs](http://localhost:8000/docs).

### 4. Rodando os Testes

Se você configurou os testes com **pytest**, você pode executá-los da seguinte maneira:

1. **Dentro do Container Docker**:

   Para rodar os testes no ambiente Docker, use o seguinte comando:

   ```bash
   docker-compose exec web poetry run pytest
   ```

2. **Localmente** (se as dependências estiverem instaladas via Poetry):

   ```bash
   poetry run pytest
   ```

### 5. Configurações Adicionais para Produção

Para rodar a aplicação em ambiente de produção, alguns ajustes são recomendados:

1. **Desabilitar o modo `--reload`** no arquivo `docker-compose.yml` ou no script de inicialização.
   
2. **Utilizar um Servidor de Produção**:
   - Use um servidor como **Gunicorn** ou outro server de WSGI/ASGI para servir a aplicação em produção.

### Estrutura do Projeto

A estrutura do projeto segue a arquitetura **Clean Architecture** com as seguintes pastas principais:

```bash
├── .github           # Workflows CI/CD
├── docker            # Configurações dos containers
├── app
│   ├── core          # Configurações e autenticação
│   ├── domain        # Entidades e casos de uso
│   ├── infra         # Repositórios e integração com DB
│   ├── http          # Rotas e controllers (FastAPI)
│   ├── tests         # Testes unitários e E2E    
│   └── main.py       # Ponto de entrada da aplicação
├── alembic           # Migrações de banco de dados
├── .env              # Variáveis de ambiente
├── pytest.ini        # Configurações do pytest
├── docker-compose.yml # Orquestração do Docker
├── Dockerfile        # Arquivo para build da imagem Docker
└── pyproject.toml    # Arquivo de configuração do Poetry
```

## Comandos Úteis

### Iniciar e Parar os Containers

- **Iniciar os containers**:

  ```bash
  docker-compose up -d
  ```

- **Parar os containers**:

  ```bash
  docker-compose down
  ```

### Executar Migrações com Alembic

- **Criar uma nova migração**:

  ```bash
  docker-compose exec web alembic revision --autogenerate -m "Descrição da migração"
  ```

- **Aplicar migrações**:

  ```bash
  docker-compose exec web alembic upgrade head
  ```

### Limpeza do Banco de Dados (Destruir Dados)

Para destruir todos os dados e parar os containers:

```bash
docker-compose down -v
```

---

Essa documentação fornece um guia básico para configurar, rodar e testar sua aplicação com **FastAPI**, **Poetry**, **PostgreSQL** e **Docker**.