from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
import os

# --- STYLE CONSTANTS ---
PRIMARY_COLOR = colors.HexColor("#111827")
SECONDARY_COLOR = colors.HexColor("#ff4b44")
ACCENT_TEAL = colors.HexColor("#00d2d3")
BG_SOFT = colors.HexColor("#f9fafb")
BORDER_LIGHT = colors.HexColor("#e5e7eb")

def draw_modern_header(c, title, width, height):
    """Draws a sleek, modern header with a subtle accent line."""
    c.setFillColor(PRIMARY_COLOR)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(0.5 * inch, height - 0.75 * inch, title)
    
    # Bottom accent line
    c.setStrokeColor(SECONDARY_COLOR)
    c.setLineWidth(3)
    c.line(0.5 * inch, height - 0.95 * inch, 1.2 * inch, height - 0.95 * inch)
    
    c.setStrokeColor(BORDER_LIGHT)
    c.setLineWidth(0.5)
    c.line(0.5 * inch, height - 0.95 * inch, width - 0.5 * inch, height - 0.95 * inch)
    
    c.setFillColor(colors.HexColor("#6b7280"))
    c.setFont("Helvetica", 9)
    c.drawRightString(width - 0.5 * inch, height - 0.75 * inch, "TECHNICAL PERFORMANCE DOSSIER")

def create_report(match_info, top_creators, heatmap_path, pizza_path, shotmap_path, output_path):
    """Assembles a high-end technical report with modern aesthetics."""
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    
    abs_heatmap = os.path.abspath(heatmap_path)
    abs_pizza = os.path.abspath(pizza_path)
    abs_shotmap = os.path.abspath(shotmap_path)
    
    # --- PAGE 1: EXECUTIVE SUMMARY ---
    draw_modern_header(c, "MATCH PERFORMANCE", width, height)
    
    # Clean Info Card
    c.setFillColor(BG_SOFT)
    c.rect(0.5 * inch, height - 2.5 * inch, width - inch, 1.2 * inch, fill=1, stroke=0)
    c.setFillColor(PRIMARY_COLOR)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(0.75 * inch, height - 1.7 * inch, f"{match_info['home_team']} vs {match_info['away_team']}")
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#4b5563"))
    c.drawString(0.75 * inch, height - 2.0 * inch, f"{match_info['competition']} | {match_info['match_date']}")
    
    c.setFillColor(PRIMARY_COLOR)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.5 * inch, height - 3.2 * inch, "ANALYTICAL SUMMARY")
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#374151"))
    y = height - 3.5 * inch
    summary = [
        "This dossier provides a data-driven evaluation of team performance and individual player influence.",
        "We prioritize metrics that correlate with sustained tactical success: xT (Expected Threat) and xG (Expected Goals).",
        "",
        f"MATCH HIGHLIGHT: {top_creators.iloc[0]['player'].upper()} emerged as the most critical offensive architect,",
        f"contributing a match-high {top_creators.iloc[0]['xt']:.3f} net threat share."
    ]
    for line in summary:
        c.drawString(0.5 * inch, y, line)
        y -= 0.22 * inch
    
    # Top Players Table (Modern Layout)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.5 * inch, height - 5.5 * inch, "OFFENSIVE ARCHITECTS (RANKED BY xT)")
    y_pos = height - 6.0 * inch
    for i, row in top_creators.head(10).iterrows():
        # Row zebra striping
        if i % 2 == 0:
            c.setFillColor(BG_SOFT)
            c.rect(0.5 * inch, y_pos - 0.05 * inch, width - inch, 0.22 * inch, fill=1, stroke=0)
        
        c.setFillColor(PRIMARY_COLOR)
        c.setFont("Helvetica", 10)
        c.drawString(0.75 * inch, y_pos, f"{i+1}")
        c.setFont("Helvetica-Bold", 10)
        c.drawString(1.2 * inch, y_pos, f"{row['player'].upper()}")
        c.setFillColor(SECONDARY_COLOR)
        c.drawRightString(width - 0.75 * inch, y_pos, f"{row['xt']:.3f}")
        y_pos -= 0.25 * inch
        
    c.showPage()
    
    # --- PAGE 2: ZONAL THREAT ---
    draw_modern_header(c, "SPATIAL ANALYSIS", width, height)
    if os.path.exists(abs_heatmap):
        c.drawImage(abs_heatmap, 0.5 * inch, 4.0 * inch, width=width - inch, height=4.5 * inch, preserveAspectRatio=True)
    
    c.setFillColor(PRIMARY_COLOR)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.5 * inch, 3.8 * inch, "TACTICAL INTELLIGENCE: SPATIAL FOCUS")
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#4b5563"))
    desc = [
        "YOU ARE SEEING: The distribution of attacking danger (xT) across tactical pitch zones.",
        "KEY METRIC: The percentages identify exactly where the team successfully creates goal-scoring",
        "probabilities. High central volume indicates defensive penetration, while wing bias suggests",
        "a wide-based offensive strategy relying on full-backs or wingers."
    ]
    y = 3.5 * inch
    for line in desc:
        c.drawString(0.5 * inch, y, line)
        y -= 0.2 * inch
    
    c.showPage()
    
    # --- PAGE 3: PLAYER PIZZA ---
    draw_modern_header(c, "INDIVIDUAL PROFILE", width, height)
    if os.path.exists(abs_pizza):
        c.drawImage(abs_pizza, 1 * inch, 4.0 * inch, width=width - 2*inch, height=4.5 * inch, preserveAspectRatio=True)
        
    c.setFillColor(PRIMARY_COLOR)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.5 * inch, 3.8 * inch, "TACTICAL INTELLIGENCE: PLAYER FINGERPRINT")
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#4b5563"))
    desc = [
        "YOU ARE SEEING: A multi-dimensional performance profile of the team's primary creator.",
        "KEY METRIC: Slices represent percentile ranks against the team average. Fuller slices indicate",
        "elite performance in that specific category (e.g., VOLUME, ACCURACY, or DANGER).",
        "TEAL = POSSESSION METRICS | RED = ATTACKING METRICS."
    ]
    y = 3.5 * inch
    for line in desc:
        c.drawString(0.5 * inch, y, line)
        y -= 0.2 * inch
    
    c.showPage()
    
    # --- PAGE 4: SHOT MAP ---
    draw_modern_header(c, "CONVERSION ANALYSIS", width, height)
    if os.path.exists(abs_shotmap):
        c.drawImage(abs_shotmap, 0.5 * inch, 4.0 * inch, width=width - inch, height=4.5 * inch, preserveAspectRatio=True)
        
    c.setFillColor(PRIMARY_COLOR)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.5 * inch, 3.8 * inch, "TACTICAL INTELLIGENCE: FINISHING QUALITY")
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#4b5563"))
    desc = [
        "YOU ARE SEEING: The location and mathematical quality (xG) of every shot attempt.",
        "KEY METRIC: Marker size indicates the probability of the shot resulting in a goal.",
        "RED MARKERS signify successful goals. Concentrated volume inside the penalty area",
        "is a hallmark of elite tactical chance creation."
    ]
    y = 3.5 * inch
    for line in desc:
        c.drawString(0.5 * inch, y, line)
        y -= 0.2 * inch
    
    c.showPage()
    
    c.save()
    print(f"Modern Technical Dossier generated at {output_path}")
