# URL Shortener Service

A production-grade **URL Shortener** built with **FastAPI** and powered by **MongoDB, Redis, Elasticsearch, and Kibana**.  
This project was designed as a **learning + portfolio project** to demonstrate backend system design, caching, search indexing, analytics, and containerized deployment.

---

## Features

- **Shorten URLs**: Generate short links for long URLs.
- **Custom Aliases**: Choose your own short URL keyword.
- **TTL (Expiration)**: Set expiry for short URLs (default: 7 days).
- **Redirection**: Short URL redirects to the original URL.
- **Analytics**: Track click count and last accessed timestamp.
- **Leaderboard**: See top accessed domains (global & daily) using Redis Sorted Sets.
- **Search**: Search URLs by original link, alias, or analytics filters (Elasticsearch).
- **Caching**: Redis cache for fast redirection.
- **Filtering**: Filter by click count or date range.
- **Visualization with Kibana**: Visualization with Kibana: Interactive dashboards for Top Domains Leaderboard and Clicks Over Time analytics.
- **Deployment**: Dockerized with docker-compose, includes FastAPI, MongoDB, Redis, Elasticsearch, and Kibana.
---

## Tech Stack

- **Backend**: FastAPI (async Python web framework)
- **Database**: MongoDB (with Motor async driver)
- **Cache & Leaderboard**: Redis
- **Search**: Elasticsearch
- **Visualization:** Kibana
- **Containerization**: Docker, Docker Compose

---

## Getting Started

### 1. Clone the Repository

```sh
git clone <your-repo-url>
cd <repo-folder>
```

### 2. Environment Variables

Copy `.env` and adjust if needed (default values work with Docker Compose):

```env
MONGO_URI=mongodb://mongodb:27017
REDIS_URI=redis://redis:6379
ELASTIC_PASSWORD=MineSweeper@akaRocks
ELASTIC_TOKEN=...
ES_URI=http://elastic:${ELASTIC_PASSWORD}@elasticsearch:9200
```

To generate the `ELASTIC_TOKEN`, run the following command inside the Elasticsearch container:

```sh
docker exec -it elasticsearch bin/elasticsearch-service-tokens create elastic/kibana kibana-token
```

This will output a token string like:

```
eyJhbGciOiJIUzI1NiJ9... (long token string)
```

Copy this token and set it as the value for `ELASTIC_TOKEN` in your `.env` file.

### 3. Build & Run with Docker Compose

```sh
docker-compose up --build
```

- FastAPI: [http://localhost:8000](http://localhost:8000)
- FastAPI Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
- MongoDB: `localhost:27017`
- Redis: `localhost:6379`
- Elasticsearch: `localhost:9200`
- Kibana: [http://localhost:5601](http://localhost:5601)

### 4. API Endpoints

| Method | Endpoint                       | Description                                  |
|--------|-------------------------------|----------------------------------------------|
| POST   | `/shorten`                    | Shorten a URL (optionally with custom alias) |
| GET    | `/{short_id}`                 | Redirect to original URL                     |
| GET    | `/analytics/{short_id}`       | Get click count & last accessed              |
| GET    | `/leaderboard`                | Top domains (global)                         |
| GET    | `/leaderboard/daily`          | Top domains (daily, optional date param)     |
| GET    | `/search`                     | Search URLs (by alias, original, analytics)  |
| GET    | `/ping`                       | Health check                                 |
| GET    | `/search/health`              | Elasticsearch health                         |

#### Example: Shorten a URL

```json
POST /shorten
{
  "original_url": "https://google.com",
  "custom_alias": "rahulgoogle",   // optional
  "ttl": 7                         // optional, days
}
```

#### Example: Redirect

```
GET /rahulgoogle
```

#### Example: Analytics

```
GET /analytics/rahulgoogle
```

#### Example: Leaderboard

```
GET /leaderboard
GET /leaderboard/daily?date=2024-06-01
```

#### Example: Search

```
GET /search?original_url=google
GET /search?short_id=rahulgoogle
GET /search?min_clicks=5
GET /search?created_from=2024-06-01&created_to=2024-06-10
```

---

## Project Structure

```
app/
  main.py         # FastAPI app & endpoints
  db.py           # MongoDB connection & TTL index
  cache.py        # Redis connection
  leaderboard.py  # Redis leaderboard logic
  search.py       # Elasticsearch integration
  enrichData.py   # Data enrichment/testing script
Dockerfile
docker-compose.yml
requirements.txt
README.md
```

---

## Learning Focus

- Async Python (FastAPI, Motor, Redis)
- API design & validation
- Caching strategies
- Leaderboards with Redis Sorted Sets
- Search with Elasticsearch
- Building analytics dashboards with Kibana
- Docker deployment

---

## License

MIT (or your preferred license)

---

## Author

Rahul Maurya
