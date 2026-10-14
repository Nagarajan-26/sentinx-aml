"""
SentinX: Official Regulatory PDF Exporter for SAR / STR Packets
Compliant with FIU / FATF reporting document structures.
"""

from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def generate_sar_pdf(target_id: str, profile: dict, auditor_report: str, investigator_report: str) -> bytes:
    """Generates an in-memory PDF dossier conforming to FIU STR standards."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=6,
    )
    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#475569"),
        spaceAfter=12,
    )
    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1E293B"),
        spaceBefore=10,
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1E293B"),
    )
    bold_cell_style = ParagraphStyle(
        "BoldCell",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#0F172A"),
    )

    story = []

    # 1. Header Banner
    story.append(Paragraph("SENTINX AML FORENSIC INTELLIGENCE", title_style))
    story.append(
        Paragraph(
            f"OFFICIAL SUSPICIOUS TRANSACTION REPORT (STR) | FIU REGULATORY SUBMISSION PACKET<br/>"
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')} | Standard: FATF 40 Recommendations",
            subtitle_style,
        )
    )
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#EF4444"), spaceAfter=12))

    # 2. Target Subject Metadata Table
    story.append(Paragraph("1. TARGET ENTITY REGULATORY DOSSIER", heading_style))

    metadata_data = [
        [
            Paragraph("Target Entity ID:", bold_cell_style),
            Paragraph(target_id, body_style),
            Paragraph("Jurisdiction:", bold_cell_style),
            Paragraph(str(profile.get("jurisdiction", "IND")), body_style),
        ],
        [
            Paragraph("Legal Registered Name:", bold_cell_style),
            Paragraph(str(profile.get("legal_name", "N/A")), body_style),
            Paragraph("Entity Classification:", bold_cell_style),
            Paragraph(str(profile.get("entity_type", "UNKNOWN")), body_style),
        ],
        [
            Paragraph("Risk Rating:", bold_cell_style),
            Paragraph(f"<b>{profile.get('risk_rating', 'HIGH')}</b>", body_style),
            Paragraph("Incorporation Date:", bold_cell_style),
            Paragraph(str(profile.get("incorporation_date", "N/A")), body_style),
        ],
    ]

    meta_table = Table(metadata_data, colWidths=[110, 160, 110, 150])
    meta_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # 3. Agent 2: Statutory Compliance Audit (Ground Truth)
    story.append(Paragraph("2. STATUTORY COMPLIANCE AUDIT & FATF MAPPING", heading_style))
    for line in auditor_report.split("\n"):
        clean = line.strip().replace("#", "").replace("**", "")
        if clean:
            if clean.startswith("[AUDIT_APPROVED]"):
                story.append(Paragraph(f"<b>VERDICT: {clean}</b>", bold_cell_style))
            else:
                story.append(Paragraph(clean, body_style))
            story.append(Spacer(1, 3))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#94A3B8"), spaceAfter=10))

    # 4. Agent 1: Underlying Forensic Factual Evidence
    story.append(Paragraph("3. UNDERLYING FORENSIC LEDGER & EVIDENCE TRAIL", heading_style))
    for line in investigator_report.split("\n"):
        clean = line.strip().replace("#", "").replace("**", "")
        if clean:
            story.append(Paragraph(clean, body_style))
            story.append(Spacer(1, 3))

    # Build PDF
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes