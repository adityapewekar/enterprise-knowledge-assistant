# Enterprise Knowledge Assistant

An intelligent knowledge management system that leverages OpenAI and LangGraph to provide an interactive question-answering interface for enterprise documents. This application allows users to upload PDFs, build a searchable knowledge base, and query it using natural language.

## Features

- **AI-Powered Q&A**: Ask natural language questions about your documents using OpenAI's GPT models
- **Vector Database**: Efficient document retrieval using ChromaDB for semantic search
- **PDF Support**: Extract and index content from PDF documents
- **LangGraph Workflow**: Sophisticated multi-step reasoning using LangGraph agents
- **REST API**: FastAPI-based backend for seamless integration
- **CORS Support**: Pre-configured for Angular frontend integration
- **Azure Integration**: Optional Azure Key Vault and Identity support for enterprise security
- **Fuzzy Matching**: Intelligent search with fuzzy string matching
- **Token Management**: Track, monitor, and control OpenAI API token usage and costs
- **Usage Limits**: Set daily, monthly, and cost-based limits per user role
- **Analytics Dashboard**: Comprehensive token usage statistics and trends

## Prerequisites

### Backend (Python)

- **Python 3.8+**: The application is built with Python
- **pip**: Python package manager (usually comes with Python)
- **Git**: For cloning the repository
- **OpenAI API Key**: Required for AI-powered features
  - Sign up at https://platform.openai.com/
  - Get your API key from https://platform.openai.com/account/api-keys
- **Virtual Environment**: Recommended (venv or conda)

### Frontend (Angular UI)

- **Node.js 18+**: Required for Angular development
  - Download from https://nodejs.org/
  - Includes npm package manager
- **npm 9+**: Node package manager (comes with Node.js)
- **Angular CLI 21+**: Install globally with `npm install -g @angular/cli`

### Optional Prerequisites

- **Azure Setup** (Optional): If using Azure Key Vault for secrets management:
  - Azure subscription
  - Azure CLI installed
  - Appropriate Azure RBAC permissions

## Setup Instructions

### Backend Setup (Python FastAPI)

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/enterprise-knowledge-assistant.git
cd enterprise-knowledge-assistant
```

#### 2. Create a Virtual Environment

##### Using venv (Windows)
```bash
python -m venv .venv
.venv\Scripts\activate
```

##### Using venv (macOS/Linux)
```bash
python3 -m venv .venv
source .venv/bin/activate
```

##### Using conda
```bash
conda create -n eka python=3.8
conda activate eka
```

#### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- FastAPI and Uvicorn (web framework)
- LangChain and LangGraph (AI workflow)
- OpenAI (AI models)
- ChromaDB (vector database)
- PyMuPDF (PDF processing)
- Azure libraries (optional, for enterprise security)

#### 4. Configure Environment Variables

Create a `.env` file in the project root directory:

```bash
# Create .env file
echo > .env
```

Add the following environment variables to the `.env` file:

```env
# Azure Configuration
AZURE_KEYVAULT_URL=https://your-keyvault.vault.azure.net/
AZURE_TENANT_ID=your_azure_tenant_id
AZURE_CLIENT_ID=your_azure_client_id
AZURE_CLIENT_SECRET=your_azure_client_secret

# Optional: Application Configuration
LOG_LEVEL=INFO
```

**Important**: Never commit the `.env` file to version control. It's already in `.gitignore`.

### Frontend Setup (Angular)

#### 1. Navigate to the UI Directory

```bash
cd presentation/ui/eka
```

#### 2. Install Node Dependencies

```bash
npm install
```

This will install all required packages including:
- Angular 21 framework
- Angular Material (UI components)
- Angular CDK (Component Development Kit)
- RxJS (reactive programming)
- TypeScript

#### 3. Configure Backend URL (Optional)

If your backend runs on a different port or host, update the API configuration in the Angular environment files:

**File**: `src/environments/environment.ts`
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000'  // Update if backend runs on different port
};
```

**File**: `src/environments/environment.prod.ts`
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://api.yourdomain.com'  // Production API URL
};
```

## Build and Run

### Running the Application (Backend + Frontend)

The application consists of two parts: a Python FastAPI backend and an Angular frontend. You can run them in separate terminals.

#### Terminal 1: Start the Backend (FastAPI)

From the project root directory:

```bash
# Activate Python virtual environment (if not already activated)
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Start the FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at: `http://localhost:8000`

#### Terminal 2: Start the Frontend (Angular)

From a new terminal:

```bash
cd presentation/ui/eka
npm start
```

The frontend will be available at: `http://localhost:4200`

### Verify Both Services Are Running

Once both servers are running, you should see:

**Backend (Terminal 1)**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Frontend (Terminal 2)**:
```
⠙ Building...
✔ Compiled successfully.
✔ build: 15.234s

→ Local:   http://localhost:4200/
```

### Access the Application

1. **Frontend UI**: Open your browser and navigate to `http://localhost:4200/`
2. **Backend API Documentation**: Visit `http://localhost:8000/docs` (Swagger UI)
3. **Alternative API Docs**: Visit `http://localhost:8000/redoc` (ReDoc)

### Build for Production

#### Backend Production Build

```bash
# The FastAPI app is already production-ready
# For production deployment without auto-reload:
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Frontend Production Build

From the `presentation/ui/eka` directory:

```bash
npm run build
```

This will create an optimized build in the `dist/eka/` directory. The output can be:
- Deployed to a web server (Nginx, Apache)
- Served from Azure Static Web Apps
- Integrated with a Docker container

### Alternative: Run Backend Only (for API Testing)

If you only want to run the backend without the frontend:

```bash
# Activate virtual environment and run FastAPI
.venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Then visit `http://localhost:8000/docs` to test the API using Swagger UI.

## Project Structure

```
enterprise-knowledge-assistant/
├── main.py                          # FastAPI application entry point
├── requirements.txt                 # Python dependencies
├── .env                            # Environment variables (create this)
├── README.md                       # This file
├── application/                    # Application layer
│   └── decorators.py              # Custom decorators
├── domain/                        # Domain models
│   └── models/                    # Data models
├── infrastructure/                # Infrastructure layer
│   ├── langgraph_service.py      # LangGraph workflow management
│   └── chroma_service.py         # ChromaDB integration
├── presentation/                  # API and UI layer
│   ├── api/
│   │   └── controllers/          # API endpoint controllers
│   │       ├── ask_controller.py
│   │       └── kb_controller.py
│   └── ui/                        # Angular Frontend Application
│       └── eka/                   # Angular Project
│           ├── src/               # Angular source code
│           │   ├── app/           # Angular components & services
│           │   ├── assets/        # Static assets
│           │   ├── environments/  # Environment configuration
│           │   └── main.ts        # Angular entry point
│           ├── public/            # Public assets
│           ├── angular.json       # Angular CLI configuration
│           ├── package.json       # Node dependencies
│           ├── tsconfig.json      # TypeScript configuration
│           └── README.md          # Angular project documentation
└── chroma_db/                     # ChromaDB data (auto-generated)
```

### Directory Explanations

- **main.py**: Entry point for the FastAPI backend. Handles routing and middleware setup.
- **application/**: Contains business logic, decorators, and utility functions.
- **domain/**: Defines data models and domain entities.
- **infrastructure/**: Contains integration with external services (ChromaDB, LangGraph).
- **presentation/api/**: REST API controllers and endpoints.
- **presentation/ui/eka/**: Complete Angular 21 frontend application with Material Design UI.
- **chroma_db/**: Vector database storage (auto-created, safe to delete for reset).

## Development Workflow

### Backend Development (Python)

#### 1. Activate Virtual Environment

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

#### 2. Start the Development Server with Auto-Reload

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 3. Make Changes and Test

- Edit Python files in the backend
- Changes will automatically reload (due to `--reload` flag)
- View API documentation at http://localhost:8000/docs

#### 4. Deactivate Virtual Environment

```bash
deactivate
```

### Frontend Development (Angular)

#### 1. Navigate to Angular Project

```bash
cd presentation/ui/eka
```

#### 2. Start the Development Server with Hot Module Replacement (HMR)

```bash
npm start
```

Or explicitly:

```bash
ng serve
```

#### 3. Make Changes and Test

- Edit Angular components and services
- Changes will automatically reload in the browser
- Open http://localhost:4200/ to view your changes

#### 4. Generate New Components

```bash
# Create a new component
ng generate component components/my-component

# Create a new service
ng generate service services/my-service

# Create a new pipe
ng generate pipe pipes/my-pipe
```

#### 5. Run Angular Tests

```bash
npm test
```

Or:

```bash
ng test
```

### Full Stack Development (Backend + Frontend)

To develop the complete application:

1. **Terminal 1 - Backend**:
   ```bash
   .venv\Scripts\activate
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Terminal 2 - Frontend**:
   ```bash
   cd presentation/ui/eka
   npm start
   ```

3. **Terminal 3 - IDE/Editor** (optional):
   - Use VS Code or your preferred editor
   - Frontend code changes: Update in `presentation/ui/eka/src/`
   - Backend code changes: Update in root directory

### CORS Configuration

The backend is pre-configured to accept requests from the Angular dev server. If you change the frontend port, update `main.py`:

```python
origins = [
    "http://localhost:4200",      # Default Angular port
    "http://127.0.0.1:4200",      # Localhost alternative
    "http://localhost:PORT",       # Your custom port
]
```

## Common Issues and Troubleshooting

### Backend Issues

#### Issue: OpenAI API Key Error
**Solution**: Ensure your OpenAI API key is correctly set in the `.env` file and has proper permissions.

#### Issue: Port 8000 Already in Use
**Solution**: Specify a different port:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

#### Issue: ChromaDB Connection Error
**Solution**: Ensure the `chroma_db/` directory exists and is writable. If corrupted, you can safely delete it and restart the application.

### Frontend Issues

#### Issue: Port 4200 Already in Use
**Solution**: Specify a different port:
```bash
ng serve --port 4300
```

Then update the backend CORS configuration to accept the new port.

#### Issue: CORS Error ("Access to XMLHttpRequest has been blocked")
**Solution 1**: Update `main.py` backend:
```python
origins = [
    "http://localhost:4200",
    "http://localhost:4300",  # Or your custom port
    "http://127.0.0.1:4200"
]
```

**Solution 2**: Ensure the frontend is making requests to the correct backend URL:
```typescript
// In your Angular service
private apiUrl = 'http://localhost:8000';  // Update if backend runs elsewhere
```

#### Issue: `npm install` fails or slow
**Solution**: Clear npm cache and reinstall:
```bash
npm cache clean --force
rm -r node_modules package-lock.json  # or del node_modules /s on Windows
npm install
```

#### Issue: Angular compilation error
**Solution**: Ensure you have the correct Node.js version:
```bash
node --version  # Should be 18+
npm --version   # Should be 9+
```

### Integration Issues

#### Issue: Frontend can't reach backend API
**Solution**: 
1. Verify backend is running: `http://localhost:8000/docs`
2. Check frontend's API URL configuration in `environment.ts`
3. Verify backend CORS settings include frontend origin
4. Check browser console for exact error messages

#### Issue: Hot Module Replacement (HMR) not working in Angular
**Solution**: Restart the Angular dev server:
```bash
# Stop with Ctrl+C, then restart
npm start
```

## Environment-Specific Configuration

### Development Setup

#### Backend Development
```bash
# Run with auto-reload for development
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Development
```bash
cd presentation/ui/eka
# Run with HMR enabled (default)
npm start
```

### Staging Setup

#### Backend Staging
```bash
# Run without reload with increased workers
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2
```

#### Frontend Staging
```bash
cd presentation/ui/eka
# Build staging bundle with source maps
ng build --configuration development
```

### Production Setup

#### Backend Production
```bash
# Run with multiple workers for better performance
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Frontend Production
```bash
cd presentation/ui/eka
# Build optimized production bundle
ng build --configuration production
```

The optimized build will be in `dist/eka/` and ready for deployment to:
- Azure Static Web Apps
- Nginx/Apache web servers
- Cloud CDN services

### Environment Files for Angular

**Development** (`src/environments/environment.ts`):
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000'
};
```

**Production** (`src/environments/environment.prod.ts`):
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://api.production.domain.com'
};
```

## Usage

### Using the Web UI (Angular Frontend)

1. **Access the Application**:
   - Navigate to `http://localhost:4200` in your browser
   - The Angular Material UI will load with the knowledge assistant interface

2. **Upload Documents**:
   - Click on the "Upload" or "Knowledge Base" section
   - Select PDF files to upload
   - The documents will be processed and indexed

3. **Ask Questions**:
   - Use the search/query interface
   - Type your question about the uploaded documents
   - The AI will process and return relevant answers

### Using the API Directly (for Testing/Integration)

#### Access API Documentation

When the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

#### Example API Calls

**Upload a PDF**:
```bash
curl -X POST "http://localhost:8000/kb/upload" \
  -H "accept: application/json" \
  -F "file=@document.pdf"
```

**Ask a Question**:
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the company policy on remote work?"
  }'
```

**Check Knowledge Base Status**:
```bash
curl -X GET "http://localhost:8000/kb/status" \
  -H "accept: application/json"
```

**Clear Knowledge Base**:
```bash
curl -X DELETE "http://localhost:8000/kb/clear" \
  -H "accept: application/json"
```

## Architecture

### Application Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Layer (Angular 21)              │
│  - Components for UI/UX                                     │
│  - Services for API communication                           │
│  - Material Design UI components                            │
│  - Forms for document upload and queries                    │
│  Port: 4200                                                 │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
                         │ (CORS Enabled)
┌────────────────────────▼────────────────────────────────────┐
│               Backend Layer (FastAPI)                       │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            Presentation Layer                         │  │
│  │  - API Controllers (ask_controller, kb_controller)   │  │
│  │  - Request/Response handling                         │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
│  ┌──────────────────────▼──────────────────────────────┐  │
│  │            Application Layer                         │  │
│  │  - Business logic                                   │  │
│  │  - Decorators and utilities                         │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
│  ┌──────────────────────▼──────────────────────────────┐  │
│  │            Infrastructure Layer                      │  │
│  │  - LangGraph service (AI workflow)                  │  │
│  │  - ChromaDB integration (vector storage)            │  │
│  │  - Document processing (PyMuPDF)                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  Port: 8000                                                │
└──────────────────────┬─────────────────┬──────────────────┘
                       │                 │
        ┌──────────────▼──┐   ┌──────────▼──────────┐
        │  OpenAI API     │   │  ChromaDB           │
        │  (GPT Models)   │   │  (Vector Database)  │
        │                 │   │                     │
        │ - gpt-4         │   │  - Document index   │
        │ - gpt-3.5       │   │  - Embeddings       │
        │ - Text embedding│   │  - Similarity search│
        └─────────────────┘   └─────────────────────┘
```

### Technology Stack

**Frontend**:
- Angular 21 (Component-based framework)
- Angular Material (UI components library)
- TypeScript (Strongly-typed JavaScript)
- RxJS (Reactive programming)
- Angular CLI (Development tools)

**Backend**:
- Python 3.8+ (Programming language)
- FastAPI (Web framework)
- Uvicorn (ASGI server)
- LangChain & LangGraph (AI orchestration)
- ChromaDB (Vector database)
- OpenAI (LLM provider)
- PyMuPDF (PDF processing)

**Deployment Ready**:
- Docker support (can be containerized)
- Azure integration (Key Vault, App Service, Static Web Apps)
- CORS configured for production

## Contributing

1. Create a feature branch (`git checkout -b feature/amazing-feature`)
2. Commit your changes (`git commit -m 'Add amazing feature'`)
3. Push to the branch (`git push origin feature/amazing-feature`)
4. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the API documentation at `/docs` when the server is running

## Roadmap

- [ ] Add support for additional document formats (DOCX, TXT)
- [ ] Implement document management UI
- [ ] Add conversation history and context management
- [ ] Multi-language support
- [ ] Advanced analytics and usage metrics
- [ ] Docker containerization
- [ ] CI/CD pipeline setup

## Token Management

The application includes a comprehensive **in-memory token management system** to monitor and control OpenAI API usage:

- **Automatic Tracking**: Every query automatically tracks prompt tokens, completion tokens, and costs
- **In-Memory Storage**: Fast, real-time tracking without database overhead (no persistence)
- **Accurate Token Counting**: Uses OpenAI's tiktoken library for precise token encoding
- **Usage Limits**: Set daily, monthly, and cost-based limits per user role
- **Real-time Monitoring**: Check current usage via REST API endpoints
- **Cost Analysis**: Detailed breakdown of costs by model and role
- **Alert Levels**: Get warnings when approaching limits
- **Session-Based**: Data exists only while application is running (resets on restart)

For detailed information about token management, see [TOKEN_MANAGEMENT_INMEMORY.md](TOKEN_MANAGEMENT_INMEMORY.md)

### Token Management Endpoints

- `GET /tokens/status` - Get service status (in-memory mode indicator)
- `GET /tokens/usage/stats` - Get aggregated token usage statistics
- `GET /tokens/usage/recent` - Get recent token usage records
- `GET /tokens/limits` - Check token limits and current usage
- `GET /tokens/session/{session_id}` - Get specific session information
- `POST /tokens/limits/set` - Set token limits for a role
- `GET /tokens/dashboard` - Get comprehensive usage dashboard

### Quick Example

```bash
# Check service status
curl http://localhost:8000/tokens/status

# Check your current token usage
curl -H "x-role: admin" http://localhost:8000/tokens/limits

# Get usage statistics for last 7 days
curl http://localhost:8000/tokens/usage/stats?days=7

# Set daily limit to 150,000 tokens for admin role
curl -X POST http://localhost:8000/tokens/limits/set \
  -H "Content-Type: application/json" \
  -d '{
    "role": "admin",
    "daily_limit": 150000,
    "cost_limit_usd": 75.0
  }'

# Check a specific session
curl http://localhost:8000/tokens/session/session_abc123
```

### Important Notes

⚠️ **In-Memory Storage**: Token usage data is tracked in application memory only:
- Data is **NOT** persisted to a database
- Data resets when the application restarts
- Limited to the 1000 most recent records
- Perfect for monitoring current session usage
```

## Changelog

### Version 1.0.0
- Initial release
- PDF document indexing
- OpenAI integration
- REST API with FastAPI
- ChromaDB vector storage
- **Token management system**
- **Usage tracking and analytics**
- **Cost monitoring and limits**
