import os
import sqlite3
import uuid
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

# --- Config ---
# On Render: set DATA_DIR=/var/data and attach a Disk at /var/data
DATA_DIR = os.getenv("DATA_DIR", ".")
DB_PATH = os.path.join(DATA_DIR, "sightings.sqlite3")

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS sightings (
            id TEXT PRIMARY KEY,
            created_at_utc TEXT NOT NULL,
            lat REAL NOT NULL,
            lon REAL NOT NULL,
            accuracy_m REAL
        )
        """)
        conn.commit()


init_db()


class SightingIn(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    accuracy_m: float | None = Field(None, ge=0)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/stats")
def stats():
    with sqlite3.connect(DB_PATH) as conn:
        (count,) = conn.execute("SELECT COUNT(*) FROM sightings").fetchone()
    return {"count": int(count)}


@app.get("/api/sightings")
def list_sightings(limit: int = 2000):
    # reasonable cap to avoid accidentally serving a giant payload forever
    limit = max(1, min(limit, 5000))
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT id, created_at_utc, lat, lon, accuracy_m FROM sightings ORDER BY created_at_utc DESC LIMIT ?",
            (limit,)
        ).fetchall()

    return {
        "items": [
            {
                "id": r[0],
                "created_at_utc": r[1],
                "lat": r[2],
                "lon": r[3],
                "accuracy_m": r[4],
            }
            for r in rows
        ]
    }


@app.post("/api/sightings")
def create_sighting(sighting: SightingIn):
    sighting_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO sightings (id, created_at_utc, lat, lon, accuracy_m) VALUES (?, ?, ?, ?, ?)",
            (sighting_id, created_at, sighting.lat, sighting.lon, sighting.accuracy_m)
        )
        conn.commit()

    return JSONResponse(
        {
            "id": sighting_id,
            "created_at_utc": created_at,
            "lat": sighting.lat,
            "lon": sighting.lon,
            "accuracy_m": sighting.accuracy_m
        },
        status_code=201
    )
