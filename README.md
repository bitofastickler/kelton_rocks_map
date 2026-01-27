# Kelton Rocks — Memorial Map

A lightweight, privacy-respecting web application that allows people to log and visualize Kelton's impact around the world!

Visitors can tap a single button to record an anonymous GPS location (with permission), which is then displayed on a public map along with a running count of total impacts.

This project is intentionally simple, transparent, and respectful of user privacy.

---

## Features

- 🌍 Public interactive map showing rock sighting locations (or impacts!)
- 🔢 Live counter of total impacts
- 📍 One-click geolocation capture (with explicit user consent)
- 🕒 Stores timestamp + GPS coordinates only
- 🔐 No accounts, no names, no emails, no IP storage
- ⚙️ Minimal tech stack, easy to deploy

---

## Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** SQLite (persisted via Render Disk)
- **Frontend:** Server-rendered HTML + JavaScript
- **Mapping:** Leaflet + OpenStreetMap tiles
- **Hosting:** Render

---

## Data Model

Each sighting records **only**:

- `id` — UUID
- `created_at_utc` — ISO 8601 timestamp
- `lat` — latitude
- `lon` — longitude
- `accuracy_m` — reported GPS accuracy (optional)

No personally identifying information is collected or stored.

---

## Local Development

### Requirements
- Python 3.10+
- pip

### Setup

```bash
pip install -r requirements.txt
uvicorn app:app --reload

```
![image](https://raw.githubusercontent.com/bitofastickler/kelton_rocks_map/main/Screenshot%202026-01-27%20133730.png)

