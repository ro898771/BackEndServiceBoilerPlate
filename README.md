# BackEnd Service Boilerplate

Django REST API with SQLite — Reviews (Rating + Comment)

---

## Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager

---

## Setup

### 1. Install dependencies

```bash
uv sync
```

---

## Database Commands

### 2. Create migration files (run after changing models)

```bash
uv run python manage.py makemigrations
```

### 3. Apply migrations to the database

```bash
uv run python manage.py migrate
```

### 4. Show all migrations and their status

```bash
uv run python manage.py showmigrations
```

---

## Superuser / Admin Commands

### 5. Create a superuser interactively

```bash
uv run python manage.py createsuperuser
```

### 6. Change a user password

```bash
uv run python manage.py changepassword <username>
```

---

## Run Server Commands

### 7. Run on localhost only (development)

```bash
uv run python manage.py runserver
```

Access at: `http://127.0.0.1:8000`

### 8. Run on all interfaces — intranet / LAN access (everyone on the same network can connect)

```bash
uv run python manage.py runserver 0.0.0.0:8000
```

Other devices on the same network connect using your machine's IP address, e.g.:
`http://192.168.1.x:8000`

To find your IP address:
- **Windows** → run `ipconfig` in terminal, look for **IPv4 Address**

### 9. Run on a custom port

```bash
uv run python manage.py runserver 0.0.0.0:9000
```

---

## Django Admin

| URL | Description |
|-----|-------------|
| `http://<host>:8000/admin/` | Django Admin panel |

Default credentials: `admin` / `admin1234`

---

## API Endpoints

Base path: `/api/dinasour/reviews/`

| Method | URL | Description |
|--------|-----|-------------|
| `GET` | `/api/dinasour/reviews/` | List all reviews |
| `POST` | `/api/dinasour/reviews/` | Create a new review |
| `GET` | `/api/dinasour/reviews/<id>/` | Get a single review |
| `PUT` | `/api/dinasour/reviews/<id>/` | Full update a review |
| `PATCH` | `/api/dinasour/reviews/<id>/` | Partial update a review |
| `DELETE` | `/api/dinasour/reviews/<id>/` | Delete a review |

### Request body (POST / PUT / PATCH)

```json
{
    "rating": 5,
    "comment": "Your comment here"
}
```

- `rating` — integer between **1** and **5**
- `comment` — any text string

---

## Test Script

Run the dummy test script against the API:

```bash
uv run python trial/test_api.py
```

---

## Other Useful Commands

### Check for project errors

```bash
uv run python manage.py check
```

### Open Django shell (interactive Python with Django loaded)

```bash
uv run python manage.py shell
```

### List all available manage.py commands

```bash
uv run python manage.py help
```

### Collect static files (for production)

```bash
uv run python manage.py collectstatic
```
