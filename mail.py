"""Email sending for Siskin Labs (confirmation loop + notifications)."""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_HOST = os.environ.get("SMTP_HOST", "")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
FROM_EMAIL = os.environ.get("FROM_EMAIL", "hello@siskin.amsterdam")
FROM_NAME = os.environ.get("FROM_NAME", "Siskin Labs")
BASE_URL = os.environ.get("BASE_URL", "https://siskin.amsterdam")


def _send(to: str, subject: str, html: str, text: str = ""):
    """Send an email via SMTP."""
    if not SMTP_HOST:
        print(f"[mail] SMTP not configured. Would send to {to}: {subject}")
        return False

    msg = MIMEMultipart("alternative")
    msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"] = to
    msg["Subject"] = subject

    if text:
        msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"[mail] Failed to send to {to}: {e}")
        return False


def send_confirmation(email: str, confirm_token: str, lang: str = "en"):
    """Send a double opt-in confirmation email."""
    confirm_url = f"{BASE_URL}/subscribe/confirm/{confirm_token}"

    if lang == "nl":
        subject = "Bevestig je aanmelding — Siskin Labs"
        html = f"""
        <div style="font-family: 'Helvetica Neue', Arial, sans-serif; max-width: 480px; margin: 0 auto; padding: 2rem;">
            <div style="border-bottom: 3px solid #f0e51b; padding-bottom: 1rem; margin-bottom: 1.5rem;">
                <strong style="font-size: 1.2rem;">Siskin Labs</strong>
            </div>
            <h2 style="font-size: 1.3rem; margin-bottom: 0.5rem;">Bevestig je aanmelding</h2>
            <p style="color: #4a4a4a; line-height: 1.6;">
                Bedankt voor je interesse! Klik op de onderstaande knop om je aanmelding
                voor de Siskin Labs mailinglijst te bevestigen.
            </p>
            <div style="margin: 1.5rem 0;">
                <a href="{confirm_url}"
                   style="display: inline-block; background: #f0e51b; color: #000; padding: 0.7rem 1.5rem;
                          border-radius: 6px; font-weight: 600; text-decoration: none;">
                    Bevestig aanmelding
                </a>
            </div>
            <p style="color: #717171; font-size: 0.85rem; line-height: 1.6;">
                Als je je niet hebt aangemeld, kun je deze email negeren.
            </p>
            <div style="margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #e5e5e5; color: #717171; font-size: 0.8rem;">
                Siskin Labs &middot; Amsterdam
            </div>
        </div>
        """
        text = f"Bevestig je aanmelding voor de Siskin Labs mailinglijst: {confirm_url}"
    else:
        subject = "Confirm your subscription — Siskin Labs"
        html = f"""
        <div style="font-family: 'Helvetica Neue', Arial, sans-serif; max-width: 480px; margin: 0 auto; padding: 2rem;">
            <div style="border-bottom: 3px solid #f0e51b; padding-bottom: 1rem; margin-bottom: 1.5rem;">
                <strong style="font-size: 1.2rem;">Siskin Labs</strong>
            </div>
            <h2 style="font-size: 1.3rem; margin-bottom: 0.5rem;">Confirm your subscription</h2>
            <p style="color: #4a4a4a; line-height: 1.6;">
                Thanks for your interest! Click the button below to confirm your
                subscription to the Siskin Labs mailing list.
            </p>
            <div style="margin: 1.5rem 0;">
                <a href="{confirm_url}"
                   style="display: inline-block; background: #f0e51b; color: #000; padding: 0.7rem 1.5rem;
                          border-radius: 6px; font-weight: 600; text-decoration: none;">
                    Confirm subscription
                </a>
            </div>
            <p style="color: #717171; font-size: 0.85rem; line-height: 1.6;">
                If you didn't sign up, you can safely ignore this email.
            </p>
            <div style="margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #e5e5e5; color: #717171; font-size: 0.8rem;">
                Siskin Labs &middot; Amsterdam
            </div>
        </div>
        """
        text = f"Confirm your subscription to the Siskin Labs mailing list: {confirm_url}"

    return _send(email, subject, html, text)


def _wrap_newsletter(body_html: str, unsubscribe_url: str, lang: str = "en") -> str:
    """Wrap newsletter body content in the Siskin Labs email template."""
    unsub_text = "Afmelden" if lang == "nl" else "Unsubscribe"
    return f"""
    <div style="font-family: 'Helvetica Neue', Arial, sans-serif; max-width: 560px; margin: 0 auto; padding: 2rem;">
        <div style="border-bottom: 3px solid #f0e51b; padding-bottom: 1rem; margin-bottom: 1.5rem;">
            <strong style="font-size: 1.2rem;">Siskin Labs</strong>
        </div>
        {body_html}
        <div style="margin-top: 2.5rem; padding-top: 1rem; border-top: 1px solid #e5e5e5; color: #717171; font-size: 0.8rem;">
            Siskin Labs &middot; Amsterdam<br>
            <a href="{unsubscribe_url}" style="color: #717171;">{unsub_text}</a>
        </div>
    </div>
    """


def send_newsletter(email: str, subject: str, body_html: str,
                    unsubscribe_token: str, lang: str = "en") -> bool:
    """Send a newsletter email to a single subscriber."""
    unsubscribe_url = f"{BASE_URL}/unsubscribe/{unsubscribe_token}"
    html = _wrap_newsletter(body_html, unsubscribe_url, lang)
    return _send(email, subject, html)
