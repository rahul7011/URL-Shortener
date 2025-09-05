# 1. Use an official Python base image
FROM python:3.12.3-slim

# 2. Set working directory inside the container
WORKDIR /app

# 3. Install system dependencies (if needed for Mongo/ES drivers)
RUN apt-get update && apt-get install -y \
    gcc libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy project code into the container
COPY . .

# 6. Expose FastAPI port
EXPOSE 8000

# 7. Run FastAPI with Uvicorn (production-friendly settings)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
