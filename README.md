# LegalTech MVP

A scalable and maintainable Legal Technology MVP application built with modern web technologies.

## 🏗️ Architecture

This is a monorepo containing:
- **Frontend**: React + TypeScript + Vite
- **Backend**: Python + FastAPI + SQLAlchemy
- **CI/CD**: GitHub Actions
- **Package Management**: npm (frontend) + pip (backend)

## 📁 Project Structure

```
legaltech-mvp/
├── frontend/                 # React frontend application
│   ├── src/
│   ├── package.json
│   └── ...
├── backend/                  # Python FastAPI backend
│   ├── app/
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── ...
├── docs/                     # Documentation
├── scripts/                  # Build and deployment scripts
├── .github/
│   └── workflows/           # GitHub Actions CI/CD
├── package.json             # Root package.json with workspace scripts
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+** - [Download here](https://python.org/)
- **pip** - Comes with Python
- **Node.js 18+** - [Download here](https://nodejs.org/) (for frontend)
- **npm 9+** - Comes with Node.js
- **Git** - [Download here](https://git-scm.com/)

**Verify installation:**
```bash
python3 --version  # Should be 3.9.0 or higher
pip --version      # Any recent version
node --version     # Should be 18.0.0 or higher
npm --version      # Should be 9.0.0 or higher  
git --version      # Any recent version
```

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Liongchenglex/LegalTech.git
   cd LegalTech
   ```

2. **Set up Python virtual environment**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   # venv\Scripts\activate
   ```

3. **Install all dependencies**
   ```bash
   # Step 3a: Install root dependencies (contains scripts for running dev servers)
   npm install
   
   # Step 3b: Install frontend dependencies  
   cd frontend
   npm install
   cd ..
   
   # Step 3c: Install backend dependencies (ensure venv is activated first!)
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

4. **Start development servers** (run from LegalTech root directory)
   
   **Option A: Start both servers with one command (recommended for development)**
   ```bash
   # From LegalTech root directory:
   npm run dev
   ```
   This starts both frontend (http://localhost:5173) and backend (http://localhost:8000) concurrently.

   **Option B: Start servers individually (recommended for focused development)**
   ```bash
   # Terminal 1 - From LegalTech root directory:
   npm run dev:frontend   # Runs on http://localhost:5173
   
   # Terminal 2 - From LegalTech root directory (ensure venv is activated):
   npm run dev:backend    # Runs on http://localhost:8000
   ```

5. **Verify everything works**
   - Open http://localhost:5173 in your browser
   - You should see the LegalTech MVP homepage
   - Check that "Backend API: ✅ Connected" appears on the page
   - Visit http://localhost:8000/docs for interactive API documentation

### Development Notes

**Why three separate npm install commands?**
- **Root `npm install`**: Installs `concurrently` package needed for `npm run dev` command
- **Frontend `npm install`**: Installs React, Vite, TypeScript and frontend dependencies  
- **Backend `pip install`**: Installs Python FastAPI, PyPDF2, and legal processing libraries

**Why these ports?**
- **Frontend (5173)**: Vite's default port, optimized for fast HMR (Hot Module Replacement)
- **Backend (8000)**: FastAPI's conventional port, separate from frontend for clear API boundary

**Why virtual environment?**
- **Isolation**: Prevents Python package conflicts with your system
- **Reproducibility**: Ensures consistent dependencies across different machines
- **Best Practice**: Industry standard for Python development

**Single vs Individual Commands:**
- **`npm run dev`**: Convenient for full-stack development, sees both frontend and backend logs
- **Individual commands**: Better for focused development, cleaner logs, easier debugging

## 📜 Available Scripts

### Root Level Commands

| Command | Description |
|---------|-------------|
| `npm run dev` | Start both frontend and backend in development mode |
| `npm run build` | Build both applications for production |
| `npm run test` | Run tests for both applications |
| `npm run lint` | Lint code in both applications |
| `npm run typecheck` | Type check both applications |
| `npm run setup:venv` | Create Python virtual environment |
| `npm run install:all` | Install frontend dependencies (backend requires venv) |
| `npm run clean` | Remove all node_modules and build outputs |

### Frontend Commands (in `frontend/` directory)

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server with hot reload |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm test` | Run tests with Vitest |
| `npm run lint` | Lint TypeScript and React code |
| `npm run typecheck` | Type check without emitting files |

### Backend Commands (in `backend/` directory, with venv activated)

| Command | Description |
|---------|-------------|
| `python3 -m uvicorn app.main:app --reload` | Start development server with auto-reload |
| `pip install -r requirements.txt` | Install Python dependencies |
| `python3 -m pytest` | Run tests with pytest |
| `python3 -m black .` | Format code with Black |
| `python3 -m flake8 .` | Lint Python code |
| `python3 -m mypy .` | Type check Python code |

**Note**: Always activate the virtual environment first: `source venv/bin/activate`

## 🔄 CI/CD Pipeline

### GitHub Actions Workflows

1. **CI Pipeline** (`.github/workflows/ci.yml`)
   - Runs on push/PR to `main` and `develop` branches
   - Type checking, linting, testing, and building
   - Matrix strategy for parallel frontend/backend testing
   - Security audit with npm audit

2. **Security Scan** (`.github/workflows/security.yml`)
   - Weekly vulnerability scanning with Trivy
   - Dependency review on pull requests
   - Results uploaded to GitHub Security tab

### Deployment Strategy

- **Staging**: Auto-deploy on push to `develop` branch
- **Production**: Auto-deploy on push to `main` branch

## 🛠️ Technology Stack

### Frontend
- **Framework**: React 18
- **Language**: TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Testing**: Vitest
- **Code Quality**: ESLint, Prettier

### Backend
- **Runtime**: Python 3.9+
- **Framework**: FastAPI
- **Language**: Python with Type Hints
- **Database**: SQLAlchemy (PostgreSQL/SQLite)
- **Authentication**: JWT with passlib
- **Validation**: Pydantic
- **Security**: Built-in FastAPI security, CORS
- **Testing**: pytest
- **Code Quality**: Black, Flake8, MyPy
- **Legal Processing**: PyPDF2, python-docx, spaCy, NLTK

## 🔧 Development Workflow

1. **Feature Development**
   ```bash
   git checkout -b feature/your-feature-name
   npm run dev
   # Make your changes
   npm run lint
   npm run typecheck
   npm test
   ```

2. **Before Committing**
   ```bash
   npm run lint      # Fix linting issues
   npm run typecheck # Ensure no type errors
   npm test          # Verify all tests pass
   ```

3. **Create Pull Request**
   - Push your branch and create a PR
   - CI pipeline will automatically run
   - Ensure all checks pass before merging

## 🌱 Scaling Considerations

### Infrastructure Ready Features

- **Environment Configuration**: Separate configs for dev/staging/prod
- **Database**: MongoDB ready with Mongoose ODM
- **Authentication**: JWT-based auth system
- **Security**: Helmet, CORS, input validation
- **Monitoring**: Structured logging with Morgan
- **Testing**: Comprehensive test setup
- **Code Quality**: Automated linting and type checking

### Future Enhancements

- **Docker**: Add Dockerfile and docker-compose.yml
- **Kubernetes**: Add k8s manifests for container orchestration
- **Monitoring**: Add APM tools (Datadog, New Relic)
- **Logging**: Centralized logging (ELK stack)
- **Caching**: Redis integration
- **CDN**: Static asset optimization
- **Database**: Read replicas and connection pooling

## 📝 Environment Variables

### Backend (.env)
```env
ENVIRONMENT=development
PORT=8000
HOST=0.0.0.0
DATABASE_URL=sqlite:///./legaltech.db
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=["http://localhost:5173"]
LOG_LEVEL=info
MAX_FILE_SIZE=10485760
UPLOAD_DIR=./uploads
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=LegalTech MVP
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🔗 Useful Links

- [Frontend Documentation](./frontend/README.md)
- [Backend Documentation](./backend/README.md)
- [API Documentation](./docs/api.md)
- [Deployment Guide](./docs/deployment.md)

---

**Built with ❤️ for the Legal Tech community**