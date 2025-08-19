# 🪄 AI-Powered Survey Generator for BoundaryAI Backend Task

A full-stack application that transforms user descriptions into structured surveys using OpenAI's API

## Tech Stack & Architecture

- **FastAPI** (Python 3.11)
- **PostgreSQL** with SQLAlchemy ORM
- **OpenAI API** for survey generation
- **Docker** for containerization
- **Pydantic** for data validation

### Why FastAPI over Flask?

| Feature               | FastAPI                               | Flask                         |
| --------------------- | ------------------------------------- | ----------------------------- |
| **Performance**       | 2-3x faster (async support)           | Synchronous by default        |
| **API Documentation** | Auto-generated (Swagger/OpenAPI)      | Manual setup required         |
| **Type Safety**       | Built-in with Pydantic                | Requires additional libraries |
| **Data Validation**   | Automatic request/response validation | Manual validation             |

FastAPI provides superior developer experience, automatic documentation, and better performance for API-heavy applications. I did not know anything about FastAPI before this project and I managed to build a complete working project.

### Key Library Choices

- **SQLAlchemy 2.0**: Modern ORM with async support and type safety
- **Pydantic**: Robust data validation and serialization
- **psycopg2-binary**: High-performance PostgreSQL adapter
- **python-dotenv**: Secure environment variable management

## 🚀 Setup & Installation

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- OpenAI API Key

### Quick Start (Docker - Recommended)

1. **Clone and navigate to project**

   ```bash
   git clone <repository-url>
   cd boundaryAITask
   ```

2. **Set up environment variables**

   ```bash
   # Edit backend/.env with your OpenAI API key
   cp backend/.env.example backend/.env
   # Add your OpenAI API key to backend/.env
   ```

3. **Start with Docker**

   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Frontend: http://localhost:3000

### Manual Setup (Development)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up PostgreSQL database
createdb survey_generator

# Start the server
uvicorn main:app --reload --port 8000
```

## 🎯 Areas of Focus & Advanced Features

### What Sets This Implementation Apart

#### 0. (future feature) **Semantic Embeddings to survey generation requests**

- Exact matching is too rigid. Users often phrase the same intent differently. We could take an approach to test for similarity between the current survey generation request and the previous ones.
- Convert text to high-dimensional vectors that capture meaning using OpenAI Embeddings
- Compare vectors using cosine similarity
- Threshold-based matching (e.g., >85% similarity)
  **Pros:**
- ✅ Captures semantic meaning
- ✅ Handles synonyms and paraphrasing
- ✅ Language-aware
- ✅ Robust to typos and formatting

#### 1. **Enterprise-Grade Architecture**

- **Modular Design**: Clean separation between routes, services, models, and config
- **Dependency Injection**: FastAPI's built-in DI system for database sessions
- **Service Layer Pattern**: Business logic separated from API endpoints
- **Repository Pattern**: Database operations abstracted through services

#### 2. **Advanced Database Integration**

- **Intelligent Caching**: SHA-256 hashing to prevent duplicate AI generations
- **Connection Pooling**: Optimized database connections with SQLAlchemy
- **Data Persistence**: PostgreSQL with proper indexing and constraints

#### 4. **API Design Excellence**

- **RESTful Endpoints**: Intuitive URL structure and HTTP methods
- **Auto-Generated Documentation**: Interactive Swagger UI at `/docs`
- **Response Metadata**: Cache hit information and generation timestamps
- **Health Monitoring**: Comprehensive health checks for all services

#### 5. **Advanced OpenAI Integration**

- **Configurable Models**: Easy switching between GPT-3.5, GPT-4, etc.
- **Prompt Engineering**: Structured prompts for consistent survey generation

#### 6. **Frontend UX improvement**

- Created a button with gradient background color for the generate Survey button to give a feel of a magical AI
- Inverted the length constraint between the title and description of the survey
- Removed the left sidebar because it was useless
- Implemented a toast feature to inform the user of successes and failures

#### 7. **DevOps & Deployment**

- **Docker Containerization**: Multi-stage builds for optimization
- **Docker Compose**: One-command local development environment
- **Health Checks**: Container-level health monitoring

#### 8. **Code Quality & Maintainability**

- **Type Safety**: Full Python type annotations
- **Code Organization**: Clear folder structure and naming conventions
- **Documentation**: Comprehensive docstrings and comments
- **Configuration Management**: Centralized settings with validation

## API Endpoints

| Method | Endpoint                | Description                      |
| ------ | ----------------------- | -------------------------------- |
| `GET`  | `/`                     | Root endpoint                    |
| `GET`  | `/health`               | System health check              |
| `POST` | `/api/surveys/generate` | Generate survey from description |
| `GET`  | `/docs`                 | Interactive API documentation    |

## Environment Variables

| Variable          | Description                   | Default  |
| ----------------- | ----------------------------- | -------- |
| `OPENAI_API_KEY`  | OpenAI API key                | Required |
| `LLM_MODEL`       | OpenAI model to use           | `gpt-4`  |
| `LLM_TEMPERATURE` | Response creativity (0.0-1.0) | `0.7`    |
