from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Privacy Inspector Backend",
    description="API for Privacy Inspector",
    version="0.1.0",
)

# Allow frontend local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    "Health check endpoint."
    return {"status": "ok"}
