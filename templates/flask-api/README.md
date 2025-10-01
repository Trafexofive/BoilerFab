# {{PROJECT_NAME}}

A modern Flask REST API with SQLAlchemy, migrations, and CORS support.

## Features

- **Flask** web framework with blueprints
- **SQLAlchemy** ORM with Flask-SQLAlchemy
- **Flask-Migrate** for database migrations
- **CORS** support for cross-origin requests
- **JWT** authentication ready
- **Error handling** with custom error pages
- **Environment-based configuration**
- **Testing** setup with pytest

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
export SECRET_KEY="your-secret-key-here"
export DATABASE_URL="sqlite:///{{PROJECT_NAME}}.db"
```

### 3. Database Setup

```bash
# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 4. Run the Application

```bash
# Development mode
python app.py

# Or with flask command
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

The API will be available at http://localhost:5000

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /api/v1/items` - Get all items (example)

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

## Production Deployment

```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Using Docker
docker build -t {{PROJECT_NAME}} .
docker run -p 5000:5000 {{PROJECT_NAME}}
```

## Project Structure

```
{{PROJECT_NAME}}/
├── app.py              # Main application
├── requirements.txt    # Python dependencies  
├── .env.example       # Environment variables template
├── tests/             # Test files
└── migrations/        # Database migrations
```

Happy coding! 🚀