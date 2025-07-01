# Coffee Shop Backend

FastAPI backend for the Coffee Shop application.

## Setup

1. Create and activate a Python virtual environment with uv:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install Python dependencies:
```bash
uv pip install -r requirements.txt
```

3. Install Node dependencies (for Prisma):
```bash
pnpm install
```

4. Copy environment variables:
```bash
cp .env.example .env
```

5. Push database schema:
```bash
pnpm db:push
```

6. Run the development server:
```bash
pnpm dev
```

The API will be available at http://localhost:5001
API documentation at http://localhost:5001/docs