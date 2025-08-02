# LegalTech MVP

A scalable and maintainable Legal Technology MVP application built with modern web technologies.

## 🏗️ Architecture

This is a monorepo containing:
- **Frontend**: React + TypeScript + Vite
- **Backend**: Node.js + Express + TypeScript
- **CI/CD**: GitHub Actions
- **Package Management**: npm workspaces

## 📁 Project Structure

```
legaltech-mvp/
├── frontend/                 # React frontend application
│   ├── src/
│   ├── package.json
│   └── ...
├── backend/                  # Node.js backend API
│   ├── src/
│   ├── package.json
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

- **Node.js 18+** - [Download here](https://nodejs.org/)
- **npm 9+** - Comes with Node.js
- **Git** - [Download here](https://git-scm.com/)

**Verify installation:**
```bash
node --version    # Should be 18.0.0 or higher
npm --version     # Should be 9.0.0 or higher  
git --version     # Any recent version
```

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Liongchenglex/LegalTech.git
   cd LegalTech
   ```

2. **Install all dependencies**
   ```bash
   npm run install:all
   ```

3. **Start development servers**
   ```bash
   npm run dev
   ```
   This starts both frontend (http://localhost:5173) and backend (http://localhost:3000) concurrently.

4. **Verify everything works**
   - Open http://localhost:5173 in your browser
   - You should see the LegalTech MVP homepage
   - Check that "Backend API: ✅ Connected" appears on the page

### Individual Commands

- **Frontend only**: `npm run dev:frontend`
- **Backend only**: `npm run dev:backend`

## 📜 Available Scripts

### Root Level Commands

| Command | Description |
|---------|-------------|
| `npm run dev` | Start both frontend and backend in development mode |
| `npm run build` | Build both applications for production |
| `npm run test` | Run tests for both applications |
| `npm run lint` | Lint code in both applications |
| `npm run typecheck` | Type check both applications |
| `npm run install:all` | Install dependencies for all packages |
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

### Backend Commands (in `backend/` directory)

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server with nodemon |
| `npm run build` | Compile TypeScript to JavaScript |
| `npm start` | Start production server |
| `npm test` | Run tests with Jest |
| `npm run lint` | Lint TypeScript code |
| `npm run typecheck` | Type check without emitting files |

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
- **Runtime**: Node.js
- **Framework**: Express.js
- **Language**: TypeScript
- **Database**: MongoDB (Mongoose)
- **Authentication**: JWT
- **Validation**: Joi
- **Security**: Helmet, CORS
- **Testing**: Jest
- **Code Quality**: ESLint, Prettier

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
NODE_ENV=development
PORT=3000
MONGODB_URI=mongodb://localhost:27017/legaltech
JWT_SECRET=your_jwt_secret_here
JWT_EXPIRES_IN=7d
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:3000/api
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