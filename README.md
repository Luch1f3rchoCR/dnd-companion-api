# D&D Companion API — by Luch1f3rchoCR

FastAPI + OpenAPI (Swagger) listo en **/docs**.

## Quickstart (local)
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload  # luego abrir http://localhost:8000/docs

## Docker
docker build -t dnd-api .
docker run -p 8000:8000 dnd-api
