# 📊 API de Contas a Pagar e Receber (FastAPI + SQLAlchemy)

Este projeto fornece uma API para gerenciar contas a pagar e a receber, desenvolvida com **FastAPI** e **SQLAlchemy**. Ela se conecta a um banco de dados PostgreSQL e realiza operações de **CRUD**.

---

## 🚀 Como executar o projeto localmente

### 1️⃣ Pré-requisitos

- Python 3.11 ou superior
- PostgreSQL instalado e rodando
- Git (opcional)

---

### 2️⃣ Criar o banco de dados

Você deve criar manualmente um banco de dados PostgreSQL com o seguinte nome:

```sql
CREATE DATABASE db_fastapi;
```

---

### 3️⃣ Criar o arquivo `.env`

Você **deve criar um arquivo `.env`** na raiz do projeto com os dados de conexão com seu banco PostgreSQL. Exemplo:

```env
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
DB_NAME=db_fastapi
```

---

### 4️⃣ Instalar dependências

Ative seu ambiente virtual (se necessário) e instale as dependências com:

```bash
pip install -r requirements.txt
```

---

### 5️⃣ Criar as tabelas e inserir dados iniciais

Depois de criar o banco e configurar o `.env`, execute o seguinte comando:

```bash
python criar_db.py
```

Este script irá:
- Criar a tabela `contas_a_pagar_e_receber`
- Inserir dados iniciais:
  - `{id: 1, descricao: "Aluguel", valor: 1000.5, tipo: "PAGAR"}`
  - `{id: 2, descricao: "Salário", valor: 5000.0, tipo: "RECEBER"}`

---

### 6️⃣ Rodar a API

Com tudo configurado, execute a aplicação com:

```bash
uvicorn main:app --reload --port 8001
```

A API estará disponível em: [http://localhost:8001](http://localhost:8001)

---

## 📌 Endpoints principais

- `GET /contas-a-pagar-e-receber/`: Listar contas
- `GET /contas-a-pagar-e-receber/{id}`: Buscar por ID
- `POST /contas-a-pagar-e-receber/`: Criar conta
- `PUT /contas-a-pagar-e-receber/{id}`: Atualizar conta
- `DELETE /contas-a-pagar-e-receber/{id}`: Excluir conta

---

## 🧪 Rodar os testes

```bash
python -m pytest
```

---

## 👨‍💻 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir *issues* ou *pull requests*.

---