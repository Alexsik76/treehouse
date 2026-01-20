# treehouse

## Local Development Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose

### Backend

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .\.venv\Scripts\Activate.ps1
   # Linux/Mac:
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the server:
   ```bash
   uvicorn src.main:app --reload
   ```

### Frontend

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

### Database

The project is designed to use a remote database (e.g., on `treehouse.lan`) during development.

1. **On the Server**:
   Ensure the database container is running and ports are exposed:

   ```bash
   docker-compose up -d db
   ```

   (Verify port `5432` is exposed in `docker-compose.yml`)

2. **Local Configuration**:
   Ensure `backend/.env` points to the remote host:
   ```properties
   DB_HOST=treehouse.lan
   ```
