# 📦 CRUD User API

REST API sederhana untuk manajemen data user, dibangun dengan **FastAPI (Python)** menggunakan data dummy in-memory.

> ⚠️ Ini adalah aplikasi existing yang sudah berjalan di production. **Jangan diubah.**

---

## 🛠 Tech Stack

- Python 3.12
- FastAPI 0.115.0
- Uvicorn 0.30.6
- Docker
- Docker Compose

---

## 🚀 Menjalankan Aplikasi

### Via Docker Compose (recommended)

1. Copy file environment:

```bash
cp .env.example .env
```

2. Sesuaikan nilainya bila perlu:

```env
API_KEY=your-secret-api-key
HOST_PORT=8080
```

3. Jalankan service:

```bash
docker compose up -d --build
```

Aplikasi akan tersedia di:

- UI Dashboard: `http://localhost:8080`
- API info: `http://localhost:8080/api`
- Swagger UI: `http://localhost:8080/docs`

Untuk menghentikan service:

```bash
docker compose down
```

### Catatan port

- Port default host adalah `8080`.
- Dari pengecekan container yang sedang berjalan, port `8080` saat ini **belum dipakai**, jadi tidak conflict.
- Jika nanti bentrok, cukup ubah `HOST_PORT` di `.env`, misalnya menjadi `8082`.

Contoh:

```env
HOST_PORT=8082
```

Lalu akses aplikasi di `http://localhost:8082`.

### Via Docker

```bash
# Build image
docker build -t crud-api:latest .

# Run container
docker run -d --name crud-api \
  -p 8080:8000 \
  -e API_KEY="your-secret-api-key" \
  crud-api:latest
```

---

## 🌍 Environment Variables

| Variable    | Default                | Keterangan                         |
|-------------|------------------------|------------------------------------|
| `API_KEY`   | `secret-api-key-12345` | API Key untuk autentikasi          |
| `HOST_PORT` | `8080`                 | Port host untuk expose service     |

---

## 🔐 Autentikasi

Semua endpoint `/users` membutuhkan header:

```text
X-API-Key: <your-api-key>
```

Endpoint `/`, `/api`, dan `/health` bebas diakses tanpa key.

---

## 📡 Endpoints

### `GET /`
Menampilkan UI dashboard sederhana untuk melihat dan mengelola data user.

Buka langsung di browser:

```text
http://localhost:8080
```

---

### `GET /api`
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

> Jika `HOST_PORT` diubah, sesuaikan port pada URL request.

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
| Field   | Type    | Required | Keterangan |
|---------|---------|----------|------------|
| `name`  | string  | ✅       | Nama user  |
| `email` | string  | ✅       | Email user |
| `age`   | integer | ❌       | Usia user  |

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

| Code | Keterangan                             |
|------|----------------------------------------|
| 200  | OK                                     |
| 201  | Created                                |
| 401  | Unauthorized (API Key salah/tidak ada) |
| 404  | User tidak ditemukan                   |
| 422  | Validation error                       |

---

## ⚠️ Catatan

- Data bersifat **in-memory**, akan reset setiap kali container di-restart.
- UI dashboard memakai API yang sama dan meminta `API_KEY` untuk load/manipulasi data user.
- Aplikasi ini adalah **existing service** yang digunakan oleh middleware. Tidak boleh dimodifikasi.
