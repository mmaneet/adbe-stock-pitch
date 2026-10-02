#!/usr/bin/env python3
"""Parse ADBE earnings-call transcripts (5 source formats) into uniform turns,
extract analyst questions, classify topics, compute fear index + vocab counts.
Writes to research/ws4_call_nlp/data/.  No network access.
"""
import re, json, os, csv, random, shutil, sys
from collections import Counter, defaultdict

RAW = "/tmp/claude-0/-home-user-adbe-stock-pitch/434e9d74-e598-592e-aa01-e9e6b55767df/scratchpad/raw"
OUT = "/home/user/adbe-stock-pitch/research/ws4_call_nlp/data"
os.makedirs(OUT + "/transcripts", exist_ok=True)

MGMT_SURNAMES = ["Narayen", "Wadhwani", "Chakravarthy", "Durn", "Vaas", "Day", "Clark", "Garfield"]
STOP_NAMES = set("""Adobe Cloud Creative Acrobat Firefly Express Digital Document Experience GenStudio Photoshop
Premiere Lightroom Summit MAX AI ARR FY Services Pro Reader Workfront Marketo Note Presentation Operator
Instructions Media Enterprise Platform Sensei Stock Frame Illustrator Journey Optimizer Assistant Analytics
Target Commerce Content Supply Chain Brand Concierge Semrush Figma Canva Google OpenAI Microsoft Amazon
Thank Thanks Great Okay Yes Yeah Q1 Q2 Q3 Q4 Q&A Question Answer Follow Up Newsletter Browsing Guarantee Reports Premium Readership Ad-Free Money-Back Bonus Lifetime Game-Changing Quarterly""".split())

CALLS = [
    # call_id, date, fiscal label, source file, format
    ("FY23_Q1", "2023-03-15", "A"),
    ("FY23_Q2", "2023-06-15", "A"),
    ("FY23_Q3", "2023-09-14", "A"),
    ("FY23_Q4", "2023-12-13", "A"),
    ("FY24_Q1", "2024-03-14", "A"),
    ("FY24_Q2", "2024-06-13", "A"),
    ("FY24_Q3", "2024-09-12", "B1"),
    ("FY24_Q4", "2024-12-11", "B1"),
    ("FY25_Q1", "2025-03-12", "B1"),
    ("FY25_Q3", "2025-09-11", "D"),
    ("FY25_Q4", "2025-12-10", "E"),
    ("FY26_Q1", "2026-03-12", "B2"),
    ("FY26_Q2", "2026-06-11", "D"),
]
SRC_FILE = {"FY25_Q3": "FY25_Q3_citi.txt", "FY26_Q2": "FY26_Q2_citi.txt", "FY25_Q4": "lseg_16547194.json"}


def role_of(name, firm="", title=""):
    n = name.strip()
    if n.lower().startswith("operator"):
        return "operator"
    if "Adobe" in firm or any(s in n for s in MGMT_SURNAMES):
        return "mgmt"
    if title and "Analyst" in title:
        return "analyst"
    return "analyst"


# ---------------- Format A: S&P CapIQ style (vectorsearch repo) ----------------
def parse_A(text):
    lines = [l.rstrip("\n") for l in text.split("\n")]
    # header participants
    hdr = {}
    try:
        i0 = lines.index("Event Transcript")
    except ValueError:
        i0 = 0
    for l in lines[:i0]:
        if " · " in l:
            before = l.split(" · ")[0]
            hdr[re.sub(r"\s+", "", before)] = before
    turns = []
    section = "prepared"
    cur = None
    for l in lines[i0 + 1:]:
        s = l.strip()
        if not s:
            continue
        if s == "Prepared Remarks":
            section = "prepared"; continue
        if s in ("Question and Answer", "Questions and Answers"):
            section = "qa"; continue
        if s == "Operator":
            cur = {"section": section, "speaker": "Operator", "firm": "", "role": "operator", "text": []}
            turns.append(cur); continue
        if " · " in s and len(s) < 260:
            before = s.split(" · ")[0]
            key = re.sub(r"\s+", "", before)
            name, firm = before, ""
            if key in hdr:
                h = hdr[key]
                # find the first char position where body (no space) differs from header
                pos = None
                for k, ch in enumerate(h):
                    if k >= len(before) or before[k] != ch:
                        pos = k; break
                if pos is not None:
                    name, firm = h[:pos].strip(), h[pos:].strip()
            cur = {"section": section, "speaker": name, "firm": firm, "role": role_of(name, firm), "text": []}
            turns.append(cur); continue
        if cur is not None:
            cur["text"].append(s)
    return turns


# ---------------- Format B1: Fool-like with "--" title lines (Ngafney 2024/early-2025) ----------------
def parse_B1(text):
    lines = [l.rstrip("\n") for l in text.split("\n")]
    turns, section, cur = [], "prepared", None
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if not s:
            i += 1; continue
        if s.startswith("Questions & Answers") or s.startswith("Questions and Answers"):
            section = "qa"; i += 1; continue
        if i + 2 < len(lines) and lines[i + 1].strip() == "--":
            name, title = s, lines[i + 2].strip()
            cur = {"section": section, "speaker": name, "firm": "", "role": role_of(name, "", title), "text": []}
            if cur["role"] == "analyst" and "Analyst" not in title and any(x in title for x in ["President", "Officer", "CEO", "CFO", "Investor"]):
                cur["role"] = "mgmt"
            turns.append(cur); i += 3; continue
        if s == "Operator":
            cur = {"section": section, "speaker": "Operator", "firm": "", "role": "operator", "text": []}
            turns.append(cur); i += 1; continue
        if cur is not None:
            cur["text"].append(s)
        i += 1
    return turns


# ---------------- Format B2: "Name:" line style (Ngafney late-2025/2026) ----------------
def parse_B2(text):
    lines = [l.rstrip("\n") for l in text.split("\n")]
    turns, cur = [], None
    for l in lines:
        s = l.strip()
        if not s or s == "Full Conference Call Transcript":
            continue
        m = re.match(r"^([A-Z][A-Za-z\.' -]{2,40}):$", s)
        if m:
            name = m.group(1)
            cur = {"section": "prepared", "speaker": name, "firm": "", "role": role_of(name), "text": []}
            turns.append(cur); continue
        if cur is not None:
            cur["text"].append(s)
    mark_qa_by_operator(turns)
    return turns


def mark_qa_by_operator(turns):
    """Switch to Q&A at the first operator turn (after >=2 mgmt turns) whose text mentions 'question'."""
    seen_mgmt, qa = 0, False
    for i, t in enumerate(turns):
        if t["role"] == "mgmt":
            seen_mgmt += 1
        txt = " ".join(t["text"]).lower()
        if (not qa) and t["role"] == "operator" and ("question" in txt or "instructions" in txt) and "welcome" not in txt:
            qa = True
        t["section"] = "qa" if qa else "prepared"


# ---------------- Format D: Insider Monkey one-line "Name: text" (citibank-arp repo) ----------------
def parse_D(text):
    body = text.split("=== EARNINGS CALL TRANSCRIPT ===", 1)[1]
    j = body.find("Operator: ")
    body = body[j:]
    pat = re.compile(r"(?:(?<=\s)|^)((?:[A-Z]\.|[A-Z][a-zA-Z'\-]+)(?: (?:[A-Z]\.|[A-Z][a-zA-Z'\-]+)){0,3}): ")
    body = re.sub(r"[^\.]*?(?:Premium Readership|Ad-Free|Money-Back|Insider Monkey|Newsletter|Unlock Now|\$9\.99|Bonus Report|Lifetime Price)[^\.]*\.", " ", body)
    cands = Counter(m.group(1) for m in pat.finditer(body))
    # analyst names introduced by operator
    intro = set()
    for m in re.finditer(r"(?:from|is from|comes from) (?:the line of )?([A-Z][\w\.'\-]+(?: [A-Z][\w\.'\-]+){0,3}) (?:with|at|from|of) ", body):
        intro.add(m.group(1))
    intro_surnames = {x.split()[-1] for x in intro}
    valid = set()
    for n, c in cands.items():
        toks = n.split()
        if n == "Operator":
            valid.add(n); continue
        if any(t in STOP_NAMES for t in toks):
            continue
        if any(s in n for s in MGMT_SURNAMES) or n in intro or c >= 2 or toks[-1] in intro_surnames:
            valid.add(n)
    turns, cur = [], None
    pos = 0
    prev_name = None
    for m in pat.finditer(body):
        n = m.group(1)
        ok = n in valid or (prev_name == "Operator" and not any(t in STOP_NAMES for t in n.split()) and 1 <= len(n.split()) <= 3)
        if not ok:
            continue
        prev_name = n
        if cur is not None:
            cur["text"].append(body[pos:m.start()].strip())
        cur = {"section": "prepared", "speaker": n, "firm": "", "role": role_of(n), "text": []}
        turns.append(cur)
        pos = m.end()
    if cur is not None:
        cur["text"].append(body[pos:].strip())
    mark_qa_by_operator(turns)
    return turns


# ---------------- Format E: LSEG JSON ----------------
def parse_E(text):
    d = json.loads(text)
    sp = d["transcript"]["speakers"]
    turns = []
    for sec in d["transcript"]["episode"]["sections"]:
        section = "qa" if sec["name"] == "q-and-a" else "prepared"
        for t in sec["turns"]:
            s = sp.get(t["speaker_id"], {})
            name = ((s.get("first_name") or "") + " " + (s.get("last_name") or "")).strip() or t["speaker_id"]
            firm = s.get("company_name", "") or ""
            txt = " ".join(seg["text"] for seg in t["segments"])
            turns.append({"section": section, "speaker": "Operator" if t["speaker_id"] == "operator" else name,
                          "firm": firm, "role": role_of(name if t["speaker_id"] != "operator" else "Operator", firm),
                          "text": [txt]})
    return turns


PARSERS = {"A": parse_A, "B1": parse_B1, "B2": parse_B2, "D": parse_D, "E": parse_E}

# ---------------- Topic rubric ----------------
RUBRIC = {
    "ai_disruption_competition": r"\b(disrupt\w*|competit\w*|canva|openai|chatgpt|gpt|sora|midjourney|veo|gemini|nano banana|imagen|moat|commoditi\w*|displac\w*|cannibal\w*|threat\w*|figma|runway|open[- ]source|lose share|share loss|take share|substitut\w*|existential|deflation\w*|replace\w*|obsolete|frontier model|third[- ]party model\w*|partner model\w*|best model\w*|who wins|hyperscaler\w*|big tech|ad platform\w*)\b",
    "seats_pricing_retention": r"\b(seat|seats|per[- ]user|per[- ]seat|price|prices|pricing|price increase\w*|net retention|nrr|churn|retention|subscriber\w*|arpu|tier|tiers|freemium|conversion|convert\w*|downgrade\w*|line optimization\w*|net new arr|digital media arr|creative arr|arr growth|arr guide\w*|mau|monthly active|user growth|new users|paid subscri\w*|discount\w*|packag\w*|bundle\w*|upsell|cross-sell|renewal\w*)\b",
    "ai_monetization": r"\b(firefly|generative credit\w*|credit pack\w*|credits?|ai[- ]first|ai[- ]influenced|firefly services|genstudio|ai assistant|consumption|usage[- ]based|monetiz\w*|generations|custom model\w*|book of business|agentic|agents?|ai revenue|ai arr|video model\w*|llm optimizer|brand concierge|foundry|content supply chain|ai (?:product\w*|offering\w*))\b",
    "digital_experience": r"\b(digital experience|dx|aep|experience platform|experience cloud|enterprise\w*|workfront|marketo|journey optimizer|real[- ]time cdp|semrush|customer experience orchestration|cxo|agenc(?:y|ies)|marketing|marketer\w*|cmo\w*)\b",
    "margins_ai_costs": r"\b(margin\w*|opex|operating expense\w*|cost\w*|gpu\w*|compute|capex|inference|investment level\w*|headcount|hiring|efficien\w*|cash flow|buyback\w*|repurchase\w*|capital allocation|tax|profitab\w*|operating income)\b",
    "leadership": r"\b(ceo|cfo|succession|transition\w*|retire\w*|search|board|leadership|reorg\w*|org (?:structure|change)\w*|leaving|departure|successor|interim)\b",
    "macro_other": r"\b(macro\w*|demand environment|linearity|fx|currency|guidance|guide|outlook|seasonal\w*|rpo|crpo|billings|bookings|regulat\w*|doj|ftc|antitrust|termination fee|tariff\w*|recession|budget\w*|sales cycle\w*|deferred revenue|cash|international|geograph\w*|europe|asia|japan|smb|mid-market)\b",
}
TIE_ORDER = ["leadership", "ai_disruption_competition", "seats_pricing_retention", "ai_monetization",
             "margins_ai_costs", "digital_experience", "macro_other"]
STRICT_FEAR = {"ai_disruption_competition", "seats_pricing_retention"}
BROAD_EXTRA = r"\b(net new arr|digital media arr|arr growth|arr guide\w*|arr target\w*|deceleration|decelerat\w*|growth algorithm|growth rate|slow\w*)\b"


def classify(q):
    ql = q.lower()
    hits = {k: len(set(re.findall(v, ql))) for k, v in RUBRIC.items()}
    # leadership only if explicit personnel terms + no stronger product signal
    best = max(hits.values())
    if best == 0:
        return "macro_other", hits
    cands = [k for k in TIE_ORDER if hits[k] == best]
    return cands[0], hits


SEAT_VOCAB = [r"\bseat\b", r"\bseats\b", r"\bper user\b", r"\blicense\b", r"\blicenses\b", r"\bsubscriber\b", r"\bsubscribers\b"]
USAGE_VOCAB = [r"\bcredit\b", r"\bcredits\b", r"\bconsumption\b", r"\busage\b", r"\bgenerations\b", r"\bfirefly services\b", r"\bapis?\b", r"\boutcome\b", r"\boutcomes\b"]
FIRST_TERMS = {"generative credits": r"generative credits?", "credit packs": r"credit packs?", "Firefly Services": r"firefly services",
               "AI-first ARR": r"ai[- ]first (?:arr|book of business|standalone|ending arr)", "AI-influenced ARR": r"ai[- ]influenced", "consumption (any sense)": r"\bconsumption\b", "consumption (pricing sense)": r"consumption[- ]based|consumption model|credit consumption|consumption of (?:credits|generative)|consume (?:more )?(?:generative )?credits",
               "usage-based": r"usage[- ]based", "Firefly app": r"firefly (?:app|application|web app)", "GenStudio": r"genstudio",
               "freemium": r"freemium", "AI book of business": r"(?:ai|firefly|generative|new)[^.]{0,40}book of business", "Creative Cloud Pro": r"creative cloud pro\b",
               "premium tier(s)": r"premium tiers?", "Acrobat AI Assistant": r"ai assistant", "MAU": r"\bmau\b|monthly active users?",
               "Firefly credit": r"firefly credits?|credits? (?:per|a) month", "outcome-based": r"outcome[- ]based|pay for outcomes?"}


def main():
    all_turns, questions, fear_rows, vocab_rows, first_rows, headline_rows = [], [], [], [], [], []
    first_seen = {}
    for cid, date, fmt in CALLS:
        fn = SRC_FILE.get(cid, cid + ".txt")
        raw = open(os.path.join(RAW, fn), encoding="utf-8", errors="replace").read()
        turns = PARSERS[fmt](raw)
        for t in turns:
            t["text"] = " ".join(x for x in t["text"] if x).strip()
            t["call"] = cid; t["date"] = date
        # save a clean copy of the transcript in uniform format
        with open(os.path.join(OUT, "transcripts", f"{cid}.txt"), "w") as f:
            f.write(f"# {cid} | call date {date} | source file {fn} | format {fmt}\n")
            for t in turns:
                f.write(f"\n[{t['section'].upper()}] {t['speaker']} ({t['role']}{', ' + t['firm'] if t['firm'] else ''}):\n{t['text']}\n")
        all_turns.extend(turns)
        # analyst questions: analyst turns in qa section
        qa = [t for t in turns if t["section"] == "qa"]
        last_intro = ""
        qn = 0
        for k, t in enumerate(qa):
            if t["role"] == "operator":
                last_intro = t["text"]; continue
            if t["role"] != "analyst":
                continue
            words = len(t["text"].split())
            if words < 8 or ("?" not in t["text"] and words < 25):
                continue
            # merge with immediately-preceding analyst turn of same speaker (no mgmt in between)
            if questions and questions[-1]["call"] == cid and questions[-1]["speaker"] == t["speaker"] and k > 0 and qa[k - 1]["role"] == "analyst":
                questions[-1]["question_text"] += " " + t["text"]; continue
            qn += 1
            firm = t["firm"]
            if not firm:
                m = re.search(r"(?:from|is from|comes from) (?:the line of )?(?:[A-Z][\w\.'\-]+(?: [A-Z][\w\.'\-]+){0,3}) (?:with|at|from|of) ([A-Z][\w&\.' ]+?)(?:\.|,|$| Please| Your)", last_intro)
                if m: firm = m.group(1).strip()
                else:
                    m = re.search(r"(?:[A-Z][\w\.'\-]+ ){1,3}, ([A-Z][\w&\.' ]+)\.$", last_intro.strip())
                    if m: firm = m.group(1).strip()
            questions.append({"call": cid, "date": date, "q_no": qn, "speaker": t["speaker"], "firm": firm,
                              "question_text": t["text"], "operator_intro": last_intro[:160]})
        # vocab over mgmt text
        mg = " ".join(t["text"] for t in turns if t["role"] == "mgmt")
        mg_l = mg.lower()
        nwords = len(mg.split())
        seat = sum(len(re.findall(p, mg_l)) for p in SEAT_VOCAB)
        usage = sum(len(re.findall(p, mg_l)) for p in USAGE_VOCAB)
        detail = {p: len(re.findall(p, mg_l)) for p in SEAT_VOCAB + USAGE_VOCAB}
        vocab_rows.append({"call": cid, "date": date, "mgmt_words": nwords, "seat_hits": seat, "usage_hits": usage,
                           "seat_per_10k": round(seat / nwords * 1e4, 2), "usage_per_10k": round(usage / nwords * 1e4, 2),
                           "usage_minus_seat_per_10k": round((usage - seat) / nwords * 1e4, 2),
                           "detail": json.dumps({k.replace("\\b", ""): v for k, v in detail.items() if v})})
        for term, pat in FIRST_TERMS.items():
            n = len(re.findall(pat, mg_l))
            if n and term not in first_seen:
                first_seen[term] = cid
                m = re.search(pat, mg_l)
                ctx = mg[max(0, m.start() - 160): m.end() + 160].replace("\n", " ")
                first_rows.append({"term": term, "first_call": cid, "date": date, "mentions_in_call": n, "context": ctx})
        # headline / guidance candidate sentences (prepared remarks, mgmt) for manual verification
        prep = " ".join(t["text"] for t in turns if t["role"] == "mgmt")
        sents = re.split(r"(?<=[\.\!\?])\s+", prep)
        for s in sents:
            sl = s.lower()
            if ("non-gaap" in sl and ("earnings per share" in sl or "eps" in sl)) or re.search(r"revenue (?:of|was) \$\d", sl):
                headline_rows.append({"call": cid, "sentence": s[:400]})
    # classify
    for q in questions:
        topic, hits = classify(q["question_text"])
        q["topic_auto"] = topic
        q["hits"] = json.dumps(hits)
        q["broad_arr_growth_flag"] = int(bool(re.search(BROAD_EXTRA, q["question_text"].lower())))
        q["source"] = "full_transcript"
        q["coverage"] = "full"
    # fear index
    bycall = defaultdict(list)
    for q in questions:
        bycall[q["call"]].append(q)
    for cid, date, fmt in CALLS:
        qs = bycall[cid]
        n = len(qs)
        strict = sum(1 for q in qs if q["topic_auto"] in STRICT_FEAR)
        broad = sum(1 for q in qs if q["topic_auto"] in STRICT_FEAR or q["broad_arr_growth_flag"])
        tc = Counter(q["topic_auto"] for q in qs)
        fear_rows.append({"call": cid, "date": date, "n_questions": n, "n_fear_strict": strict, "n_fear_broad": broad,
                          "fear_index_strict": round(strict / n, 3) if n else "", "fear_index_broad": round(broad / n, 3) if n else "",
                          "n_ai_disruption": tc["ai_disruption_competition"], "n_seats_pricing": tc["seats_pricing_retention"],
                          "n_ai_monetization": tc["ai_monetization"], "n_dx": tc["digital_experience"], "n_margins": tc["margins_ai_costs"],
                          "n_leadership": tc["leadership"], "n_macro_other": tc["macro_other"],
                          "coverage": "full transcript", "confidence": "medium"})
    # write
    def w(name, rows):
        if not rows: return
        with open(os.path.join(OUT, name), "w", newline="") as f:
            wr = csv.DictWriter(f, fieldnames=list(rows[0].keys())); wr.writeheader(); wr.writerows(rows)
    w("turns.csv", [{k: t[k] for k in ["call", "date", "section", "speaker", "role", "firm", "text"]} for t in all_turns])
    w("analyst_questions_auto.csv", questions)
    w("fear_index_fulltext.csv", fear_rows)
    w("vocab_counts.csv", vocab_rows)
    w("usage_term_first_mentions.csv", first_rows)
    w("headline_guidance_candidates.csv", headline_rows)
    # diagnostics
    for cid, date, fmt in CALLS:
        ts = [t for t in all_turns if t["call"] == cid]
        an = [t["speaker"] + ("/" + t["firm"] if t["firm"] else "") for t in ts if t["role"] == "analyst" and t["section"] == "qa"]
        print(f"{cid} fmt={fmt} turns={len(ts)} prepared_mgmt_words={sum(len(t['text'].split()) for t in ts if t['section']=='prepared' and t['role']=='mgmt')} "
              f"qa_turns={sum(1 for t in ts if t['section']=='qa')} questions={len(bycall[cid])} analysts={sorted(set(an))}")
    print("fear:", [(r["call"], r["n_questions"], r["fear_index_strict"], r["fear_index_broad"]) for r in fear_rows])
    print("vocab:", [(r["call"], r["seat_per_10k"], r["usage_per_10k"]) for r in vocab_rows])
    print("first:", [(r["term"], r["first_call"]) for r in first_rows])


if __name__ == "__main__":
    main()
