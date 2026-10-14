"""
SentinX v5.0: Clean Interactive Architecture Inspector (Zero Cut-Off, No Fake Loading Bar)
"""

def generate_architecture_diagram_html(
    active_target: str,
    hop_count: int,
    direct_count: int,
    is_audited: bool,
    source_mode: str,
    risk_score: str
) -> str:
    state_label = "AUDIT VERIFIED" if is_audited else "READY TO EXECUTE"
    state_bg = "#DCFCE7" if is_audited else "#FEF3C7"
    state_fg = "#166534" if is_audited else "#92400E"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
      * {{ box-sizing: border-box; font-family: 'Inter', -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; }}
      body {{
        margin: 0;
        padding: 16px;
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 12px;
        color: #0F172A;
      }}
      .header-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 14px;
        padding-bottom: 10px;
        border-bottom: 1px solid #E2E8F0;
      }}
      .header-title {{
        font-size: 13.5px;
        font-weight: 800;
        color: #0F172A;
      }}
      .header-badge {{
        font-size: 11px;
        font-weight: 800;
        padding: 4px 10px;
        border-radius: 6px;
        background: {state_bg};
        color: {state_fg};
      }}
      .steps-row {{
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 8px;
        margin-bottom: 14px;
      }}
      .step-box {{
        background: #F8FAFC;
        border: 1.5px solid #CBD5E1;
        border-radius: 8px;
        padding: 10px 6px;
        text-align: center;
        cursor: pointer;
        transition: all 0.15s ease;
      }}
      .step-box:hover {{
        border-color: #2563EB;
        background: #EFF6FF;
      }}
      .step-box.active {{
        background: #1E40AF;
        border-color: #1E3A8A;
        color: #FFFFFF;
        box-shadow: 0 4px 10px rgba(30, 64, 175, 0.2);
      }}
      .step-num {{
        font-size: 10px;
        font-weight: 800;
        text-transform: uppercase;
        color: #2563EB;
        margin-bottom: 4px;
      }}
      .step-box.active .step-num {{ color: #93C5FD; }}
      .step-title {{
        font-size: 12px;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 3px;
      }}
      .step-box.active .step-title {{ color: #FFFFFF; }}
      .step-meta {{
        font-size: 10.5px;
        color: #64748B;
        font-weight: 600;
      }}
      .step-box.active .step-meta {{ color: #DBEAFE; }}
      .inspector-box {{
        background: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-left: 5px solid #2563EB;
        border-radius: 8px;
        padding: 14px 16px;
      }}
      .ins-top {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
      }}
      .ins-name {{
        font-size: 14px;
        font-weight: 800;
        color: #1E3A8A;
      }}
      .ins-tag {{
        font-size: 11px;
        font-weight: 700;
        background: #DBEAFE;
        color: #1E40AF;
        padding: 3px 9px;
        border-radius: 4px;
      }}
      .ins-desc {{
        font-size: 13px;
        color: #334155;
        line-height: 1.55;
      }}
    </style>
    </head>
    <body>
      <div class="header-row">
        <div class="header-title">🏗️ SentinX 6-Stage Architecture Inspector (Click Any Box Below to View Stage Details)</div>
        <div class="header-badge">{state_label} • Mode: {source_mode}</div>
      </div>

      <div class="steps-row">
        <div class="step-box active" onclick="pick(0)" id="s0">
          <div class="step-num">1. Data Layer</div>
          <div class="step-title">🗄️ BigQuery</div>
          <div class="step-meta">{hop_count} Edges</div>
        </div>
        <div class="step-box" onclick="pick(1)" id="s1">
          <div class="step-num">2. FinOps</div>
          <div class="step-title">🔐 SHA-256</div>
          <div class="step-meta">{source_mode}</div>
        </div>
        <div class="step-box" onclick="pick(2)" id="s2">
          <div class="step-num">3. Agent 1</div>
          <div class="step-title">🕵️ Flash 2.5</div>
          <div class="step-meta">SQL Tools</div>
        </div>
        <div class="step-box" onclick="pick(3)" id="s3">
          <div class="step-num">4. Agent 2</div>
          <div class="step-title">⚖️ Pro 2.5</div>
          <div class="step-meta">FATF Audit</div>
        </div>
        <div class="step-box" onclick="pick(4)" id="s4">
          <div class="step-num">5. Copilot</div>
          <div class="step-title">✨ Senti AI</div>
          <div class="step-meta">Translator</div>
        </div>
        <div class="step-box" onclick="pick(5)" id="s5">
          <div class="step-num">6. Output</div>
          <div class="step-title">📕 SAR PDF</div>
          <div class="step-meta">Risk: {risk_score}</div>
        </div>
      </div>

      <div class="inspector-box">
        <div class="ins-top">
          <div class="ins-name" id="i-name">Stage 1: BigQuery Multi-Rail Forensic Ledger</div>
          <div class="ins-tag" id="i-tag">Account: {active_target} ({direct_count} Direct / {hop_count} Network Hops)</div>
        </div>
        <div class="ins-desc" id="i-desc">
          Queries high-velocity payment records across <b>IMPS, SWIFT, NEFT, and RTGS</b>. Uses a 2-hop recursive SQL Common Table Expression (CTE) to uncover upstream originators and downstream mule rings connected to <b>{active_target}</b>.
        </div>
      </div>

      <script>
        const data = [
          {{
            name: "Stage 1: BigQuery Multi-Rail Forensic Ledger",
            tag: "Account: {active_target} ({direct_count} Direct / {hop_count} Network Hops)",
            desc: "Queries high-velocity payment records across <b>IMPS, SWIFT, NEFT, and RTGS</b>. Uses a 2-hop recursive SQL Common Table Expression (CTE) to uncover upstream originators and downstream mule rings connected to <b>{active_target}</b>."
          }},
          {{
            name: "Stage 2: SHA-256 FinOps Cache & Execution Router",
            tag: "Active Mode: {source_mode}",
            desc: "Generates a unique SHA-256 fingerprint of <b>{active_target}</b>'s ledger. In <b>Instant Cache Mode</b>, verified audits load in 0.01s at $0 token cost. Flip the sidebar toggle to <b>Live Cloud API Mode</b> to force a fresh real-time Vertex AI execution."
          }},
          {{
            name: "Stage 3: Agent 1 — Forensic Investigator (Gemini 2.5 Flash)",
            tag: "4 Parameterized BigQuery Tools • Temperature 0.1",
            desc: "Autonomously executes Python function calls against BigQuery to inspect incorporation age, inbound/outbound rupee velocity, and 12-minute pass-through retention ratios."
          }},
          {{
            name: "Stage 4: Agent 2 — Statutory Compliance Auditor (Gemini 2.5 Pro)",
            tag: "Zero-Hallucination Challenger • Temperature 0.0",
            desc: "Audits Agent 1's factual brief against <b>FATF Recommendations 10, 16, 20, and 24</b>. Plays devil's advocate to clear innocent businesses (False-Positive immunity) and outputs a strict JSON schema."
          }},
          {{
            name: "Stage 5: Senti AI — Plain-English Executive Copilot",
            tag: "Context-Grounded Live Q&A",
            desc: "Reads the active account's KYC profile, transaction ledger, and statutory audit so non-technical executives can ask questions in plain English without reading dense legal reports."
          }},
          {{
            name: "Stage 6: Official FIU-IND Regulatory STR/SAR Exporter",
            tag: "Risk Score: {risk_score} • ReportLab PDF Engine",
            desc: "Compiles the verified KYC metadata, statutory rebuttal, and transaction evidence ledger into a 1-click downloadable <b>PDF & Markdown Suspicious Transaction Report</b>."
          }}
        ];
        function pick(idx) {{
          for (let i = 0; i < 6; i++) {{
            document.getElementById("s" + i).classList.remove("active");
          }}
          document.getElementById("s" + idx).classList.add("active");
          document.getElementById("i-name").innerHTML = data[idx].name;
          document.getElementById("i-tag").innerHTML = data[idx].tag;
          document.getElementById("i-desc").innerHTML = data[idx].desc;
        }}
      </script>
    </body>
    </html>
    """