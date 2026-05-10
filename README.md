# Excel zu Text Konverter

Kleiner Web-Server der Excel/CSV Dateien in Text umwandelt.

## Deployment auf Railway

1. Geh auf https://railway.app und erstelle einen kostenlosen Account
2. Klick auf "New Project" → "Deploy from GitHub repo"
3. Lade diese Dateien auf GitHub hoch (oder nutze Railway's direkten Upload)
4. Railway deployt automatisch und gibt dir eine URL wie: https://dein-projekt.railway.app

## API Nutzung

POST /convert
- Form-data: file = Excel/CSV Datei
- Response: {"text": "CSV Text", "rows": 8}

GET /health
- Response: {"status": "ok"}
