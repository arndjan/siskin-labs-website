"""Database for Siskin Labs website (waitlist + mailing list)."""

import sqlite3
import os
import secrets
from datetime import datetime

DB_PATH = os.environ.get("WEBSITE_DB_PATH", "website.db")


def get_db() -> sqlite3.Connection:
    """Get a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """Initialize the database schema."""
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS waitlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            name TEXT,
            product TEXT NOT NULL DEFAULT 'both',
            language TEXT DEFAULT 'en',
            ip_address TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            name TEXT,
            language TEXT DEFAULT 'en',
            interests TEXT DEFAULT 'all',
            confirmed INTEGER DEFAULT 0,
            confirm_token TEXT,
            unsubscribe_token TEXT NOT NULL,
            ip_address TEXT,
            created_at TEXT NOT NULL,
            confirmed_at TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS newsletters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_en TEXT NOT NULL,
            subject_nl TEXT NOT NULL,
            body_en TEXT NOT NULL,
            body_nl TEXT NOT NULL,
            target TEXT DEFAULT 'all',
            status TEXT DEFAULT 'draft',
            created_at TEXT NOT NULL,
            scheduled_at TEXT,
            sent_at TEXT,
            sent_count INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


def add_to_waitlist(email: str, name: str = "", product: str = "both",
                    language: str = "en", ip_address: str = "") -> bool:
    """Add an email to the waitlist. Returns True if added, False if exists."""
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO waitlist (email, name, product, language, ip_address, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (email.lower().strip(), name.strip(), product, language, ip_address, datetime.utcnow().isoformat()),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


# --- Mailing list ---

def subscribe(email: str, name: str = "", language: str = "en",
              interests: str = "all", ip_address: str = "") -> tuple[str, str, bool]:
    """Subscribe to the mailing list.

    Returns (confirm_token, unsubscribe_token, is_new).
    If already subscribed but unconfirmed, returns existing tokens.
    If already confirmed, returns ('', unsubscribe_token, False).
    """
    email = email.lower().strip()
    conn = get_db()
    try:
        existing = conn.execute(
            "SELECT confirm_token, unsubscribe_token, confirmed FROM subscribers WHERE email = ?",
            (email,)
        ).fetchone()

        if existing:
            if existing["confirmed"]:
                return ("", existing["unsubscribe_token"], False)
            # Resend: return existing tokens
            return (existing["confirm_token"], existing["unsubscribe_token"], False)

        confirm_token = secrets.token_urlsafe(32)
        unsubscribe_token = secrets.token_urlsafe(32)
        conn.execute(
            """INSERT INTO subscribers
               (email, name, language, interests, confirm_token, unsubscribe_token, ip_address, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (email, name.strip(), language, interests, confirm_token, unsubscribe_token,
             ip_address, datetime.utcnow().isoformat()),
        )
        conn.commit()
        return (confirm_token, unsubscribe_token, True)
    finally:
        conn.close()


def confirm_subscriber(token: str) -> bool:
    """Confirm a subscriber by token. Returns True if confirmed."""
    conn = get_db()
    try:
        row = conn.execute(
            "SELECT id, confirmed FROM subscribers WHERE confirm_token = ?", (token,)
        ).fetchone()
        if not row:
            return False
        if row["confirmed"]:
            return True  # Already confirmed
        conn.execute(
            "UPDATE subscribers SET confirmed = 1, confirmed_at = ?, confirm_token = NULL WHERE id = ?",
            (datetime.utcnow().isoformat(), row["id"]),
        )
        conn.commit()
        return True
    finally:
        conn.close()


def unsubscribe(token: str) -> bool:
    """Unsubscribe by token. Returns True if found and removed."""
    conn = get_db()
    try:
        result = conn.execute(
            "DELETE FROM subscribers WHERE unsubscribe_token = ?", (token,)
        )
        conn.commit()
        return result.rowcount > 0
    finally:
        conn.close()


# --- Newsletters ---

def create_newsletter(subject_en: str, subject_nl: str, body_en: str, body_nl: str,
                      target: str = "all") -> int:
    """Create a draft newsletter. Returns the newsletter ID."""
    conn = get_db()
    try:
        cursor = conn.execute(
            """INSERT INTO newsletters (subject_en, subject_nl, body_en, body_nl, target, status, created_at)
               VALUES (?, ?, ?, ?, ?, 'draft', ?)""",
            (subject_en, subject_nl, body_en, body_nl, target, datetime.utcnow().isoformat()),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def update_newsletter(newsletter_id: int, subject_en: str, subject_nl: str,
                      body_en: str, body_nl: str, target: str = "all") -> bool:
    """Update a draft newsletter."""
    conn = get_db()
    try:
        result = conn.execute(
            """UPDATE newsletters SET subject_en = ?, subject_nl = ?, body_en = ?, body_nl = ?, target = ?
               WHERE id = ? AND status = 'draft'""",
            (subject_en, subject_nl, body_en, body_nl, target, newsletter_id),
        )
        conn.commit()
        return result.rowcount > 0
    finally:
        conn.close()


def get_newsletter(newsletter_id: int) -> dict | None:
    """Get a single newsletter by ID."""
    conn = get_db()
    try:
        row = conn.execute("SELECT * FROM newsletters WHERE id = ?", (newsletter_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def list_newsletters() -> list[dict]:
    """List all newsletters, newest first."""
    conn = get_db()
    try:
        rows = conn.execute("SELECT * FROM newsletters ORDER BY created_at DESC").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def schedule_newsletter(newsletter_id: int) -> bool:
    """Mark a draft newsletter as ready to send."""
    conn = get_db()
    try:
        result = conn.execute(
            "UPDATE newsletters SET status = 'scheduled', scheduled_at = ? WHERE id = ? AND status = 'draft'",
            (datetime.utcnow().isoformat(), newsletter_id),
        )
        conn.commit()
        return result.rowcount > 0
    finally:
        conn.close()


def mark_newsletter_sent(newsletter_id: int, count: int) -> None:
    """Mark a newsletter as sent with the number of recipients."""
    conn = get_db()
    try:
        conn.execute(
            "UPDATE newsletters SET status = 'sent', sent_at = ?, sent_count = ? WHERE id = ?",
            (datetime.utcnow().isoformat(), count, newsletter_id),
        )
        conn.commit()
    finally:
        conn.close()


def get_confirmed_subscribers(target: str = "all") -> list[dict]:
    """Get all confirmed subscribers, optionally filtered by interest."""
    conn = get_db()
    try:
        if target == "all":
            rows = conn.execute(
                "SELECT * FROM subscribers WHERE confirmed = 1"
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM subscribers WHERE confirmed = 1 AND (interests = ? OR interests = 'all')",
                (target,)
            ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def delete_newsletter(newsletter_id: int) -> bool:
    """Delete a draft newsletter."""
    conn = get_db()
    try:
        result = conn.execute(
            "DELETE FROM newsletters WHERE id = ? AND status = 'draft'",
            (newsletter_id,),
        )
        conn.commit()
        return result.rowcount > 0
    finally:
        conn.close()
