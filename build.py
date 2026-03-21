"""Static site builder for Siskin Labs website.

Renders all Jinja2 templates to static HTML for both nl and en languages.
Output goes to dist/ directory.

Usage: python build.py
"""

import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from i18n import t as _t

# Configuration
REPO_DIR = Path(__file__).parent
TEMPLATES_DIR = REPO_DIR / "templates"
STATIC_DIR = REPO_DIR / "static"
DIST_DIR = REPO_DIR / "dist"

LANGUAGES = ["nl", "en"]

# Pages to render: (template_name, output_name, active_value, extra_context)
PAGES = [
    ("index.html", "index.html", "home", {}),
    ("dash.html", "dash.html", "dash", {}),
    ("perch.html", "perch.html", "perch", {}),
    ("cache.html", "cache.html", "cache", {}),
    ("waitlist.html", "waitlist.html", "waitlist", {}),
    ("subscribe.html", "subscribe.html", "subscribe", {}),
    # Confirmation/unsubscribe pages: render both states for each
    ("subscribe_confirmed.html", "subscribe-confirmed.html", "subscribe", {"confirmed": True}),
    ("subscribe_confirmed.html", "subscribe-invalid-token.html", "subscribe", {"confirmed": False}),
    ("unsubscribed.html", "unsubscribed.html", "subscribe", {"removed": True}),
    ("unsubscribed.html", "unsubscribe-invalid.html", "subscribe", {"removed": False}),
]


def url_for_page(page_name: str, lang: str) -> str:
    """Generate URL for a page in the given language."""
    if page_name == "index.html":
        return f"/{lang}/"
    return f"/{lang}/{page_name}"


def build():
    """Build the static site."""
    # Clean dist directory
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)

    # Copy static files
    shutil.copytree(STATIC_DIR, DIST_DIR / "static")
    print("Copied static/ -> dist/static/")

    # Set up Jinja2 environment
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=True,
    )

    # Render pages for each language
    for lang in LANGUAGES:
        lang_dir = DIST_DIR / lang
        lang_dir.mkdir(parents=True, exist_ok=True)

        other_lang = "nl" if lang == "en" else "en"
        other_lang_label = "Nederlands" if lang == "en" else "English"

        for template_name, output_name, active, extra_ctx in PAGES:
            template = env.get_template(template_name)

            # Build the language-aware URL rewriter
            # In static site, nav links point to /{lang}/page.html
            context = {
                "lang": lang,
                "t": lambda key, _lang=lang, **kw: _t(key, _lang, **kw),
                "other_lang": other_lang,
                "other_lang_label": other_lang_label,
                "active": active,
                **extra_ctx,
            }

            html = template.render(**context)

            # Rewrite internal links for static site
            html = rewrite_links(html, lang)

            # Write output
            output_path = lang_dir / output_name
            output_path.write_text(html, encoding="utf-8")
            print(f"  {lang}/{output_name}")

    # Create root index.html that redirects to /nl/
    root_index = DIST_DIR / "index.html"
    root_index.write_text(
        '<!DOCTYPE html>\n'
        '<html>\n'
        '<head>\n'
        '  <meta charset="UTF-8">\n'
        '  <meta http-equiv="refresh" content="0;url=/nl/">\n'
        '  <script>document.location.href="/nl/";</script>\n'
        '</head>\n'
        '<body>\n'
        '  <p>Redirecting to <a href="/nl/">Dutch version</a>...</p>\n'
        '</body>\n'
        '</html>\n',
        encoding="utf-8",
    )
    print("  index.html (redirect -> /nl/)")

    print(f"\nBuild complete! Output in {DIST_DIR}/")


def rewrite_links(html: str, lang: str) -> str:
    """Rewrite internal links for the static site.

    Transforms:
    - href="/"           -> href="/{lang}/"
    - href="/dash"       -> href="/{lang}/dash.html"
    - href="/perch"      -> href="/{lang}/perch.html"
    - href="/cache"      -> href="/{lang}/cache.html"
    - href="/waitlist"   -> href="/{lang}/waitlist.html"
    - href="/subscribe"  -> href="/{lang}/subscribe.html"
    - href="/lang/{other}" -> href="/{other_lang}/current_page" (handled per-page)
    - hx-post="/waitlist"  -> hx-post="/api/waitlist"
    - hx-post="/subscribe" -> hx-post="/api/subscribe"

    Preserves:
    - /static/... paths
    - External URLs (https://...)
    - Anchor links (#...)
    - mailto: links
    """
    import re

    other_lang = "nl" if lang == "en" else "en"

    # Rewrite HTMX form posts to API endpoints
    html = html.replace('hx-post="/waitlist"', 'hx-post="/api/waitlist"')
    html = html.replace('hx-post="/subscribe"', 'hx-post="/api/subscribe"')

    # Rewrite language switcher: /lang/{other} -> /{other_lang}/ (same page)
    # The language switcher link in the nav just needs to point to the other language root
    # We use a regex to handle this properly
    html = re.sub(
        r'href="/lang/' + re.escape(other_lang) + r'"',
        f'href="/{other_lang}/"',
        html,
    )

    # Rewrite internal page links (but not /static/, external, anchors, mailto)
    # Map of Flask routes to static file paths
    page_routes = {
        "/dash": f"/{lang}/dash.html",
        "/perch": f"/{lang}/perch.html",
        "/cache": f"/{lang}/cache.html",
        "/waitlist": f"/{lang}/waitlist.html",
        "/subscribe": f"/{lang}/subscribe.html",
    }

    for route, static_path in page_routes.items():
        # Match href="/dash" or href="/dash#demo" (with optional fragment)
        html = re.sub(
            r'href="' + re.escape(route) + r'(#[^"]*)?"',
            lambda m, sp=static_path: f'href="{sp}{m.group(1) or ""}"',
            html,
        )

    # Rewrite root href="/" to href="/{lang}/"
    # Be careful not to match /static/ etc. - only exact href="/"
    html = re.sub(r'href="/"', f'href="/{lang}/"', html)

    return html


if __name__ == "__main__":
    build()
