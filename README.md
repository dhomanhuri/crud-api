# 📦 CRUD User API

REST API sederhana untuk manajemen data user, dibangun dengan **FastAPI (Python)** menggunakan data dummy in-memory.

> ⚠️ Ini adalah aplikasi existing yang sudah berjalan di production. **Jangan diubah.**

---

## 🛠 Tech Stack

- Python 3.12
- FastAPI 0.115.0
- Uvicorn 0.30.6
- Docker

---

## 🚀 Menjalankan Aplikasi

### Via Docker (recommended)

```bash
# Build image
docker build -t crud-api:latest .

# Run container
docker run -d --name crud-api \
  -p 8080:8000 \
  -e API_KEY="your-secret-api-key" \
  crud-api:latest
```

### Environment Variables

| Variable  | Default                  | Keterangan          |
|-----------|--------------------------|---------------------|
| `API_KEY` | `secret-api-key-12345`   | API Key untuk autentikasi |

---

## 🔐 Autentikasi

Semua endpoint `/users` membutuhkan header:

```
X-API-Key: <your-api-key>
```

Endpoint `/` dan `/health` bebas diakses tanpa key.

---

## 📡 Endpoints

### `GET /`
Info aplikasi (tanpa auth).

**Response:**
```json
{
  "message": "CRUD User API is running 🚀"
}
```

---

### `GET /health`
Health check (tanpa auth).

**Response:**
```json
{
  "status": "ok"
}
```

---

### `GET /users`
Ambil semua user.

**Request:**
```bash
curl http://localhost:8080/users \
  -H "X-API-Key: your-secret-api-key"
```

**Response `200`:**
```json
[
  { "id": "1", "name": "Ilyas", "email": "ilyas@example.com", "age": 25 },
  { "id": "2", "name": "Budi",  "email": "budi@example.com",  "age": 30 },
  { "id": "3", "name": "Siti",  "email": "siti@example.com",  "age": 22 }
]
```

---

### `GET /users/{id}`
Ambil user berdasarkan ID.

**Request:**
```bash
curl http://localhost:8080/users/1 \
  -H "X-API-Key: your-secret-api-key"
```

**Response `200`:**
```json
{ "id": "1", "name": "Ilyas", "email": "ilyas@example.com", "age": 25 }
```

**Response `404`:**
```json
{ "detail": "User not found" }
```

---

### `POST /users`
Buat user baru.

**Request:**
```bash
curl -X POST http://localhost:8080/users \
  -H "X-API-Key: your-secret-api-key" \
  -H "Content-Type: application/json" \
  -d '{"name": "Ahmad", "email": "ahmad@example.com", "age": 28}'
```

**Body:**
| Field   | Type    | Required | Keterangan        |
|---------|---------|----------|-------------------|
| `name`  | string  | ✅       | Nama user         |
| `email` | string  | ✅       | Email user        |
| `age`   | integer | ❌       | Usia user         |

**Response `201`:**
```json
{ "id": "a1b2c3d4", "name": "Ahmad", "email": "ahmad@example.com", "age": 28 }
```

---

### `PUT /users/{id}`
Update data user.

**Request:**
```bash
curl -X PUT http://localhost:8080/users/1 \
  -H "X-API-Key: your-secret-api-key" \
  -H "Content-Type: application/json" \
  -d '{"name": "Ilyas Updated", "email": "ilyas@new.com", "age": 26}'
```

**Response `200`:**
```json
{ "id": "1", "name": "Ilyas Updated", "email": "ilyas@new.com", "age": 26 }
```

---

### `DELETE /users/{id}`
Hapus user.

**Request:**
```bash
curl -X DELETE http://localhost:8080/users/1 \
  -H "X-API-Key: your-secret-api-key"
```

**Response `200`:**
```json
{ "message": "User 1 deleted" }
```

---

## 📋 HTTP Status Codes

| Code | Keterangan              |
|------|-------------------------|
| 200  | OK                      |
| 201  | Created                 |
| 401  | Unauthorized (API Key salah/tidak ada) |
| 404  | User tidak ditemukan    |
| 422  | Validation error        |

---

## 📖 Swagger UI

Dokumentasi interaktif tersedia di:

```
http://localhost:8080/docs
```

---

## ⚠️ Catatan

- Data bersifat **in-memory** — akan reset setiap kali container di-restart.
- Aplikasi ini adalah **existing service** yang digunakan oleh middleware. Tidak boleh dimodifikasi.
