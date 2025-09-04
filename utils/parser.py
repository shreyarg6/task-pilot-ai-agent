import re
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import dateparser

try:
    import spacy
    _NLP = spacy.load("en_core_web_sm")
except Exception:
    _NLP = None


def _simple_split(text: str) -> List[str]:
    # split on newline, semicolon, comma, or the word "and"
    parts = re.split(r"(?:\band\b)|[,\n;]", text, flags=re.I)
    return [p.strip() for p in parts if p and p.strip()]


def _extract_due_ts(chunk: str) -> Optional[datetime]:
    s = chunk.lower().strip()

    # special phrases
    if "by midnight" in s or s.endswith("by 12am"):
        base = datetime.now()
        midnight = base.replace(hour=23, minute=59, second=0, microsecond=0)
        return midnight

    # "in X hours/minutes"
    m = re.search(r"\bin\s+(\d+)\s*(hour|hours|hr|hrs|minute|minutes|min|mins)\b", s)
    if m:
        n = int(m.group(1))
        unit = m.group(2)
        delta = timedelta(hours=n) if "hour" in unit else timedelta(minutes=n)
        return datetime.now() + delta

    # generic: today/tonight/tomorrow/at 5pm/by Friday etc.
    dt = dateparser.parse(
        s,
        settings={
            "PREFER_DATES_FROM": "future",
            "RELATIVE_BASE": datetime.now(),
            "RETURN_AS_TIMEZONE_AWARE": False,
        },
    )
    return dt


def _extract_minutes(chunk: str) -> Optional[int]:
    m = re.search(r"(\d+)\s*(min|mins|minutes)\b", chunk, flags=re.I)
    if m:
        return int(m.group(1))
    m = re.search(r"(\d+)\s*(h|hr|hrs|hour|hours)\b", chunk, flags=re.I)
    if m:
        return int(m.group(1)) * 60
    return None


def parse_tasks(text: str) -> List[Dict]:
    # sentence split: spaCy if available, otherwise our splitter
    if _NLP is not None:
        chunks = [s.text.strip() for s in _NLP(text).sents]
    else:
        chunks = _simple_split(text)

    tasks = []
    for i, ch in enumerate(chunks):
        if not ch:
            continue
        due_ts = _extract_due_ts(ch)
        due_str = due_ts.strftime("%Y-%m-%d %H:%M") if due_ts else None
        importance = "high" if any(k in ch.lower() for k in ["urgent", "asap", "today", "tonight", "by "]) else "medium"
        tasks.append(
            {
                "title": ch,
                "due_date": due_str,     # human friendly display
                "due_ts": due_ts.timestamp() if due_ts else None,  # for sorting
                "estimated_minutes": _extract_minutes(ch),
                "importance": importance,
                "sequence": i,           # fallback order = mention order
            }
        )
    return tasks
