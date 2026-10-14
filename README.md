<div align="center">

# 🛡️ SentinX v6.0
### Autonomous Multi-Rail AML Forensics & Statutory Grounding Platform

[![Google Cloud Vertex AI](https://img.shields.io/badge/Vertex_AI-Gemini_2.5_Flash_%2B_Pro-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)](https://cloud.google.com/vertex-ai)
[![Google BigQuery](https://img.shields.io/badge/BigQuery-2--Hop_Contagion_Graph-669DF6?style=for-the-badge&logo=googlebigquery&logoColor=white)](https://cloud.google.com/bigquery)
[![FATF Compliant](https://img.shields.io/badge/Compliance-FATF_40_Recommendations-059669?style=for-the-badge&logo=shield&logoColor=white)](https://www.fatf-gafi.org/)
[![FinOps Certified](https://img.shields.io/badge/FinOps-SHA--256_Zero--Token_Cache-D97706?style=for-the-badge&logo=lightning&logoColor=white)](#finops--institutional-roi-benchmarks)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Enterprise_Daylight_Cockpit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)

**Transforming 4.5-hour manual Anti-Money Laundering (AML) investigations into 3.2-second autonomous, zero-hallucination statutory audits.**

</div>

---

## 🚨 The Billion-Dollar Problem

Global financial institutions spend over **$200 Billion annually** on Financial Crime Compliance, yet less than 1% of illicit global financial flows are ever intercepted. Legacy rule-based AML systems fail across four critical dimensions:

1. **Multi-Rail Fragmentation:** Laundering syndicates split funds across instant domestic rails (**UPI, IMPS, NEFT, RTGS**) and cross-border correspondent rails (**SWIFT**) within minutes.
2. **1-Hop Blindness:** Traditional transaction monitoring only inspects direct counterparties (1-hop), completely missing **2-hop syndicate hubs** that seed smurf runners upstream.
3. **90%+ False-Positive Fatigue:** Legitimate businesses running high-volume payroll or vendor settlements trigger static threshold alerts, forcing compliance analysts to spend **4.5 hours per alert** manually querying SQL databases and drafting clearance memos.
4. **Unstructured AI Hallucination Risk:** Generic LLM wrappers summarize text without statutory grounding, making their outputs unusable for regulatory submission to the **Financial Intelligence Unit (FIU-IND)**.

---

## 🧠 The Solution: SentinX v6.0

**SentinX** is an enterprise-grade, **Dual-Agent Financial Crime Intelligence & Statutory Grounding Platform** built natively on **Google Cloud Vertex AI** and **BigQuery**. Instead of relying on a single prompt, SentinX separates **Forensic Fact-Gathering** from **Adversarial Statutory Auditing**:

* **🕵️ Agent 1 — Autonomous Forensic Investigator (`Gemini 2.5 Flash`):** Uses Vertex AI Automatic Function Calling (AFC) to execute parameterized BigQuery SQL tools, tracing 1-hop direct flows, 2-hop recursive syndicate contagion rings, corporate shell maturity, and pass-through retention velocity.
* **⚖️ Agent 2 — Statutory Compliance Challenger (`Gemini 2.5 Pro`):** Operates at `temperature=0.0` with a strict **Pydantic `response_schema`**. It challenges Agent 1's findings against the **FATF 40 Recommendations** (Recs 10, 16, 20, 24/25), plays **Devil's Advocate** to actively clear legitimate commercial activity (False-Positive Immunity), and outputs a calibrated **0–100 Composite Risk Score**.
* **✨ Senti AI Executive Copilot:** A context-grounded conversational assistant that translates dense financial and legal findings into plain, jargon-free English for banking executives and generates immediate freeze directives.

---

## 🏗️ System Architecture

~~~mermaid
flowchart TB
    subgraph DataLayer["1. Google Cloud Data & Graph Layer (BigQuery)"]
        BQ_ENT[("entities (KYC & Corporate Age)")]
        BQ_TX[("transactions (IMPS / SWIFT / NEFT / RTGS)")]
        BQ_VIEW[("v_rapid_pass_through (Velocity Telemetry View)")]
        BQ_CTE["2-Hop Recursive SQL CTE (Syndicate Contagion Tracer)"]
        BQ_ENT & BQ_TX --> BQ_CTE
        BQ_TX --> BQ_VIEW
    end

    subgraph FinOps["2. Triple-Layer SHA-256 FinOps Cache Engine"]
        HASH["SHA-256 Ledger Fingerprinting (target_id + sorted tx_id:amount)"]
        DISK_CACHE[(".cache/ SSD Store (Ledger + Audit + Chat Cache)")]
        MODE_SWITCH{{"Execution Mode Toggle: Instant Cache (0.01s) vs Live API"}}
        HASH --> MODE_SWITCH
        MODE_SWITCH -- "Cache Hit ($0 Token Cost)" --> DISK_CACHE
    end

    subgraph VertexAI["3. Vertex AI Dual-Agent Intelligence Loop"]
        AGENT1["🕵️ Agent 1: Forensic Investigator - Gemini 2.5 Flash (temp=0.1)"]
        AGENT2["⚖️ Agent 2: Statutory Compliance Auditor - Gemini 2.5 Pro (temp=0.0)"]
        FATF_CORPUS["📜 Regulatory Ground Truth: FATF 40 Recommendations"]
        COPILOT["✨ Senti AI Copilot: Live Case-Grounded Translator"]

        MODE_SWITCH -- "Live Cloud API Run" --> AGENT1
        AGENT1 -- "Parameterized Tool Calls" --> DataLayer
        AGENT1 -- "Factual Forensic Brief" --> AGENT2
        FATF_CORPUS --> AGENT2
        AGENT2 -- "Verified Structured Dossier" --> DISK_CACHE
    end

    subgraph Cockpit["4. SentinX v6.0 Enterprise Daylight Cockpit (Streamlit)"]
        UI_TRIAGE["🌍 Color-Coded Portfolio Leaderboard"]
        UI_GRAPH["🕸️ Zero-Zoom PyVis Threat Topology"]
        UI_BLUF["📋 Executive Plain-English BLUF + ₹10L Visualizer"]
        UI_SIM["🛑 Preventive Freeze Simulator"]
        UI_PDF["📕 ReportLab FIU-IND SAR PDF Exporter"]
    end

    DISK_CACHE --> Cockpit
    AGENT2 --> Cockpit
    COPILOT <--> Cockpit
~~~

---

## 🚀 Flagship Innovations in v6.0

| Innovation | Technical Implementation | Business & Compliance Value |
| :--- | :--- | :--- |
| **1. Color-Coded Portfolio Triage Leaderboard** | Batch BigQuery aggregation (`scan_portfolio_leaderboard`) + Pandas Styler row highlighting + `ProgressColumn` gauges. | Eliminates manual scrolling; compliance officers immediately spot **🔴 Critical Violations** vs. **🟢 Cleared Safe Accounts** across the entire bank portfolio. |
| **2. 2-Hop Recursive Syndicate Contagion Graph** | Recursive SQL CTE (`trace_2hop_network`) rendered in an Enterprise Daylight PyVis canvas with formatted Lakhs (`L`) / Crores (`Cr`) labels. | Exposes upstream master originators (e.g., Dubai shell hubs) that simultaneously fund multiple downstream mule rings. |
| **3. Visual ₹10-Lakh Threshold Evasion Analyzer** | Automated bar chart plotting individual inbound transfers against the statutory **₹10.00 Lakh CTR limit**. | Visually proves deliberate structuring (`92%–98%` threshold hugging) under **FATF Recommendation 10** at a single glance. |
| **4. False-Positive Immunity (Devil's Advocate)** | Mandatory `adversarial_defense_rebuttal` field inside Agent 2's Pydantic schema (`StatutoryAuditStructured`). | Tests whether an alert could be legitimate trade/payroll—clearing innocent businesses (`ACC_LEGIT_PAYROLL_01`) and saving 4.5 analyst hours per case. |
| **5. Triple-Layer SHA-256 FinOps Cache Engine** | Cryptographic SHA-256 hash of `(target_id + ledger_state)` caching BigQuery ledgers, Dual-Agent audits, and Senti AI chat replies. | Reduces repeat LLM token spend by **100%** on unchanged ledgers (`0.01s` response time) while offering a live toggle to force fresh Vertex AI runs. |
| **6. Preventive Freeze & Blast-Radius Simulator** | Interactive `What-If` contagion engine calculating blocked outbound volume and isolated counterparty nodes. | Quantifies exact **Illicit Capital Flight Intercepted (in INR)** prior to offshore SWIFT settlement. |
| **7. In-Memory FIU-IND Regulatory PDF Generator** | `ReportLab` Platypus engine (`app/pdf_exporter.py`) generating structured tables, KYC headers, and statutory mappings in RAM. | Produces court- and regulator-ready **Suspicious Transaction Reports (STR/SAR)** in one click with zero disk temp-file clutter. |

---

## 🎯 Verified AML Typology Scenarios

| Account ID | Legal Name & Profile | Active Typology | FATF Grounding | SentinX AI Verdict & Score |
| :--- | :--- | :--- | :--- | :--- |
| **`ACC_SMURF_CENTRAL_01`** | **Apex Holdings Ltd** (`SHELL_CORP` • 15 Days Old) | **Structuring / Smurfing Ring**: 5 inbound IMPS transfers (`₹9.20L–₹9.79L`) in 8 hours from 5 mule runners totaling `₹47.98 Lakhs`. | **FATF Rec 10, 20, 24** | 🚨 **`AUDIT_APPROVED_SAR_REQUIRED`** (Score: **`96 / 100`**) |
| **`ACC_RAPID_MULE_88`** | **Kavitha Logistics** (`INDIVIDUAL` • 11 Days Old) | **12-Min Cross-Border Pass-Through**: `₹25.00L` inbound via IMPS followed by `₹24.50L` (`98%`) wired to Singapore via SWIFT in **12 minutes**. | **FATF Rec 16, 10, 20** | 🚨 **`AUDIT_APPROVED_SAR_REQUIRED`** (Score: **`94 / 100`**) |
| **`ACC_ORIGINATOR_X`** | **Vanguard Global Trading LLC** (`SHELL_CORP` • UAE Hub) | **Master Syndicate Command Hub**: 2-hop upstream originator simultaneously seeding smurf runners and velocity pass-through mules. | **FATF Rec 16, 24/25** | 🚨 **`AUDIT_APPROVED_SAR_REQUIRED`** (Score: **`92 / 100`**) |
| **`ACC_LEGIT_PAYROLL_01`** | **TechFlow Enterprise Pvt Ltd** (`CORPORATE` • 7+ Years Old) | **Legitimate B2B & Payroll (False Positive Test)**: Standard monthly NEFT salary disbursements (`₹1.18L–₹1.62L`) and invoiced RTGS server hosting. | **FATF Rec 10** (Verified Baseline) | 🟢 **`AUDIT_CLEARED_FALSE_POSITIVE`** (Score: **`6 / 100`**) |

---

## 🌱 FinOps & Institutional ROI Benchmarks

| Operational Metric | Legacy Manual AML Review | SentinX v6.0 (Live Cloud API) | SentinX v6.0 (FinOps Cache Hit) |
| :--- | :--- | :--- | :--- |
| **End-to-End Investigation Time** | `4.5 Hours` / Alert | **`3.2 Seconds`** | **`0.01 Seconds`** |
| **Contagion Trace Depth** | 1-Hop Manual CSV Export | **Automated 2-Hop SQL CTE** | **Pre-Verified 2-Hop Graph** |
| **False-Positive Triage Cost** | `~$180 USD` (Analyst Labor) | **`~$0.005 USD`** (Vertex AI Tokens) | **`$0.000 USD`** (Zero Tokens) |
| **FIU-IND STR Dossier Drafting** | `2.0 Hours` Legal Formatting | **1-Click PDF & Markdown** | **1-Click PDF & Markdown** |

---

## 📂 Project Directory Structure

~~~text
sentinx-aml/
├── .cache/                              # Persistent SHA-256 FinOps Cache (Instant 0.01s Demo Load)
│   ├── sentinx_audit_cache.json         # Pre-warmed Dual-Agent Statutory Audit Dossiers
│   └── sentinx_ledger_cache.json        # Cached 1-Hop & 2-Hop BigQuery Graph Topologies
├── agents/                              # Dual-Agent Vertex AI Intelligence Core
│   ├── __init__.py
│   ├── auditor.py                       # Agent 2: Gemini 2.5 Pro (Zero-Temp Statutory Auditor & Senti AI)
│   ├── investigator.py                  # Agent 1: Gemini 2.5 Flash (AFC Multi-Hop SQL Investigator)
│   └── tools.py                         # Parameterized BigQuery SQL Tools & Portfolio Scanner
├── app/                                 # Enterprise Daylight Streamlit Cockpit
│   ├── __init__.py
│   ├── architecture_widget.py           # Interactive 6-Stage HTML5/SVG Pipeline Inspector
│   ├── cache_manager.py                 # Triple-Layer SHA-256 FinOps Disk & Session Cache Engine
│   ├── graph_builder.py                 # High-Contrast PyVis Threat Topology Builder (Lakhs/Crores)
│   ├── main.py                          # Multi-Tab Command Center, Triage Board & Freeze Simulator
│   └── pdf_exporter.py                  # In-Memory ReportLab FIU-IND Regulatory PDF Generator
├── config/
│   ├── __init__.py
│   └── settings.py                      # Centralized GCP Project, BigQuery & Model Guardrails
├── regulations/                         # Statutory Ground Truth Corpus
│   └── FATF_40_Recommendations.md       # International FATF Recommendations (10, 16, 20, 24/25)
├── .env.example                         # Environment Variable Template
├── .gitignore                           # Git Security & Artifact Exclusion Rules
├── prewarm_cache.py                     # 1-Click FinOps Demo Cache Pre-Warmer
├── README.md                            # Flagship Project Documentation
└── requirements.txt                     # Pinned Production Python Dependencies
~~~

---

## ⚡ Installation & Quickstart

### 1. Clone & Install Dependencies
~~~bash
git clone https://github.com/<your-username>/sentinx-aml.git
cd sentinx-aml

python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
~~~

### 2. Configure Environment Variables
~~~bash
cp .env.example .env
gcloud auth application-default login
~~~

### 3. Pre-Warm the FinOps Demo Cache & Launch UI
~~~bash
python prewarm_cache.py
streamlit run app/main.py
~~~

---

## 🛡️ Responsible AI & Regulatory Disclaimer

SentinX is architected under strict **Human-in-the-Loop (HITL)** and **Zero-Hallucination** principles:
* **Deterministic Grounding:** Agent 2 operates at `temperature=0.0` and is restricted strictly to transaction records retrieved via parameterized BigQuery SQL queries.
* **Adversarial Fairness:** Every investigation undergoes mandatory Devil's Advocate evaluation to protect legitimate customers and businesses from wrongful account freezes.
* **Synthetic Data:** All entities, account IDs, and transactions in this repository are 100% synthetic and generated solely for financial crime compliance research and demonstration.