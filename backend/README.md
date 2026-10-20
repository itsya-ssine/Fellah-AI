# Backend

FastAPI service. **Owner: @itsya-ssine.**

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
pytest
```

The API contract lives in `docs/api.yaml`. Build against the contract, and replace mocks endpoint by endpoint.
