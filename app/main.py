import os
import re
import time

import requests
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

RESEND_API_KEY = os.environ["RESEND_API_KEY"]
CONTACT_RECIPIENT = os.environ.get("CONTACT_RECIPIENT", "m.canada13960@gmail.com")

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

# Simple in-memory spam guard (the original Vercel function had none at all).
# No database needed for a service this small and stateless — an in-process
# dict is fine; it just resets on restart/redeploy, which is an acceptable
# tradeoff here.
RATE_LIMIT_MAX = 3
RATE_LIMIT_WINDOW = 600  # 10 minutes
_recent_submissions: dict[str, list[float]] = {}

app = FastAPI(title="portfolio-backend")


class ContactIn(BaseModel):
    name: str
    email: str
    message: str


def client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def is_rate_limited(ip: str) -> bool:
    now = time.time()
    timestamps = [t for t in _recent_submissions.get(ip, []) if now - t < RATE_LIMIT_WINDOW]
    _recent_submissions[ip] = timestamps
    return len(timestamps) >= RATE_LIMIT_MAX


@app.post("/api/contact")
def contact(payload: ContactIn, request: Request):
    ip = client_ip(request)
    if is_rate_limited(ip):
        raise HTTPException(status_code=429, detail="Trop de messages envoyés, réessaie plus tard")

    name = payload.name.strip()
    email = payload.email.strip()
    message = payload.message.strip()

    if len(name) < 2 or not EMAIL_RE.match(email) or len(message) < 10:
        raise HTTPException(status_code=400, detail="Champs invalides")
    if len(message) > 2000:
        raise HTTPException(status_code=400, detail="Message trop long")

    resp = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "from": "Portfolio <onboarding@resend.dev>",
            "to": [CONTACT_RECIPIENT],
            "reply_to": email,
            "subject": f"Nouveau message de {name}",
            "text": f"Nom: {name}\nEmail: {email}\n\nMessage:\n{message}",
        },
        timeout=10,
    )
    if not resp.ok:
        raise HTTPException(status_code=502, detail="Échec de l'envoi")

    _recent_submissions.setdefault(ip, []).append(time.time())
    return {"ok": True}


@app.get("/health")
def health():
    return {"status": "ok"}
