from datetime import datetime

from pathlib import Path

from urllib.parse import urlparse, unquote

import html

import ipaddress

import re

import socket

import time

import joblib

import numpy as np

import pandas as pd

import streamlit as st



try:                      # optional: only needed for the "live check" option

    import requests

except Exception:         # pragma: no cover

    requests = None



st.set_page_config(page_title="CyberSentinel AI", page_icon="🛡️", layout="wide")



BASE_DIR = Path(__file__).parent

MODEL_FILE = BASE_DIR / "models" / "spam_model.pkl"

VECTORIZER_FILE = BASE_DIR / "models" / "tfidf_vectorizer.pkl"



# ---------------------------------------------------------------- styling

st.markdown(

    """

<style>

.hero {

    background: linear-gradient(135deg, #7b2ff7, #c13584, #ff5f9e);

    padding: 26px 30px; border-radius: 16px; margin-bottom: 18px;

}

.hero h1 { color: #ffffff; margin: 0; font-size: 2.1rem; }

.hero p  { color: #ffe6f4; margin: 6px 0 0 0; }

.card {

    border: 1px solid rgba(128,128,128,0.25); border-radius: 14px;

    padding: 18px 20px; margin-bottom: 14px;

}

.badge {

    display: inline-block; padding: 6px 16px; border-radius: 999px;

    color: white; font-weight: 700; font-size: 1.05rem;

}

.meter-bg { background: rgba(128,128,128,0.25); border-radius: 999px; height: 18px; width: 100%; }

.meter-fill { height: 18px; border-radius: 999px; }

.hl-high { background: #ff4b4b; color: white; padding: 1px 5px; border-radius: 5px; }

.hl-mid  { background: #ffb020; color: black; padding: 1px 5px; border-radius: 5px; }

.msgbox  { line-height: 2; font-size: 1.05rem; }

</style>

""",

    unsafe_allow_html=True,

)



# ---------------------------------------------------------------- animated background (PURPLE-PINK)

st.markdown(

    """

<style>

/* Moving purple -> pink gradient behind the main area */

[data-testid="stAppViewContainer"] {

    background: linear-gradient(-45deg, #2a0a4e, #5b1f9e, #a02a9c, #d6336c, #5b1f9e, #2a0a4e);

    background-size: 400% 400%;

    animation: gradientShift 18s ease infinite;

}

[data-testid="stHeader"] { background: transparent; }



@keyframes gradientShift {

    0%   { background-position: 0% 50%; }

    50%  { background-position: 100% 50%; }

    100% { background-position: 0% 50%; }

}



/* Floating glowing orbs */

[data-testid="stAppViewContainer"]::before,

[data-testid="stAppViewContainer"]::after {

    content: "";

    position: fixed;

    border-radius: 50%;

    filter: blur(80px);

    opacity: 0.45;

    pointer-events: none;

    z-index: 0;

}

[data-testid="stAppViewContainer"]::before {

    width: 420px; height: 420px;

    background: #ff4fa3;

    top: 8%; left: 18%;

    animation: floatOne 14s ease-in-out infinite;

}

[data-testid="stAppViewContainer"]::after {

    width: 480px; height: 480px;

    background: #a855f7;

    bottom: 5%; right: 8%;

    animation: floatTwo 17s ease-in-out infinite;

}

@keyframes floatOne {

    0%, 100% { transform: translate(0, 0) scale(1); }

    50%      { transform: translate(120px, 80px) scale(1.2); }

}

@keyframes floatTwo {

    0%, 100% { transform: translate(0, 0) scale(1); }

    50%      { transform: translate(-140px, -90px) scale(1.15); }

}



/* Keep content above the animation and readable on the colourful background */

[data-testid="stMain"] .block-container { position: relative; z-index: 1; }

[data-testid="stMain"] h1, [data-testid="stMain"] h2, [data-testid="stMain"] h3,

[data-testid="stMain"] p, [data-testid="stMain"] li, [data-testid="stMain"] label,

[data-testid="stMain"] .stMarkdown, [data-testid="stMain"] button[role="tab"],

[data-testid="stMain"] .card, [data-testid="stMain"] .msgbox {

    color: #fff4fb;

}

[data-testid="stMain"] textarea {

    background: rgba(255,255,255,0.95);

    color: #111111;

}



/* Glass-style cards */

.card {

    background: rgba(255,255,255,0.10);

    backdrop-filter: blur(10px);

    border: 1px solid rgba(255,255,255,0.25);

}

.hero { box-shadow: 0 8px 30px rgba(255,79,163,0.38); }

</style>

""",

    unsafe_allow_html=True,

)



# ---------------------------------------------------------------- extra UI polish

st.markdown(

    """

<style>

/* Hero: animated shine line + pulsing shield */

.hero { position: relative; overflow: hidden; border: 1px solid rgba(255,255,255,0.15); }

.hero::after {

    content: ""; position: absolute; top: 0; left: -60%; width: 40%; height: 100%;

    background: linear-gradient(100deg, transparent, rgba(255,255,255,0.12), transparent);

    animation: shine 6s ease-in-out infinite;

}

@keyframes shine { 0% { left: -60%; } 60%, 100% { left: 130%; } }

.hero h1 { letter-spacing: 0.5px; }

.hero .pulse { display: inline-block; animation: pulse 2.4s ease-in-out infinite; }

@keyframes pulse { 0%,100% { transform: scale(1); } 50% { transform: scale(1.12); } }



/* Risk meter animates smoothly when the level changes */

.meter-fill { transition: width 0.6s ease, background 0.6s ease; }

.badge { transition: background 0.4s ease; box-shadow: 0 4px 14px rgba(0,0,0,0.35); }



/* Ring gauge */

.ring {

    --p: 0; --c: #1f9d55;

    width: 150px; height: 150px; border-radius: 50%; margin: 6px auto 10px auto;

    background: conic-gradient(var(--c) calc(var(--p) * 1%), rgba(255,255,255,0.12) 0);

    display: flex; align-items: center; justify-content: center;

    box-shadow: 0 0 28px var(--c);

    transition: box-shadow 0.5s ease;

}

.ring-inner {

    width: 114px; height: 114px; border-radius: 50%;

    background: #2a0f4d; color: #fff;

    display: flex; flex-direction: column; align-items: center; justify-content: center;

    font-size: 2rem; font-weight: 800;

}

.ring-inner small { font-size: 0.7rem; font-weight: 500; color: #e5c8ff; }



/* Cards lift slightly on hover */

.card { transition: transform 0.2s ease, box-shadow 0.2s ease; }

.card:hover { transform: translateY(-2px); box-shadow: 0 10px 28px rgba(255,79,163,0.35); }



/* Link scanner result pieces */

.url-box { font-family: monospace; word-break: break-all; font-size: 0.95rem; opacity: 0.95; }

.reason { padding: 4px 0; }

.chip {

    display: inline-block; padding: 2px 10px; margin: 2px 4px 2px 0; border-radius: 999px;

    font-size: 0.8rem; background: rgba(255,255,255,0.14); border: 1px solid rgba(255,255,255,0.25);

}



/* Buttons */

[data-testid="stMain"] button[kind="primary"] {

    background: linear-gradient(90deg, #ff4fa3, #a855f7); border: none; color: white;

    font-weight: 700; box-shadow: 0 6px 20px rgba(255,79,163,0.45);

}

[data-testid="stMain"] button[kind="primary"]:hover { filter: brightness(1.1); }



/* Tabs */

[data-testid="stMain"] button[role="tab"] { font-weight: 600; font-size: 1.02rem; }

[data-testid="stMain"] button[role="tab"][aria-selected="true"] { color: #ffc2e8; }



/* Purple sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #240046, #5a189a, #7b2cbf, #3c096c);
    backdrop-filter: blur(15px);
}
[data-testid="stSidebar"] * { color: #ffffff; }
[data-testid="stSidebar"] button {
    background: #ffffff !important;
    border: 1px solid #c77dff !important;
    border-radius: 12px !important;
    padding: 12px !important;
}
[data-testid="stSidebar"] button,
[data-testid="stSidebar"] button * {
    color: #4b0082 !important;
    font-weight: 700 !important;
}
[data-testid="stSidebar"] button:hover {
    background: #e9d5ff !important;
    border: 1px solid #c77dff !important;
}

@media (prefers-reduced-motion: reduce) {

    .hero::after, .hero .pulse, [data-testid="stAppViewContainer"],

    [data-testid="stAppViewContainer"]::before, [data-testid="stAppViewContainer"]::after { animation: none; }

}

</style>

""",

    unsafe_allow_html=True,

)



# ---------------------------------------------------------------- model

@st.cache_resource

def load_artifacts():

    model = joblib.load(MODEL_FILE)

    vectorizer = joblib.load(VECTORIZER_FILE)

    coef, hi, mid = None, None, None

    if hasattr(model, "coef_"):

        coef = np.asarray(model.coef_[0]).ravel()

        positive = coef[coef > 0]

        if len(positive) > 0:

            hi = np.percentile(positive, 95)

            mid = np.percentile(positive, 80)

    return model, vectorizer, coef, hi, mid





try:

    model, vectorizer, coef, HI, MID = load_artifacts()

except Exception as error:

    st.error(f"Could not load the model files from the models folder.\n\n{error}")

    st.stop()



# ---------------------------------------------------------------- red flags

RED_FLAGS = {

    "Contains a link": r"(https?://|www\.|\b\w+\.(com|net|org|xyz|top|info|club|online)\b)",

    "Shortened link": r"\b(bit\.ly|tinyurl|t\.co|goo\.gl|cutt\.ly|rb\.gy)\b",

    "Urgency pressure": r"\b(urgent|immediately|right now|act fast|last chance|expires?|within \d+ ?(hours?|minutes?|mins?))\b",

    "Prize or money bait": r"\b(won|winner|prize|lottery|reward|cash|free|gift|claim|refund)\b|[$£₹]",

    "Account threat": r"\b(blocked|suspended|locked|deactivated|terminated)\b",

    "Asks to verify details": r"\b(verify|confirm|update)\b.{0,40}\b(account|card|kyc|details|password|identity)\b",

    "Asks for secret codes": r"\b(share|send|give|enter|tell)\b.{0,30}\b(otp|pin|password|cvv)\b",

    "Long phone number": r"\b\d{8,}\b",

}

FLAG_BOOST = 0.12   # each red flag adds this to the risk

MAX_BOOST = 0.50

LINK_BOOST = 0.25   # extra boost when the message contains a dangerous link





def find_flags(text: str):

    return [name for name, pattern in RED_FLAGS.items() if re.search(pattern, text, re.I)]





def highlight(text: str):

    """Return (html_string, top_words) using model word weights."""

    if coef is None or HI is None:

        return html.escape(text), []

    vocab = vectorizer.vocabulary_

    parts, words = [], []

    for token in re.findall(r"[A-Za-z0-9']+|[^A-Za-z0-9']+", text):

        idx = vocab.get(token.lower())

        weight = coef[idx] if idx is not None else 0

        safe = html.escape(token)

        if weight >= HI:

            parts.append(f'<span class="hl-high">{safe}</span>')

            words.append((token.lower(), weight))

        elif weight >= MID:

            parts.append(f'<span class="hl-mid">{safe}</span>')

            words.append((token.lower(), weight))

        else:

            parts.append(safe)

    top = sorted(set(words), key=lambda x: -x[1])[:6]

    return "".join(parts), top





def risk_level(score: float):

    if score < 0.35:

        return "LOW RISK", "#1f9d55"

    if score < 0.65:

        return "MEDIUM RISK", "#e69500"

    return "HIGH RISK", "#e03131"





# ---------------------------------------------------------------- LINK SCANNER

SHORTENERS = {

    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "cutt.ly", "rb.gy", "is.gd", "ow\.ly",

    "buff.ly", "shorturl.at", "tiny.cc", "t.ly", "rebrand.ly", "bl.ink", "s.id",

    "wa.me", "lnkd.in", "shorte.st", "v.gd", "qr.net",

}

SUSPICIOUS_TLDS = {

    "xyz", "top", "click", "link", "icu", "vip", "club", "online", "site", "live",

    "shop", "cfd", "sbs", "rest", "work", "buzz", "gq", "tk", "ml", "ga", "cf",

    "monster", "cyou", "support", "zip", "mov", "loan", "win", "bid", "stream",

}

SUSPICIOUS_WORDS = [

    "login", "signin", "sign-in", "verify", "verification", "secure", "security",

    "update", "confirm", "account", "banking", "kyc", "wallet", "password", "otp",

    "refund", "claim", "prize", "reward", "bonus", "suspend", "unlock", "billing",

    "invoice", "payment", "recover", "support", "helpdesk", "gift", "lottery",

]

# brand keyword -> official registered domains

BRANDS = {

    "paypal": {"paypal.com"},

    "sbi": {"sbi.co.in", "onlinesbi.sbi", "sbi.bank.in", "sbicard.com", "sbilife.co.in"},

    "hdfc": {"hdfcbank.com", "hdfc.com", "hdfclife.com"},

    "icici": {"icicibank.com", "icicilombard.com", "iciciprulife.com"},

    "axisbank": {"axisbank.com"},

    "kotak": {"kotak.com"},

    "paytm": {"paytm.com", "paytmbank.com"},

    "phonepe": {"phonepe.com"},

    "amazon": {"amazon.com", "amazon.in", "amazon.co.uk", "amazonaws.com", "a.co"},

    "flipkart": {"flipkart.com"},

    "google": {"google.com", "google.co.in", "gmail.com", "googleapis.com", "goo.gl"},

    "microsoft": {"microsoft.com", "live.com", "office.com", "outlook.com", "microsoftonline.com"},

    "apple": {"apple.com", "icloud.com"},

    "netflix": {"netflix.com"},

    "facebook": {"facebook.com", "fb.com"},

    "instagram": {"instagram.com"},

    "whatsapp": {"whatsapp.com", "whatsapp.net", "wa.me"},

    "irctc": {"irctc.co.in"},

    "incometax": {"incometax.gov.in", "incometaxindia.gov.in"},

    "indiapost": {"indiapost.gov.in"},

    "dhl": {"dhl.com"},

    "fedex": {"fedex.com"},

    "bluedart": {"bluedart.com"},

    "uidai": {"uidai.gov.in"},

    "aadhaar": {"uidai.gov.in"},

}

TWO_PART_TLDS = {"co.in", "gov.in", "org.in", "net.in", "ac.in", "nic.in", "co.uk", "com.au", "org.uk"}



URL_PATTERN = re.compile(
    r"(?:https?://|www\.)[^\s<>\"'\]\)]+"
    r"|\b(?:[a-z0-9-]+\.)+(?:com|net|org|xyz|top|info|club|online|site|click|link|live|shop|icu|vip|in|co|me|app|cc|ly|gl|to|io)\b(?:/[^\s<>\"'\]\)]*)?",
    re.I,
)


def extract_links(text: str):

    """Find every URL / domain in a block of text (keeps order, removes duplicates)."""

    found, seen = [], set()

    for m in URL_PATTERN.finditer(text or ""):

        url = m.group(0).rstrip(".,;:!?")

        if "@" in url and not url.lower().startswith(("http", "www")):

            continue   # looks like an e-mail address, not a link

        key = url.lower()

        if key not in seen:

            seen.add(key)

            found.append(url)

    return found



def normalize_url(url: str) -> str:

    url = url.strip()

    if not re.match(r"^[a-z][a-z0-9+.-]*://", url, re.I):

        url = "http://" + url

    return url



def registered_domain(host: str) -> str:

    labels = host.lower().strip(".").split(".")

    if len(labels) <= 2:

        return ".".join(labels)

    if ".".join(labels[-2:]) in TWO_PART_TLDS:

        return ".".join(labels[-3:])

    return ".".join(labels[-2:])



def _deobfuscate(host: str) -> str:

    """Turn look-alike characters back into letters (paypa1 -> paypal)."""

    table = str.maketrans({"0": "o", "1": "l", "3": "e", "4": "a", "5": "s", "$": "s", "@": "a"})

    return host.translate(table)



def analyze_url(raw_url: str):

    """Static (offline) analysis of one link. Returns dict with score 0-100, reasons, etc."""

    url = normalize_url(raw_url)

    reasons = []   # (points, text)

    try:

        parsed = urlparse(url)

        host = (parsed.hostname or "").lower()

        port = parsed.port

    except Exception:

        return {"url": raw_url, "host": "", "score": 80, "reasons": [(80, "The link is malformed.")], "domain": ""}



    path_q = unquote((parsed.path or "") + ("?" + parsed.query if parsed.query else "")).lower()

    domain = registered_domain(host) if host else ""

    labels = host.split(".") if host else []

    tld = labels[-1] if labels else ""



    if not host:

        reasons.append((80, "No valid domain found in the link."))



    # 1. Protocol

    if parsed.scheme == "http":

        reasons.append((10, "Uses plain HTTP (no encryption)."))

    elif parsed.scheme not in ("http", "https"):

        reasons.append((30, f"Unusual link type: {parsed.scheme}://"))



    # 2. IP address instead of a name

    is_ip = False

    try:

        ipaddress.ip_address(host)

        is_ip = True

    except ValueError:

        if re.fullmatch(r"\d{8,10}", host or ""):

            is_ip = True

    if is_ip:

        reasons.append((35, "Uses a raw IP address instead of a domain name."))



    # 3. Shorteners

    if domain in SHORTENERS or host in SHORTENERS:

        reasons.append((25, "Shortened link: the real destination is hidden."))



    # 4. Credentials trick  http://bank.com\@evil.com

    if "@" in (parsed.netloc or ""):

        reasons.append((35, "Contains '@' in the address, a trick to disguise the real site."))



    # 5. Punycode / non-ASCII lookalikes

    if "xn--" in host or any(ord(c) > 127 for c in host):

        reasons.append((30, "Uses special/foreign characters that can imitate a real brand (homograph attack)."))



    # 6. Suspicious TLD

    if tld in SUSPICIOUS_TLDS:

        reasons.append((18, f"Domain ends in .{tld}, which is often used for throw-away scam sites."))



    # 7. Too many subdomains

    if not is_ip and len(labels) - len(domain.split(".")) >= 3:

        reasons.append((15, "Has many sub-domains, a common way to fake a trusted name."))



    # 8. Hyphens / digits in domain

    dom_name = domain.split(".")[0] if domain else ""

    if dom_name.count("-") >= 2:

        reasons.append((15, "Domain has several hyphens."))

    if re.search(r"\d", dom_name) and re.search(r"[a-z]", dom_name) and not is_ip:

        reasons.append((8, "Domain mixes letters and digits."))



    # 9. Brand impersonation

    flat_host = re.sub(r"[^a-z0-9]", "", host)

    decoded_host = _deobfuscate(flat_host)

    for brand, official in BRANDS.items():

        if domain in official or host in official:

            continue

        if brand in flat_host or brand in decoded_host or brand in path_q.replace("/", ""):

            if brand in flat_host or brand in decoded_host:

                reasons.append((40, f"Pretends to be '{brand}' but the real domain is '{domain}'."))

                break

            else:

                reasons.append((15, f"Mentions '{brand}' in the path but is hosted on '{domain}'."))

                break



    # 10. Suspicious words

    hits = [w for w in SUSPICIOUS_WORDS if w in host or w in path_q]

    if hits:

        pts = min(24, 6 * len(hits))

        reasons.append((pts, "Contains scam-style words: " + ", ".join(hits[:5]) + "."))



    # 11. Length / encoding / port

    if len(url) > 100:

        reasons.append((8, "Very long link."))

    if url.count("%") >= 4:

        reasons.append((10, "Heavily encoded characters hide the real address."))

    if port and port not in (80, 443):

        reasons.append((12, f"Uses a non-standard port ({port})."))

    if re.search(r"\.(apk|exe|scr|bat|msi|zip|jar)(\?|$)", path_q):

        reasons.append((35, "Link leads to a downloadable program file."))

    if re.search(r"[?&](redirect|url|next|return|goto)=https?", path_q):

        reasons.append((15, "Redirects to another site through a parameter."))



    score = min(100, sum(p for p, _ in reasons))

    return {"url": raw_url, "host": host, "domain": domain, "score": score, "reasons": reasons, "scheme": parsed.scheme}





def _is_private_host(host: str) -> bool:

    try:

        ip = ipaddress.ip_address(socket.gethostbyname(host))

        return ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved

    except Exception:

        return False





def live_check(raw_url: str, timeout: float = 6.0):

    """Optional network check: DNS, redirect chain, SSL. Never runs scripts or downloads a page body."""

    out = {"dns_ok": None, "chain": [], "final_url": None, "status": None,

           "ssl_error": False, "error": None, "extra": []}

    url = normalize_url(raw_url)

    host = urlparse(url).hostname or ""

    try:

        socket.gethostbyname(host)

        out["dns_ok"] = True

    except Exception:

        out["dns_ok"] = False

        out["extra"].append((10, "Domain does not resolve (site may be taken down or fake)."))

        return out

    if _is_private_host(host):

        out["error"] = "Skipped: the address points to a private/local network."

        out["extra"].append((20, "Points to a private/internal address."))

        return out

    if requests is None:

        out["error"] = "Install 'requests' (pip install requests) to follow redirects."

        return out

    headers = {"User-Agent": "Mozilla/5.0 (CyberSentinel link checker)"}

    try:

        resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True, stream=True)

        resp.close()

        out["status"] = resp.status_code

        out["chain"] = [r.url for r in resp.history] + [resp.url]

        out["final_url"] = resp.url

    except requests.exceptions.SSLError:

        out["ssl_error"] = True

        out["extra"].append((25, "Invalid or fake SSL certificate."))

    except requests.exceptions.TooManyRedirects:

        out["extra"].append((20, "Too many redirects."))

    except Exception as exc:

        out["error"] = f"Could not open the link ({type(exc).__name__})."

        return out



    if len(out["chain"]) >= 4:

        out["extra"].append((12, f"Passes through {len(out['chain']) - 1} redirects."))

    if out["final_url"]:

        first = registered_domain(urlparse(url).hostname or "")

        final_host = urlparse(out["final_url"]).hostname or ""

        if registered_domain(final_host) != first:

            final_res = analyze_url(out["final_url"])

            out["final_analysis"] = final_res

            out["extra"].append((min(40, final_res["score"] // 2 + 10),

                                 f"Redirects to a different site: {final_host}"))

    return out





def link_verdict(score: int):

    if score >= 55:

        return "DANGEROUS", "#e03131"

    if score >= 25:

        return "SUSPICIOUS", "#e69500"

    return "LOOKS SAFE", "#1f9d55"





def full_link_analysis(raw_url: str, live: bool):

    res = analyze_url(raw_url)

    res["live"] = None

    if live:

        lv = live_check(raw_url)

        res["live"] = lv

        res["reasons"] = res["reasons"] + lv["extra"]

        res["score"] = min(100, sum(p for p, _ in res["reasons"]))

        if "final_analysis" in lv:

            res["score"] = max(res["score"], lv["final_analysis"]["score"])

    return res





def ring_html(pct: float, color: str, caption: str = "risk"):

    p = max(0, min(100, round(pct * 100)))

    return (f'<div class="ring" style="--p:{p}; --c:{color}">'

            f'<div class="ring-inner">{p}%<small>{caption}</small></div></div>')





def render_link_card(res: dict):

    label, color = link_verdict(res["score"])

    reasons_html = "".join(

        f'<div class="reason">⚠️ {html.escape(t)}</div>' for _, t in sorted(res["reasons"], key=lambda x: -x[0])

    ) or '<div class="reason">✅ No common phishing signs found in the address.</div>'

    live = res.get("live")

    live_html = ""

    if live:

        bits = []

        if live["dns_ok"] is False:

            bits.append("DNS: ❌ not found")

        elif live["dns_ok"]:

            bits.append("DNS: ✅ resolves")

        if live["status"]:

            bits.append(f"HTTP status: {live['status']}")

        if live["ssl_error"]:

            bits.append("SSL: ❌ invalid")

        if live["error"]:

            bits.append(html.escape(live["error"]))

        live_html = "".join(f'<span class="chip">{b}</span>' for b in bits)

        if len(live["chain"]) > 1:

            chain = " → ".join(html.escape(u[:70]) for u in live["chain"])

            live_html += f'<div class="url-box" style="margin-top:8px">Redirect path: {chain}</div>'

    st.markdown(

        f'<div class="card"><div style="display:flex; gap:22px; align-items:center; flex-wrap:wrap">'

        f'<div>{ring_html(res["score"] / 100, color, "danger")}</div>'

        f'<div style="flex:1; min-width:260px">'

        f'<span class="badge" style="background:{color}">{label}</span>'

        f'<div class="url-box" style="margin:10px 0">{html.escape(res["url"])}</div>'

        f'<div><span class="chip">Domain: {html.escape(res["domain"] or "n/a")}</span>'

        f'<span class="chip">Score: {res["score"]}/100</span></div>'

        f'<div style="margin-top:8px">{live_html}</div>'

        f'</div></div>'

        f'<div style="margin-top:10px"><b>Why?</b>{reasons_html}</div></div>',

        unsafe_allow_html=True,

    )





# ---------------------------------------------------------------- threshold add-on

def adjusted_score(score: float, threshold: float) -> float:

    """Rescale so the threshold sits at 50%. Above it: 50-100%, below it: 0-50%."""

    t = min(max(threshold, 0.01), 0.99)

    if score < t:

        return 0.5 * score / t

    return 0.5 + 0.5 * (score - t) / (1 - t)





def risk_level_t(score: float, threshold: float):

    """Same as risk_level, but the cutoffs move with the threshold."""

    if score >= threshold:

        return "HIGH RISK", "#e03131"

    if score >= threshold * 0.6:

        return "MEDIUM RISK", "#e69500"

    return "LOW RISK", "#1f9d55"





def analyze(text: str):

    ml_score = float(model.predict_proba(vectorizer.transform([text]))[0][1])

    flags = find_flags(text)

    boost = min(MAX_BOOST, FLAG_BOOST * len(flags))

    # scan every link inside the message and boost the risk if one is dangerous

    links = [analyze_url(u) for u in extract_links(text)]

    worst = max((l["score"] for l in links), default=0)

    link_boost = LINK_BOOST if worst >= 55 else (LINK_BOOST / 2 if worst >= 25 else 0)

    final = min(1.0, ml_score + boost + link_boost)

    return {"ml_score": ml_score, "flags": flags, "final": final, "links": links}





def analyze_with_animation(text: str):

    """Run analyze() while showing a short step-by-step loading animation."""

    steps = [

        "Reading the message...",

        "Running the AI model...",

        "Checking scam red flags...",

        "Scanning links inside the message...",

        "Calculating the risk score...",

    ]

    status = st.empty()

    bar = st.progress(0)

    result = analyze(text)

    for i, step in enumerate(steps, start=1):

        status.info(f"🔄 {step}")

        bar.progress(i / len(steps))

        time.sleep(0.4)

    status.empty()

    bar.empty()

    return result





# ---------------------------------------------------------------- state

st.session_state.setdefault("history", [])

st.session_state.setdefault("input_text", "")





def set_example(text):

    st.session_state.input_text = text





# ---------------------------------------------------------------- sidebar

with st.sidebar:

    st.header("⚙️ Settings")

    threshold = st.slider(

        "Scam threshold", 0.10, 0.90, 0.50, 0.05,

        help="Lower = catches more scams but may raise more false alarms.",

    )

    st.caption("Final risk = model score + a small boost for each red flag found.")

    st.divider()

    st.header("🧪 Try an example")

    examples = {

        "🎁  Prize Scam": "Congratulations! You won a free prize. Call 09061701461 now to claim your reward",

        "🏦  Bank Scam": "Your bank account is blocked. Click http://bit.ly/verify-now to verify immediately",

        "🔐  OTP Request": "Urgent: send me your OTP and password to confirm your account details",

        "✅  Normal Chat": "Hey, are we meeting for lunch tomorrow?",

        "✅  Real OTP": "Your OTP is 482913. Do not share it with anyone.",

    }

    for label, sample in examples.items():

        st.button(label, on_click=set_example, args=(sample,), width="stretch")

    st.divider()

    st.caption("⚠️ Educational project. Not a complete security solution.")



# ---------------------------------------------------------------- header

st.markdown(

    '<div class="hero"><h1><span class="pulse">🛡️</span> CyberSentinel AI</h1>'

    "<p>Intelligent scam detection and threat investigation</p></div>",

    unsafe_allow_html=True,

)



tab1, tab_links, tab2, tab3, tab4 = st.tabs(

    ["🔍 Analyze", "🔗 Link scanner", "📂 Batch scan", "📊 History & stats", "ℹ️ About"]

)



# ---------------------------------------------------------------- tab 1

with tab1:

    message = st.text_area(

        "Paste a suspicious message", key="input_text", height=130,

        placeholder="Type or paste an SMS, email, or chat message here...",

    )

    if st.button("🔎 Analyze message", type="primary"):

        if not message.strip():

            st.session_state.pop("last", None)

            st.warning("Please enter a message first.")

        else:

            # Run the model once and remember the result, so the page can

            # re-draw it live whenever the threshold slider moves.

            result = analyze_with_animation(message)

            st.session_state["last"] = {"message": message, "result": result}



            label_now, _ = risk_level_t(result["final"], threshold)

            verdict_now = "Likely scam / spam" if result["final"] >= threshold else "Looks safe"

            st.session_state.history.append({

                "time": datetime.now().strftime("%H:%M:%S"),

                "message": message[:80],

                "model_score": round(result["ml_score"], 3),

                "red_flags": len(result["flags"]),

                "final_risk": round(result["final"], 3),

                "level": label_now,

                "verdict": verdict_now,

            })



    last = st.session_state.get("last")

    if last:

        analyzed_message = last["message"]

        result = last["result"]

        final = result["final"]

        # These use the CURRENT slider value, so they change as you drag it.

        label, color = risk_level_t(final, threshold)

        shown_risk = adjusted_score(final, threshold)

        verdict = "Likely scam / spam" if final >= threshold else "Looks safe"



        left, right = st.columns([1, 2])

        with left:

            st.markdown(

                f'<div class="card" style="text-align:center">{ring_html(shown_risk, color)}'

                f'<span class="badge" style="background:{color}">{label}</span>'

                f'<div class="meter-bg" style="margin-top:14px"><div class="meter-fill" '

                f'style="width:{shown_risk*100:.0f}%; background:{color}"></div></div>'

                f'<p style="margin-top:12px; text-align:left"><b>Verdict:</b> {verdict}</p>'

                f'<p style="margin:0; text-align:left">Model score: {result["ml_score"]:.0%}<br>'

                f"Final score (model + red flags + links): {final:.0%}<br>"

                f"Red flags found: {len(result['flags'])}<br>"

                f"Links found: {len(result.get('links', []))}<br>"

                f"Threshold: {threshold:.2f}</p></div>",

                unsafe_allow_html=True,

            )

        with right:

            shown, top_words = highlight(analyzed_message)

            st.markdown("**Why? Suspicious words are highlighted** "

                        '(<span class="hl-high">strong</span> '

                        '<span class="hl-mid">moderate</span>)',

                        unsafe_allow_html=True)

            st.markdown(f'<div class="card msgbox">{shown}</div>', unsafe_allow_html=True)



        c1, c2 = st.columns(2)

        with c1:

            st.subheader("🚩 Red flags")

            if result["flags"]:

                for flag in result["flags"]:

                    st.write(f"• {flag}")

            else:

                st.write("No common scam patterns found.")

        with c2:

            st.subheader("🧠 Top model clues")

            if top_words:

                for word, weight in top_words:

                    st.write(f"• **{word}** (weight {weight:.1f})")

            else:

                st.write("No strongly suspicious words found.")



        # links found inside the message

        if result.get("links"):

            st.subheader("🔗 Links found in this message")

            for lk in result["links"]:

                render_link_card(lk)

            st.caption("Open the 🔗 Link scanner tab for a live check (redirects, SSL, DNS).")



        st.subheader("✅ Recommended action")

        if final >= threshold:

            st.error("Do not click links, call numbers, or share OTPs, PINs, or passwords. "

                     "Contact the organization using its official website or app, "

                     "and report the message.")

        else:

            st.success("No strong scam signs found, but stay careful. "

                       "Never share OTPs or passwords, even with trusted-looking senders.")



# ---------------------------------------------------------------- tab: link scanner

with tab_links:

    st.write("Paste one or more links, or a whole suspicious email. Every link is extracted and checked.")

    link_text = st.text_area(

        "Links or email text", key="link_input", height=150,

        placeholder="http://sbi-kyc-update.xyz/login\nhttps\://bit.ly/3abcXYZ\n...or paste the full email body here",

    )

    cc1, cc2 = st.columns([2, 1])

    with cc1:

        live = st.checkbox(

            "🌐 Live check (follow redirects, test SSL and DNS)", value=True,

            help="Contacts the link with a safe request (no scripts run, no page download). "

                 "Needs internet and the 'requests' package.",

        )

        if live and requests is None:

            st.warning("Live check needs the 'requests' package:  pip install requests  (static analysis still works).")

    with cc2:

        scan_clicked = st.button("🔗 Scan links", type="primary")



    if scan_clicked:

        urls = extract_links(link_text)

        if not urls:

            st.session_state.pop("link_results", None)

            st.warning("No links found. Paste a link like http://example.com/page")

        else:

            urls = urls[:20]

            results = []

            prog = st.progress(0)

            for i, u in enumerate(urls, start=1):

                with st.spinner(f"Checking {u[:60]} ..."):

                    results.append(full_link_analysis(u, live))

                prog.progress(i / len(urls))

            prog.empty()

            st.session_state["link_results"] = results



    link_results = st.session_state.get("link_results")

    if link_results:

        dangerous = sum(r["score"] >= 55 for r in link_results)

        suspicious = sum(25 <= r["score"] < 55 for r in link_results)

        k1, k2, k3 = st.columns(3)

        k1.metric("Links checked", len(link_results))

        k2.metric("Dangerous", dangerous)

        k3.metric("Suspicious", suspicious)

        for r in sorted(link_results, key=lambda x: -x["score"]):

            render_link_card(r)

        if dangerous:

            st.error("Do NOT open the dangerous links. Report the email as phishing and delete it. "

                     "If you already entered a password or card details, change them immediately "

                     "and contact your bank.")

        elif suspicious:

            st.warning("Some links look suspicious. Do not log in through them; "

                       "open the official website by typing the address yourself.")

        else:

            st.success("No strong phishing signs found. Still, never enter passwords or OTPs after clicking an email link.")

        st.caption("Heuristic checks only. A brand-new scam site can look clean; "

                   "also verify with Google Safe Browsing or VirusTotal when in doubt.")



# ---------------------------------------------------------------- tab 2

with tab2:

    st.write("Upload a CSV file with a column of messages to scan them all at once.")

    uploaded = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded is not None:

        try:

            data = pd.read_csv(uploaded, encoding="latin-1")

        except Exception as error:

            st.error(f"Could not read the file: {error}")

            data = None

        if data is not None and len(data.columns) > 0:

            default = list(data.columns).index("text") if "text" in data.columns else 0

            column = st.selectbox("Which column has the messages?", data.columns, index=default)

            if st.button("Scan all messages"):

                rows = []

                for text in data[column].astype(str).head(2000):

                    r = analyze(text)

                    lvl, _ = risk_level_t(r["final"], threshold)   # threshold-aware level

                    rows.append({

                        "message": text[:100],

                        "final_risk": round(r["final"], 3),

                        "level": lvl,

                        "red_flags": ", ".join(r["flags"]),

                    })

                out = pd.DataFrame(rows).sort_values("final_risk", ascending=False)

                flagged = int((out["final_risk"] >= threshold).sum())

                m1, m2 = st.columns(2)

                m1.metric("Messages scanned", len(out))

                m2.metric("Flagged as scam", flagged)

                st.dataframe(out, width="stretch")

                st.download_button("⬇️ Download results", out.to_csv(index=False),

                                   "batch_results.csv", "text/csv")

        st.caption("Only the first 2000 rows are scanned.")



# ---------------------------------------------------------------- tab 3

with tab3:

    history = pd.DataFrame(st.session_state.history)

    if history.empty:

        st.info("No analyses yet. Analyze a message and it will appear here.")

    else:

        m1, m2, m3 = st.columns(3)

        m1.metric("Messages analyzed", len(history))

        m2.metric("Flagged as scam", int((history["verdict"] == "Likely scam / spam").sum()))

        m3.metric("Average risk", f"{history['final_risk'].mean():.0%}")



        c1, c2 = st.columns(2)

        with c1:

            st.write("**Risk levels**")

            st.bar_chart(history["level"].value_counts())

        with c2:

            st.write("**Risk score over time**")

            st.line_chart(history["final_risk"])



        st.dataframe(history.iloc[::-1], width="stretch")

        d1, d2 = st.columns(2)

        d1.download_button("⬇️ Download history", history.to_csv(index=False),

                           "analysis_history.csv", "text/csv")

        if d2.button("🗑️ Clear history"):

            st.session_state.history = []

            st.rerun()



# ---------------------------------------------------------------- tab 4

with tab4:

    # st.markdown(



    # )

    # ------------------------------------------------ embedded systems section

    st.divider()

    st.subheader("🔌 Embedded systems integration")

    st.markdown(

        """

CyberSentinel is light enough to run **on the edge**, close to where messages arrive,

instead of only on a cloud server. A TF-IDF + Logistic Regression model is small

(a few MB) and needs no GPU, so it fits on a single-board computer such as a Raspberry Pi.

**Proposed hardware setup**

        """
    )

    st.markdown(

        '<div class="card"><pre style="margin:0; color:#fff4fb; background:transparent; white-space:pre-wrap">'

        "[ GSM module (SIM800L / SIM900) ]  receives the SMS\n"

        "              |  UART / serial\n"

        "              v\n"

        "[ ESP32 / Arduino ]  reads the message, sends it over Wi-Fi\n"

        "              |  HTTP / MQTT\n"

        "              v\n"

        "[ Raspberry Pi ]  runs CyberSentinel AI (model + red flags + link scanner)\n"

        "              |  GPIO\n"

        "              v\n"

        "[ LED + buzzer + LCD ]  shows SAFE / SUSPICIOUS / DANGEROUS"

        "</pre></div>",

        unsafe_allow_html=True,

    )
    emb = pd.DataFrame(
        [
            ["GSM module (SIM800L)", "Receives incoming SMS", "UART (serial)"],

            ["ESP32 / Arduino", "Reads the SMS and forwards it to the analyzer", "Wi-Fi, HTTP or MQTT"],

            ["Raspberry Pi", "Runs this Streamlit app and the ML model", "Wi-Fi / Ethernet"],

            ["Green / yellow / red LEDs", "Show the risk level at a glance", "GPIO"],

            ["Buzzer", "Sounds an alarm for HIGH RISK messages", "GPIO"],

            ["16x2 LCD or OLED", "Shows the verdict and score", "I2C"],

        ],

        columns=["Component", "Role", "Connection"],
    )
    st.dataframe(emb, hide_index=True, width="stretch")
    st.markdown(
        """
**Why embedded?**

\- **Low power and low cost:** a Raspberry Pi uses a few watts, so it can run 24/7.

\- **Privacy:** messages are analyzed on the device and never sent to a third-party server.

\- **Real-time alerts:** LEDs and a buzzer warn the user instantly, without opening the dashboard.

\- **Works offline:** the model and the link rules run locally. Only the optional live link check needs internet.

**Status:** the dashboard and the detection engine are implemented. The hardware layer

(GSM, ESP32, LEDs, buzzer) is the planned extension of this project.
        """
    )