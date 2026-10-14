import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    # GCP Infrastructure Targets
    PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "project-f680f24a-c696-4201-847")
    LOCATION: str = os.getenv("GCP_LOCATION", "us-central1")
    BQ_DATASET: str = os.getenv("BQ_DATASET", "aml_forensics_ledger")
    GCS_BUCKET: str = os.getenv("GCS_BUCKET", "sentinx-regulatory-corpus")

    # Vertex AI Production Quota Models (Supported on billing credits)
    INVESTIGATOR_MODEL: str = "gemini-2.5-flash"
    AUDITOR_MODEL: str = "gemini-2.5-pro"

    # Engine Guardrails
    INVESTIGATOR_TEMP: float = 0.1
    AUDITOR_TEMP: float = 0.0
    MAX_AUDIT_ROUNDS: int = 3

settings = Settings()