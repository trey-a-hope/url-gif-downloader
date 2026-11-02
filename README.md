# URL GIF Downloader

A tiny Flask app that downloads a GIF from a URL and hands it to your browser as a file. Paste a GIF link into the page, and the server fetches it with browser-like headers (which gets past sites that block hotlinking), checks that it really is a GIF, and returns it as a download.

## Endpoints

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/` | a simple page with a URL box and a **Download GIF** button |
| `GET` | `/download-gif?url=<gif url>` | fetches the URL and returns it as an `image/gif` attachment |

`/download-gif` returns `400` if the URL is missing or invalid (checked with `validators`) or the response isn't a GIF, and `500` if the download fails. The file keeps its original name when it ends in `.gif`, and otherwise is saved as `downloaded.gif`. CORS is open to all origins, so other front ends can call it too.

## Getting started

Requires Python 3.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py              # http://localhost:5000
```

Set `PORT` to use a different port (the app binds to `0.0.0.0`).

```sh
curl -OJ "http://localhost:5000/download-gif?url=https://example.com/funny.gif"
```

## Notes

- The server will fetch any URL it's given, so put it behind auth or an allow-list before exposing it publicly.
- It uses Flask's development server. For production, run it under a WSGI server such as `gunicorn app:app`.

## Tech stack

- Flask 2.0, Werkzeug 2.0, requests, validators, flask-cors
