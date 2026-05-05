FROM python:3.11-slim

WORKDIR /app

# Create data directory
RUN mkdir -p data

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8002

CMD ["python", "main.py"]