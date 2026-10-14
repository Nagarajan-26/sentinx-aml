"""
SentinX v4.0: 1-Click Demo Cache Pre-Warmer
Run `python prewarm_cache.py` once before your demo to cache all 4 1-Hop & 2-Hop ledgers and Dual-Agent Audits to disk.
"""

from agents.tools import inspect_entity_profile, query_entity_transactions, trace_2hop_network
from agents.investigator import investigate_target
from agents.auditor import audit_case_structured
from app.cache_manager import save_cached_ledger, save_cached_audit, get_cached_audit

DEMO_TARGETS = [
    "ACC_SMURF_CENTRAL_01",
    "ACC_RAPID_MULE_88",
    "ACC_ORIGINATOR_X",
    "ACC_LEGIT_PAYROLL_01"
]

if __name__ == "__main__":
    print("=== SentinX v4.0 Demo Cache Pre-Warmer ===")
    for target in DEMO_TARGETS:
        print(f"\n[1/2] Caching 1-Hop & 2-Hop BigQuery Ledgers for {target}...")
        profile = inspect_entity_profile(target)
        txs_1hop = query_entity_transactions(target, direction="ALL", limit=35)
        txs_2hop = trace_2hop_network(target, limit=60)
        save_cached_ledger(target, profile, txs_1hop, txs_2hop)

        if get_cached_audit(target, txs_1hop):
            print(f"[2/2] Audit already cached on disk for {target} — skipping LLM call.")
        else:
            print(f"[2/2] Running Dual-Agent Audit on {target} and saving to disk...")
            inv = investigate_target(target)
            aud = audit_case_structured(inv)
            save_cached_audit(target, txs_1hop, inv, aud)
            print(f"      -> Saved {target} (Risk Score: {aud.get('composite_risk_score')}/100)")

    print("\n✅ All 4 scenarios are now pre-warmed on disk! Launch `streamlit run app/main.py` for 0.01s instant responses.")