# Kraken OHLCVT Backend API

A beginner-friendly backend application built with FastAPI and PostgreSQL for storing and fetching OHLCVT crypto market data.

---

## Features

- Upload Kraken OHLCVT CSV data to PostgreSQL
- Store all data in one table
- REST APIs for inserting and fetching data
- PostgreSQL integration using SQLAlchemy
- Environment variable support with `.env`
- FastAPI Swagger documentation

---

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pandas

---

## Project Structure

```bash
kraken_ohlcvt/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
│
├── kraken_data/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd kraken_ohlcvt
```

---

### 2. Create a Virtual Environment

#### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/kraken_db
```

---

## Database Setup

Make sure PostgreSQL is installed and running.

Create the database:

```sql
CREATE DATABASE kraken_db;
```

---

## Running the Server

Start the FastAPI application:

```bash
uvicorn app.main:app --reload
```

Server runs on:

```bash
http://127.0.0.1:8000
```

---

## API Documentation

FastAPI automatically generates API documentation.

### Swagger UI

```bash
http://127.0.0.1:8000/docs
```

### ReDoc

```bash
http://127.0.0.1:8000/redoc
```

---

## API Endpoints

### Insert OHLCVT Data

```http
POST /insert
```

Example JSON body:

```json
{
  "timestamp": "2025-01-01T12:00:00",
  "open": 65000.5,
  "high": 65200.8,
  "low": 64800.1,
  "close": 65120.4,
  "volume": 120.75,
  "trades": 340
}
```

---

### Fetch Data

```http
GET /data
```

Returns rows from the `ohlcvt` table.


---

## Database Schema

| Column | Type |
|---|---|
| timestamp | TIMESTAMP |
| open | DOUBLE PRECISION |
| high | DOUBLE PRECISION |
| low | DOUBLE PRECISION |
| close | DOUBLE PRECISION |
| volume | DOUBLE PRECISION |
| trades | BIGINT |

---
