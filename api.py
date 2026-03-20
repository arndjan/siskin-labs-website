"""Minimal API backend for Siskin Labs static site.

Handles only dynamic endpoints: waitlist, subscribe, confirm, unsubscribe, health.
Returns HTML snippets for HTMX forms, JSON for other endpoints.

Usage: uvicorn api:app --host 0.0.0.0 --port 8082
"""

import os
import re
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from database import init_db, add_to_waitlist, subscribe, confirm_subscriber, unsubscribe
from i18n import t
from mail import send_confirmation

BASE_URL = os.environ.get("BASE_URL", "https://labs.siskin.amsterdam")

app = FastAPI(title="Siskin Labs API", docs_url=None, redoc_url=None)

# Allow the static site to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[BASE_URL, "http://localhost:8080", "http://localhost:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")


@app.on_event("startup")
def startup():
    init_db()


def _detect_lang(request: Request) -> str:
    """Simple language detection from Referer URL or Accept-Language header."""
    referer = request.headers.get("referer", "")
    if "/nl/" in referer:
        return "nl"
    if "/en/" in referer:
        return "en"
    accept = request.headers.get("accept-language", "")
    for part in accept.split(","):
        code = part.split(";")[0].strip().lower()
        if code.startswith("nl"):
            return "nl"
        if code.startswith("en"):
            return "en"
    return "nl"


def _result_html(success: bool, message: str, variant: str = "waitlist") -> str:
    """Render an HTMX result snippet matching the partial templates."""
    if success:
        css_class = "waitlist-result--success"
    elif "already" in message.lower() or "al op" in message.lower() or "al aangemeld" in message.lower():
        css_class = "waitlist-result--info"
    else:
        css_class = "waitlist-result--error"
    return f'<div class="waitlist-result {css_class}">{message}</div>'


# --- Waitlist ---

@app.post("/api/waitlist", response_class=HTMLResponse)
async def waitlist_submit(
    request: Request,
    email: str = Form(...),
    name: str = Form(""),
    product: str = Form("both"),
):
    lang = _detect_lang(request)

    if not EMAIL_RE.match(email):
        return HTMLResponse(_result_html(False, t("waitlist_invalid_email", lang)))

    if product not in ("perch", "cache", "dash", "all"):
        product = "all"

    ip = request.headers.get("x-forwarded-for", request.client.host if request.client else "")
    added = add_to_waitlist(email, name, product, lang, ip)

    if added:
        message = t("waitlist_success", lang)
    else:
        message = t("waitlist_exists", lang)

    return HTMLResponse(_result_html(added, message))


# --- Subscribe ---

@app.post("/api/subscribe", response_class=HTMLResponse)
async def subscribe_submit(
    request: Request,
    email: str = Form(...),
    name: str = Form(""),
    interests: str = Form("all"),
):
    lang = _detect_lang(request)

    if not EMAIL_RE.match(email):
        return HTMLResponse(_result_html(False, t("subscribe_invalid_email", lang), "subscribe"))

    if interests not in ("all", "perch", "cache", "dash", "announcements"):
        interests = "all"

    ip = request.headers.get("x-forwarded-for", request.client.host if request.client else "")
    confirm_token, unsubscribe_token, is_new = subscribe(
        email, name, interests=interests, language=lang, ip_address=ip
    )

    if not confirm_token:
        message = t("subscribe_already_confirmed", lang)
        return HTMLResponse(_result_html(False, message, "subscribe"))

    send_confirmation(email, confirm_token, lang)
    message = t("subscribe_check_email", lang)
    return HTMLResponse(_result_html(True, message, "subscribe"))


# --- Confirm / Unsubscribe ---

@app.get("/api/subscribe/confirm/{token}")
async def subscribe_confirm(request: Request, token: str):
    """Confirm a subscriber and redirect to the static thank-you page."""
    lang = _detect_lang(request)
    confirmed = confirm_subscriber(token)
    if confirmed:
        return RedirectResponse(url=f"/{lang}/subscribe-confirmed.html", status_code=302)
    else:
        return RedirectResponse(url=f"/{lang}/subscribe-invalid-token.html", status_code=302)


@app.get("/api/unsubscribe/{token}")
async def unsubscribe_handler(request: Request, token: str):
    """Unsubscribe and redirect to the static unsubscribed page."""
    lang = _detect_lang(request)
    removed = unsubscribe(token)
    if removed:
        return RedirectResponse(url=f"/{lang}/unsubscribed.html", status_code=302)
    else:
        return RedirectResponse(url=f"/{lang}/unsubscribe-invalid.html", status_code=302)


# --- Health ---

@app.get("/api/health")
async def health():
    return JSONResponse({"status": "ok"})
