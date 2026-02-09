"""Siskin Labs website — FastAPI application."""

import os
import re
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from i18n import t, detect_language, SUPPORTED_LANGUAGES
from database import (
    init_db, add_to_waitlist, subscribe, confirm_subscriber, unsubscribe,
    create_newsletter, update_newsletter, get_newsletter, list_newsletters,
    schedule_newsletter, mark_newsletter_sent, get_confirmed_subscribers,
    delete_newsletter,
)
from mail import send_confirmation, send_newsletter

ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "")

app = FastAPI(title="Siskin Labs", docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def startup():
    init_db()


def ctx(request: Request, **kwargs) -> dict:
    """Build template context with language support."""
    lang = detect_language(request)
    return {
        "request": request,
        "lang": lang,
        "t": lambda key, **kw: t(key, lang, **kw),
        "other_lang": "nl" if lang == "en" else "en",
        "other_lang_label": "Nederlands" if lang == "en" else "English",
        **kwargs,
    }


# --- Language switcher ---

@app.get("/lang/{lang}")
async def switch_language(request: Request, lang: str):
    """Switch language and redirect back."""
    if lang not in SUPPORTED_LANGUAGES:
        lang = "en"
    referer = request.headers.get("referer", "/")
    response = RedirectResponse(url=referer, status_code=302)
    response.set_cookie("lang", lang, max_age=60 * 60 * 24 * 365)
    return response


# --- Pages ---

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", ctx(request, active="home"))


@app.get("/perch", response_class=HTMLResponse)
async def perch(request: Request):
    return templates.TemplateResponse("perch.html", ctx(request, active="perch"))


@app.get("/cache", response_class=HTMLResponse)
async def cache(request: Request):
    return templates.TemplateResponse("cache.html", ctx(request, active="cache"))


@app.get("/waitlist", response_class=HTMLResponse)
async def waitlist_page(request: Request):
    return templates.TemplateResponse("waitlist.html", ctx(request, active="waitlist"))


# --- Waitlist API ---

EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")


@app.post("/waitlist", response_class=HTMLResponse)
async def waitlist_submit(
    request: Request,
    email: str = Form(...),
    name: str = Form(""),
    product: str = Form("both"),
):
    lang = detect_language(request)

    if not EMAIL_RE.match(email):
        return templates.TemplateResponse(
            "partials/waitlist_result.html",
            {"request": request, "lang": lang, "t": lambda key, **kw: t(key, lang, **kw),
             "success": False, "message": t("waitlist_invalid_email", lang)},
        )

    if product not in ("perch", "cache", "both"):
        product = "both"

    ip = request.headers.get("x-forwarded-for", request.client.host if request.client else "")
    added = add_to_waitlist(email, name, product, lang, ip)

    if added:
        message = t("waitlist_success", lang)
    else:
        message = t("waitlist_exists", lang)

    return templates.TemplateResponse(
        "partials/waitlist_result.html",
        {"request": request, "lang": lang, "t": lambda key, **kw: t(key, lang, **kw),
         "success": added, "message": message},
    )


# --- Mailing list ---

@app.get("/subscribe", response_class=HTMLResponse)
async def subscribe_page(request: Request):
    return templates.TemplateResponse("subscribe.html", ctx(request, active="subscribe"))


@app.post("/subscribe", response_class=HTMLResponse)
async def subscribe_submit(
    request: Request,
    email: str = Form(...),
    name: str = Form(""),
    interests: str = Form("all"),
):
    lang = detect_language(request)

    if not EMAIL_RE.match(email):
        return templates.TemplateResponse(
            "partials/subscribe_result.html",
            {"request": request, "lang": lang, "t": lambda key, **kw: t(key, lang, **kw),
             "success": False, "message": t("subscribe_invalid_email", lang)},
        )

    if interests not in ("all", "perch", "cache", "announcements"):
        interests = "all"

    ip = request.headers.get("x-forwarded-for", request.client.host if request.client else "")
    confirm_token, unsubscribe_token, is_new = subscribe(email, name, interests=interests, language=lang, ip_address=ip)

    if not confirm_token:
        # Already confirmed
        message = t("subscribe_already_confirmed", lang)
        return templates.TemplateResponse(
            "partials/subscribe_result.html",
            {"request": request, "lang": lang, "t": lambda key, **kw: t(key, lang, **kw),
             "success": False, "message": message},
        )

    # Send confirmation email
    send_confirmation(email, confirm_token, lang)
    message = t("subscribe_check_email", lang)

    return templates.TemplateResponse(
        "partials/subscribe_result.html",
        {"request": request, "lang": lang, "t": lambda key, **kw: t(key, lang, **kw),
         "success": True, "message": message},
    )


@app.get("/subscribe/confirm/{token}", response_class=HTMLResponse)
async def subscribe_confirm(request: Request, token: str):
    lang = detect_language(request)
    confirmed = confirm_subscriber(token)
    return templates.TemplateResponse(
        "subscribe_confirmed.html",
        ctx(request, active="subscribe", confirmed=confirmed),
    )


@app.get("/unsubscribe/{token}", response_class=HTMLResponse)
async def unsubscribe_page(request: Request, token: str):
    lang = detect_language(request)
    removed = unsubscribe(token)
    return templates.TemplateResponse(
        "unsubscribed.html",
        ctx(request, active="subscribe", removed=removed),
    )


# --- Admin: Newsletter management ---

def verify_admin(request: Request):
    """Check admin token via cookie or query parameter."""
    token = request.cookies.get("admin_token") or request.query_params.get("token")
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Forbidden")


@app.get("/admin/login")
async def admin_login(request: Request, token: str = ""):
    """Set admin cookie from token query param."""
    if token and token == ADMIN_TOKEN:
        response = RedirectResponse(url="/admin/newsletters", status_code=302)
        response.set_cookie("admin_token", token, max_age=60 * 60 * 24 * 30, httponly=True)
        return response
    raise HTTPException(status_code=403, detail="Forbidden")


@app.get("/admin/newsletters", response_class=HTMLResponse)
async def admin_newsletters_list(request: Request):
    verify_admin(request)
    newsletters = list_newsletters()
    subscribers_count = len(get_confirmed_subscribers())
    return templates.TemplateResponse(
        "admin/newsletters.html",
        ctx(request, active="admin", newsletters=newsletters, subscribers_count=subscribers_count),
    )


@app.get("/admin/newsletters/new", response_class=HTMLResponse)
async def admin_newsletter_new(request: Request):
    verify_admin(request)
    return templates.TemplateResponse(
        "admin/newsletter_edit.html",
        ctx(request, active="admin", newsletter=None),
    )


@app.post("/admin/newsletters/new", response_class=HTMLResponse)
async def admin_newsletter_create(
    request: Request,
    subject_en: str = Form(...),
    subject_nl: str = Form(...),
    body_en: str = Form(...),
    body_nl: str = Form(...),
    target: str = Form("all"),
):
    verify_admin(request)
    newsletter_id = create_newsletter(subject_en, subject_nl, body_en, body_nl, target)
    return RedirectResponse(url=f"/admin/newsletters/{newsletter_id}", status_code=302)


@app.get("/admin/newsletters/{newsletter_id}", response_class=HTMLResponse)
async def admin_newsletter_view(request: Request, newsletter_id: int):
    verify_admin(request)
    newsletter = get_newsletter(newsletter_id)
    if not newsletter:
        raise HTTPException(status_code=404, detail="Not found")
    target_count = len(get_confirmed_subscribers(newsletter["target"]))
    return templates.TemplateResponse(
        "admin/newsletter_detail.html",
        ctx(request, active="admin", newsletter=newsletter, target_count=target_count),
    )


@app.get("/admin/newsletters/{newsletter_id}/edit", response_class=HTMLResponse)
async def admin_newsletter_edit(request: Request, newsletter_id: int):
    verify_admin(request)
    newsletter = get_newsletter(newsletter_id)
    if not newsletter or newsletter["status"] != "draft":
        raise HTTPException(status_code=404, detail="Not found or not editable")
    return templates.TemplateResponse(
        "admin/newsletter_edit.html",
        ctx(request, active="admin", newsletter=newsletter),
    )


@app.post("/admin/newsletters/{newsletter_id}/edit", response_class=HTMLResponse)
async def admin_newsletter_update(
    request: Request,
    newsletter_id: int,
    subject_en: str = Form(...),
    subject_nl: str = Form(...),
    body_en: str = Form(...),
    body_nl: str = Form(...),
    target: str = Form("all"),
):
    verify_admin(request)
    update_newsletter(newsletter_id, subject_en, subject_nl, body_en, body_nl, target)
    return RedirectResponse(url=f"/admin/newsletters/{newsletter_id}", status_code=302)


@app.post("/admin/newsletters/{newsletter_id}/schedule", response_class=HTMLResponse)
async def admin_newsletter_schedule(request: Request, newsletter_id: int):
    verify_admin(request)
    schedule_newsletter(newsletter_id)
    return RedirectResponse(url=f"/admin/newsletters/{newsletter_id}", status_code=302)


@app.post("/admin/newsletters/{newsletter_id}/send", response_class=HTMLResponse)
async def admin_newsletter_send(request: Request, newsletter_id: int):
    """Send a scheduled newsletter to all matching subscribers."""
    verify_admin(request)
    newsletter = get_newsletter(newsletter_id)
    if not newsletter or newsletter["status"] not in ("scheduled", "draft"):
        raise HTTPException(status_code=400, detail="Newsletter not sendable")

    subscribers = get_confirmed_subscribers(newsletter["target"])
    sent = 0
    for sub in subscribers:
        lang = sub.get("language", "en")
        subject = newsletter["subject_nl"] if lang == "nl" else newsletter["subject_en"]
        body = newsletter["body_nl"] if lang == "nl" else newsletter["body_en"]
        if send_newsletter(sub["email"], subject, body, sub["unsubscribe_token"], lang):
            sent += 1

    mark_newsletter_sent(newsletter_id, sent)
    return RedirectResponse(url=f"/admin/newsletters/{newsletter_id}", status_code=302)


@app.post("/admin/newsletters/{newsletter_id}/delete", response_class=HTMLResponse)
async def admin_newsletter_delete(request: Request, newsletter_id: int):
    verify_admin(request)
    delete_newsletter(newsletter_id)
    return RedirectResponse(url="/admin/newsletters", status_code=302)


@app.get("/admin/newsletters/{newsletter_id}/preview", response_class=HTMLResponse)
async def admin_newsletter_preview(request: Request, newsletter_id: int):
    """Preview a newsletter as it would appear in email."""
    verify_admin(request)
    newsletter = get_newsletter(newsletter_id)
    if not newsletter:
        raise HTTPException(status_code=404, detail="Not found")
    lang = detect_language(request)
    subject = newsletter["subject_nl"] if lang == "nl" else newsletter["subject_en"]
    body = newsletter["body_nl"] if lang == "nl" else newsletter["body_en"]
    return templates.TemplateResponse(
        "admin/newsletter_preview.html",
        ctx(request, active="admin", newsletter=newsletter, subject=subject, body=body),
    )


# --- Health check ---

@app.get("/health")
async def health():
    return {"status": "ok"}
