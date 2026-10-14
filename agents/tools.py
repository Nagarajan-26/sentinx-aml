"""
SentinX v3.0: Multi-Hop Forensic BigQuery Toolkit (Lazy-Initialized for Instant Startup)
"""

import math
from typing import Dict, Any, List
from google.cloud import bigquery
from config.settings import settings

_bq_client = None

def get_bq_client() -> bigquery.Client:
    """Lazy singleton pattern so importing tools.py takes 0.00ms on app startup."""
    global _bq_client
    if _bq_client is None:
        _bq_client = bigquery.Client(project=settings.PROJECT_ID)
    return _bq_client

def _sanitize_val(v):
    if v is None:
        return None
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return None
    return str(v) if not isinstance(v, (int, float, bool, str)) else v

def _clean_records(df) -> List[Dict[str, Any]]:
    records = df.to_dict(orient="records")
    return [{k: _sanitize_val(v) for k, v in row.items()} for row in records]

def inspect_entity_profile(entity_id: str) -> Dict[str, Any]:
    """Retrieves KYC, corporate age, jurisdiction, and risk metadata for an account or entity ID."""
    query = f"""
        SELECT entity_id, legal_name, jurisdiction, entity_type, 
               SAFE_CAST(incorporation_date AS STRING) AS incorporation_date,
               DATE_DIFF(CURRENT_DATE(), incorporation_date, DAY) AS corporate_age_days,
               risk_rating, SAFE_CAST(created_at AS STRING) AS created_at
        FROM `{settings.PROJECT_ID}.{settings.BQ_DATASET}.entities`
        WHERE entity_id = @entity_id
        LIMIT 1
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("entity_id", "STRING", entity_id)]
    )
    df = get_bq_client().query(query, job_config=job_config).to_dataframe()
    records = _clean_records(df)
    if not records:
        return {"status": "NOT_FOUND", "entity_id": entity_id, "legal_name": entity_id, "entity_type": "EXTERNAL", "risk_rating": "MEDIUM"}
    return records[0]

def query_entity_transactions(entity_id: str, direction: str = "ALL", limit: int = 35) -> List[Dict[str, Any]]:
    """
    Queries direct (1-hop) inbound, outbound, or all ledger transactions for an entity.
    direction must be one of: 'INBOUND', 'OUTBOUND', 'ALL'.
    """
    if direction == "INBOUND":
        where_clause = "WHERE destination_entity_id = @entity_id"
    elif direction == "OUTBOUND":
        where_clause = "WHERE source_entity_id = @entity_id"
    else:
        where_clause = "WHERE source_entity_id = @entity_id OR destination_entity_id = @entity_id"

    query = f"""
        SELECT transaction_id, source_entity_id, destination_entity_id, 
               CAST(amount AS FLOAT64) AS amount, currency, rail_type,
               SAFE_CAST(transaction_timestamp AS STRING) AS transaction_timestamp,
               declared_purpose
        FROM `{settings.PROJECT_ID}.{settings.BQ_DATASET}.transactions`
        {where_clause}
        ORDER BY transaction_timestamp DESC
        LIMIT @limit
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("entity_id", "STRING", entity_id),
            bigquery.ScalarQueryParameter("limit", "INT64", limit)
        ]
    )
    df = get_bq_client().query(query, job_config=job_config).to_dataframe()
    return _clean_records(df)

def trace_2hop_network(entity_id: str, limit: int = 60) -> List[Dict[str, Any]]:
    """Traces 2-hop upstream and downstream financial contagion around target entity_id."""
    query = f"""
        WITH hop1_entities AS (
            SELECT DISTINCT source_entity_id AS connected_id
            FROM `{settings.PROJECT_ID}.{settings.BQ_DATASET}.transactions`
            WHERE destination_entity_id = @entity_id
            UNION DISTINCT
            SELECT DISTINCT destination_entity_id AS connected_id
            FROM `{settings.PROJECT_ID}.{settings.BQ_DATASET}.transactions`
            WHERE source_entity_id = @entity_id
            UNION DISTINCT
            SELECT @entity_id AS connected_id
        )
        SELECT DISTINCT t.transaction_id, t.source_entity_id, t.destination_entity_id,
               CAST(t.amount AS FLOAT64) AS amount, t.currency, t.rail_type,
               SAFE_CAST(t.transaction_timestamp AS STRING) AS transaction_timestamp,
               t.declared_purpose
        FROM `{settings.PROJECT_ID}.{settings.BQ_DATASET}.transactions` t
        WHERE t.source_entity_id IN (SELECT connected_id FROM hop1_entities)
           OR t.destination_entity_id IN (SELECT connected_id FROM hop1_entities)
        ORDER BY transaction_timestamp DESC
        LIMIT @limit
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("entity_id", "STRING", entity_id),
            bigquery.ScalarQueryParameter("limit", "INT64", limit)
        ]
    )
    df = get_bq_client().query(query, job_config=job_config).to_dataframe()
    return _clean_records(df)

def detect_pass_through_mules(min_retention_minutes: int = 60) -> List[Dict[str, Any]]:
    """Queries pre-computed telemetry view to identify intermediate accounts draining funds rapidly."""
    query = f"""
        SELECT originator, intermediate_mule, ultimate_beneficiary,
               CAST(inbound_amount AS FLOAT64) AS inbound_amount,
               CAST(outbound_amount AS FLOAT64) AS outbound_amount,
               retention_minutes
        FROM `{settings.PROJECT_ID}.{settings.BQ_DATASET}.v_rapid_pass_through`
        WHERE retention_minutes <= @min_minutes
        ORDER BY retention_minutes ASC
        LIMIT 10
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("min_minutes", "INT64", min_retention_minutes)]
    )
    df = get_bq_client().query(query, job_config=job_config).to_dataframe()
    return _clean_records(df)

def scan_portfolio_leaderboard() -> List[Dict[str, Any]]:
    """
    Aggregates all entities in the BigQuery ledger with their inbound/outbound counts,
    total volume, sub-10L structuring hits, and corporate age for portfolio-wide triage.
    """
    query = f"""
        WITH tx_summary AS (
            SELECT
                e.entity_id,
                e.legal_name,
                e.jurisdiction,
                e.entity_type,
                SAFE_CAST(e.incorporation_date AS STRING) AS incorporation_date,
                DATE_DIFF(CURRENT_DATE(), e.incorporation_date, DAY) AS corporate_age_days,
                e.risk_rating,
                COUNT(DISTINCT t_in.transaction_id) AS inbound_count,
                COALESCE(SUM(t_in.amount), 0) AS total_inbound_inr,
                COUNTIF(t_in.amount >= 900000 AND t_in.amount < 1000000) AS structuring_hits
            FROM `{settings.PROJECT_ID}.{settings.BQ_DATASET}.entities` e
            LEFT JOIN `{settings.PROJECT_ID}.{settings.BQ_DATASET}.transactions` t_in
                ON e.entity_id = t_in.destination_entity_id
            GROUP BY 1, 2, 3, 4, 5, 6, 7
        ),
        out_summary AS (
            SELECT
                source_entity_id AS entity_id,
                COUNT(DISTINCT transaction_id) AS outbound_count,
                COALESCE(SUM(amount), 0) AS total_outbound_inr
            FROM `{settings.PROJECT_ID}.{settings.BQ_DATASET}.transactions`
            GROUP BY 1
        )
        SELECT
            tx_summary.*,
            COALESCE(out_summary.outbound_count, 0) AS outbound_count,
            COALESCE(out_summary.total_outbound_inr, 0) AS total_outbound_inr
        FROM tx_summary
        LEFT JOIN out_summary USING (entity_id)
        ORDER BY risk_rating ASC, total_inbound_inr DESC
    """
    df = get_bq_client().query(query).to_dataframe()
    return _clean_records(df)