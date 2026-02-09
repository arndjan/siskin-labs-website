"""Internationalization for Siskin Labs website.

Supports English (en) and Dutch (nl) with auto-detection.
"""

SUPPORTED_LANGUAGES = ["en", "nl"]
DEFAULT_LANGUAGE = "en"

TRANSLATIONS = {
    # --- Navigation ---
    "nav_home": {"en": "Home", "nl": "Home"},
    "nav_perch": {"en": "Perch", "nl": "Perch"},
    "nav_cache": {"en": "Cache", "nl": "Cache"},
    "nav_waitlist": {"en": "Join Waitlist", "nl": "Wachtlijst"},
    "nav_login": {"en": "Log in", "nl": "Inloggen"},

    # --- Homepage ---
    "hero_title": {
        "en": "Tools that work the way you think",
        "nl": "Tools die werken zoals jij denkt",
    },
    "hero_subtitle": {
        "en": "Siskin Labs builds lightweight, intelligent software for professionals who value their time.",
        "nl": "Siskin Labs bouwt lichtgewicht, intelligente software voor professionals die hun tijd waarderen.",
    },
    "hero_cta": {"en": "Explore our tools", "nl": "Ontdek onze tools"},

    "products_title": {"en": "Our Products", "nl": "Onze Producten"},

    "perch_tagline": {
        "en": "Smart CRM for your network",
        "nl": "Slimme CRM voor je netwerk",
    },
    "perch_description": {
        "en": "Manage your professional relationships through a natural language chat interface. No complex forms — just type what you want to do.",
        "nl": "Beheer je professionele relaties via een natuurlijke taal chat interface. Geen ingewikkelde formulieren — gewoon typen wat je wilt doen.",
    },
    "perch_feature_1": {"en": "Chat-driven CRM", "nl": "Chat-gestuurde CRM"},
    "perch_feature_2": {"en": "Dutch & English NLP", "nl": "Nederlandse & Engelse NLP"},
    "perch_feature_3": {"en": "Multi-tenant architecture", "nl": "Multi-tenant architectuur"},
    "perch_feature_4": {"en": "Mobile-first design", "nl": "Mobile-first design"},

    "cache_tagline": {
        "en": "Your second brain for knowledge",
        "nl": "Je tweede brein voor kennis",
    },
    "cache_description": {
        "en": "Capture, organize and retrieve information effortlessly. Cache helps you remember what matters, when it matters.",
        "nl": "Leg informatie moeiteloos vast, organiseer en vind het terug. Cache helpt je onthouden wat belangrijk is, wanneer het belangrijk is.",
    },
    "cache_feature_1": {"en": "Smart knowledge capture", "nl": "Slimme kennisopslag"},
    "cache_feature_2": {"en": "Instant retrieval", "nl": "Direct terugvinden"},
    "cache_feature_3": {"en": "Connected notes", "nl": "Verbonden notities"},
    "cache_feature_4": {"en": "API integrations", "nl": "API-integraties"},

    "learn_more": {"en": "Learn more", "nl": "Meer info"},
    "try_demo": {"en": "Try the demo", "nl": "Probeer de demo"},
    "coming_soon": {"en": "Coming soon", "nl": "Binnenkort beschikbaar"},

    # --- About section ---
    "about_title": {"en": "Built in Amsterdam", "nl": "Gebouwd in Amsterdam"},
    "about_text": {
        "en": "Siskin Labs is an independent software studio based in Amsterdam. We build tools that are fast, focused, and respectful of your data.",
        "nl": "Siskin Labs is een onafhankelijke software studio in Amsterdam. We bouwen tools die snel, gefocust en respectvol met je data omgaan.",
    },

    # --- Perch product page ---
    "perch_hero_title": {
        "en": "Your relationships, managed through chat",
        "nl": "Jouw relaties, beheerd via chat",
    },
    "perch_hero_subtitle": {
        "en": "Perch is a lightweight CRM built for professionals who want to stay on top of their network — without the overhead of traditional CRM systems.",
        "nl": "Perch is een lichtgewicht CRM gebouwd voor professionals die hun netwerk willen bijhouden — zonder de overhead van traditionele CRM-systemen.",
    },
    "perch_how_title": {"en": "How it works", "nl": "Hoe het werkt"},
    "perch_how_1": {
        "en": "Type naturally — \"Had coffee with Anna from Bakery Jensen about their new website\"",
        "nl": "Typ natuurlijk — \"Koffie gehad met Anna van Bakkerij Jansen over hun nieuwe website\"",
    },
    "perch_how_2": {
        "en": "Perch extracts the contact, organization, type, and notes automatically",
        "nl": "Perch herkent automatisch het contact, de organisatie, het type en de notities",
    },
    "perch_how_3": {
        "en": "Your network stays organized without any manual data entry",
        "nl": "Je netwerk blijft georganiseerd zonder handmatige invoer",
    },
    "perch_features_title": {"en": "Features", "nl": "Features"},
    "perch_feat_chat": {"en": "Chat interface", "nl": "Chat interface"},
    "perch_feat_chat_desc": {
        "en": "Add contacts, log meetings, and search your network — all through natural language.",
        "nl": "Voeg contacten toe, log vergaderingen en doorzoek je netwerk — alles via natuurlijke taal.",
    },
    "perch_feat_relations": {"en": "Relations & Organizations", "nl": "Relaties & Organisaties"},
    "perch_feat_relations_desc": {
        "en": "Contact cards with flexible many-to-many links between people and organizations.",
        "nl": "Contactkaarten met flexibele M:N koppelingen tussen personen en organisaties.",
    },
    "perch_feat_contacts": {"en": "Contact moments", "nl": "Contactmomenten"},
    "perch_feat_contacts_desc": {
        "en": "Track calls, emails, meetings, coffees — with dates, notes, and follow-ups.",
        "nl": "Registreer telefoontjes, emails, meetings, koffie — met datum, notities en opvolgacties.",
    },
    "perch_feat_tags": {"en": "Smart tagging", "nl": "Slim taggen"},
    "perch_feat_tags_desc": {
        "en": "Categorize and filter your network with flexible tags.",
        "nl": "Categoriseer en filter je netwerk met flexibele tags.",
    },
    "perch_feat_mobile": {"en": "Mobile-first", "nl": "Mobile-first"},
    "perch_feat_mobile_desc": {
        "en": "Chat-first on mobile, split-view on desktop. Optimized for on-the-go use.",
        "nl": "Chat-eerst op mobiel, split-view op desktop. Geoptimaliseerd voor onderweg.",
    },
    "perch_feat_multi": {"en": "Multi-tenant", "nl": "Multi-tenant"},
    "perch_feat_multi_desc": {
        "en": "Separate environments per team or project, with role-based access.",
        "nl": "Gescheiden omgevingen per team of project, met toegangsbeheer.",
    },
    "perch_demo_title": {"en": "Try Perch", "nl": "Probeer Perch"},
    "perch_demo_text": {
        "en": "Explore the sandbox environment — no account needed. Data resets nightly.",
        "nl": "Verken de sandbox omgeving — geen account nodig. Data wordt elke nacht gereset.",
    },
    "perch_demo_btn": {"en": "Open sandbox demo", "nl": "Open sandbox demo"},
    "perch_access_title": {"en": "Get access", "nl": "Toegang krijgen"},
    "perch_access_text": {
        "en": "Perch is currently in private alpha. Join the waitlist to get early access.",
        "nl": "Perch is momenteel in private alpha. Schrijf je in op de wachtlijst voor vroege toegang.",
    },

    # --- Cache product page ---
    "cache_hero_title": {
        "en": "Remember everything that matters",
        "nl": "Onthoud alles wat belangrijk is",
    },
    "cache_hero_subtitle": {
        "en": "Cache is a smart knowledge tool that helps you capture, connect, and retrieve information when you need it.",
        "nl": "Cache is een slimme kennistool die je helpt informatie vast te leggen, te verbinden en terug te vinden wanneer je het nodig hebt.",
    },
    "cache_status_title": {"en": "Status", "nl": "Status"},
    "cache_status_text": {
        "en": "Cache is currently in development. Join the waitlist to be notified when it launches.",
        "nl": "Cache is momenteel in ontwikkeling. Schrijf je in op de wachtlijst om op de hoogte te blijven.",
    },
    "cache_vision_title": {"en": "The vision", "nl": "De visie"},
    "cache_vision_1": {
        "en": "Capture information from any source — web, conversations, documents",
        "nl": "Leg informatie vast uit elke bron — web, gesprekken, documenten",
    },
    "cache_vision_2": {
        "en": "Automatic connections between related knowledge",
        "nl": "Automatische verbindingen tussen gerelateerde kennis",
    },
    "cache_vision_3": {
        "en": "Instant retrieval through natural language search",
        "nl": "Direct terugvinden via natuurlijke taal zoekopdrachten",
    },
    "cache_vision_4": {
        "en": "Privacy-first — your data stays yours",
        "nl": "Privacy-first — jouw data blijft van jou",
    },

    # --- Waitlist ---
    "waitlist_title": {"en": "Join the waitlist", "nl": "Schrijf je in op de wachtlijst"},
    "waitlist_subtitle": {
        "en": "Be the first to know when our tools are ready. No spam, just updates.",
        "nl": "Wees de eerste die het hoort wanneer onze tools klaar zijn. Geen spam, alleen updates.",
    },
    "waitlist_email": {"en": "Email address", "nl": "E-mailadres"},
    "waitlist_name": {"en": "Name (optional)", "nl": "Naam (optioneel)"},
    "waitlist_product": {"en": "Interested in", "nl": "Geïnteresseerd in"},
    "waitlist_both": {"en": "Both", "nl": "Beide"},
    "waitlist_submit": {"en": "Join waitlist", "nl": "Aanmelden"},
    "waitlist_success": {
        "en": "You're on the list! We'll be in touch.",
        "nl": "Je staat op de lijst! We nemen contact op.",
    },
    "waitlist_exists": {
        "en": "This email is already on our waitlist.",
        "nl": "Dit e-mailadres staat al op onze wachtlijst.",
    },
    "waitlist_error": {
        "en": "Something went wrong. Please try again.",
        "nl": "Er ging iets mis. Probeer het opnieuw.",
    },
    "waitlist_invalid_email": {
        "en": "Please enter a valid email address.",
        "nl": "Vul een geldig e-mailadres in.",
    },

    # --- Mailing list / Subscribe ---
    "nav_subscribe": {"en": "Newsletter", "nl": "Nieuwsbrief"},
    "subscribe_title": {"en": "Stay in the loop", "nl": "Blijf op de hoogte"},
    "subscribe_subtitle": {
        "en": "Get updates on product launches, new features, and occasional offers. No spam — unsubscribe anytime.",
        "nl": "Ontvang updates over productlanceringen, nieuwe features en aanbiedingen. Geen spam — altijd opzegbaar.",
    },
    "subscribe_email": {"en": "Email address", "nl": "E-mailadres"},
    "subscribe_name": {"en": "Name (optional)", "nl": "Naam (optioneel)"},
    "subscribe_interests": {"en": "I'm interested in", "nl": "Ik ben geïnteresseerd in"},
    "subscribe_all": {"en": "Everything", "nl": "Alles"},
    "subscribe_announcements": {"en": "Announcements only", "nl": "Alleen aankondigingen"},
    "subscribe_submit": {"en": "Subscribe", "nl": "Aanmelden"},
    "subscribe_check_email": {
        "en": "Check your inbox! We've sent you a confirmation email.",
        "nl": "Check je inbox! We hebben een bevestigingsmail gestuurd.",
    },
    "subscribe_already_confirmed": {
        "en": "This email is already subscribed.",
        "nl": "Dit e-mailadres is al aangemeld.",
    },
    "subscribe_invalid_email": {
        "en": "Please enter a valid email address.",
        "nl": "Vul een geldig e-mailadres in.",
    },
    "subscribe_confirmed_title": {"en": "You're subscribed!", "nl": "Je bent aangemeld!"},
    "subscribe_confirmed_text": {
        "en": "Thanks for confirming. You'll hear from us when there's something worth sharing.",
        "nl": "Bedankt voor het bevestigen. Je hoort van ons wanneer er iets te delen is.",
    },
    "subscribe_invalid_token": {
        "en": "This confirmation link is invalid or has expired.",
        "nl": "Deze bevestigingslink is ongeldig of verlopen.",
    },
    "unsubscribed_title": {"en": "Unsubscribed", "nl": "Afgemeld"},
    "unsubscribed_text": {
        "en": "You've been removed from our mailing list. Sorry to see you go.",
        "nl": "Je bent verwijderd van onze mailinglijst. Jammer dat je gaat.",
    },
    "unsubscribed_invalid": {
        "en": "This unsubscribe link is invalid.",
        "nl": "Deze afmeldlink is ongeldig.",
    },
    "footer_newsletter": {"en": "Newsletter", "nl": "Nieuwsbrief"},
    "footer_subscribe_text": {
        "en": "Product updates & announcements",
        "nl": "Productupdates & aankondigingen",
    },

    # --- Footer ---
    "footer_tagline": {
        "en": "Independent software studio, Amsterdam",
        "nl": "Onafhankelijke software studio, Amsterdam",
    },
    "footer_products": {"en": "Products", "nl": "Producten"},
    "footer_company": {"en": "Company", "nl": "Bedrijf"},
    "footer_about": {"en": "About", "nl": "Over ons"},
    "footer_contact": {"en": "Contact", "nl": "Contact"},
    "footer_privacy": {"en": "Privacy", "nl": "Privacy"},
    "footer_copyright": {
        "en": "Siskin Labs. All rights reserved.",
        "nl": "Siskin Labs. Alle rechten voorbehouden.",
    },
}


def t(key: str, lang: str = "en", **kwargs) -> str:
    """Translate a key to the given language."""
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE
    if key not in TRANSLATIONS:
        return key
    text = TRANSLATIONS[key].get(lang, TRANSLATIONS[key].get(DEFAULT_LANGUAGE, key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text
    return text


def detect_language(request) -> str:
    """Detect preferred language from request.

    Priority:
    1. ?lang= query parameter
    2. lang cookie (manual override)
    3. Accept-Language header
    4. GeoIP headers (Cloudflare / Fly.io)
    5. Default (en)
    """
    # 1. Explicit query parameter
    lang_param = request.query_params.get("lang")
    if lang_param in SUPPORTED_LANGUAGES:
        return lang_param

    # 2. Cookie override
    lang_cookie = request.cookies.get("lang")
    if lang_cookie in SUPPORTED_LANGUAGES:
        return lang_cookie

    # 3. Accept-Language header
    accept = request.headers.get("accept-language", "")
    for part in accept.split(","):
        code = part.split(";")[0].strip().lower()
        if code.startswith("nl"):
            return "nl"
        if code.startswith("en"):
            return "en"

    # 4. GeoIP via Cloudflare or Fly headers
    country = (
        request.headers.get("cf-ipcountry", "")
        or request.headers.get("fly-client-country", "")
    ).upper()
    if country in ("NL", "BE", "SR"):
        return "nl"

    return DEFAULT_LANGUAGE
