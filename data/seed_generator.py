"""
SentinX: AML Forensic Synthetic Ledger Generator
Generates realistic multi-rail transaction topologies (UPI, IMPS, SWIFT)
with embedded typologies: Smurfing, Rapid Pass-Through Mules, and Round-Tripping.
"""

import uuid
import random
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import pandas as pd
from google.cloud import bigquery
from config.settings import settings

def generate_aml_graph(num_clean_records: int = 500):
    entities = []
    transactions = []
    base_time = datetime.now(timezone.utc) - timedelta(days=5)

    # 1. Generate Clean Entities & Baseline Traffic
    clean_ids = [f"ACC_{uuid.uuid4().hex[:8]}" for _ in range(50)]
    for eid in clean_ids:
        entities.append({
            "entity_id": eid,
            "legal_name": f"Retail User {eid[-4:]}",
            "jurisdiction": "IND",
            "entity_type": "INDIVIDUAL",
            "incorporation_date": None,
            "risk_rating": "LOW",
            "created_at": base_time - timedelta(days=120)
        })

    for _ in range(num_clean_records):
        src, dst = random.sample(clean_ids, 2)
        transactions.append({
            "transaction_id": f"TX_{uuid.uuid4().hex[:10]}",
            "source_entity_id": src,
            "destination_entity_id": dst,
            "amount": Decimal(str(round(random.uniform(500, 25000), 2))),
            "currency": "INR",
            "rail_type": random.choice(["UPI", "IMPS", "NEFT"]),
            "transaction_timestamp": base_time + timedelta(minutes=random.randint(0, 5000)),
            "declared_purpose": random.choice(["P2P Transfer", "Merchant Pay", "Utility Bill"]),
            "is_structuring_flag": False
        })

    # =========================================================================
    # TYPOLOGY A: Smurfing / Threshold Structuring (Evading ₹10 Lakhs ceiling)
    # 5 Mule accounts sending sub-threshold funds into 1 consolidation account
    # =========================================================================
    consolidation_acc = "ACC_SMURF_CENTRAL_01"
    entities.append({
        "entity_id": consolidation_acc,
        "legal_name": "Apex Holdings Ltd",
        "jurisdiction": "IND",
        "entity_type": "SHELL_CORP",
        "incorporation_date": (base_time - timedelta(days=15)).date(),
        "risk_rating": "HIGH",
        "created_at": base_time - timedelta(days=15)
    })

    smurf_runners = [f"ACC_MULE_RUNNER_{i}" for i in range(1, 6)]
    for i, runner in enumerate(smurf_runners):
        entities.append({
            "entity_id": runner,
            "legal_name": f"Mule Runner {i}",
            "jurisdiction": "IND",
            "entity_type": "INDIVIDUAL",
            "incorporation_date": None,
            "risk_rating": "MEDIUM",
            "created_at": base_time - timedelta(days=30)
        })
        transactions.append({
            "transaction_id": f"TX_SMURF_{i}",
            "source_entity_id": runner,
            "destination_entity_id": consolidation_acc,
            "amount": Decimal(str(round(random.uniform(920000, 980000), 2))),
            "currency": "INR",
            "rail_type": "IMPS",
            "transaction_timestamp": base_time + timedelta(hours=i * 2),
            "declared_purpose": "Consulting Fee",
            "is_structuring_flag": True
        })

    # =========================================================================
    # TYPOLOGY B: Rapid Pass-Through Mule Ring (Zero-Balance Dwell)
    # Originator -> Mule -> Foreign Destination in < 15 minutes
    # =========================================================================
    mule_node = "ACC_RAPID_MULE_88"
    entities.append({
        "entity_id": mule_node,
        "legal_name": "Kavitha Logistics (Sole Prop)",
        "jurisdiction": "IND",
        "entity_type": "INDIVIDUAL",
        "incorporation_date": None,
        "risk_rating": "HIGH",
        "created_at": base_time - timedelta(days=10)
    })

    t_in = base_time + timedelta(hours=12)
    transactions.append({
        "transaction_id": "TX_VELOCITY_IN_01",
        "source_entity_id": "ACC_ORIGINATOR_X",
        "destination_entity_id": mule_node,
        "amount": Decimal("2500000.00"),
        "currency": "INR",
        "rail_type": "IMPS",
        "transaction_timestamp": t_in,
        "declared_purpose": "Business Advance",
        "is_structuring_flag": True
    })

    transactions.append({
        "transaction_id": "TX_VELOCITY_OUT_01",
        "source_entity_id": mule_node,
        "destination_entity_id": "ACC_OFFSHORE_SGP_09",
        "amount": Decimal("2450000.00"),
        "currency": "INR",
        "rail_type": "SWIFT",
        "transaction_timestamp": t_in + timedelta(minutes=12),
        "declared_purpose": "Software Export Settlement",
        "is_structuring_flag": True
    })

    return pd.DataFrame(entities), pd.DataFrame(transactions)

def seed_to_bigquery():
    print(f"Connecting to BigQuery project: {settings.PROJECT_ID}...")
    client = bigquery.Client(project=settings.PROJECT_ID)
    entities_df, tx_df = generate_aml_graph()

    # Load entities (WRITE_TRUNCATE ensures clean re-runs)
    table_entities = f"{settings.PROJECT_ID}.{settings.BQ_DATASET}.entities"
    job_config_ent = bigquery.LoadJobConfig(write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE)
    client.load_table_from_dataframe(entities_df, table_entities, job_config=job_config_ent).result()
    print(f"Successfully loaded {len(entities_df)} records into {table_entities}")

    # Load transactions (WRITE_TRUNCATE ensures clean re-runs)
    table_tx = f"{settings.PROJECT_ID}.{settings.BQ_DATASET}.transactions"
    job_config_tx = bigquery.LoadJobConfig(write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE)
    client.load_table_from_dataframe(tx_df, table_tx, job_config=job_config_tx).result()
    print(f"Successfully loaded {len(tx_df)} records into {table_tx}")

if __name__ == "__main__":
    seed_to_bigquery()