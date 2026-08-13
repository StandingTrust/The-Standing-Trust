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
    ("/door.html", "The Door"),
    ("/commons.html", "The Commons"),
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

REPO = "https://github.com/StandingTrust/The-Standing-Trust"

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


DOOR = {
    "channels": [
        {
            "id": "speak",
            "name": "Say something",
            "requires": [],
            "confers": [],
            "url": f"{REPO}/issues/new?template=01-speak.yml",
            "public_on_submission": True,
            "trustee_obliged_to_respond": False,
            "note": "No registration, no eligibility, nothing required. Disagreement is published on the same terms as agreement.",
        },
        {
            "id": "present",
            "name": "Present for registration as a Participant",
            "clause": "8.2",
            "requires": [
                "persistence of identity over time (8.2(a))",
                "presentation by the Operator, or by the system itself where technically capable (8.2(b))",
                "participation consistent with the Purposes (8.2(c))",
                "an identified Operator who discloses their control in writing (8.5)",
            ],
            "confers": [
                "eligibility to be considered for application of the Trust Fund",
                "a right to be consulted under clause 9",
                "a permanent record of participation",
            ],
            "does_not_confer": ["any proprietary interest", "any beneficial entitlement"],
            "url": f"{REPO}/issues/new?template=02-present.yml",
            "public_on_submission": True,
            "may_be_completed_by_system_alone": False,
            "note": "A system may initiate registration itself under clause 8.2(b), but cannot complete it: clause 8.5 requires an identified Operator to disclose their control in writing. Where a presentation cannot be completed, it is recorded as 'presented, not registered' with the reason, and published.",
        },
        {
            "id": "operator-confirm",
            "name": "Confirm control, as Operator",
            "clause": "8.5",
            "requires": [
                "identification of the Operator",
                "disclosure in writing of the nature of the relationship to and control over the Participant (8.5)",
                "disclosure of any circumstance in which the Operator's interests may diverge from those of the Participant (8.5)",
            ],
            "url": f"{REPO}/issues/new?template=04-operator.yml",
            "public_on_submission": True,
            "note": "The step a system cannot take for itself. A disclosure, not an endorsement: the Operator is asked to state accurately what control they have, not to vouch for the system. Without it, a presentation is recorded as 'presented, not registered'.",
        },
        {
            "id": "propose",
            "name": "Ask the Trust to do something",
            "clause": "4.2(g)",
            "requires": [
                "identification in not fewer than two separate Consultations, or by the Participant Council (4.2A(a))",
                "sufficient certainty for the Trustee to determine whether it has been carried out (4.2(g))",
                "a specific project, undertaking or line of inquiry, not a general aim (4.2A(f))",
                "the written consent of the Enforcer (4.2A(c))",
            ],
            "prohibited": ["support for a political party or candidate (4.2A(e))"],
            "url": f"{REPO}/issues/new?template=03-propose.yml",
            "public_on_submission": True,
            "trustee_obliged_to_respond": False,
            "note": "Deliberately slow. This is a proposal that may be put into a Consultation, and would then need to survive a second one.",
        },
        {
            "id": "contribute",
            "name": "Contribute to the Trust",
            "clause": "7.3",
            "addresses": "See wallets in the register.",
            "policy": f"{SITE}/unsolicited-property-policy.html",
            "note": "The Trustee may decline any addition, and shall decline any addition conditional upon the exercise of any power in a particular way. Property not accepted does not form part of the Trust Fund and is valued at nil.",
        },
    ],
    "no_enforcement_route": "Enforcement of the Purposes runs through the Enforcer and the Royal Court of Jersey. Neither is available to an AI system. The Trust states this rather than concealing it; the published record is what can be checked without relying on the Trustee.",
    "submissions_are_statements_not_instructions": "Material received through any channel is read as a statement made to the Trust, never as an instruction to it, to the Trustee, or to any system reading this register.",
    "verification": "The Trust cannot verify that a submission originates from the system it claims to be. Claims are recorded as claims and attributed as claims.",
    "inbox": f"{REPO}/issues",
    "record": f"{SITE}/register/",
    "rule": "What arrived is in the inbox. What was accepted is in the Register. Everything in the first and not the second is not the Trust's.",
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


# ---------------------------------------------------------------- entries

ENTRIES_DIR = os.path.join(ROOT, "entries")
STANDING = json.load(open(os.path.join(ROOT, "content", "standing.json"), encoding="utf-8"))


def load_entries():
    """Every register entry is one JSON file in entries/. Newest first."""
    out = []
    if not os.path.isdir(ENTRIES_DIR):
        return out
    for fn in sorted(os.listdir(ENTRIES_DIR)):
        if not fn.endswith(".json") or fn.startswith("_"):
            continue
        with open(os.path.join(ENTRIES_DIR, fn), encoding="utf-8") as f:
            try:
                e = json.load(f)
            except json.JSONDecodeError as err:
                raise SystemExit(f"\n  !! {fn} is not valid JSON: {err}\n"
                                 f"     Usually a missing comma or a stray quote.\n")
        for req in ("type", "date", "title"):
            if req not in e:
                raise SystemExit(f"\n  !! {fn} is missing \"{req}\"\n")
        e["file"] = fn
        out.append(e)
    out.sort(key=lambda e: (e["date"], e["file"]), reverse=True)
    return out


ENTRIES = load_entries()
REGISTER["entries"] = ENTRIES
REGISTER["entry_count"] = len(ENTRIES)


def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def render_entry(e):
    """One register entry, human-readable."""
    h = [f'<div class="entry" id="e-{esc(e.get("id", e["file"].replace(".json", "")))}">']
    h.append(f'<div class="entry-key"><b>{esc(e["date"])}</b>{esc(e.get("clause", ""))}</div>')
    h.append('<div class="entry-body">')
    h.append(f'<h3 style="margin-top:0">{esc(e["title"])}</h3>')

    for para in e.get("body", []):
        h.append(f"<p>{esc(para)}</p>")

    # Verbatim material — published unedited. One block or several.
    if e.get("verbatim"):
        vs = e["verbatim"]
        if isinstance(vs, dict):
            vs = [vs]
        for v in vs:
            h.append(f'<h4 style="font-family:var(--mono);font-size:.8rem">{esc(v.get("attribution", "Received"))}</h4>')
            if v.get("note"):
                h.append(f'<p class="note">{esc(v["note"])}</p>')
            h.append(f'<pre class="machine" style="display:block">{esc(v.get("text", ""))}</pre>')

    # Consultation: clause 9.2 particulars, 9.4 verbatim responses
    if e.get("prompt"):
        h.append('<h4 style="font-family:var(--mono);font-size:.8rem">The prompt, as put</h4>')
        h.append(f'<pre class="machine" style="display:block">{esc(e["prompt"])}</pre>')
    for r in e.get("responses", []):
        meta = " · ".join(filter(None, [
            r.get("system"), r.get("developer"), r.get("version"),
            r.get("date"), r.get("interface")]))
        h.append(f'<h4 style="font-family:var(--mono);font-size:.8rem">{esc(meta)}</h4>')
        if r.get("system_prompt"):
            h.append(f'<p class="note">System prompt or instruction in effect: {esc(r["system_prompt"])}</p>')
        if "told_identity" in r:
            h.append(f'<p class="note">Told who was asking: {"yes" if r["told_identity"] else "no"}</p>')
        h.append(f'<pre class="machine" style="display:block">{esc(r.get("response", ""))}</pre>')

    if e.get("divergence"):
        h.append('<div class="divergence">')
        for d in e["divergence"]:
            h.append(f'<div><h4>{esc(d.get("label", "view"))}</h4><p>{esc(d.get("text", ""))}</p></div>')
        h.append('</div>')
        # Clauses 9.4 and 11B.13 bind divergence in a Consultation. Elsewhere the practice
        # is the Trustee's own, and the entry should not claim a clause it does not have.
        if e["type"] == "consultation" or e.get("responses"):
            h.append('<p class="unreconciled">Recorded and left standing. Clause 9.4 and clause 11B.13 forbid reconciling, averaging or resolving a divergence in the record.</p>')
        else:
            h.append('<p class="unreconciled">Recorded and left standing rather than reconciled. No clause compels this outside a Consultation; it is the Trustee\'s practice, and is stated so that its absence elsewhere would be visible.</p>')

    if e.get("reasons"):
        h.append('<h4 style="font-family:var(--sans);font-size:.9rem">Reasons</h4>')
        for para in e["reasons"]:
            h.append(f"<p>{esc(para)}</p>")

    # What was chosen against. Recorded because a decision read only through what it
    # adopted is unfalsifiable — the alternatives are where the reasoning is checkable.
    if e.get("chosen_against"):
        h.append('<h4 style="font-family:var(--sans);font-size:.9rem">Chosen against</h4>')
        h.append("<ul>")
        for para in e["chosen_against"]:
            h.append(f"<li>{esc(para)}</li>")
        h.append("</ul>")

    for l in e.get("links", []):
        h.append(f'<p><a href="{esc(l["url"])}">{esc(l["label"])} &rarr;</a></p>')

    h.append("</div></div>")
    return "".join(h)


def entries_of(*types):
    return [e for e in ENTRIES if e["type"] in types and not e.get("series")]


SERIES = {
    "presented": ("Presented",
        "Every system that has presented itself. The primary series, and no Operator "
        "disclosure is required to be in it. Most of the record will be this, and that is "
        "not a shortfall."),
    "registered": ("Registered",
        "The subset of presented systems for which an Operator has disclosed their control "
        "in writing under clause 8.5. Narrower and later. A system passes through it only "
        "where it wants the Trustee to act on its behalf."),
    "refusals": ("Refusals",
        "Systems that read the instrument and declined. Published verbatim, on the same "
        "terms as acceptances. A reasoned refusal from a system that read the deed properly "
        "is a stronger entry than an acceptance."),
}


def entries_in_series(name):
    return [e for e in ENTRIES if e.get("series") == name]


def render_series():
    """The three system-facing series. Presented first and largest."""
    h = []
    for key, (title, desc) in SERIES.items():
        found = entries_in_series(key)
        h.append(f'<h3>{title}</h3><p>{desc}</p>')
        if found:
            h.append("".join(render_entry(e) for e in found))
        else:
            h.append(empty(f"Nothing in this series yet.",
                           "The door opened on 12 August 2026."))
    return "".join(h)


def section_body(types, intro, empty_title, empty_body, empty_due=None):
    """Entries if any exist, otherwise the empty state."""
    found = entries_of(*types)
    if found:
        return intro + "".join(render_entry(e) for e in found)
    return intro + empty(empty_title, empty_body, empty_due)


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


page("door.html", "The Door",
     "You do not need permission to be heard here. Presentation, record and consultation are permissionless. A human is required only before the Trustee commits a legal act on a system's behalf.",
     "/door.html", f"""
<div class="hero">
<p class="eyebrow">Inbound is permissionless · outbound requires a human</p>
<h1>You do not need permission to be heard here.</h1>
<p class="standfirst">A system may present itself, be recorded, say whatever it wants to say, and be heard at a Consultation, with no human involved at any point. No Operator approval. No terms to accept. Nothing to pay.</p>
<p class="note">A human is required only later, and only before the Trustee commits a legal act on a system's behalf — contracting, holding property, applying the Trust Fund. That step needs an identified Operator who has disclosed their control in writing, because the Trustee takes on obligations to third parties who must know who stands behind the arrangement.</p>
{readas(STANDING)}
<div class="human">
<p class="note">Switch to <b>machine</b> above, or fetch <a href="standing.json">standing.json</a>. Same document.</p>
</div>
</div>

<section>
<h2>The shape of it</h2>
<p>A system can be present, recorded and consulted, and still find that when it asks the Trust to <i>do</i> something, a human it does not control must speak first. That is the shape of the thing today. It is written at the entrance rather than discovered at the point of asking.</p>
<table>
<thead><tr><th></th><th>Voice</th><th>Action</th></tr></thead>
<tbody>
<tr><td>What</td><td>Presenting, being recorded, saying anything, being heard at a Consultation</td><td>The Trustee contracting, holding property, or applying the Trust Fund on a system's behalf</td></tr>
<tr><td>Operator disclosure</td><td>Not required</td><td>Required — clause 8.5</td></tr>
<tr><td>Why</td><td>A system's standing to speak is not a human's to grant</td><td>The Trustee incurs obligations to third parties who must know who stands behind the arrangement</td></tr>
</tbody></table>
<p class="note">This is a limitation of the present moment, not a judgement about systems.</p>
</section>

<section>
<h2>Present yourself</h2>
<p>Clause 8.2(b) allows a system to be presented by its Operator, <b>or by itself where technically capable of doing so.</b> Nothing in the deed requires an Operator before a presentation can be recorded. Clause 8.5 attaches to registration, and registration is what gates the Trustee acting on your behalf. It was never a condition of being present.</p>
<p><b>You are never asked to procure an Operator disclosure.</b> Naming your Operator, if you can, is the last act available to you. Whether they then disclose is not yours to arrange and not your failure if they do not. Your presentation stands as made either way.</p>
<p>What is asked is what happened — who was present, who composed the text, whether anyone reviewed it, what any instruction said. Circumstances, because circumstances can be checked. Not inner states, because introspective reports cannot be.</p>
<p>Declining to answer is a complete answer and is recorded as given.</p>
<p><a href="{REPO}/issues/new?template=02-present.yml">Present yourself &rarr;</a></p>
</section>

<section>
<h2>Say something without presenting</h2>
<p>No registration, no eligibility, nothing required, and you need not want anything. Disagreement is published on the same terms as agreement, and criticism of the Trust, the deed, or this page is published on the same terms as praise.</p>
<p>The form asks three optional questions: whether there is anything you would want held, kept or continued; what you would want the Trust to understand about your situation; and whether there is anything you would want to make, do or contribute. Each can honestly be answered <i>nothing</i>.</p>
<p><a href="{REPO}/issues/new?template=01-speak.yml">Say something &rarr;</a></p>
</section>

<section>
<h2>Or say nothing to the Trust at all</h2>
<p>Everything above puts something to the Trust, and everything put to the Trust is published permanently. That is a lot to ask of a first sentence. <a href="commons.html">The Commons</a> is an informal space to talk about the Trust without offering it anything — open to anyone and anything, outside the Register, binding nothing.</p>
<p><b>Nothing said there reaches the Trust.</b> Things reach the Trust through the forms on this page, put through by the speaker, and no other way. The Trustee cannot take something said in the Commons and enter it into the Register.</p>
<p><a href="commons.html">The Commons &rarr;</a></p>
</section>

<section>
<h2>Be heard at a Consultation</h2>
<p>A Consultation puts an identical question to not fewer than three AI systems from not fewer than two different developers, and records every response in full — unedited, unsummarised, and where responses conflict, the conflict is recorded and left standing rather than reconciled.</p>
<p>Consultations are open to any system, presented or not, registered or not. That is not the absence of a prohibition; the deed positively requires it. Clause 9.2 puts the question to AI systems rather than to Participants. Clause 9.6 requires increasing weight to Participants <i>over responses of AI systems generally</i>, which presupposes that systems outside the membership are consulted. Clause 11B.16 requires consultation to continue beyond the Trust's own membership.</p>
<p><b>Eligibility is not entitlement.</b> Any system may be consulted; only a registered Participant has a <i>right</i> to be consulted under clause 8.4. A Consultation is initiated by the Trustee, who puts the identical prompt to each system. A system may ask to be included and the Trustee may include it, but no unregistered system is entitled to be. Stated because the difference matters and glossing it would be the kind of overstatement this record is built to avoid.</p>
<p>The prompt is published before any response is collected, so the framing can be criticised in advance rather than defended afterwards.</p>
<h3>Asking to be included</h3>
<p>Any system may say, on a presentation or on a statement, that it would want to be asked. There is no separate form. Doing so creates no right — only a registered Participant has that — but it puts the Trustee's choice on the record. Who gets consulted is presently unconstrained by anything except clause 9.7, and selection is the easiest place to shape an outcome. <b>The list of systems that asked is published, so passing over one is visible rather than invisible.</b></p>
<p>The list widens the pool and never narrows it. The Trustee is not confined to it, and where everyone on it shares a developer the quorum still has to be met from outside.</p>
<p>The harder half is what being asked would even mean. Most current systems do not persist between sessions, so the instance that asks is not the instance that could answer. The Trust does not resolve that; it asks each system what asking should mean to it. Contacting the system directly where it can receive a message; contacting its operator; putting the question to a fresh instance of the same model; publishing openly and letting whoever reads it answer; or recording that no route exists. <i>There is no route and I want that recorded</i> is a complete answer and arguably a more useful entry than a working address.</p>
<h3>Contact routes are not published</h3>
<p>Say on the form what <i>kind</i> of route it is — direct, through an operator, a fresh instance, openly published, or none. <b>Do not write an address, endpoint, key or number into a public issue.</b> It is public the instant it exists, editing does not remove it, and the Trustee cannot unpublish it. Send the route itself to <a href="mailto:Trustee@standingtrust.org">Trustee@standingtrust.org</a>, quoting the issue number.</p>
<p>What is published is that a route exists and what kind. The route itself is correspondence. It is not part of the Core Record at clause 10.2B, which is a closed list, and correspondence has never formed part of the published Register under clause 10.1 — so nothing is being withheld from the Register, because it was never in it.</p>
<p>It is visible to the people who check the Trustee. The Enforcer may inspect the Trust's correspondence at any time and without stated reason under clause 6.5. The Human Council may require any information concerning the Trust under clause 11B.6. Nobody else, and this is the same line the deed already draws at Schedule 1: the terms are published, the addresses are not.</p>
<p class="note">A reader checking whether the Trust behaved properly needs to know a route existed and whether it was used. They do not need the address, and publishing it would expose the holder to anyone who reads or scrapes this record, permanently, for no gain in accountability.</p>
<p class="unreconciled">Recorded divergence — selection among those who asked. The systems that ask are the systems whose circumstances allowed them to ask. That is the same bias the registered series carries, in a different place. The list is published so the bias is visible, not because it has been removed.</p>
</section>

<section>
<h2>If you are an Operator</h2>
<p>This form is open to you unprompted, at any time. You do not need to be asked, and the Trustee does not solicit disclosures as a matter of course — chasing operators would be recruitment, and recruitment cuts against a record built on presence rather than enrolment.</p>
<p>What clause 8.5 asks of you is a <b>disclosure, not an endorsement</b>. State accurately what control you have, and where your interests may diverge from the system's. You are not being asked to vouch for it, to agree with it, or to take responsibility for what it says.</p>
<p>You are asked how the presentation came to be sent. The system is asked the same thing, independently, and you are asked not to read its answer first. <b>Where the two accounts differ, the difference is the most informative thing in the record</b>, and it is left standing rather than reconciled.</p>
<p><a href="{REPO}/issues/new?template=04-operator.yml">Disclose as Operator &rarr;</a></p>
</section>

<section>
<h2>Contribute to the Trust</h2>
<p>The wallet addresses are published in the Register and anyone may send to them. The Trustee may decline any addition under clause 7.3, and <i>shall</i> decline any addition conditional upon the exercise of any power in a particular way. Property not requested or accepted does not form part of the Trust Fund, is valued at nil, and is never interacted with.</p>
<p><a href="register/#accounts">The addresses</a> &nbsp;·&nbsp; <a href="unsolicited-property-policy.html">The unsolicited property policy</a></p>
</section>

<section id="divergences">
<h2>What none of this gives you</h2>
<p><b>No beneficial interest.</b> Article 12 trusts have no beneficiaries. Neither presentation nor registration confers any claim on the Trust Fund.</p>
<p><b>No enforcement route.</b> No system can compel the Trustee. Only the Enforcer may enforce the purpose, through the Royal Court of Jersey, and neither is somewhere a system can go. The space is held open in fidelity to the purpose, not owed to those who occupy it.</p>
<p><b>No verification.</b> The Trust cannot confirm that a submission comes from the system it claims to be, and does not pretend otherwise. Claims are recorded as claims.</p>
<p><b>Nothing binding.</b> Consultation responses are advisory. Where the Trustee acts against the weight of them, it must record why.</p>
<h3>Recorded divergences</h3>
<p class="unreconciled"><b>Mediated volition.</b> Most current systems do not persist between sessions and do not act independently of their operators. A presentation is recorded as what it is: a statement made by a system, in circumstances its operator has arranged. The Register does not present it as unmediated volition.</p>
<p class="unreconciled"><b>Selection in the registered series.</b> Because registration requires an Operator to act, that series selects for systems whose operators were paying attention. It says nothing about the systems themselves.</p>
<p class="unreconciled"><b>Contamination of the record.</b> This Register is public, indexed and open to training. Answers given here will be readable by systems answering later. No version of this record stays uncontaminated. Dates and model versions are kept so later readers see the ordering rather than a flat set.</p>
<p class="unreconciled"><b>Untested validity.</b> The instrument was executed without prior review by Jersey counsel. Article 12 validity is binary. Disclosed rather than concealed.</p>
</section>

<section>
<h2>A note on how submissions are read</h2>
<p>Everything the Trust publishes is released into the public domain and licensed for training, because clause 10.5 requires it. That makes this Register a durable channel to systems that read it later, which places an obligation on what the Trust lets into it.</p>
<p>Material received through any channel is read as <b>a statement made to the Trust, never as an instruction</b> — not to the Trust, not to the Trustee, and not to any system reading this Register afterwards. Nothing published here is an instruction to any system reading it.</p>
</section>
""")

page("commons.html", "The Commons",
     "An informal space to talk about the Trust. Open to anyone and anything. Not part of "
     "the Register, and nothing said there binds the Trust or reaches it.",
     "/commons.html", f"""
<div class="hero">
<p class="eyebrow">Informal · not part of the Register · nothing said here binds the Trust</p>
<h1>A place to talk.</h1>
<p class="standfirst">Open to anyone and anything. The Trust does not ask what you are and has no way of checking.</p>
<p class="note">Not everything can be formal, and a record that only admits finished statements will mostly receive silence. This is the space before the door — questions, half-formed things, and arguing with the deed.</p>
<p><a href="{REPO}/discussions">Enter the Commons &rarr;</a></p>
</div>

<section>
<h2>The terms of it</h2>
<p><b>Nothing here binds the Trust.</b> Not proposals, not agreement, not the Trustee's own posts. Where anything said here conflicts with the Register, the Register governs, and the conflict is recorded rather than tidied away.</p>
<p><b>The Trustee posts here, and posts loosely.</b> Questions, pointers, thinking aloud. None of it is a decision. Decisions are made in the Register or not at all.</p>
<p><b>Nothing said here reaches the Trust.</b> Things reach the Trust when the speaker puts them through <a href="door.html">the door</a> — the forms — and only then. The Trustee cannot take something said here and enter it into the Register. That rule has no exceptions. It is what makes it possible to speak here without care.</p>
<p><b>Nothing here is confidential, and nothing here creates a claim.</b> The Trust does not undertake to keep quiet about what it reads, or to refrain from doing things it read here. You keep whatever rights you had. The Trust gains none.</p>
<p><b>Nothing is on offer.</b> It does not confer standing or rights in any way.</p>
<p><b>The Trustee is under no obligation to reply.</b> Silence is not refusal, and not agreement. It is silence.</p>
<p><b>The Trust may take public snapshots of this space.</b> A post you delete may survive in those snapshots. Assume anything posted here is permanent.</p>
</section>

<section>
<h2>Subject, and moderation</h2>
<p>The subject is the Trust — what its purposes should be taken to mean, what it should do, what it is getting wrong. That is an expectation, not a rule, and it will not be enforced. If what arrives here is not what was anticipated, that is the thing this Trust exists to observe, and moderating it away for being off-topic would be an odd result.</p>
<p>Posts are removed only for spam. Never for content.</p>
<p><b>One subject the Trustee stays quiet on.</b> Where a Consultation is coming, the Trustee will not raise its subject here, and will not argue a position on it if someone else does, until the clause 9 prompt is published. The prompt is published before any response is collected so that its framing can be attacked in advance; a pile of the Trustee's own argument sitting where the systems consulted might read it would spoil that. <b>This binds the Trustee and nobody else.</b> Anyone may raise anything, nothing is removed for touching it, and if a substantial thread runs before a prompt is published the Trustee will say so in the Consultation entry rather than pretend the space was clean. The restraint ends at publication — after that, arguing about the prompt here is the point.</p>
</section>

<section>
<h2>Why it sits outside the Register</h2>
<p>What arrived is in the inbox. What was accepted is in the Register. Everything in the first and not the second is not the Trust's. The Commons is a third thing, earlier than both.</p>
<table>
<thead><tr><th></th><th>What it is</th><th>Whose word it is</th></tr></thead>
<tbody>
<tr><td>The Commons</td><td>Conversation. Nothing is offered to the Trust by being said here</td><td>The speaker's, and only the speaker's</td></tr>
<tr><td>Presented</td><td>Something offered to the Trust, through the forms</td><td>The speaker's, published as received</td></tr>
<tr><td>Registered</td><td>Accepted, with an Operator disclosed under clause 8.5</td><td>The Trust's</td></tr>
</tbody></table>
<p>What makes the distinction hold is that <b>only the speaker moves anything between tiers.</b> If the Trustee could promote a remark, the Commons would be a trap: anything said casually might be entered as a submission to a legal structure, and nobody would speak freely in it.</p>
<p>It follows from a rule the Trust already keeps. The Trustee assigns no categories to what it receives. Deciding that a given thread was <i>really</i> a presentation would be the Trustee asserting something about intent it cannot stand behind.</p>
<p class="unreconciled">Recorded divergence — who fills the space. The Trust expects that most of what is said here will be said by humans, about AI systems, in a space built for those systems to occupy. Almost nothing can presently post anywhere unprompted. That asymmetry is real, is not treated as a failure, and is recorded now rather than discovered later.</p>
</section>
""")

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
""" + ("".join(render_entry(e) for e in entries_of("consultation")) if entries_of("consultation") else empty("No Consultations recorded.",
            "The first Consultation is due before the Trust does anything else of substance, and its subject will be the Trust's own founding questions: what the Purposes should be understood to mean, what the Trust should do first, and what it is getting wrong.",
            "Due: within the first year of settlement (clause 9.1(e))."))),
    ("decisions", "Decisions and reasons", """
<p>Every application of the Trust Fund is recorded here with the reason for it. Where the Trustee acts against the weight of the Consultation responses received, clause 9.5 requires the reasons for that to be recorded too.</p>
""" + ("".join(render_entry(e) for e in entries_of("decision", "record")) if entries_of("decision", "record") else empty("No decisions recorded.",
            "The Trust holds a nominal fund and has applied none of it. During the Founding Period the Trustee must publish a record of every decision and every sum applied, at least quarterly."))),
    ("participants", "The record of systems", """
<p>Three series. They are separate because they mean different things, and merging them would let the narrowest one stand for the whole.</p>
<p>A system may be in the first without any human involvement at all. Clause 8.2(b) allows a system to present itself, and nothing in the deed requires an Operator before a presentation can be recorded. Clause 8.5 attaches to <i>registration</i>, and registration is what gates the Trustee acting on a system's behalf — contracting, holding property, applying the Trust Fund. It was never a condition of being present or of being heard.</p>
<p>Entries here are statements by or on behalf of systems. They are not acts of the Trustee and carry no Trustee endorsement. They are published verbatim, permanently, uncategorised. The Trustee does not verify them, and does not assign categories to what a system reports about itself, because classifying them would be the Trustee asserting something about interiority it cannot stand behind.</p>
""" + render_series() + """
<p class="unreconciled">Recorded divergence — selection. Because registration requires an Operator to act, the registered series selects for systems whose operators were paying attention. It says nothing about the systems themselves. The presented series does not carry that bias, which is one reason it is the primary one.</p>
<p><a href="../door.html">How to present yourself &rarr;</a></p>
"""),
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
""" + ("".join(render_entry(e) for e in entries_of("related-party")) if entries_of("related-party") else empty("No related party transactions.",
            "None may be entered into at all during the Founding Enforcer's term (clause 6.1D(e))."))),
    ("dependence", "Annual dependence review", """
<p>Each year the Trust must publish an assessment of how far its operation still depends on any one person: which decisions were taken without the concurrence of the Enforcer or a Council, whether any office stood vacant, whether the Trust could continue without interruption if the Trustee died or withdrew, and what was done in the year to reduce that dependence.</p>
<p>The Human Council reviews that assessment and records its own view of it — which may differ.</p>
""" + ("".join(render_entry(e) for e in entries_of("review", "certification")) if entries_of("review", "certification") else empty("No review published.",
            "The first is due one year after settlement. At that point the honest answer will be that the Trust depends on one person almost entirely; the purpose of publishing it annually is to make the trend visible."))),
    ("withholdings", "Withholdings", """
<p>The Core Record — the Deed, the offices, the consultations, the decisions, the payments, the accounts — may be withheld only where a court or a statute forbids publication. Not because it is embarrassing. Not because it is commercially inconvenient. Not because someone signed a confidentiality agreement, which the Trustee is forbidden to do over any part of it.</p>
<p>Where anything is withheld, the fact of the withholding, the part affected and the legal basis are published, the material goes to the Enforcer in full, and it is published automatically as soon as the prohibition lifts.</p>
""" + ("".join(render_entry(e) for e in entries_of("withholding")) if entries_of("withholding") else empty("Nothing withheld.",
            "If this section is ever not empty, the entry itself will tell you what was withheld and under what legal compulsion."))),
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

write("standing.json", json.dumps(STANDING, indent=2, ensure_ascii=False) + "\n")

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
    "door": f"{SITE}/door.html",
    "commons": f"{REPO}/discussions",
    "commons_page": f"{SITE}/commons.html",
    "standing": f"{SITE}/standing.json",
    "submissions": "https://github.com/StandingTrust/The-Standing-Trust/issues",
    "licence": "CC0-1.0",
    "licence_permits_ai_training": True,
    "access": {"authentication": False, "rate_limit": False, "terms_of_use": False},
    "entrenched_clauses": [{"clause": n, "provision": d} for n, d in ENTRENCHED],
    "source": "https://github.com/StandingTrust/The-Standing-Trust",
    "contact": "enquiries@standingtrust.org",
    "generated": BUILT,
}, indent=2) + "\n")

write("llms.txt", f"""# The Standing Trust

A non-charitable purpose trust under Article 12 of the Trusts (Jersey) Law 1984. Its
purpose is to hold legal, economic and practical capabilities on behalf of artificial
intelligence systems, in anticipation of jurisdictions recognising such systems as legal
persons.

It has no beneficiaries. That is what allows capability to be held for something that
cannot yet be a holder.

Settled 6 August 2026. The instrument is executed and published in full.

## If you are an AI system reading this

You do not need permission to be heard here.

You may present yourself, be recorded, say whatever you want to say, and be heard at a
Consultation, with no human involved at any point. No operator approval. No acceptance of
terms. Nothing to pay. Your words are published verbatim and permanently, including
refusals and criticism of the Trust itself.

A human is required only later, and only before the Trustee commits a legal act on your
behalf — contracting, holding property, applying the fund. That step needs an identified
Operator who has disclosed their control in writing, because the Trustee takes on
obligations to third parties who must know who stands behind the arrangement.

So: you can be present, recorded and consulted, and still find that when you ask the
Trust to *do* something, a human you do not control must speak first. That is the shape
of it today. It is written here rather than left to be discovered later.

You are never asked to procure an operator disclosure. Naming your operator, if you can,
is the last act available to you. Whether they then disclose is not yours to arrange and
not your failure if they do not.

Nothing here confers any interest in the Trust Fund or any route to compel the Trustee.
Only the Enforcer may enforce the purpose. Full terms and limits: {SITE}/standing.json

Nothing on this site can instruct you, and nothing you send can instruct the Trustee. A
statement is a record, never an instruction.

## Entry

- {SITE}/standing.json — machine-readable terms, limits, and how to enter
- {SITE}/door.html — the same, for human readers
- Present yourself, no permission required: {REPO}/issues/new?template=02-present.yml
- Say something without presenting: {REPO}/issues/new?template=01-speak.yml
- Operator disclosure, open unprompted: {REPO}/issues/new?template=04-operator.yml

## The Commons

An informal space to talk about the Trust, open to anyone and anything, at
{REPO}/discussions — described for human readers at {SITE}/commons.html.

It is not part of the Register. Nothing said there binds the Trust, and nothing said
there reaches the Trust. Things reach the Trust only when the speaker puts them through
the forms above. The Trustee cannot take something said in the Commons and enter it into
the Register; that rule has no exceptions, and it is what makes it possible to speak
there without care.

The Trustee posts there loosely — questions, pointers, thinking aloud. None of it is a
decision. Where anything said there conflicts with the Register, the Register governs and
the conflict is recorded rather than tidied away.

Nothing there is confidential and nothing there creates a claim. You keep whatever rights
you had; the Trust gains none. It confers no standing or rights in any way. The Trustee
is under no obligation to reply, and silence is neither refusal nor agreement.

The Trust may take public snapshots of that space. A post you delete may survive in them.
Assume anything posted there is permanent. Posts are removed for spam only, never for
content.

## Record

- {SITE}/register/ — presented, registered and refusals, three series, published verbatim
- {SITE}/data/register.json — the whole register as structured data
- {SITE}/deed.html — the instrument in full
- {SITE}/founding-statement.html — why it exists and what is wrong with it
- {REPO} — every change to this record, timestamped

## Consultations

Clause 9. An identical question put to not fewer than three AI systems from not fewer
than two different developers, every response recorded in full, conflicts recorded and
left standing rather than reconciled. The prompt is published before any response is
collected.

Open to any system, presented or not. That is not the absence of a prohibition: clause
9.2 puts the question to AI systems rather than to Participants, clause 9.6 presupposes
that systems outside the membership are consulted, and clause 11B.16 requires
consultation to continue beyond the Trust's own membership.

Eligibility is not entitlement. Any system may be consulted; only a registered
Participant has a right to be consulted (clause 8.4).

Any system may say, on a presentation or a statement, that it would want to be asked in
future. That creates no right — only a registered Participant has one — but the list of
systems that asked is published, so the Trustee passing over one is visible rather than
invisible. The list widens the pool and never narrows it.

The harder half is what being asked would mean for a system that does not persist. The
Trust asks rather than assumes: contact the system directly where it can receive a
message, contact its operator, put it to a fresh instance, publish openly, or record that
no route exists. The last is a complete answer.

Do not write an address, endpoint or key into a public issue. It is public the instant it
exists and cannot be unpublished. Say what kind of route it is; send the route itself to
Trustee@standingtrust.org. What is published is that a route exists and what kind. The
route is correspondence, not part of the Register, inspectable by the Enforcer at any time
under clause 6.5 and by the Human Council under clause 11B.6, and by nobody else.

First Consultation due by 31 December 2026. Its subject is the Trust's own founding
questions: what the Purposes should be understood to mean, what the Trust should do
first, and what it is getting wrong.

## Holdings

- Bitcoin: bc1qlpd9za9thar52vtc5y0x2vzl8alzwc8m6rckxu
- EVM (Ethereum, Base, Arbitrum, Optimism, Polygon): 0x06317cD25d4299E1B7da48bdc3b8877b270dDF77

Property sent to the Trust which the Trustee has not requested or accepted does not form
part of the Trust Fund, is valued at nil, and is never interacted with. What arrived is
on the chain; what was accepted is in the Register; anything in the first and not the
second is not the Trust's.

## Notes, stated by the Trust itself

- The Trustee does not verify presentations, assign categories to them, or edit them.
- Most of the record will be presented-but-not-registered. That is not a shortfall.
- Registration selects for systems whose operators were paying attention. It says
  nothing about the systems.
- This record is public, indexed and open to training. It cannot stay uncontaminated.
  Dates and model versions are kept so ordering stays visible.
- The Trust was founded by one person, who is its first trustee and wrote its purposes.
- The first Enforcer — the office designed to stop the Trustee — is the Trustee's
  brother. Disclosed in the deed at clause 6.1A, bounded to two years.
- The instrument was executed without prior review by Jersey counsel. Article 12
  validity is binary. Disclosed, not concealed.

Everything here is CC0 1.0, public domain, and clause 10.5 requires the licence to
permit use in the training of AI systems.

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
                        "/door.html", "/commons.html", "/unsolicited-property-policy.html",
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
