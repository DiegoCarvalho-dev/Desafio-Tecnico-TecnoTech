# 🎓 Sistema Acadêmico

Este projeto foi desenvolvido como parte do **Desafio Técnico para a vaga de Estágio em Python/Django**.

O sistema permite gerenciar **alunos, cursos, matrículas e financeiro**, além de gerar relatórios em **HTML** e **JSON**, utilizando **Django Rest Framework** e integração com **PostgreSQL via Docker**.

---

## 🚀 Tecnologias utilizadas

- Python 3.12  
- Django 5.2.8  
- Django Rest Framework  
- PostgreSQL  
- Docker & Docker Compose  
- HTML + CSS (relatórios)  
- Django Admin  
- SQL bruto (JOIN, COUNT, SUM, GROUP BY)

---

## 📌 Funcionalidades implementadas

### ✅ Alunos
- Cadastro de aluno (nome, e-mail, CPF e data de ingresso)
- Gerenciamento via Django Admin
- API REST completa (CRUD)
- Histórico financeiro individual

### ✅ Cursos
- Cadastro de curso (nome, carga horária, valor e status)
- Gerenciamento via Django Admin
- API REST completa (CRUD)

### ✅ Matrículas
- Matrícula de alunos em cursos
- Controle automático de status (pago / pendente)
- Bloqueio de matrícula em curso inativo
- API para:
  - Criar matrícula
  - Listar matrículas
  - Marcar como paga

### ✅ Financeiro
- Registro de transações (pagamentos e reembolsos)
- Cálculo automático de:
  - Total pago por aluno
  - Total devido por aluno
  - Saldo da matrícula

### ✅ Relatórios
- 📄 **Histórico do aluno (HTML)**
- 📊 **Dashboard geral (HTML)**
- 📑 **Relatório geral em JSON** (`/api/relatorios/`)
- 🧮 **Relatório via SQL bruto** (`/api/sql-bruto/`)

---

## 🌐 URLs principais

| Funcionalidade | URL |
|------|-----|
Admin Django | http://localhost:8000/admin/
Dashboard Geral | http://localhost:8000/dashboard/
Histórico do Aluno | http://localhost:8000/aluno/1/historico/
API de Alunos | http://localhost:8000/api/alunos/
API Relatórios | http://localhost:8000/api/relatorios/
Relatório SQL Bruto | http://localhost:8000/api/sql-bruto/

---

## 🐳 Como rodar o projeto com Docker (Recomendado)

### 1. Clonar o repositório
```bash
git clone https://github.com/DiegoCarvalho-dev/Desafio-Tecnico-TecnoTech.git
cd Desafio-Tecnico-TecnoTech
```

### 2. Subir os containers
```bash
docker compose up --build
# ou
docker-compose up --build
# (Opcional – em outro terminal)
docker compose exec web python manage.py createsuperuser
```

O Docker irá:
- Criar o banco PostgreSQL
- Instalar as dependências do projeto
- Aplicar as migrações
- Subir o servidor Django automaticamente

Depois, acesse:
```
http://localhost:8000
```

---

## 🖥️ Como rodar SEM Docker (opcional)

### 1. Criar ambiente virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar banco (opcional – SQLite)

Caso não queira usar PostgreSQL, substitua o banco em `settings.py` por:

```python
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
  }
}
```

### 4. Rodar as migrações e iniciar o servidor
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 📂 Estrutura principal do projeto

```
core/
alunos/
cursos/
matriculas/
financeiro/
templates/
Dockerfile
docker-compose.yml
requirements.txt
meu_database.sql
README.md
```

---

## ✅ Considerações finais

Este projeto atende todos os requisitos do desafio técnico:

✔ CRUD completo  
✔ Django Admin  
✔ API REST com DRF  
✔ Docker + PostgreSQL  
✔ Relatórios em HTML  
✔ Relatórios em JSON  
✔ Consulta em SQL bruto  

Foi desenvolvido com foco em:
- Organização de código
- Boas práticas
- Clareza na arquitetura
- Facilidade de manutenção

---

### 👨‍💻 Desenvolvido por
**Diego Ricardo Carvalho**

📧 E-mail: diegoricardo2527@gmail.com  
🔗 LinkedIn: https://www.linkedin.com/in/diegoricardo-dev
