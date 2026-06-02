# Prova Técnica — Desenvolvedor Backend

Projeto desenvolvido como parte de uma prova técnica para a vaga de Desenvolvedor Backend.

A solução foi construída em Python utilizando FastAPI, SQLite, SQLAlchemy, Pydantic, autenticação JWT, integração simples com modelo de Machine Learning e execução com Docker.

---

## Objetivo

O objetivo do projeto é atender às quatro partes propostas na prova:

1. Responder uma questão teórica sobre uma arquitetura de serviços para drones.
2. Criar uma API RESTful com CRUD de usuários.
3. Integrar a API com um modelo de IA para realizar predições numéricas.
4. Criar Dockerfile e docker-compose.yml para execução da aplicação em containers.

---

## Tecnologias utilizadas

- Python
- FastAPI
- Uvicorn
- SQLite
- SQLAlchemy
- Pydantic
- JWT com python-jose
- Passlib e bcrypt para hash de senha
- Scikit-learn
- Joblib
- Docker
- Docker Compose
- Jupyter Notebook

---

## Estrutura do projeto

```text
.
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── users.py
│   │   └── predict.py
│   └── services/
│       └── prediction_service.py
├── model/
│   └── model.joblib
├── train_model.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── Prova_Tecnica_Desenvolvedor_Backend_Victor_Prates.ipynb
```

---

## Funcionalidades implementadas

### Parte 1 — Questão teórica

A resposta teórica sobre a arquitetura de drones está documentada no notebook:

```text
Prova_Tecnica_Desenvolvedor_Backend_Victor_Prates.ipynb
```

A resposta descreve o papel dos principais componentes da arquitetura, como Gateway/Kong, API REST, banco de dados, Storage S3, proxy de segurança, Prometheus, Grafana e containers.

---

### Parte 2 — API RESTful com CRUD

A API possui CRUD de usuários com os seguintes campos:

- `id`
- `name`
- `email`
- `hashed_password`
- `is_active`
- `created_at`

Rotas principais:

```text
POST   /users/
GET    /users/
GET    /users/{user_id}
PUT    /users/{user_id}
DELETE /users/{user_id}
```

A rota `POST /users/` permite criar um novo usuário.

As demais rotas de usuários são protegidas por autenticação JWT.

A rota `DELETE /users/{user_id}` realiza soft delete, alterando o campo `is_active` para `false`, em vez de remover o usuário definitivamente do banco.

---

### Parte 3 — Integração com modelo de IA

Foi criado um modelo simples de regressão linear com `scikit-learn`.

O objetivo dessa etapa é demonstrar o fluxo de integração entre uma API e um modelo treinado.

O modelo é treinado pelo script:

```bash
python train_model.py
```

Após o treinamento, o modelo é salvo em:

```text
model/model.joblib
```

A rota de predição é:

```text
POST /predict/
```

Exemplo de entrada:

```json
{
  "feature_1": 1,
  "feature_2": 10,
  "feature_3": 100
}
```

Exemplo de resposta:

```json
{
  "prediction": 15.0
}
```

A rota `/predict/` é protegida por token JWT.

---

### Parte 4 — Docker e Docker Compose

A aplicação possui `Dockerfile` e `docker-compose.yml` para facilitar a execução em container.

Como o projeto utiliza SQLite, não foi criado um container separado para banco de dados. O banco é persistido por volume configurado no Docker Compose.

---

## Autenticação

A API utiliza autenticação JWT.

Rotas públicas:

```text
GET  /
POST /users/
POST /auth/login
```

Rotas protegidas por token JWT:

```text
GET    /users/
GET    /users/{user_id}
PUT    /users/{user_id}
DELETE /users/{user_id}
POST   /predict/
```

Para acessar rotas protegidas, é necessário realizar login em:

```text
POST /auth/login
```

O login retorna um token JWT, que deve ser enviado no cabeçalho das próximas requisições:

```text
Authorization: Bearer <token>
```

---

## Como rodar localmente

### 1. Criar ambiente virtual

```bash
python -m venv .venv
```

### 2. Ativar ambiente virtual

No Windows:

```bash
.venv\Scripts\activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Treinar o modelo

```bash
python train_model.py
```

### 5. Rodar a API

```bash
uvicorn app.main:app --reload
```

Acesse a API em:

```text
http://127.0.0.1:8000
```

Documentação Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## Como rodar com Docker

### Subir aplicação

```bash
docker compose up --build
```

Acesse a documentação em:

```text
http://127.0.0.1:8000/docs
```

### Encerrar containers

```bash
docker compose down
```

---

## Exemplos de uso

### Criar usuário

Rota:

```text
POST /users/
```

Body:

```json
{
  "name": "Victor Prates",
  "email": "victor.teste@email.com",
  "password": "123456"
}
```

Resposta esperada:

```json
{
  "name": "Victor Prates",
  "email": "victor.teste@email.com",
  "id": 1,
  "is_active": true,
  "created_at": "2026-06-02T..."
}
```

---

### Login

Rota:

```text
POST /auth/login
```

No Swagger, preencher:

```text
username: victor.teste@email.com
password: 123456
```

Resposta esperada:

```json
{
  "access_token": "token_jwt_gerado",
  "token_type": "bearer"
}
```

---

### Predição

Rota protegida:

```text
POST /predict/
```

Body:

```json
{
  "feature_1": 1,
  "feature_2": 10,
  "feature_3": 100
}
```

Resposta esperada:

```json
{
  "prediction": 15.0
}
```

---

## Observações técnicas

- Para simplificar a prova técnica, as tabelas são criadas automaticamente com `Base.metadata.create_all`.
- Em um ambiente de produção, o ideal seria utilizar migrations com Alembic.
- O `SECRET_KEY` está fixo no código para simplificar a execução da prova. Em produção, deveria ser configurado via variável de ambiente.
- O modelo de IA utilizado é simples e fictício, com foco em demonstrar o fluxo de integração entre API e modelo treinado.
- O SQLite foi escolhido por ser simples, leve e adequado para testes técnicos.
- A autenticação JWT foi aplicada nas rotas sensíveis da API.

---

## Autor

Victor Prates