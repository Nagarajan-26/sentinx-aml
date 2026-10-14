"""
SentinX v3.0: Enterprise Daylight Topology Graph Builder
Clean slate-white canvas (#F8FAFC) with high-contrast navy typography and zero-zoom Lakhs/Crores labels.
"""

from pyvis.network import Network
from typing import List, Dict, Any

def _fmt_inr(amount: float) -> str:
    """Formats raw INR into readable Lakhs (L) or Crores (Cr) for instant visual scanning."""
    if amount >= 10_000_000:
        return f"₹{amount / 10_000_000:.2f} Cr"
    elif amount >= 100_000:
        return f"₹{amount / 100_000:.2f} L"
    else:
        return f"₹{amount:,.0f}"

def generate_subgraph_html(transactions: List[Dict[str, Any]], target_entity_id: str) -> str:
    # Clean Enterprise Alabaster/Slate Canvas instead of pitch black
    net = Network(height="490px", width="100%", bgcolor="#F8FAFC", font_color="#0F172A", directed=True)

    net.set_options("""
    var options = {
      "nodes": {
        "font": {
          "size": 16,
          "face": "Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif",
          "color": "#0F172A",
          "strokeWidth": 4,
          "strokeColor": "#FFFFFF"
        },
        "borderWidth": 3,
        "borderWidthSelected": 5,
        "shadow": {"enabled": true, "color": "rgba(15, 23, 42, 0.14)", "size": 12, "x": 0, "y": 4}
      },
      "edges": {
        "color": { "inherit": false },
        "smooth": { "type": "curvedCW", "roundness": 0.16 },
        "font": {
          "size": 14,
          "face": "Inter, Segoe UI, sans-serif",
          "align": "horizontal",
          "color": "#0F172A",
          "strokeWidth": 5,
          "strokeColor": "#F8FAFC"
        },
        "arrows": { "to": { "enabled": true, "scaleFactor": 1.0, "type": "arrow" } }
      },
      "physics": {
        "barnesHut": {
          "gravitationalConstant": -8500,
          "centralGravity": 0.25,
          "springLength": 210,
          "springStrength": 0.045,
          "damping": 0.18
        },
        "minVelocity": 0.75
      },
      "interaction": { "hover": true, "navigationButtons": true, "tooltipDelay": 80 }
    }
    """)

    entities = set()
    node_inflow = {}
    node_outflow = {}
    amounts = [float(tx["amount"]) for tx in transactions] if transactions else [1.0]
    max_amount = max(amounts) if max(amounts) > 0 else 1.0

    for tx in transactions:
        src = tx["source_entity_id"]
        dst = tx["destination_entity_id"]
        amt = float(tx["amount"])
        entities.add(src)
        entities.add(dst)
        node_outflow[src] = node_outflow.get(src, 0.0) + amt
        node_inflow[dst] = node_inflow.get(dst, 0.0) + amt

    for node in entities:
        in_amt = node_inflow.get(node, 0.0)
        out_amt = node_outflow.get(node, 0.0)
        vol_tag = f"In: {_fmt_inr(in_amt)}" if in_amt >= out_amt else f"Out: {_fmt_inr(out_amt)}"

        if node == target_entity_id:
            bg, border = "#DC2626", "#991B1B"  # Crimson Target
            shape, size = "dot", 34
            label = f"🎯 {node}\n[{vol_tag}]"
        elif "MULE" in node or "SMURF" in node:
            bg, border = "#D97706", "#92400E"  # Amber Mule/Smurf
            shape, size = "dot", 26
            label = f"⚠️ {node}\n[{vol_tag}]"
        elif "OFFSHORE" in node or "ORIGINATOR" in node:
            bg, border = "#7C3AED", "#4C1D95"  # Royal Purple Offshore/Originator
            shape, size = "diamond", 30
            label = f"🌐 {node}\n[{vol_tag}]"
        else:
            bg, border = "#059669", "#065F46"  # Emerald Clean Counterparty
            shape, size = "dot", 23
            label = f"🏢 {node}\n[{vol_tag}]"

        tooltip = (
            f"Account: {node}\n"
            f"Inbound Flow: {_fmt_inr(in_amt)} (₹{in_amt:,.2f})\n"
            f"Outbound Flow: {_fmt_inr(out_amt)} (₹{out_amt:,.2f})"
        )
        net.add_node(
            node,
            label=label,
            title=tooltip,
            shape=shape,
            size=size,
            color={"background": bg, "border": border, "highlight": {"background": "#2563EB", "border": "#1D4ED8"}}
        )

    for tx in transactions:
        amt = float(tx["amount"])
        rail = tx["rail_type"]
        weight = max(2.5, (amt / max_amount) * 8.0)
        edge_color = "#0284C7" if rail == "IMPS" else ("#E11D48" if rail == "SWIFT" else "#059669")

        net.add_edge(
            tx["source_entity_id"],
            tx["destination_entity_id"],
            label=f"{rail}: {_fmt_inr(amt)}",
            title=(
                f"Transaction ID: {tx['transaction_id']}\n"
                f"Amount: ₹{amt:,.2f} ({_fmt_inr(amt)})\n"
                f"Payment Rail: {rail}\n"
                f"Timestamp: {tx['transaction_timestamp']}\n"
                f"Declared Purpose: {tx['declared_purpose']}"
            ),
            color={"color": edge_color, "highlight": "#1E293B"},
            width=weight
        )

    raw_html = net.generate_html()

    # Crisp Daylight HUD Legend Overlay
    hud_overlay = """
    <div style="position:absolute; top:10px; left:10px; background:rgba(255,255,255,0.95); border:1px solid #CBD5E1; border-radius:8px; padding:10px 14px; color:#0F172A; font-family:Inter,sans-serif; font-size:12px; z-index:9999; pointer-events:none; box-shadow:0 4px 12px rgba(15,23,42,0.08);">
      <div style="font-weight:800; margin-bottom:5px; color:#334155; text-transform:uppercase; letter-spacing:0.6px; font-size:11px;">Network Topology Legend</div>
      <div style="margin-bottom:3px;"><span style="color:#DC2626; font-weight:bold;">●</span> Target Subject &nbsp;&nbsp;<span style="color:#D97706; font-weight:bold;">●</span> Smurf / Mule Node</div>
      <div style="margin-bottom:6px;"><span style="color:#7C3AED; font-weight:bold;">◆</span> Offshore / Hub &nbsp;<span style="color:#059669; font-weight:bold;">●</span> Verified Counterparty</div>
      <div style="border-top:1px solid #E2E8F0; padding-top:5px; font-size:11px; color:#475569;">
        <b>Payment Rails:</b> <span style="color:#0284C7; font-weight:700;">━ IMPS</span> &nbsp;<span style="color:#E11D48; font-weight:700;">━ SWIFT</span> &nbsp;<span style="color:#059669; font-weight:700;">━ NEFT/RTGS</span>
      </div>
    </div>
    """
    return raw_html.replace("<body>", f"<body style='margin:0; position:relative; border:1px solid #E2E8F0; border-radius:10px; overflow:hidden;'>{hud_overlay}")