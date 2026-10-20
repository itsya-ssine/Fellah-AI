from fastapi import FastAPI

app = FastAPI(title="Fellah AI API", version="0.0.1")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
