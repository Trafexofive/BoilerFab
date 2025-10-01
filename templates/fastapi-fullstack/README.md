# {{PROJECT_NAME}}

{{#if description}}{{description}}{{else}}A production-ready FastAPI application with authentication, database integration, and comprehensive testing.{{/if}}

## Features

- **FastAPI** with async/await support
- **{{database_type}}** database with SQLAlchemy ORM
- **JWT Authentication** with secure password hashing
- **CORS middleware** for cross-origin requests
- **Docker** containerization with multi-stage builds
- **Database migrations** with Alembic
- **Comprehensive testing** with pytest
- **API documentation** with Swagger UI and ReDoc
- **Code formatting** with Black and isort
- **Linting** with flake8

## Quick Start

### 1. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env
```

### 2. Installation Options

#### Option A: Docker (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### Option B: Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations (if using PostgreSQL/MySQL)
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. API Access

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Usage

### Authentication

```bash
# Register a new user
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "testpassword"}'

# Login to get access token
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpassword"

# Use the token in subsequent requests
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Items Management

```bash
# Create an item
curl -X POST "http://localhost:8000/api/v1/items/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Item", "description": "Item description"}'

# Get user items
curl -X GET "http://localhost:8000/api/v1/items/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Development

### Code Quality

```bash
# Format code
black app/
isort app/

# Lint code
flake8 app/

# Run tests
pytest

# Run tests with coverage
pytest --cov=app tests/
```

### Database Management

```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Configuration

Key environment variables:

- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: JWT secret key (change in production!)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time
- `CORS_ORIGINS`: Allowed CORS origins
- `DEBUG`: Enable debug mode

## Deployment

### Production Checklist

- [ ] Change `SECRET_KEY` in production
- [ ] Set `DEBUG=false`
- [ ] Configure proper `DATABASE_URL`
- [ ] Set up SSL/HTTPS
- [ ] Configure proper CORS origins
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy

### Docker Production

```dockerfile
# Build production image
docker build -t {{PROJECT_NAME}}:latest .

# Run in production mode
docker run -d \
  --name {{PROJECT_NAME}} \
  -p 8000:8000 \
  -e DATABASE_URL="your-production-db-url" \
  -e SECRET_KEY="your-production-secret" \
  {{PROJECT_NAME}}:latest
```

## Project Structure

```
{{PROJECT_NAME}}/
├── app/
│   ├── api/              # API routes
│   ├── core/             # Core configuration
│   ├── database/         # Database configuration
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   └── main.py           # FastAPI application
├── tests/                # Test files
├── scripts/              # Utility scripts
├── docs/                 # Documentation
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose configuration
└── .env.example         # Environment template
```

## License

MIT License - see LICENSE file for details.