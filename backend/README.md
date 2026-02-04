# Backend API

Python-based backend for the Privacy Inspector tool.

Quick start

- Install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

- Run the FastAPI app:

```bash
python -m uvicorn src.api.app:app --reload --port 8000
```

- Open API docs (Swagger UI): http://localhost:8000/docs
