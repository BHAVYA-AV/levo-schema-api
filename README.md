# Levo Schema API – OpenAPI Versioning & Validation Backend

This project implements a complete backend for managing OpenAPI specs via CLI or API.  
Built with **FastAPI**, it supports:

- Uploading `.yaml` / `.json` OpenAPI specs
- Schema validation using `openapi-spec-validator`
- Automatic versioning by application & service
- Retrieval of latest or specific versioned schemas
- Unit testing with `pytest`

---

## Setup Instructions

### 1. Clone & Setup Environment

```bash
git clone <repo-url>
cd levo_schema_api
python -m venv venv
venv\Scripts\activate   
pip install -r requirements.txt
```
---

### 2. Run the App

```bash
uvicorn app.main:app --reload
```

Then visit:  
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Folder Structure

```
levo_schema_api/
├── app/                    # FastAPI logic
│   ├── main.py             # App entrypoint
│   ├── routes.py           # API routes
│   ├── database.py         # SQLAlchemy DB setup
│   ├── models.py           # SchemaVersion model
│   └── validators.py       # OpenAPI validation logic
├── schemas/                # Uploaded OpenAPI files (auto-saved)
├── sample_openapi.yaml     # Example OpenAPI file for testing
├── schemas.db              # SQLite DB storing metadata
├── tests/                  # Unit tests
│   └── test_upload.py
├── README.md
├── requirements.txt
```

---

## API Endpoints

### `POST /upload`
Upload and validate OpenAPI YAML/JSON specs.

**Form Fields:**
- `application` (str, required)
- `service` (str, optional)
- `file` (UploadFile)

Returns: version, file path

---

### `GET /get-latest`
Fetch the latest version of a schema.

**Query Parameters:**
- `application` (str)
- `service` (str)

---

### `GET /get-schema`
Fetch a specific version.

**Query Parameters:**
- `application` (str)
- `service` (str)
- `version` (int)

---

## Run Unit Test

```bash
pytest tests/test_upload.py
```

---

## Curl Example

curl -X 'POST' \
  'http://127.0.0.1:8000/upload' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@schema_20250607113853.yaml' \
  -F 'application=demo-app' \
  -F 'service=booking-service'

  
## Notes

- Schemas are saved in: `schemas/{application}/{service}/schema_v{version}.yaml`
- Version is auto-incremented using SQLite table `schema_versions`

---

## Author

Developed by Bhavya for the Levo.ai Backend Take-Home Assignment – 2025
