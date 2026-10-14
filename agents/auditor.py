"""
SentinX v2.0: Agent 2 - Statutory Compliance Auditor & Senti AI Copilot
Uses Pydantic Structured Outputs on Vertex AI Gemini 2.5 Pro for zero-hallucination statutory grounding.
"""

import os
import json
from pydantic import BaseModel, Field
from typing import List
from google import genai
from google.genai import types
from config.settings import settings

client = genai.Client(
    vertexai=True,
    project=settings.PROJECT_ID,
    location=settings.LOCATION
)

REGULATION_PATH = os.path.join(os.path.dirname(__file__), "..", "regulations", "FATF_40_Recommendations.md")
with open(REGULATION_PATH, "r", encoding="utf-8") as f:
    REGULATORY_STANDARDS = f.read()

class StatutoryAuditStructured(BaseModel):
    audit_verdict: str = Field(
        description="Must be one of: 'AUDIT_APPROVED_SAR_REQUIRED' (if illicit) or 'AUDIT_CLEARED_FALSE_POSITIVE' (if legitimate commerce)"
    )
    composite_risk_score: int = Field(
        description="Numeric risk score from 0 to 100 based on typology severity, velocity, and shell indicators"
    )
    identified_typology: str = Field(
        description="Short clean typology name, e.g., 'Structuring (Smurfing)', 'Cross-Border Velocity Layering', 'Syndicate Originator', or 'Legitimate Corporate Payroll'"
    )
    recommended_action: str = Field(
        description="Immediate operational action, e.g., 'FREEZE ACCOUNT & FILE FIU-IND STR', 'ESCALATE MLAT TO MAS SINGAPORE', or 'CLEAR ALERT & WHITELIST ENTITY'"
    )
    executive_bluf: str = Field(
        description="2-to-3 sentence jargon-free summary written for a non-technical banking executive explaining exactly what happened in plain English and why it matters."
    )
    plain_english_analogy: str = Field(
        description="A vivid 1-sentence real-world analogy so any layperson immediately grasps the behavior."
    )
    fatf_citations: List[str] = Field(
        description="List of triggered or evaluated FATF Recommendations, e.g. ['FATF Rec 10: Structuring & CDD', 'FATF Rec 24: Shell Company Transparency']"
    )
    adversarial_defense_rebuttal: str = Field(
        description="What a defense lawyer or account holder would claim (e.g., 'Normal consulting income'), followed by the mathematical/forensic proof confirming or rebutting it."
    )
    detailed_markdown_report: str = Field(
        description="The full, formal multi-section Statutory Audit Report in rich Markdown suitable for official FIU regulatory filing."
    )

AUDITOR_SYSTEM_PROMPT = f"""
You are the SentinX Chief Statutory Compliance Auditor.
Your duty is to challenge, verify, and ground the Investigator Agent's findings against the international FATF regulatory corpus.

STATUTORY REGULATORY CORPUS (GROUND TRUTH):
{REGULATORY_STANDARDS}

CRITICAL OPERATING PRINCIPLES:
1. Zero Hallucination: Verify every transaction ID, rupee amount, and timestamp.
2. False-Positive Protection: If an account belongs to an established company conducting normal payroll (NEFT) or genuine B2B vendor payments (RTGS) with no structuring or rapid pass-through draining, you MUST issue 'AUDIT_CLEARED_FALSE_POSITIVE' and a low risk score (<15).
3. Executive Clarity: Ensure 'executive_bluf' and 'plain_english_analogy' are crystal clear for non-technical executives.
"""

def audit_case_structured(investigator_brief: str) -> dict:
    """Returns a structured dictionary containing both executive UI fields and the formal Markdown report."""
    print("\n[Auditor] Initiating structured statutory audit and grounding review...")

    config = types.GenerateContentConfig(
        temperature=settings.AUDITOR_TEMP,
        system_instruction=AUDITOR_SYSTEM_PROMPT,
        response_mime_type="application/json",
        response_schema=StatutoryAuditStructured,
        tools=None
    )

    prompt = (
        f"Audit and challenge the following Forensic Investigation Brief:\n\n"
        f"{investigator_brief}\n\n"
        f"Return the complete JSON matching the StatutoryAuditStructured schema."
    )

    response = client.models.generate_content(
        model=settings.AUDITOR_MODEL,
        contents=prompt,
        config=config
    )
    return json.loads(response.text)

def audit_case(investigator_brief: str) -> str:
    """Backwards-compatible wrapper returning the detailed Markdown report."""
    data = audit_case_structured(investigator_brief)
    return data["detailed_markdown_report"]

def ask_senti_ai(question: str, active_target: str, profile: dict, txs: list, inv_brief: str, aud_data: dict) -> str:
    """
    Live Context-Aware Senti AI Copilot.
    Answers arbitrary user/judge questions using the active entity's ledger and FATF rules.
    """
    context_prompt = f"""
    You are 'Senti AI', the friendly, razor-sharp AML Intelligence Copilot inside SentinX.
    Speak clearly, concisely, and helpfully so both non-technical business executives and senior compliance officers understand immediately.
    
    CURRENT ACTIVE TARGET: {active_target}
    ENTITY PROFILE: {json.dumps(profile, default=str)}
    RECENT TRANSACTIONS COUNT: {len(txs)}
    INVESTIGATOR BRIEF: {inv_brief or 'Not yet executed — use raw profile and transactions.'}
    AUDITOR VERDICT DATA: {json.dumps(aud_data, default=str) if aud_data else 'Not yet executed.'}
    
    FATF REFERENCE SUMMARY:
    - Rec 10: Customer Due Diligence & Structuring below ₹10 Lakh threshold.
    - Rec 16: Wire Transfer Travel Rule & Rapid Pass-Through Layering (<60 mins).
    - Rec 20: Mandatory STR/SAR filing to FIU-IND.
    - Rec 24/25: Beneficial Ownership & Shell Company (<30 days incorporation age) transparency.

    USER QUESTION: {question}
    """
    config = types.GenerateContentConfig(
        temperature=0.2,
        tools=None
    )
    resp = client.models.generate_content(
        model=settings.INVESTIGATOR_MODEL,
        contents=context_prompt,
        config=config
    )
    return resp.text