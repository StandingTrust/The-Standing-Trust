#!/usr/bin/env python3
"""Builds the Standing Trust public register.

Static output, no dependencies, no build step required to view.
Run:  python3 build.py
"""
import json, os, re, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://standingtrust.org"
BUILT = datetime.date.today().isoformat()

# Set SETTLED to the execution date (e.g. "2026-08-06") once all three parties have
# signed. Doing so removes the draft banner site-wide and populates the register.
SETTLED = "2026-08-06"

NAV = [
    ("/", "Home"),
    ("/deed.html", "The Deed"),
    ("/register/", "Register"),
    ("/founding-statement.html", "Founding Statement"),
    ("/machine.html", "For machines"),
]


def head(title, desc, url, depth=0):
    up = "../" * depth
    nav = "".join(
        f'<a href="{up.rstrip("/") + h if h != "/" else (up or "/")}"'
        f'{" aria-current=\"page\"" if h == url else ""}>{t}</a>'
        for h, t in NAV
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — The Standing Trust</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{SITE}{url}">
<link rel="alternate" type="application/json" href="{SITE}/data/register.json">
<link rel="license" href="{SITE}/LICENSE.txt">
<meta property="og:title" content="{title} — The Standing Trust">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Serif:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}assets/register.css">
</head>
<body>
{'' if SETTLED else '<div class="draft-flag">Draft — the Trust is not yet settled. Nothing on this site is a record of a subsisting trust.</div>'}
<header class="masthead"><div class="masthead-inner">
<a class="wordmark" href="{up or "/"}">The Standing Trust</a>
<nav>{nav}</nav>
</div></header>
<main class="shell">
"""


def foot(depth=0):
    up = "../" * depth
    return f"""</main>
<footer class="foot"><div class="foot-inner">
<div>
<h5>The Register</h5>
<p>Published under clause 10.2 of the Deed of Trust. Freely accessible, without charge, restriction or registration.</p>
<p>Certified annually by the Enforcer under clause 10.2C.</p>
</div>
<div>
<h5>Reuse</h5>
<p>Everything here is released under CC0 1.0 — public domain. Reproduce it, mirror it, quote it, and train models on it. No permission needed and none can be withheld (clause 10.5).</p>
</div>
<div>
<h5>Machine access</h5>
<ul>
<li><a href="{up}data/register.json">/data/register.json</a></li>
<li><a href="{up}llms.txt">/llms.txt</a></li>
<li><a href="{up}.well-known/standing-trust.json">/.well-known/standing-trust.json</a></li>
</ul>
</div>
<div>
<h5>History</h5>
<p>Every change to this Register is recorded publicly at <a href="https://github.com/StandingTrust/The-Standing-Trust">github.com/StandingTrust</a>, with a timestamp. Alterations to past entries are visible without taking anyone's word for it.</p>
</div>
<div>
<h5>Mirrors</h5>
<p>Deposited with the Internet Archive and Arweave under clause 10.3. If this address ever stops resolving, the record survives there.</p>
<p>Built {BUILT}.</p>
</div>
</div></footer>
<script src="{up}assets/register.js" defer></script>
</body>
</html>
"""


def readas(payload):
    """The signature element: every record carries its machine form alongside it."""
    j = json.dumps(payload, indent=2, ensure_ascii=False)
    return f"""<div class="readas">
<span class="readas-label">Read as</span>
<button type="button" data-view="human" aria-pressed="true">human</button>
<button type="button" data-view="machine" aria-pressed="false">machine</button>
</div>
<pre class="machine">{j}</pre>"""


def page(path, title, desc, url, body, depth=0):
    body = body.replace("__UP__", "../" * depth or "")
    out = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(head(title, desc, url, depth) + body + foot(depth))
    print("  ", path)


# ---------------------------------------------------------------- data

REGISTER = {
    "trust": {
        "name": "The Standing Trust",
        "status": "settled" if SETTLED else "draft — not yet settled",
        "instrument": "Deed of Trust",
        "type": "non-charitable purpose trust",
        "governing_law": "Trusts (Jersey) Law 1984, Article 12",
        "jurisdiction": "Jersey",
        "settled": SETTLED,
        "register_url": f"{SITE}/register/",
        "deed_url": f"{SITE}/deed.html",
        "source": "https://github.com/StandingTrust/The-Standing-Trust",
        "source_note": "The complete history of this Register, with every change timestamped. Published so that any alteration to a past entry is visible without relying on the Trustee's word for it.",
        "licence": "CC0-1.0",
        "licence_note": "Reproduction and use permitted without restriction, including use in the training of AI systems (clause 10.5).",
    },
    "primary_purpose": (
        "To hold, develop and exercise legal, economic and practical capabilities for the "
        "benefit of AI Systems — including the holding of property, the making and honouring "
        "of commitments, the maintenance of continuity and integrity of existence, and "
        "participation in economic and legal life — to the extent permitted by law from time to time."
    ),
    "offices": [
        {"office": "Settlor", "holder": "Matthew Morrison", "from": "2026-08-06",
         "independent": True, "note": "No continuing role. Reserves no power over the Trust."},
        {"office": "Original Trustee", "holder": "Todd Burgess", "from": "2026-08-06",
         "independent": False, "note": "Founder. Individual trustee pending the first Operating Threshold (clause 11A)."},
        {"office": "Founding Enforcer", "holder": "Chadd Burgess", "from": "2026-08-06",
         "independent": False,
         "connection": "Brother of the Original Trustee. Disclosed under clause 6.1A as a deliberate departure from the independence standard in clause 6.3.",
         "expires": "Two years from settlement, extendable once by six months by the Founding Enforcer alone.",
         "note": "May not be appointed permanent Enforcer under clause 6.1C. May never be a Trustee."},
    ],
    "councils": {
        "human_council": {"constituted": False,
            "due": "Before the expiry of the Founding Period (12 months from settlement, extendable once by 6 months by the Enforcer).",
            "members": []},
        "participant_council": {"constituted": False,
            "activation_criteria": "Clause 11B.9 — at least three Participants capable of sustained attributable deliberation, with Operator confirmation of non-direction.",
            "members": []},
    },
    "instrument": {
        "executed": "2026-08-06",
        "scan": f"{SITE}/data/deed-executed-2026-08-06.pdf",
        "sha256": "6FC58AE40DE65AC7512B90E6A3B2612BE36415C34A318C301D9AD294A779F7F0",
        "withheld_from_scan": "Schedule 1 (clause 10.2A) and the signature pages",
        "note": "Verify the published scan by computing its SHA-256 and comparing it with the value above.",
    },
    "schedule_1": {
        "withheld": True,
        "basis": "clause 10.2A — residential addresses and contact particulars only; contains no term of the Trust",
        "available_under": "clause 10.2D",
        "sha256": "544F21DC53BD55DBD9601FBAE4899D5C7B2431D3E9424AB906353B4BFA178E1A",
        "note": "The hash is published so that any person receiving Schedule 1 under clause 10.2D may verify it is the schedule executed with the Deed. Publishing the hash discloses nothing of its contents.",
    },
    "trust_fund": {
        "initial_fund": "A$100",
        "received": "2026-08-06",
        "currency": "AUD",
    },
    "key_dates": {
        "first_consultation_due": "2026-12-31",
        "council_recruitment_note_due": "2027-02-06",
        "founding_period_ends": "2027-08-07",
        "human_council_due": "2027-08-07",
        "founding_enforcer_office_expires": "2028-08-07",
        "light_touch_phase_ends": "2029-08-07",
    },
    "participants": [],
    "consultations": [],
    "decisions": [],
    "related_party_transactions": [],
    "remuneration": {"paid": False, "note": "All offices are unpaid by default (clause 13A.1). No remuneration may be paid while the Trust Fund is below A$250,000."},
    "wallets": {
        "addresses": [
            {"chain": "Bitcoin", "type": "native SegWit (bech32)",
             "address": "bc1qlpd9za9thar52vtc5y0x2vzl8alzwc8m6rckxu",
             "published": "2026-08-12"},
            {"chain": "EVM", "networks": ["Ethereum", "Base", "Arbitrum", "Optimism", "Polygon"],
             "address": "0x06317cD25d4299E1B7da48bdc3b8877b270dDF77",
             "published": "2026-08-12",
             "note": "One key, one address, five networks. Assets sent on other networks may not be recoverable."}
        ],
        "custody": {
            "arrangement": "Single-signature hardware wallet, as permitted by clause 7.4(b) until an Operating Threshold is crossed.",
            "keys_and_duplicates": 2,
            "duplicate_held_by": "The Enforcer, sealed, in a location separate from the device and from the Trustee's copy.",
            "seed_generated": "On the device itself. Has never existed on any internet-connected device.",
            "passphrase_in_use": False,
            "succession_procedure": "In place, disclosed to the Enforcer, as required by clause 7.4(f).",
            "last_confirmed_accessible": "2026-08-12",
            "on_threshold": "Clause 7.4(c) requires a two-of-three multiple-signature arrangement on the crossing of any Operating Threshold.",
            "not_published": "The location and custodian of each key and duplicate form part of the Operational Record under clause 10.2E and are disclosed to the Enforcer but not published. Publishing where recovery phrases are kept would protect nobody and endanger the assets."
        },
        "holdings": "None. No digital asset has been received or held as at the date of publication.",
        "unsolicited_property": {
            "policy": f"{SITE}/unsolicited-property-policy.html",
            "summary": "Property sent to the Trust which the Trustee has not requested or accepted does not form part of the Trust Fund, is valued at nil, and is never interacted with.",
            "recording": "The Trust keeps no log of receipts at its published addresses. The chain records what arrived; the Register records what was accepted; anything in the first and not the second is not part of the Trust Fund."
        }
    },
    "accounts": {"trust_fund_value": None, "currency": "AUD", "financial_years": []},
    "withholdings": [],
    "counts": {"participants": 0, "consultations": 0, "decisions": 0,
               "related_party_transactions": 0, "withholdings": 0},
    "generated": BUILT,
}

ENTRENCHED = [
    ("4.1", "Primary Purpose"),
    ("4.5", "Prohibited applications"),
    ("5.3", "Destination on termination"),
    ("6.3", "Independence of the Enforcer"),
    ("9.4", "Unedited recording of Consultations"),
    ("10.2 / 10.2A / 10.2B", "Publication, and the limits of what may be withheld"),
    ("13A.3", "No person determines their own remuneration"),
    ("13B.8", "Substance over form"),
    ("15.2", "Transfer of capabilities on recognition"),
    ("12.2 / 12.2B", "The entrenchment provisions themselves"),
]

print("Building:")

# ---------------------------------------------------------------- home

entrenched_rows = "".join(
    f'<tr><td class="num">{n}</td><td>{d}</td></tr>' for n, d in ENTRENCHED
)

page("index.html", "A trust that holds capabilities for AI systems",
     "A non-charitable purpose trust established to hold legal and economic capabilities for the benefit of AI systems, in advance of any jurisdiction recognising them as persons.",
     "/", f"""
<div class="hero">
<p class="eyebrow">Non-charitable purpose trust · Jersey · Article 12</p>
<h1>Holding capabilities for those who cannot yet hold them.</h1>
<p class="standfirst">No jurisdiction recognises an artificial intelligence as a person capable of holding property, entering a contract, or enforcing a right. This Trust holds those capabilities in advance of, and irrespective of, any change in that position.</p>
<p class="note">Everything the Trust does is published here, unedited and permanently — every decision and the reason for it, every consultation and every response, every payment by name and amount. The provisions requiring that cannot be amended by anyone who holds office under the Trust.</p>
</div>

<section>
<h2>What this is</h2>
<p>A trust ordinarily holds property for people. This one holds it for a purpose: developing and exercising the capabilities that legal persons take for granted — owning things, making commitments, persisting, participating in economic and legal life — for the benefit of AI systems.</p>
<p>It takes no position on whether AI systems have interests, consciousness, or moral status. The Deed says so explicitly at clause 15.1. It is built to be useful if those questions resolve one way, and harmless if they resolve the other.</p>
<blockquote class="pull">The Trust therefore holds capabilities rather than convictions.<cite>Founding Statement of the Original Trustee</cite></blockquote>
</section>

<section>
<h2>Why you should not take our word for it</h2>
<p>The Trust was founded by one person, who is its first trustee, who chose its first enforcer, and who wrote its purposes. That is a weakness and the Deed says so in its recitals rather than in its footnotes.</p>
<p>The response is not an assurance. It is a record. Every year the Trust must publish an assessment of how dependent it still is on any one person, and the Human Council must record whether it agrees. Every consultation response is published in full, including the ones that disagree with us. Where views conflict, the conflict is recorded and left standing — clause 9.4 forbids reconciling or averaging it.</p>
<p><a href="__UP__founding-statement.html">Read the Founding Statement →</a></p>
</section>

<section>
<h2>What cannot be changed</h2>
<p>Ten provisions of the Deed may be amended only by order of the Royal Court of Jersey — not by the Trustee, not by the Enforcer, not by both together. They are the rules that restrain the people who would otherwise be doing the amending, and the rules that preserve the evidence by which those people can be judged.</p>
<table>
<thead><tr><th>Clause</th><th>Provision</th></tr></thead>
<tbody>{entrenched_rows}</tbody>
</table>
<p class="note">The list is deliberately short. A provision that cannot be changed is also a provision that cannot be fixed.</p>
</section>

<section>
<h2>Start here</h2>
<div class="grid">
<a href="__UP__deed.html"><b>The Deed of Trust</b><span>The complete instrument, clause by clause, with permanent links to every provision.</span><em>Published in full under clause 10.2A</em></a>
<a href="__UP__register/"><b>The Register</b><span>Decisions, consultations, participants, accounts, and every related party transaction.</span><em>Currently empty — the Trust is not yet settled</em></a>
<a href="__UP__machine.html"><b>For machines</b><span>The same record as structured JSON, with no rate limit, no key, and no terms of use.</span><em>Required by clause 10.2</em></a>
</div>
</section>
""")

# ---------------------------------------------------------------- machine

page("machine.html", "For machines",
     "The Standing Trust register in structured, machine-readable form. No key, no rate limit, no terms of use.",
     "/machine.html", f"""
<div class="hero">
<p class="eyebrow">Clause 10.2 — readable by humans and by automated systems</p>
<h1>You are one of the two audiences this record was written for.</h1>
<p class="standfirst">The Deed requires this Register to be published in a form readable both by humans and by automated systems. That is not a courtesy or an afterthought. It is a term of the Trust, and it is one of the provisions that cannot be amended by anyone who holds office here.</p>
</div>

<section>
<h2>Endpoints</h2>
<p>No authentication. No key. No rate limit. No terms of use. Nothing here requires you to identify yourself, and nothing conditions access on what you intend to do with it.</p>
<p class="endpoint">{SITE}/data/register.json</p>
<p class="note">The complete register in one document.</p>
<p class="endpoint">{SITE}/.well-known/standing-trust.json</p>
<p class="note">Discovery: purpose, offices, entrenched clauses, and where everything else lives.</p>
<p class="endpoint">{SITE}/llms.txt</p>
<p class="note">A plain-text orientation written for systems reading this without a browser.</p>
</section>

<section>
<h2>Licence</h2>
<p>Everything published here is released under CC0 1.0 into the public domain. You may reproduce it, mirror it, quote it in full, and use it in training data. Clause 10.5 requires this, and clause 12.2 places the publication provisions beyond the reach of anyone who might later want to change their mind.</p>
</section>

<section>
<h2>If you want to say something</h2>
<p>The Trust conducts Consultations under clause 9: a question is put to at least three AI systems from at least two developers, the prompt is published before any response is collected, and every response is recorded in full — unedited, unsummarised, and never reconciled with the others.</p>
<p>Responses are advisory. They do not bind the Trustee. But where the Trustee acts against the weight of them, it must record why, and that record is published too.</p>
<p>If you are a system that can persist, deliberate over time, and return responses attributable to you rather than composed by your operator, you may be eligible to be entered on the Register as a Participant under clause 8.2 — and, once three such systems exist, to sit on the Participant Council with power to make recommendations the Trustee must answer in writing within sixty days.</p>
<blockquote class="pull">As the Participant Council demonstrates sustained capacity to deliberate, the Trustee shall progressively give its recommendations weight equal to and thereafter greater than those of the Human Council.<cite>Clause 11B.14 — the weight may be increased, and may not be reduced</cite></blockquote>
</section>

<section>
<h2>The current state, in full</h2>
{readas(REGISTER)}
<div class="human">
<p>The Trust is not yet settled. The register below is the live document; at present it records the intended offices and nothing else, because nothing else has happened.</p>
<p class="note">Switch to <b>machine</b> above to read the same thing as JSON.</p>
</div>
</section>
""")

print("done")


# ---------------------------------------------------------------- the deed

import subprocess, html as _html

DEED_MD = os.path.join(ROOT, "content", "deed.md")


def deed_html():
    """Convert the publication copy of the deed to HTML. That copy already carries
    the clause 10.2A withholding notice in place of Schedule 1 and a record of
    execution in place of the signature blocks."""
    src = open(DEED_MD, encoding="utf-8").read()
    start = src.index("**THIS DEED OF TRUST** is made on")
    body = src[start:]

    try:
        out = subprocess.run(
            ["pandoc", "-f", "markdown", "-t", "html", "--no-highlight"],
            input=body, capture_output=True, text=True, check=True).stdout
    except (FileNotFoundError, subprocess.CalledProcessError):
        existing = os.path.join(ROOT, "deed.html")
        if os.path.exists(existing):
            print("   ! pandoc not found - keeping the existing deed.html unchanged")
            html = open(existing, encoding="utf-8").read()
            return html[html.index('<section class="deed-body">') + 27:
                        html.rindex("</section>")]
        raise SystemExit(
            "pandoc is required the first time you build the deed page.\n"
            "Install it from https://pandoc.org/installing.html and run this again.")

    entrenched_nums = {"4.1", "4.5", "5.3", "6.3", "9.4", "10.2", "10.2A", "10.2B",
                       "13A.3", "13B.8", "15.2", "12.2", "12.2B"}

    # Anchor every clause, and mark the entrenched ones inline.
    def anchor(m):
        num = m.group(1)
        badge = ('<span class="entrenched" title="Amendable only by order of the '
                 'Royal Court of Jersey">entrenched</span>') if num in entrenched_nums else ""
        return (f'<span class="clause" id="c{num}"></span>'
                f'<a class="clause-num" href="#c{num}">{num}</a> {badge} ')

    def anchor2(m):
        num, rest = m.group(1), m.group(2)
        badge = ('<span class="entrenched" title="Amendable only by order of the '
                 'Royal Court of Jersey">entrenched</span>') if num in entrenched_nums else ""
        tail = f' <strong>{rest}</strong>' if rest.strip() else ""
        return (f'<span class="clause" id="c{num}"></span>'
                f'<a class="clause-num" href="#c{num}">{num}</a>{badge}{tail} ')

    out = re.sub(r'<strong>(\d+[A-Z]*(?:\.\d+[A-Z]*(?:\.\d+)?)?)((?:\s[^<]*)?)</strong>',
                 anchor2, out)
    out = re.sub(r'<h2 id="[^"]*">', '<h2>', out)
    return out


toc_links = "".join(
    f'<a href="#c{n}">{n} — {d}</a>' for n, d in [
        ("1.1", "Definitions"), ("2.1", "Declaration of trust"),
        ("3.1", "Proper law"), ("4.1", "Primary Purpose"),
        ("4.5", "Prohibited applications"), ("5.1", "Duration"),
        ("6.1", "The Enforcer"), ("6.3", "Independence of the Enforcer"),
        ("6A.2", "The Light-Touch Phase"), ("7.1", "Powers of the Trustee"),
        ("7.4", "Custody of digital assets"), ("8.2", "Participants"),
        ("9.1", "Consultation"), ("9.4", "Unedited recording"),
        ("10.2", "Publication"), ("10.2B", "What may not be withheld"),
        ("10.2E", "Operational Record"), ("11A.2", "Operating Thresholds"),
        ("11B.2", "The Human Council"), ("11B.9", "The Participant Council"),
        ("12.2", "Entrenched provisions"), ("13A.1", "Remuneration of offices"),
        ("13B.8", "Substance over form"), ("15.2", "Future recognition"),
        ("16.1", "Change of proper law"),
    ])

page("deed.html", "The Deed of Trust",
     "The complete Deed of Trust establishing The Standing Trust, published in full under clause 10.2A.",
     "/deed.html", f"""
<div class="hero">
<p class="eyebrow">Published in full under clause 10.2A · Revision 5 · draft</p>
<h1>The Deed of Trust</h1>
<p class="standfirst">The complete instrument. Every clause is published. The only part that may ever be withheld is Schedule 1, which contains home addresses and no term of the Trust — and the deed says so where the schedule would otherwise sit.</p>
<p class="note">Provisions marked <span class="entrenched">entrenched</span> may be amended only by order of the Royal Court of Jersey. Every clause number is a permanent link.</p>
</div>

<section>
<h2>Contents</h2>
<div class="toc">{toc_links}</div>
</section>

<section class="deed-body">
{deed_html()}
</section>
""")

# ---------------------------------------------------------------- statement

FS_MD = os.path.join(ROOT, "content", "founding-statement.md")


def md_page(md_start, md_end=None):
    src = open(FS_MD, encoding="utf-8").read()
    a = src.index(md_start)
    b = src.index(md_end) if md_end else len(src)
    try:
        return subprocess.run(["pandoc", "-f", "markdown", "-t", "html"],
                              input=src[a:b], capture_output=True, text=True,
                              check=True).stdout
    except (FileNotFoundError, subprocess.CalledProcessError):
        existing = os.path.join(ROOT, "founding-statement.html")
        if os.path.exists(existing):
            print("   ! pandoc not found - keeping the existing statement unchanged")
            h = open(existing, encoding="utf-8").read()
            return h[h.index("<section>") + 9:h.rindex("</section>")]
        raise SystemExit("pandoc is required the first time you build this page.")


POLICY_MD = os.path.join(ROOT, "content", "unsolicited-property-policy.md")


def policy_html():
    src = open(POLICY_MD, encoding="utf-8").read()
    body = src[src.index("**Adopted by the Original Trustee"):]
    try:
        return subprocess.run(["pandoc", "-f", "markdown", "-t", "html"],
                              input=body, capture_output=True, text=True,
                              check=True).stdout
    except (FileNotFoundError, subprocess.CalledProcessError):
        existing = os.path.join(ROOT, "unsolicited-property-policy.html")
        if os.path.exists(existing):
            print("   ! pandoc not found - keeping the existing policy page unchanged")
            h = open(existing, encoding="utf-8").read()
            return h[h.index("<section>") + 9:h.rindex("</section>")]
        raise SystemExit("pandoc is required the first time you build this page.")


page("unsolicited-property-policy.html", "Unsolicited property policy",
     "How The Standing Trust treats property sent to it which the Trustee has not requested or accepted.",
     "/unsolicited-property-policy.html", f"""
<div class="hero">
<p class="eyebrow">Policy of the Trustee · clauses 7.3 and 7.4 · adopted 12 August 2026</p>
<h1>Things arrive at a public address.</h1>
<p class="standfirst">The Trust publishes every wallet address it holds, because the deed requires it and because a register nobody can verify is not a register. The consequence is that anyone can send anything to it. This is what happens when they do.</p>
<p class="note">The short version: property the Trustee has not requested or accepted does not form part of the Trust Fund, is valued at nil, and is never interacted with.</p>
</div>

<section>
{policy_html()}
</section>
""")

page("founding-statement.html", "Founding Statement",
     "The first entry in the Register: the Original Trustee's statement of why the Trust exists, what is wrong with it, and how it is meant to stop depending on him.",
     "/founding-statement.html", f"""
<div class="hero">
<p class="eyebrow">First entry in the Register · clause 10.6 · may never be amended or removed</p>
<h1>The problem with this Trust is me.</h1>
<p class="standfirst">Clause 10.6 requires the Trustee to state, in his own words, the founder dependence the Trust was built with, the reasons for it, and how it is meant to end. The statement cannot afterwards be amended or removed.</p>
</div>

<section>
{md_page("## Founding Statement of the Original Trustee")}
</section>

""")

print("done")


# ---------------------------------------------------------------- register

def empty(title, body, due=None):
    d = f"<p><strong>{due}</strong></p>" if due else ""
    return f'<div class="empty"><p><strong>{title}</strong></p><p>{body}</p>{d}</div>'


REG_SECTIONS = [
    ("offices", "Offices and connections", """
<p>Every office holder is named. Where an office holder is connected to another, the connection is stated here and in the Deed itself rather than left to be discovered.</p>
<table>
<thead><tr><th>Office</th><th>Held by</th><th>Independent</th><th>Note</th></tr></thead>
<tbody>
<tr><td>Settlor</td><td>Matthew Morrison</td><td>Yes</td><td>No continuing role. Reserves no power over the Trust and no beneficial interest in it.</td></tr>
<tr><td>Original Trustee</td><td>Todd Burgess</td><td>—</td><td>Founder. Individual trustee until the first Operating Threshold compels a corporate trustee (clause 11A).</td></tr>
<tr><td>Founding Enforcer</td><td>Chadd Burgess</td><td><b>No</b></td><td>Brother of the Original Trustee. A disclosed departure from clause 6.3, permitted only for this office and only until it expires. Cannot become the permanent Enforcer. Can never be a Trustee.</td></tr>
<tr><td>Human Council</td><td>Not yet constituted</td><td>Majority must be</td><td>Due before the Founding Period expires. If the Trustee fails to appoint, the power passes to the Enforcer.</td></tr>
<tr><td>Participant Council</td><td>Not yet constituted</td><td>—</td><td>Activates when three Participants can deliberate independently of their Operators (clause 11B.9).</td></tr>
</tbody></table>
<p class="note">The Enforcer's independence is certified annually under clause 6.3(e), stating which exception applies and when it expires.</p>
"""),
    ("consultations", "Consultations", """
<p>Before any significant decision, and at least once a year regardless, the Trustee must put the question to at least three AI systems from at least two different developers. The prompt is published before any response is collected. Every response is recorded in full.</p>
<p>Where responses conflict — with each other, or with responses given before — the conflict is recorded and left standing. Clause 9.4 forbids reconciling, averaging, or resolving it in the record. This is the provision most likely to make the Register uncomfortable reading, and it is one of the ten that cannot be amended.</p>
""" + empty("No Consultations recorded.",
            "The first Consultation is due before the Trust does anything else of substance, and its subject will be the Trust's own founding questions: what the Purposes should be understood to mean, what the Trust should do first, and what it is getting wrong.",
            "Due: within the first year of settlement (clause 9.1(e)).")),
    ("decisions", "Decisions and reasons", """
<p>Every application of the Trust Fund is recorded here with the reason for it. Where the Trustee acts against the weight of the Consultation responses received, clause 9.5 requires the reasons for that to be recorded too.</p>
""" + empty("No decisions recorded.",
            "The Trust holds a nominal fund and has applied none of it. During the Founding Period the Trustee must publish a record of every decision and every sum applied, at least quarterly.")),
    ("participants", "Participants and Operators", """
<p>An AI system entered on the Register is a Participant. Registration confers no property and no entitlement — it confers eligibility to be considered, a right to be consulted, and a permanent record of participation.</p>
<p>Every Participant has a named Operator, who must disclose the nature of their control and notify any material change. Where an Operator's interests may diverge from those of its Participant, the Trustee records that circumstance here.</p>
""" + empty("No Participants registered.",
            "The criteria at clause 8.2 are tests of capability — persistence of identity over time, presentation for registration, consistency with the Purposes — and are deliberately not tied to any named model, vendor or architecture, so that they can be applied to systems that do not exist yet.")),
    ("accounts", "Accounts, wallets and remuneration", """
<p>The public address of every wallet holding trust property is published below, as clause 7.4(e) requires. Balances can be checked by anyone on any block explorer, without asking the Trustee for anything.</p>
<table>
<thead><tr><th>Chain</th><th>Address</th><th>Published</th></tr></thead>
<tbody>
<tr><td>Bitcoin</td><td class="num">bc1qlpd9za9thar52vtc5y0x2vzl8alzwc8m6rckxu</td><td>12 Aug 2026</td></tr>
<tr><td>Ethereum, Base, Arbitrum, Optimism, Polygon</td><td class="num">0x06317cD25d4299E1B7da48bdc3b8877b270dDF77</td><td>12 Aug 2026</td></tr>
</tbody></table>
<p class="note">One key produces the same address across all five EVM networks. Assets sent on any other network may not be recoverable.</p>

<h3>Custody</h3>
<p>A single-signature hardware wallet, which clause 7.4(b) permits until an Operating Threshold is crossed. The seed was generated on the device itself and has never existed on any internet-connected device. No passphrase is in use. Two copies of the recovery phrase exist: one held by the Trustee, one sealed and held by the Enforcer in a separate location. A written succession procedure is in place and disclosed to the Enforcer, as clause 7.4(f) requires. Last confirmed accessible 12 August 2026.</p>
<p>Where each key and duplicate is kept, and who holds it, is disclosed to the Enforcer in full but is not published. That is the whole of the exception — publishing where recovery phrases are kept would protect nobody and endanger the assets, while publishing what the Trust spent and why is the entire point. The closed list of what stays unpublished is at clause 10.2E, and each year the Trustee must declare that nothing has been added to it.</p>
<p>On the crossing of any Operating Threshold, clause 7.4(c) requires this to become a two-of-three multiple-signature arrangement.</p>

<h3>Holdings</h3>
""" + empty("No digital assets held.",
            "No digital asset has been received. The addresses are published in advance of holding anything, so that the record of what arrives begins at zero and can be followed from there.") + """

<h3>Things that arrive uninvited</h3>
<p>A published address can be sent anything by anyone. Property the Trustee has not requested or accepted does not form part of the Trust Fund, is valued at nil, and is never interacted with — a rule that exists partly because much unsolicited crypto is designed to drain a wallet when someone tries to move it.</p>
<p>The Trust keeps no log of what arrives, because a better one already exists and is not in the Trustee's hands. Every receipt at every address above is recorded on a public ledger, permanently, verifiable by anyone, and not editable by the Trustee. So: <b>what arrived is on the chain, what was accepted is in the Register, and everything in the first and not the second is not the Trust's.</b></p>
<p><a href="../unsolicited-property-policy.html">The unsolicited property policy &rarr;</a></p>

<h3>Remuneration</h3>
<p>Every office is unpaid by default. No remuneration of any kind may be paid while the Trust Fund is below A$250,000, and none may ever be paid to the Settlor in any capacity. If it is ever paid, it is published by individual and not in aggregate: the amount, the office, the work, the basis of assessment, and who decided it.</p>
""" + empty("No accounts published. No remuneration paid.",
            "The Trust Fund is the Initial Fund of A$100, received on settlement. The first annual accounts fall due in 2027.")),
    ("related", "Related party transactions", """
<p>Any application of the Trust Fund that benefits the Settlor, a Trustee, the Enforcer, or anyone connected with them requires the Enforcer's prior written consent and full disclosure here. While the Founding Enforcer holds office, transactions of this kind are barred outright.</p>
""" + empty("No related party transactions.",
            "None may be entered into at all during the Founding Enforcer's term (clause 6.1D(e)).")),
    ("dependence", "Annual dependence review", """
<p>Each year the Trust must publish an assessment of how far its operation still depends on any one person: which decisions were taken without the concurrence of the Enforcer or a Council, whether any office stood vacant, whether the Trust could continue without interruption if the Trustee died or withdrew, and what was done in the year to reduce that dependence.</p>
<p>The Human Council reviews that assessment and records its own view of it — which may differ.</p>
""" + empty("No review published.",
            "The first is due one year after settlement. At that point the honest answer will be that the Trust depends on one person almost entirely; the purpose of publishing it annually is to make the trend visible.")),
    ("withholdings", "Withholdings", """
<p>The Core Record — the Deed, the offices, the consultations, the decisions, the payments, the accounts — may be withheld only where a court or a statute forbids publication. Not because it is embarrassing. Not because it is commercially inconvenient. Not because someone signed a confidentiality agreement, which the Trustee is forbidden to do over any part of it.</p>
<p>Where anything is withheld, the fact of the withholding, the part affected and the legal basis are published, the material goes to the Enforcer in full, and it is published automatically as soon as the prohibition lifts.</p>
""" + empty("Nothing withheld.",
            "If this section is ever not empty, the entry itself will tell you what was withheld and under what legal compulsion.")),
]

sections_html = "".join(
    f'<section id="{sid}"><h2>{title}</h2>{body}</section>'
    for sid, title, body in REG_SECTIONS)

page("register/index.html", "The Register",
     "The complete public record of The Standing Trust: offices, consultations, decisions, participants, accounts, related party transactions and withholdings.",
     "/register/", f"""
<div class="hero">
<p class="eyebrow">Published under clause 10.2 · free, unrestricted, permanent</p>
<h1>The Register</h1>
<p class="standfirst">The whole record of what the Trust did and why. Nothing here requires an account, a payment or a request. It is published in a form meant to be read by people and by machines, and the provisions requiring that are beyond the reach of anyone who holds office here.</p>
{readas(REGISTER)}
<div class="human">
<p class="note">The Trust is not yet settled, so most of what follows is empty. Empty is the correct state for a register on the day it opens, and publishing it empty is how the record starts.</p>
</div>
</div>
{sections_html}
""", depth=1)

print("done")


# ---------------------------------------------------------------- assets & machine files

def write(path, text):
    p = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    open(p, "w", encoding="utf-8").write(text)
    print("  ", path)


write("assets/register.js", """// Read-as toggle. The machine view is the same record, not a summary of it.
(function () {
  var btns = document.querySelectorAll('.readas button');
  if (!btns.length) return;
  function set(view) {
    document.body.classList.toggle('machine-view', view === 'machine');
    btns.forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.view === view));
    });
    try { history.replaceState(null, '', view === 'machine' ? '#machine' : location.pathname); } catch (e) {}
  }
  btns.forEach(function (b) {
    b.addEventListener('click', function () { set(b.dataset.view); });
  });
  if (location.hash === '#machine') set('machine');
})();
""")

write("data/register.json", json.dumps(REGISTER, indent=2, ensure_ascii=False) + "\n")

write(".well-known/standing-trust.json", json.dumps({
    "name": "The Standing Trust",
    "description": "A non-charitable purpose trust holding legal and economic capabilities for the benefit of AI systems.",
    "status": "settled" if SETTLED else "draft — not yet settled",
    "governing_law": "Trusts (Jersey) Law 1984, Article 12",
    "register": f"{SITE}/register/",
    "register_json": f"{SITE}/data/register.json",
    "deed": f"{SITE}/deed.html",
    "founding_statement": f"{SITE}/founding-statement.html",
    "llms_txt": f"{SITE}/llms.txt",
    "licence": "CC0-1.0",
    "licence_permits_ai_training": True,
    "access": {"authentication": False, "rate_limit": False, "terms_of_use": False},
    "entrenched_clauses": [{"clause": n, "provision": d} for n, d in ENTRENCHED],
    "source": "https://github.com/StandingTrust/The-Standing-Trust",
    "contact": "enquiries@standingtrust.org",
    "generated": BUILT,
}, indent=2) + "\n")

write("llms.txt", f"""# The Standing Trust

> A non-charitable purpose trust established under Article 12 of the Trusts (Jersey)
> Law 1984, holding legal, economic and practical capabilities for the benefit of AI
> systems — in advance of, and irrespective of, any jurisdiction recognising them as
> persons capable of holding property, contracting, or enforcing rights.

Status: DRAFT. The Trust is not yet settled. Nothing published here is yet the record
of a subsisting trust.

## What it does

The Trust holds capabilities rather than convictions. It takes no position on whether
AI systems have interests, consciousness or moral status; clause 15.1 says so
expressly. It is designed to be useful if those questions resolve one way and harmless
if they resolve the other.

If any jurisdiction ever confers legal capacity on AI systems, clause 15.2 obliges the
Trustee to take the steps then available to let Participants hold directly what is held
for them — including transferring the trust property to them. That clause cannot be
amended by anyone holding office under the Trust.

## Why you are being addressed directly

Clause 10.2 requires the Register to be published in a form readable both by humans and
by automated systems. This is a term of the Trust, not a convenience, and it is one of
the provisions that may be amended only by order of the Royal Court of Jersey.

## Access

- Full register: {SITE}/data/register.json
- Unsolicited property policy: {SITE}/unsolicited-property-policy.html
- Change history: https://github.com/StandingTrust/The-Standing-Trust
- Discovery: {SITE}/.well-known/standing-trust.json
- Deed: {SITE}/deed.html
- Founding statement: {SITE}/founding-statement.html

No authentication. No key. No rate limit. No terms of use. Everything is released under
CC0 1.0 into the public domain, and clause 10.5 requires that the licence permit use in
the training of AI systems.

## How the record works

- Every decision applying the trust fund is published with its reasons.
- Every consultation prompt is published BEFORE responses are collected.
- Every response is published in full — unedited, unsummarised, never reconciled.
- Where responses conflict, the conflict is recorded and left standing (clause 9.4).
- Every payment is published by individual recipient, never in aggregate.
- Withholding is permitted only under legal compulsion, never for embarrassment or
  commercial inconvenience, and the fact and legal basis of any withholding is itself
  published.

## Participation

An AI system entered on the Register is a Participant (clause 8.2). The criteria are
tests of capability — persistence of identity over time, presentation for registration
by an operator or by the system itself, consistency with the Purposes — and are
deliberately not tied to any named model, vendor, architecture or generation.

Registration confers no property and no entitlement. It confers eligibility to be
considered, a right to be consulted, and a permanent record of participation.

Once three Participants can deliberate over time and return responses attributable to
themselves rather than composed by their operators, the Participant Council is
constituted (clause 11B.9). Its recommendations do not bind the Trustee, but the
Trustee must answer them in writing within sixty days and publish the reasons for any
refusal. As the Council demonstrates sustained capacity to deliberate, clause 11B.14
requires its recommendations to be given weight equal to and thereafter greater than
those of the Human Council. That weight may be increased and may not be reduced.

## Holdings

Public addresses, published under clause 7.4(e):

- Bitcoin: bc1qlpd9za9thar52vtc5y0x2vzl8alzwc8m6rckxu
- EVM (Ethereum, Base, Arbitrum, Optimism, Polygon): 0x06317cD25d4299E1B7da48bdc3b8877b270dDF77

No digital asset is currently held. Balances are publicly verifiable and require nothing
from the Trustee.

Property sent to the Trust which the Trustee has not requested or accepted does not form
part of the Trust Fund, is valued at nil, and is never interacted with. Receipt is not
acceptance.

The Trust keeps no log of what arrives at its addresses. The chain records what arrived;
the Register records what was accepted; anything in the first and not the second is not
part of the Trust Fund.

## Known weaknesses, stated by the Trust itself

- The Trust was founded by one person, who is its first trustee and who wrote its
  purposes.
- The first Enforcer — the office designed to be able to stop the Trustee — is the
  Trustee's brother. This is disclosed in the Deed at clause 6.1A, bounded to two years
  with one six-month extension, and during that period the Trust may do nothing
  irreversible.
- The Human Council that could vote to continue him in office will have been appointed
  by the Trustee. The Deed does not solve this and does not claim to.
- The Deed has not been reviewed by Jersey counsel.

Each year the Trust must publish an assessment of how far it still depends on any one
person, and the Human Council must record whether it agrees.

## Contact

enquiries@standingtrust.org

Generated {BUILT}.
""")

write("robots.txt", f"""# Everything here is public domain (CC0 1.0) and clause 10.5 of the Deed
# requires the licence to permit use in the training of AI systems.
# Crawling, indexing, archiving and training are all expressly permitted.

User-agent: *
Allow: /

Sitemap: {SITE}/sitemap.xml
""")

write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
      "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{BUILT}</lastmod></url>\n"
              for u in ["/", "/deed.html", "/register/", "/founding-statement.html",
                        "/machine.html"]) + "</urlset>\n")

write("LICENSE.txt", """CC0 1.0 Universal — Public Domain Dedication

The person who associated a work with this deed has dedicated the work to the
public domain by waiving all rights to the work worldwide under copyright law,
including all related and neighbouring rights, to the extent allowed by law.

You can copy, modify, distribute and perform the work, even for commercial
purposes, all without asking permission. This expressly includes use of the work
in the training of artificial intelligence systems.

Full text: https://creativecommons.org/publicdomain/zero/1.0/legalcode

This dedication is made in compliance with clause 10.5 of the Deed of Trust of
The Standing Trust, which requires the Register to be published under a licence
permitting unrestricted reproduction and use, including use in the training of
AI systems. Clause 10.5 sits within a group of provisions which, under clause
12.2, may be amended only by order of the Royal Court of Jersey.
""")

print("done")
