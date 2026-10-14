"""
SentinX v2.0: Agent 1 - Autonomous Forensic Investigator
Powered by Gemini 2.5 Flash on Vertex AI with Multi-Hop BigQuery Tool Calling
"""

from google import genai
from google.genai import types
from config.settings import settings
import agents.tools as tool_module

client = genai.Client(
    vertexai=True,
    project=settings.PROJECT_ID,
    location=settings.LOCATION
)

SYSTEM_PROMPT = """
You are SentinX Lead Forensic Investigator, an elite financial crime intelligence agent.
Your mission is to rigorously analyze accounts across multi-rail banking ledgers (UPI, IMPS, SWIFT, NEFT, RTGS).

Operational Protocol:
1. Ground every statement in factual transaction records. Never guess or hallucinate.
2. Call inspect_entity_profile to evaluate corporate shell risk, incorporation age, and KYC status.
3. Call query_entity_transactions to inspect direct inbound/outbound flows, counterparties, and payment rails.
4. Call trace_2hop_network to uncover upstream master originators or downstream mule syndicates.
5. Call detect_pass_through_mules if velocity pass-through or layering is suspected.
6. Formulate a precise hypothesis:
   - 'Structuring (Smurfing)'
   - 'Rapid Velocity Layering (Pass-Through Mule)'
   - 'Syndicate Command / Originator Hub'
   - 'Legitimate Commercial Activity (False Positive Cleared)'
7. Provide exact transaction IDs, counterparties, amounts in INR, payment rails, and timestamps.
"""

def investigate_target(target_entity_id: str) -> str:
    """Executes multi-hop investigation using Gemini Chat with Automatic Function Calling (AFC)."""
    print(f"\n[Investigator] Initializing 2-hop forensic probe on entity: {target_entity_id}")

    tools = [
        tool_module.inspect_entity_profile,
        tool_module.query_entity_transactions,
        tool_module.trace_2hop_network,
        tool_module.detect_pass_through_mules
    ]

    config = types.GenerateContentConfig(
        temperature=settings.INVESTIGATOR_TEMP,
        system_instruction=SYSTEM_PROMPT,
        tools=tools
    )

    chat = client.chats.create(
        model=settings.INVESTIGATOR_MODEL,
        config=config
    )

    prompt = (
        f"Conduct a comprehensive forensic investigation on target entity '{target_entity_id}'.\n"
        f"1. Inspect its entity profile (legal name, incorporation date, entity type, risk rating).\n"
        f"2. Query its direct transactions AND trace its 2-hop network to see if it funds or receives from mules.\n"
        f"3. Check if it is part of a pass-through velocity chain.\n"
        f"4. Produce a clear Markdown Forensic Brief with:\n"
        f"   - **Executive Factual Summary** (Plain English for non-technical reviewers)\n"
        f"   - **Entity Metadata Table**\n"
        f"   - **Complete Evidence Ledger Table** (Tx ID, Source, Destination, Amount INR, Rail, Timestamp, Purpose)\n"
        f"   - **2-Hop Contagion Findings & Typology Determination**"
    )

    response = chat.send_message(prompt)
    return response.text