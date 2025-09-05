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
git clone https://github.com/rahul7011/URL-Shortener
cd URL-Shortener
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

## 📸 Screenshots

### Infrastructure & Setup
<div align="center">
  <img width="90%" alt="Containerized setup with FastAPI, MongoDB, Redis, Elasticsearch, and Kibana running via Docker Compose" src="https://github.com/user-attachments/assets/c96c05c6-0802-4d06-926a-7b9041d6b26d" />
  <p><em>Dockerized microservices architecture with all dependencies containerized</em></p>
</div>

### Analytics Dashboard
<div align="center">
  <img width="90%" alt="Analytics API showing total click count and last accessed timestamp for a short URL" src="https://github.com/user-attachments/assets/cde683c8-a264-40c8-9a97-814cda58fcaf" />
  <p><em>Detailed analytics for individual short URLs with click statistics</em></p>
</div>

### Leaderboards
<div align="center">
  <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 20px;">
    <div style="flex: 1; min-width: 300px;">
      <img width="100%" alt="Global leaderboard ranking domains by total clicks" src="https://github.com/user-attachments/assets/205b6b1e-5560-47e6-8a5f-bc956793b851" />
      <p><em>Global leaderboard (Redis Sorted Set) tracking all-time top domains</em></p>
    </div>
    <div style="flex: 1; min-width: 300px;">
      <img width="100%" alt="Daily leaderboard for trending domains" src="https://github.com/user-attachments/assets/8d2b2f8e-f822-4575-be7e-9061a84e0205" />
      <p><em>Daily trending leaderboard (auto-expiring Redis Sorted Set)</em></p>
    </div>
  </div>
</div>

### Search Functionality
<div align="center">
  <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 20px;">
    <div style="flex: 1; min-width: 300px;">
      <img width="100%" alt="Exact short ID match in Elasticsearch" src="https://github.com/user-attachments/assets/92f83514-347a-4d8a-b158-5513755cfcad" />
      <p><em>Precise search results for short URL identifiers</em></p>
    </div>
    <div style="flex: 1; min-width: 300px;">
      <img width="100%" alt="Fuzzy search for original URLs" src="https://github.com/user-attachments/assets/676556d8-1f65-4d7a-9da0-c211e9096b91" />
      <p><em>Fuzzy search capabilities for original URLs</em></p>
    </div>
  </div>
</div>

### Data Visualization
<div align="center">
  <img width="90%" alt="Kibana analytics dashboard showing top domains and click trends" src="https://github.com/user-attachments/assets/47628057-6859-43e3-a824-67597ba7729f" />
  <p><em>Interactive Kibana dashboard visualizing top domains and temporal click patterns</em></p>
</div>

---

## License

MIT

---

## Author

Rahul Maurya
