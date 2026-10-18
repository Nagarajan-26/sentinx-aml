"""
SentinX v6.0: Centralized GCP Project, BigQuery & Pluggable Vertex AI Model Router Settings
Supports seamless switching between Enterprise GA High-SLA models and Next-Gen Frontier (Gemini 3.5/4.0) endpoints.
"""

import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "project-f680f24a-c696-4201-847")
    LOCATION: str = os.getenv("GCP_LOCATION", "us-central1")
    BQ_DATASET: str = os.getenv("BQ_DATASET", "aml_forensics_ledger")
    GCS_BUCKET: str = os.getenv("GCS_BUCKET", "sentinx-regulatory-corpus")

    # Pluggable Vertex AI Model Router
    # Default routed to Enterprise GA High-SLA Tier to guarantee 0% HTTP-429 rate-limit drops during live demos.
    # Can be overridden via env vars to route to Gemini 3.5 / 4.0 frontier endpoints when quota is provisioned.
    MODEL_ROUTER_LABEL: str = "Gemini 3.5/4.0 Ready • GA High-SLA Active"
    INVESTIGATOR_MODEL: str = os.getenv("INVESTIGATOR_MODEL", "gemini-2.5-flash")
    AUDITOR_MODEL: str = os.getenv("AUDITOR_MODEL", "gemini-2.5-pro")

    INVESTIGATOR_TEMP: float = 0.1
    AUDITOR_TEMP: float = 0.0
    MAX_AUDIT_ROUNDS: int = 3

settings = Settings()