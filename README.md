# AI SaaS — Document Assistant

AI-powered SaaS application for uploading documents, processing their content, generating embeddings, performing semantic search, and answering user questions using RAG.

The project also includes authentication, subscription plans, Stripe payments, chat history, and background document processing with Celery and Redis.

---

## Overview

The application allows users to:

* register and log in;
* authenticate using JWT;
* upload documents;
* process documents in the background;
* extract text from documents;
* split documents into chunks;
* generate embeddings;
* store embeddings in PostgreSQL with pgvector;
* perform semantic search;
* ask questions about uploaded documents using RAG;
* store conversation history;
* manage subscription plans;
* upgrade to PRO through Stripe;
* process documents asynchronously using Celery and Redis.

---

## Features

### Authentication

* User registration
* User login
* JWT access tokens
* Password hashing with Argon2
* Protected API endpoints
* Active/inactive user validation

### Documents

* Upload documents
* Store document metadata
* Store uploaded files
* Document processing status
* Text extraction
* Text chunking
* Embedding generation
* Vector storage
* Semantic search

### RAG

The application uses a Retrieval-Augmented Generation pipeline:

```text
User Question
      ↓
Query Embedding
      ↓
Vector Search
      ↓
Relevant Document Chunks
      ↓
Context
      ↓
LLM
      ↓
Answer
```

### Chat History

Conversation history is stored in PostgreSQL.

The application stores:

* conversations;
* messages;
* user associations;
* conversation context.

### Subscriptions

Two subscription plans are currently available:

| Plan | Document Limit |
| ---- | -------------- |
| FREE | 3 documents    |
| PRO  | 50 documents   |

The subscription system is connected to Stripe for PRO subscriptions.

### Stripe

Stripe is used for:

* creating checkout sessions;
* recurring PRO subscriptions;
* processing Stripe webhooks;
* updating the user's subscription plan.

### Background Processing

Document processing is performed asynchronously using:

* Celery
* Redis

The upload itself remains a normal FastAPI request.

Processing is started separately with:

```text
POST /documents/{document_id}/process
```

---

# Tech Stack

## Backend

* Python 3.14+
* FastAPI
* Pydantic
* SQLAlchemy 2
* asyncpg
* Alembic

## Database

* PostgreSQL 17
* pgvector

## Authentication

* JWT
* PyJWT
* pwdlib
* Argon2

## AI / RAG

* LangChain
* Mistral AI
* sentence-transformers
* vector embeddings
* pgvector

## Background Processing

* Celery
* Redis

## Payments

* Stripe

## Infrastructure

* Docker
* Docker Compose

## Testing

* pytest
* pytest-asyncio
* FastAPI TestClient
* unittest.mock

---

# Architecture

The application follows a layered architecture.

```text
                         ┌───────────────┐
                         │    Client     │
                         │ Swagger / UI  │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │    FastAPI    │
                         │    Routes     │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │   Services    │
                         │ Business Logic│
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │ Repositories  │
                         │ Data Access   │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │  PostgreSQL   │
                         │   + pgvector  │
                         └───────────────┘
```

Background document processing:

```text
FastAPI
   │
   │ POST /documents/{id}/process
   ▼
Celery Task
   │
   ▼
Redis
   │
   ▼
Celery Worker
   │
   ▼
DocumentService.process_document()
   │
   ├── Text extraction
   ├── Chunking
   ├── Embeddings
   └── Vector storage
```

---

# Document Processing Flow

Uploading a document and processing a document are separate operations.

## Upload

```text
POST /documents
      │
      ▼
DocumentService.create_document()
      │
      ├── Check subscription limit
      ├── Save file
      └── Create Document record
      │
      ▼
Return document
```

## Processing

```text
POST /documents/{document_id}/process
      │
      ▼
Check document ownership
      │
      ▼
Celery task
      │
      ▼
Redis
      │
      ▼
Celery Worker
      │
      ▼
DocumentService.process_document()
      │
      ├── PROCESSING
      ├── Extract text
      ├── Save DocumentContent
      ├── Split into chunks
      ├── Generate embeddings
      ├── Save DocumentChunks
      └── READY
```

If processing fails:

```text
PROCESSING
    ↓
FAILED
```

---

# Project Structure

A simplified project structure:

```text
AI-SaaS/
│
├── app/
│   ├── api/
│   │   ├── dependencies.py
│   │   └── routes/
│   │       ├── auth.py
│   │       ├── documents.py
│   │       ├── conversations.py
│   │       ├── subscriptions.py
│   │       └── ...
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── db/
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── document.py
│   │   ├── document_content.py
│   │   ├── document_chunk.py
│   │   ├── conversation.py
│   │   ├── message.py
│   │   └── subscription.py
│   │
│   ├── repositories/
│   │   ├── user.py
│   │   ├── document.py
│   │   ├── document_content.py
│   │   ├── document_chunk.py
│   │   ├── conversation.py
│   │   ├── message.py
│   │   └── subscription.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── document.py
│   │   ├── conversation.py
│   │   ├── message.py
│   │   └── subscription.py
│   │
│   ├── services/
│   │   ├── user.py
│   │   ├── document.py
│   │   ├── file.py
│   │   ├── text_extraction.py
│   │   ├── chunking.py
│   │   ├── embedding.py
│   │   ├── search.py
│   │   ├── rag.py
│   │   ├── llm.py
│   │   ├── subscription.py
│   │   └── stripe.py
│   │
│   ├── worker/
│   │   ├── __init__.py
│   │   ├── celery_app.py
│   │   └── tasks.py
│   │
│   └── main.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── tests/
│   ├── test_auth.py
│   ├── test_document_service.py
│   ├── test_subscription_service.py
│   └── test_jwt.py
│
├── uploads/
│   └── documents/
│
├── .env
├── .env.example
├── alembic.ini
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
└── README.md
```

---

# Environment Variables

Create a `.env` file in the project root.

Example:

```env
POSTGRES_DB=ai_saas
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/ai_saas

SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

MISTRAL_API_KEY=your-mistral-api-key

STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_PRICE_ID=your-stripe-price-id
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret

REDIS_URL=redis://localhost:6379/0
```

Do not commit `.env` to Git.

Add it to `.gitignore`:

```gitignore
.env
```

---

# Installation

## Requirements

Make sure you have installed:

* Python 3.14+
* Docker
* Docker Compose
* Git

---

## Clone the repository

```bash
git clone <repository-url>
cd AI-SaaS
```

---

## Install dependencies

The project uses `uv`.

Install dependencies:

```bash
uv sync
```

---

# Database

PostgreSQL and Redis can be started with Docker Compose.

```bash
docker compose up -d
```

Check running containers:

```bash
docker ps
```

Expected services:

```text
ai-document-postgres
ai-document-redis
```

---

# Redis

Redis is used as the Celery broker and result backend.

Check Redis:

```bash
docker exec -it ai-document-redis redis-cli ping
```

Expected result:

```text
PONG
```

Because FastAPI and the Celery worker are currently running locally, Redis is accessed through:

```env
REDIS_URL=redis://localhost:6379/0
```

If the worker is later moved into Docker, the Redis hostname can be changed to the Docker service name.

---

# Database Migrations

Run migrations with:

```bash
uv run alembic upgrade head
```

Create a new migration:

```bash
uv run alembic revision --autogenerate -m "description"
```

Then apply it:

```bash
uv run alembic upgrade head
```

---

# Running FastAPI

Start the application:

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

---

# Running Celery Worker

Start the Celery worker in a separate terminal:

```bash
uv run celery -A app.worker.celery_app worker --loglevel=info --pool=solo
```

`--pool=solo` is used for the current local Windows development environment.

The worker should show registered tasks similar to:

```text
[tasks]
  . app.worker.tasks.process_document_task
```

---

# Authentication

## Register

```http
POST /auth/register
```

Example request:

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

A new user automatically receives a FREE subscription.

---

## Login

```http
POST /auth/login
```

The login endpoint uses OAuth2 password form data.

Example:

```text
username=user@example.com
password=password123
```

Response:

```json
{
  "access_token": "jwt-token",
  "token_type": "bearer"
}
```

Use the token to authorize protected endpoints.

---

## Current User

```http
GET /auth/me
```

Requires:

```text
Authorization: Bearer <token>
```

---

# Documents API

## Upload Document

```http
POST /documents
```

The endpoint:

* checks the subscription limit;
* saves the file;
* creates a document record.

The upload itself does not perform document processing.

---

## Process Document

```http
POST /documents/{document_id}/process
```

This endpoint:

1. verifies that the document belongs to the current user;
2. creates a Celery task;
3. sends the task to Redis;
4. returns immediately;
5. lets the Celery worker process the document in the background.

Example:

```text
POST /documents/11/process
```

The worker then performs:

```text
Text extraction
      ↓
Chunking
      ↓
Embeddings
      ↓
Vector storage
      ↓
READY
```

---

# Document Status

Documents can have different processing states.

Typical flow:

```text
UPLOADED
    ↓
PROCESSING
    ↓
READY
```

If an error occurs:

```text
PROCESSING
    ↓
FAILED
```

Example response:

```json
{
  "id": 11,
  "user_id": 5,
  "filename": "CoverEng.docx",
  "file_path": "uploads\\documents\\example.docx",
  "status": "ready",
  "created_at": "2026-09-08T13:19:01.267791Z"
}
```

---

# RAG Pipeline

The RAG pipeline consists of several stages.

## 1. Document Upload

The user uploads a document.

```text
File → uploads/documents/
```

## 2. Text Extraction

The application extracts text from the document.

## 3. Chunking

The extracted text is divided into smaller chunks.

```text
Document
   ↓
Text
   ↓
Chunks
```

## 4. Embeddings

Each chunk is converted into a vector representation.

```text
Chunk
  ↓
Embedding Model
  ↓
Vector
```

## 5. Vector Storage

Embeddings are stored in PostgreSQL using pgvector.

## 6. Semantic Search

When the user asks a question:

```text
Question
   ↓
Query Embedding
   ↓
Cosine Similarity
   ↓
Relevant Chunks
```

## 7. LLM

Relevant chunks are passed to the LLM as context.

```text
Question + Context
        ↓
       LLM
        ↓
      Answer
```

---

# Chat History

The application stores conversations and messages in PostgreSQL.

Basic flow:

```text
User
 ↓
Conversation
 ↓
Messages
 ↓
RAG
```

This allows the application to preserve previous messages instead of keeping chat history only in memory.

---

# Subscriptions

Each user has a subscription.

Available plans:

```text
FREE
PRO
```

Limits:

```text
FREE → 3 documents
PRO  → 50 documents
```

The subscription service checks the number of documents before allowing an upload.

Example:

```python
if subscription.plan == SubscriptionPlan.FREE:
    return quantity < 3

if subscription.plan == SubscriptionPlan.PRO:
    return quantity < 50
```

---

# Stripe Integration

Stripe is used for PRO subscriptions.

## Checkout Flow

```text
User
  ↓
POST /subscriptions/checkout
  ↓
Stripe Checkout Session
  ↓
Stripe Payment
  ↓
checkout.session.completed
  ↓
Stripe Webhook
  ↓
Find user by metadata
  ↓
Update subscription
  ↓
FREE → PRO
```

The user ID is passed through Stripe Checkout metadata.

Example:

```json
{
  "metadata": {
    "user_id": "5"
  }
}
```

---

# Stripe Webhooks

For local development, use the Stripe CLI.

Start the webhook listener:

```bash
stripe listen --forward-to localhost:8000/subscriptions/webhooks/stripe
```

The CLI will display a webhook signing secret.

Set that secret in `.env`:

```env
STRIPE_WEBHOOK_SECRET=whsec_...
```

Restart FastAPI after changing `.env`.

---

# Stripe Test Mode

The project uses Stripe test/sandbox mode during development.

The application should use:

* Stripe test secret key;
* test price ID;
* Stripe CLI webhook secret.

Never use production Stripe credentials during local development.

---

# Celery Background Processing

Celery is responsible for long-running document processing.

The FastAPI endpoint does not execute the processing directly.

Instead:

```python
process_document_task.delay(
    document_id=document_id,
    user_id=current_user.id,
)
```

The task is sent to Redis.

The Celery worker receives it and executes:

```python
DocumentService.process_document(...)
```

The service performs the existing document-processing business logic.

This keeps the FastAPI request fast and moves expensive operations into the background.

---

# Celery Task

The main background task is:

```text
app.worker.tasks.process_document_task
```

Conceptually:

```python
@celery_app.task
def process_document_task(
    document_id: int,
    user_id: int,
):
    asyncio.run(
        _process_document(
            document_id=document_id,
            user_id=user_id,
        )
    )

    return {
        "document_id": document_id,
        "status": "processed",
    }
```

The Celery task returns only JSON-serializable data.

SQLAlchemy model objects such as `Document` should not be returned directly from a Celery task because they are not JSON serializable.

---

# Testing

Run all tests:

```bash
uv run pytest
```

Run a specific test file:

```bash
uv run pytest tests/test_auth.py
```

Example:

```bash
uv run pytest tests/test_subscription_service.py
```

The project contains tests for important business logic, including:

* authentication;
* JWT;
* current-user authentication;
* document upload limits;
* subscription limits;
* subscription information;
* document service behavior.

The goal is to test the important application logic without overloading the project with unnecessary tests.

---

# Error Handling

The API uses standard HTTP errors.

Examples:

```text
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
```

Examples:

### User already exists

```text
409 Conflict
```

### Invalid JWT

```text
401 Unauthorized
```

### Inactive user

```text
403 Forbidden
```

### Document not found

```text
404 Not Found
```

### Document limit reached

```text
403 Forbidden
```

---

# Database Models

The main entities are:

```text
User
 │
 ├── Subscription
 │
 ├── Documents
 │      │
 │      ├── DocumentContent
 │      │
 │      └── DocumentChunks
 │
 └── Conversations
        │
        └── Messages
```

---

# Dependency Injection

FastAPI dependencies are used to create:

* database sessions;
* repositories;
* services;
* authentication dependencies.

For example:

```text
FastAPI
   ↓
Depends(get_document_service)
   ↓
DocumentService
   ↓
Repositories
   ↓
AsyncSession
```

Celery tasks run outside the FastAPI dependency injection system.

Therefore, the worker creates its required repositories and services explicitly.

---

# Async Database

The project uses SQLAlchemy's asynchronous API.

Database setup:

```python
engine = create_async_engine(
    settings.database_url,
    echo=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
```

Repositories use `AsyncSession` and asynchronous SQLAlchemy operations.

---

# Development

Recommended development workflow:

### 1. Start infrastructure

```bash
docker compose up -d
```

### 2. Run migrations

```bash
uv run alembic upgrade head
```

### 3. Start FastAPI

```bash
uv run uvicorn app.main:app --reload
```

### 4. Start Celery

In another terminal:

```bash
uv run celery -A app.worker.celery_app worker --loglevel=info --pool=solo
```

### 5. Open Swagger

```text
http://localhost:8000/docs
```

---

# Typical Document Workflow

A normal user workflow looks like this:

```text
1. Register
      ↓
2. Login
      ↓
3. Receive JWT
      ↓
4. Upload document
      ↓
5. Document is stored
      ↓
6. Call /documents/{id}/process
      ↓
7. Celery task is created
      ↓
8. Redis stores the task
      ↓
9. Worker receives the task
      ↓
10. Text extraction
      ↓
11. Chunking
      ↓
12. Embeddings
      ↓
13. Vector storage
      ↓
14. Document becomes READY
      ↓
15. User asks a question
      ↓
16. Semantic search
      ↓
17. Relevant chunks
      ↓
18. LLM generates answer
```

---

# Git

Typical workflow:

```bash
git status
git add .
git commit -m "Add Celery background document processing"
git push
```

Do not commit:

```text
.env
uploads/
.venv/
__pycache__/
.pytest_cache/
```

---

# Current Project Status

## Implemented

* [x] FastAPI application
* [x] PostgreSQL
* [x] SQLAlchemy async
* [x] Alembic migrations
* [x] User registration
* [x] User login
* [x] JWT authentication
* [x] Password hashing
* [x] Protected endpoints
* [x] Document upload
* [x] Document storage
* [x] Text extraction
* [x] Document chunking
* [x] Embeddings
* [x] pgvector
* [x] Semantic search
* [x] RAG pipeline
* [x] Conversation history
* [x] Message storage
* [x] Subscription model
* [x] FREE / PRO plans
* [x] Document limits
* [x] Stripe Checkout
* [x] Stripe webhook
* [x] Subscription upgrade
* [x] Redis
* [x] Celery
* [x] Background document processing
* [x] Core tests
* [x] Docker Compose for infrastructure

---

# Background Processing Status

Current document-processing architecture:

```text
FastAPI
   │
   │ POST /documents
   ▼
Upload document
   │
   ▼
PostgreSQL
```

Processing:

```text
FastAPI
   │
   │ POST /documents/{id}/process
   ▼
Celery
   │
   ▼
Redis
   │
   ▼
Celery Worker
   │
   ▼
DocumentService
   │
   ├── Extraction
   ├── Chunking
   ├── Embeddings
   └── PostgreSQL / pgvector
```

This separation allows document upload to remain fast while potentially expensive processing runs in the background.

---

# Future Improvements

Possible future improvements include:

* better document processing status endpoint;
* task progress tracking;
* Celery task retries;
* better failed-task handling;
* Redis/Celery fully containerized;
* production Docker configuration;
* improved RAG retrieval quality;
* similarity thresholds;
* source references in answers;
* streaming LLM responses;
* rate limiting;
* subscription expiration handling;
* Stripe subscription cancellation handling;
* Stripe customer portal;
* frontend application;
* production deployment;
* CI/CD pipeline;
* monitoring and logging.

---

# Learning Goals

This project is also a practical learning project covering:

* FastAPI architecture;
* dependency injection;
* asynchronous Python;
* SQLAlchemy 2 async;
* PostgreSQL;
* pgvector;
* Alembic;
* JWT authentication;
* REST API design;
* service/repository patterns;
* RAG;
* embeddings;
* LLM integration;
* background jobs;
* Celery;
* Redis;
* Stripe;
* automated testing;
* Docker.

The main goal is to build a working end-to-end application while understanding how the individual components interact.
