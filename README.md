![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-darkblue)

# 🔐 Auth API

API de autenticação completa e reutilizável, construída com **FastAPI** e **PostgreSQL**.

> Criada para ser plugada em qualquer projeto que precise de autenticação — sem ter que reinventar a roda toda vez.

---

## 💡 Autenticação? O que é isso?

Autenticação é o sistema que responde à pergunta *"quem é você?"* em um app. Todo projeto web precisa disso — login, cadastro, senha esquecida, login com Google...

Em vez de reescrever essa lógica do zero em cada projeto, esta API resolve tudo isso em um serviço separado, pronto para reusar.

---

## ✨ Funcionalidades

| Funcionalidade | Status |
|---|---|
| Cadastro e login com email/senha | ✅ |
| JWT Access Token + Refresh Token | ✅ |
| Login com Google e GitHub (OAuth 2.0) | ✅ |
| Recuperação de senha por email | ✅  |
| Perfil do usuário autenticado | ✅ |
| Docker Compose pronto para uso | ✅ |
| Documentação interativa (Swagger UI) | ✅ |

---

## 🧱 Stack utilizada

| Tecnologia | Papel |
|---|---|
| **FastAPI** | Framework web — recebe as requisições, processa a lógica e devolve as respostas |
| **PostgreSQL** | Banco de dados — persiste os dados dos usuários |
| **SQLAlchemy** | ORM — permite escrever queries no banco usando Python |
| **python-jose** | Geração e validação de tokens JWT |
| **Passlib + Bcrypt** | Hash de senhas |
| **HTTPX** | Cliente HTTP usado nas chamadas OAuth ao Google e GitHub |
| **Docker** | Containerização — sobe API + banco com um único comando |

---

## 🚀 Como rodar localmente

### Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e **aberto**

### Passo a passo

**1. Clone o repositório**
```bash
git clone https://github.com/mattospedrof/API-Authenticator.git
cd API-Authenticator
```

**2. Crie o arquivo de variáveis de ambiente**
```bash
# Linux/Mac
cp .env.example .env

# Windows
copy .env.example .env
```

**3. Edite o `.env`**

Abra o arquivo `.env` e certifique-se que a `DATABASE_URL` aponta para `db` (não `localhost`):
```
DATABASE_URL=postgresql://user:password@db:5432/authdb
```

**4. Suba os containers**
```bash
docker-compose up --build
```

Na primeira vez pode demorar alguns minutos. Quando aparecer:
```
Application startup complete.
```
...a API está pronta! ✅

**5. Acesse a documentação interativa**
```
http://localhost:8000/docs
```

---

## 📡 Endpoints

### Auth
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/auth/register` | Criar conta |
| POST | `/auth/login` | Login — retorna access + refresh token |
| POST | `/auth/refresh` | Renovar tokens sem precisar logar novamente |
| POST | `/auth/forgot-password` | Solicitar link de reset por email |
| POST | `/auth/reset-password` | Redefinir senha com o token recebido por email |

### Usuário *(requer autenticação)*
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/users/me` | Ver perfil do usuário logado |
| PATCH | `/users/me` | Atualizar nome ou avatar |
| DELETE | `/users/me` | Deletar conta |

### OAuth
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/oauth/google` | Redireciona para login do Google |
| GET | `/oauth/google/callback` | Callback do Google após autorização |
| GET | `/oauth/github` | Redireciona para login do GitHub |
| GET | `/oauth/github/callback` | Callback do GitHub após autorização |

---

## 🔑 Como usar a autenticação

Após o login, você recebe dois tokens:

```json
{
  "access_token": "eyJhbGci...",
  "refresh_token": "eyJhbGci...",
  "token_type": "bearer"
}
```

Para acessar rotas protegidas, envie o `access_token` no header de cada requisição:

```
Authorization: Bearer eyJhbGci...
```

Quando o `access_token` expirar (após 30 minutos), use o `refresh_token` em `POST /auth/refresh` para obter um novo par de tokens — sem precisar logar novamente.

---

## 🗂️ Estrutura do projeto

```
auth-api/
├── app/
│   ├── core/
│   │   ├── config.py       # Lê variáveis do .env e expõe como settings
│   │   ├── database.py     # Conexão com o PostgreSQL via SQLAlchemy
│   │   └── security.py     # Criação e validação de tokens JWT
│   ├── middleware/
│   │   └── auth_middleware.py  # Verifica JWT antes de acessar rotas protegidas
│   ├── models/
│   │   ├── user.py         # Modelo da tabela users no banco
│   │   └── schemas.py      # Validação de entrada e saída com Pydantic
│   ├── routes/
│   │   ├── auth.py         # Endpoints de autenticação
│   │   ├── users.py        # Endpoints de perfil do usuário
│   │   └── oauth.py        # Fluxo OAuth Google e GitHub
│   ├── services/
│   │   └── email.py        # Envio de email de reset via SMTP
│   └── main.py             # Entry point — registra rotas e configura o app
├── .env.example            # Template de variáveis de ambiente
├── docker-compose.yml      # Sobe API + PostgreSQL juntos
├── Dockerfile              # Combina a aplicação em um container
├── requirements.txt        # Dependências Python
└── README.md
```

---

## 🔒 Decisões de segurança

- Senhas armazenadas com hash **bcrypt** — nunca em texto puro
- **Access token** expira em 30 minutos
- **Refresh token** expira em 7 dias
- **Token de reset** expira em 1 hora
- O endpoint `/forgot-password` sempre retorna 200, mesmo se o email não existir — isso evita o ataque de *email enumeration* (descobrir quais emails estão cadastrados)

---

## ⚙️ Variáveis de ambiente

Copie o `.env.example` para `.env` e preencha os valores:

```env
# Banco de dados
DATABASE_URL=postgresql://user:password@db:5432/authdb

# JWT
SECRET_KEY=troque-por-uma-chave-secreta-longa
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Email (necessário para reset de senha)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu@gmail.com
SMTP_PASSWORD=sua-senha-de-app

# OAuth Google (console.cloud.google.com)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# OAuth GitHub (github.com/settings/developers)
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
```

---

## 📄 Licença

MIT