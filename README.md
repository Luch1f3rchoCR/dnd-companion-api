# D&D Companion API — by Luch1f3rchoCR

Public API wrapper around [D&D 5e](https://www.dnd5eapi.co/), built with **FastAPI** and documented with **Swagger** at `/docs`.

![CI](https://img.shields.io/github/actions/workflow/status/Luch1f3rchoCR/dnd-companion-api/ci.yml?branch=main&label=CI)

> Personal, non-profit project made for learning, practicing and sharing with the community.

---

## 🔌 Available Endpoints

- **Meta**

  - `GET /health` → API status & version
- **Monsters**

  - `GET /monsters` → list with filters (`name`, `type`, `cr_min`, `cr_max`, `limit`, `offset`)
  - `GET /monsters/{index}` → monster detail
- **Spells**

  - `GET /spells` → list with filters (`name`, `limit`, `offset`)
  - `GET /spells/{index}` → spell detail
- **Generic catalog**

  - `GET /dnd/{resource}` → access to any 5e resource (e.g. `classes`, `races`, `equipment`, etc.)
  - `GET /dnd/{resource}/{index}` → resource detail

---

## 🚀 Quickstart (local)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
