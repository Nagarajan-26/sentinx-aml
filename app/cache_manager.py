"""
SentinX v4.0: Triple-Layer FinOps Cache Engine with Provenance Timestamps & Reset Controls
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

CACHE_DIR = Path(__file__).resolve().parent.parent / ".cache"
CACHE_DIR.mkdir(exist_ok=True)

AUDIT_CACHE_FILE = CACHE_DIR / "sentinx_audit_cache.json"
LEDGER_CACHE_FILE = CACHE_DIR / "sentinx_ledger_cache.json"
CHAT_CACHE_FILE = CACHE_DIR / "sentinx_chat_cache.json"

def _now_str() -> str:
    return datetime.now().strftime("%d %b %Y, %I:%M:%S %p")

def _read_json(path: Path) -> Dict[str, Any]:
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def _write_json(path: Path, data: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# --- 1. BIGQUERY LEDGER CACHE ---
def get_cached_ledger(entity_id: str) -> Optional[Dict[str, Any]]:
    store = _read_json(LEDGER_CACHE_FILE)
    return store.get(entity_id)

def save_cached_ledger(entity_id: str, profile: dict, txs_1hop: list, txs_2hop: list) -> Dict[str, Any]:
    store = _read_json(LEDGER_CACHE_FILE)
    payload = {
        "profile": profile,
        "txs_1hop": txs_1hop,
        "txs_2hop": txs_2hop,
        "ledger_fetched_at": _now_str()
    }
    store[entity_id] = payload
    _write_json(LEDGER_CACHE_FILE, store)
    return payload

# --- 2. DUAL-AGENT AUDIT CACHE ---
def compute_ledger_signature(target_id: str, txs: list) -> str:
    tx_ids = sorted([f"{t.get('transaction_id')}:{t.get('amount')}" for t in txs])
    payload = f"{target_id}|{'|'.join(tx_ids)}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]

def load_disk_cache() -> Dict[str, Any]:
    return _read_json(AUDIT_CACHE_FILE)

def get_cached_audit(target_id: str, txs: list) -> Optional[Dict[str, Any]]:
    sig = compute_ledger_signature(target_id, txs)
    store = _read_json(AUDIT_CACHE_FILE)
    entry = store.get(target_id)
    if entry and entry.get("signature") == sig:
        return entry
    return None

def save_cached_audit(target_id: str, txs: list, investigator_brief: str, auditor_struct: dict) -> Dict[str, Any]:
    sig = compute_ledger_signature(target_id, txs)
    store = _read_json(AUDIT_CACHE_FILE)
    entry = {
        "target_id": target_id,
        "signature": sig,
        "investigator": investigator_brief,
        "auditor_struct": auditor_struct,
        "auditor": auditor_struct.get("detailed_markdown_report", ""),
        "estimated_tokens_saved": 5200,
        "audit_timestamp": _now_str()
    }
    store[target_id] = entry
    _write_json(AUDIT_CACHE_FILE, store)
    return entry

# --- 3. SENTI AI COPILOT CACHE ---
def get_cached_chat_reply(target_id: str, question: str) -> Optional[str]:
    key = hashlib.sha256(f"{target_id}|{question.strip().lower()}".encode("utf-8")).hexdigest()[:16]
    store = _read_json(CHAT_CACHE_FILE)
    return store.get(key)

def save_cached_chat_reply(target_id: str, question: str, reply: str) -> None:
    key = hashlib.sha256(f"{target_id}|{question.strip().lower()}".encode("utf-8")).hexdigest()[:16]
    store = _read_json(CHAT_CACHE_FILE)
    store[key] = reply
    _write_json(CHAT_CACHE_FILE, store)