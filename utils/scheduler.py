from typing import List, Dict
from math import inf

_IMPORTANCE_WEIGHT = {"low": 0.5, "medium": 1.0, "high": 1.8}

def score_task(t: Dict) -> float:
    base = _IMPORTANCE_WEIGHT.get(t.get("importance", "medium"), 1.0)
    mins = t.get("estimated_minutes") or 60
    size_bonus = 60.0 / mins  # shorter tasks slightly favored
    return base + size_bonus

def prioritize(tasks: List[Dict]) -> List[Dict]:
    def key(t):
        has_due = 0 if t.get("due_ts") is not None else 1
        due_ts = t.get("due_ts", inf)
        # Sort primarily by due time ascending, then by score (desc), then mention order
        return (has_due, due_ts, -score_task(t), t.get("sequence", 0))
    return sorted(tasks, key=key)
