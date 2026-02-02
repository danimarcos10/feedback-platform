# Feedback Platform

A full-stack feedback management system with sentiment analysis and analytics, built with modern technologies.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi)
![Vue.js](https://img.shields.io/badge/Vue.js-3.4-4FC08D?logo=vue.js)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)

## Overview

A production-ready feedback platform where users can submit feedback and administrators can manage, categorize, and analyze it. Features AI-powered sentiment analysis and topic clustering.

### Key Features

- **User Management**: JWT authentication, role-based access (User/Admin)
- **Feedback System**: Submit, edit, delete feedback with status tracking
- **Admin Dashboard**: Manage all feedback, respond to users, change statuses
- **Analytics**: 
  - Sentiment analysis (VADER)
  - Topic clustering (TF-IDF + KMeans)
  - Trend visualization
- **Full API Documentation**: Interactive Swagger UI

## Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **SQLAlchemy** - ORM with PostgreSQL
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **JWT** - Secure authentication
- **VADER Sentiment** - Sentiment analysis
- **scikit-learn** - Topic clustering (TF-IDF + KMeans)

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **Vite** - Fast build tool
- **Pinia** - State management
- **Vue Router** - Navigation
- **Axios** - HTTP client
- **Chart.js** - Data visualization

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **PostgreSQL** - Database
- **Nginx** - Frontend server
- **GitHub Actions** - CI/CD pipeline

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │────▶│   Backend   │────▶│  PostgreSQL │
│   (Vue 3)   │     │  (FastAPI)  │     │  Database   │
│   :80       │     │   :8000     │     │   :5432     │
└─────────────┘     └─────────────┘     └─────────────┘
      │                   │
      │              ┌────┴────┐
      │              │ Analytics│
      │              │ Engine   │
      │              └─────────┘
      │                   │
      └───────────────────┘
           REST API
```

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/feedback-platform.git
cd feedback-platform

# Start all services
docker-compose up -d

# Run database migrations
docker-compose exec backend alembic upgrade head

# Create an admin user (optional)
docker-compose exec backend python -c "
from app.db.session import SessionLocal
from app.services.auth_service import AuthService
db = SessionLocal()
AuthService(db).create_admin('admin@example.com', 'admin123')
db.close()
"
```

### Access the Application

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost | User interface |
| API | http://localhost:8000 | Backend API |
| API Docs | http://localhost:8000/docs | Swagger UI |
| Database | localhost:5432 | PostgreSQL |

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login, get JWT token |
| GET | `/auth/me` | Get current user info |

### Feedback (Users)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/feedback/` | Submit feedback |
| GET | `/feedback/mine` | Get user's feedback |
| GET | `/feedback/{id}` | Get specific feedback |
| PUT | `/feedback/{id}` | Update feedback |
| DELETE | `/feedback/{id}` | Delete feedback |

### Admin
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/feedback` | Get all feedback |
| PUT | `/admin/feedback/{id}/status` | Update status |
| PUT | `/admin/feedback/{id}/category` | Set category |
| POST | `/admin/feedback/{id}/respond` | Respond to feedback |

### Analytics (Admin)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/analytics/overview` | Dashboard stats |
| GET | `/analytics/timeseries` | Volume over time |
| GET | `/analytics/sentiment-trends` | Sentiment trends |
| GET | `/analytics/topics` | Topic clusters |

## Database Schema

```
users
├── id (PK)
├── email (unique)
├── hashed_password
├── role (user/admin)
└── created_at

feedback
├── id (PK)
├── user_id (FK)
├── title
├── content
├── category_id (FK)
├── status (new/triaged/in_progress/resolved/rejected)
├── sentiment_score
├── created_at
├── updated_at
└── resolved_at

categories, tags, feedback_tags, status_events, admin_responses
```

## Testing

```bash
# Run all tests
docker-compose exec backend pytest

# Run with coverage
docker-compose exec backend pytest --cov=app --cov-report=html

# Run specific test file
docker-compose exec backend pytest tests/test_auth.py -v
```

## Project Structure

```
feedback-platform/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Config, security
│   │   ├── db/           # Database setup
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── main.py       # FastAPI app
│   ├── tests/            # Pytest tests
│   ├── alembic/          # Migrations
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/          # API client
│   │   ├── components/   # Vue components
│   │   ├── views/        # Page components
│   │   ├── router/       # Vue Router
│   │   └── stores/       # Pinia stores
│   └── package.json
├── docker-compose.yml
└── README.md
```

## Development

### Local Development (without Docker)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Environment Variables

Create `.env` files based on `.env.example`:

**Backend:**
```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/feedback_db
SECRET_KEY=your-secret-key-change-in-production
DEBUG=true
```

**Frontend:**
```env
VITE_API_URL=http://localhost:8000
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Vue.js](https://vuejs.org/) - Progressive JavaScript framework
- [VADER Sentiment](https://github.com/cjhutto/vaderSentiment) - Sentiment analysis
