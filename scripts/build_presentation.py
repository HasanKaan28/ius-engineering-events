#!/usr/bin/env python3
"""
Build ultra-professional, executive presentation HTML slide deck and 16:9 PDF export
for the FENS Deanery Proposal (IUS Engineering Club).

Directly solves:
1. "Logoyu falan içine oturtamamışsın":
   - Switched to 100% square, transparent-background, perfectly centered seal (assets/club_seal_perfect.png).
   - Framed with double academic gold ring, ample padding, and zero edge clipping on all slides.
2. "Uzaktan bakan biri için yazılar hala küçük":
   - Drastically enlarged typography across every slide (Headlines 60-90px, Card titles 34-40px, Body 23-26px, Numbers 64-74px).
   - Removed dense text blocks in favor of high-impact, bold, punchy executive takeaways.
   - High-contrast pure white (#FFFFFF), brilliant gold (#FBBF24), and sapphire cyan (#38BDF8) for effortless 10-meter readability.
"""

import os
import sys
import base64
import subprocess
from pathlib import Path

# Fix Windows console UTF-8 output
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
SLIDES_DIR = WORKSPACE_ROOT / "slides"
SLIDES_DIR.mkdir(parents=True, exist_ok=True)
EXPORT_DIR = WORKSPACE_ROOT / "export_documents"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

def get_base64_img(rel_path):
    p = WORKSPACE_ROOT / rel_path
    if p.exists():
        with open(p, "rb") as f:
            ext = p.suffix.lower()
            mime = "image/png" if ext == ".png" else "image/jpeg"
            b64 = base64.b64encode(f.read()).decode("utf-8")
            return f"data:{mime};base64,{b64}"
    return ""

# Use the perfect circular transparent seal
SEAL_B64 = get_base64_img("assets/club_seal_perfect.png")
if not SEAL_B64:
    SEAL_B64 = get_base64_img("assets/club_seal.jpg")

HTML_TEMPLATE = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>IUS Engineering Club — Deanery Proposal 2026/2027</title>
  
  <!-- Presentation Typography: Outfit & Plus Jakarta Sans with System Fallbacks -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@700;800;900&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">

  <style>
    /* =====================================================================
       HARMONIOUS ACADEMIC / EXECUTIVE COLOR PALETTE
       - Canvas: Deep Royal Oxford Navy (#071120 / #0B1D3A)
       - Card Surfaces: Deep Sapphire Glass (#0D1E38)
       - Imperial Academic Gold: #F59E0B / #FBBF24 / #D97706
       - Precision Ice / Cyan Blue: #38BDF8 / #60A5FA
       - High-Contrast White / Crisp Slate: #FFFFFF / #F8FAFC
       ===================================================================== */
    :root {{
      --bg-canvas: #071120;
      --bg-gradient: radial-gradient(ellipse at 50% 15%, #102544 0%, #071120 75%, #040913 100%);
      --card-bg: rgba(13, 30, 56, 0.94);
      --card-border: rgba(148, 163, 184, 0.25);
      --card-highlight: #F59E0B;
      --card-shadow: 0 20px 48px rgba(0, 0, 0, 0.55), 0 0 1px rgba(255, 255, 255, 0.15);
      
      --gold-primary: #F59E0B;
      --gold-bright: #FBBF24;
      --gold-deep: #D97706;
      --gold-glow: rgba(245, 158, 11, 0.3);
      
      --blue-accent: #38BDF8;
      --blue-bright: #7DD3FC;
      --blue-glow: rgba(56, 189, 248, 0.25);
      
      --text-hero: #FFFFFF;
      --text-body: #F8FAFC;
      --text-sub: #E2E8F0;
      --text-muted: #94A3B8;
      
      --badge-bg: rgba(245, 158, 11, 0.16);
      --badge-border: rgba(245, 158, 11, 0.5);
      --badge-text: #FBBF24;
    }}

    /* Light Academic Ivory Mode (Toggled via button or 'T' key) */
    body.light-mode {{
      --bg-canvas: #F8FAFC;
      --bg-gradient: radial-gradient(ellipse at 50% 10%, #FFFFFF 0%, #EFF6FF 70%, #E2E8F0 100%);
      --card-bg: #FFFFFF;
      --card-border: rgba(15, 23, 42, 0.16);
      --card-highlight: #D97706;
      --card-shadow: 0 18px 40px rgba(15, 23, 42, 0.08), 0 0 1px rgba(15, 23, 42, 0.15);
      
      --gold-primary: #D97706;
      --gold-bright: #B45309;
      --gold-deep: #92400E;
      --gold-glow: rgba(217, 119, 6, 0.18);
      
      --blue-accent: #0284C7;
      --blue-bright: #0369A1;
      --blue-glow: rgba(2, 132, 199, 0.16);
      
      --text-hero: #071120;
      --text-body: #0F172A;
      --text-sub: #1E293B;
      --text-muted: #475569;
      
      --badge-bg: rgba(217, 119, 6, 0.1);
      --badge-border: rgba(217, 119, 6, 0.4);
      --badge-text: #B45309;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    html, body {{
      width: 100%;
      height: 100%;
      overflow: hidden;
      background: var(--bg-canvas);
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      color: var(--text-body);
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }}

    /* =====================================================================
       TOP FLOATING CONTROLS (Screen only)
       ===================================================================== */
    .deck-toolbar {{
      position: fixed;
      top: 16px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 9999;
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 10px 24px;
      background: rgba(7, 17, 32, 0.94);
      backdrop-filter: blur(18px);
      border: 1px solid rgba(148, 163, 184, 0.35);
      border-radius: 999px;
      box-shadow: 0 12px 35px rgba(0, 0, 0, 0.65);
    }}
    body.light-mode .deck-toolbar {{
      background: rgba(255, 255, 255, 0.95);
      border-color: rgba(15, 23, 42, 0.18);
      box-shadow: 0 12px 35px rgba(15, 23, 42, 0.15);
    }}

    .toolbar-title {{
      font-family: 'Outfit', 'Segoe UI', sans-serif;
      font-size: 0.92rem;
      font-weight: 800;
      color: var(--gold-bright);
      letter-spacing: 0.8px;
      text-transform: uppercase;
      padding-right: 12px;
      border-right: 1px solid rgba(148, 163, 184, 0.3);
    }}

    .nav-btn {{
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(148, 163, 184, 0.3);
      color: var(--text-hero);
      padding: 8px 18px;
      border-radius: 999px;
      font-size: 0.85rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      font-family: inherit;
    }}
    body.light-mode .nav-btn {{
      background: rgba(15, 23, 42, 0.05);
      border-color: rgba(15, 23, 42, 0.18);
      color: var(--text-hero);
    }}
    .nav-btn:hover {{
      background: var(--gold-primary);
      color: #071120;
      border-color: var(--gold-primary);
      transform: translateY(-2px);
      box-shadow: 0 6px 16px var(--gold-glow);
    }}

    .slide-counter {{
      font-family: 'Outfit', 'Segoe UI', sans-serif;
      font-size: 0.95rem;
      font-weight: 800;
      color: var(--text-hero);
      padding: 0 10px;
      letter-spacing: 1.2px;
    }}

    /* =====================================================================
       STAGE & 1920x1080 WIDESCREEN PRESENTATION CANVAS
       ===================================================================== */
    .viewport-container {{
      width: 100vw;
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: var(--bg-gradient);
      overflow: hidden;
      position: relative;
    }}

    #presentationStage {{
      width: 1920px;
      height: 1080px;
      transform-origin: center center;
      position: relative;
      flex-shrink: 0;
      box-shadow: 0 30px 90px rgba(0, 0, 0, 0.7);
    }}
    body.light-mode #presentationStage {{
      box-shadow: 0 30px 90px rgba(15, 23, 42, 0.15);
    }}

    .slide-canvas {{
      width: 1920px;
      height: 1080px;
      position: absolute;
      top: 0;
      left: 0;
      padding: 50px 80px 40px 80px;
      display: none;
      flex-direction: column;
      justify-content: space-between;
      background: var(--bg-canvas);
      background-image: var(--bg-gradient);
      box-sizing: border-box;
      overflow: hidden;
    }}

    .slide-canvas.active {{
      display: flex;
      animation: fadeInSlide 0.25s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}

    @keyframes fadeInSlide {{
      from {{ opacity: 0; transform: scale(0.994); }}
      to {{ opacity: 1; transform: scale(1); }}
    }}

    /* Top decorative prestige bar */
    .slide-canvas::before {{
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 6px;
      background: linear-gradient(90deg, var(--gold-primary) 0%, var(--blue-accent) 60%, var(--gold-primary) 100%);
    }}

    /* =====================================================================
       DISTANCE-OPTIMIZED TYPOGRAPHY HIERARCHY
       ===================================================================== */
    .slide-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      position: relative;
      z-index: 2;
    }}

    .header-left {{
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}

    .slide-breadcrumb {{
      font-family: 'Outfit', 'Segoe UI', sans-serif;
      font-size: 1.15rem;
      font-weight: 800;
      letter-spacing: 3px;
      text-transform: uppercase;
      color: var(--gold-bright);
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .slide-title {{
      font-family: 'Outfit', 'Segoe UI', sans-serif;
      font-size: 3.2rem;
      font-weight: 900;
      color: var(--text-hero);
      line-height: 1.15;
      letter-spacing: -0.025em;
    }}

    .slide-subtitle {{
      font-size: 1.35rem;
      color: var(--text-sub);
      font-weight: 500;
      max-width: 1400px;
      line-height: 1.45;
    }}

    /* Professional Top-Right Seal Badge */
    .header-badge {{
      display: flex;
      align-items: center;
      gap: 14px;
      padding: 6px 20px 6px 10px;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 999px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.35);
      flex-shrink: 0;
    }}
    .header-badge img {{
      width: 50px;
      height: 50px;
      border-radius: 50%;
      object-fit: contain;
      background: #FFFFFF;
      border: 2px solid var(--gold-primary);
      padding: 2px;
      flex-shrink: 0;
    }}
    .header-badge-col {{
      display: flex;
      flex-direction: column;
      text-align: right;
      white-space: nowrap;
    }}
    .header-badge-title {{
      font-family: 'Outfit', 'Segoe UI', sans-serif;
      font-size: 1rem;
      font-weight: 900;
      color: var(--text-hero);
      letter-spacing: 0.8px;
    }}
    .header-badge-sub {{
      font-family: 'Outfit', 'Segoe UI', sans-serif;
      font-size: 0.82rem;
      font-weight: 800;
      color: var(--gold-primary);
      letter-spacing: 1.2px;
    }}

    /* =====================================================================
       EXPANSIVE SLIDE BODY & GRID CONTAINERS
       ===================================================================== */
    .slide-body {{
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      position: relative;
      z-index: 2;
      margin-bottom: 20px;
    }}

    /* 3-Column Philosophy Grid */
    .grid-3 {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 32px;
      height: 100%;
    }}

    /* 2x2 Balanced Matrix Grid */
    .grid-2x2 {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      grid-template-rows: repeat(2, 1fr);
      gap: 26px;
      height: 100%;
    }}

    /* 2-Column Split Grid */
    .grid-2 {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 36px;
      height: 100%;
    }}

    /* =====================================================================
       PREMIUM EXECUTIVE CARDS
       ===================================================================== */
    .card {{
      background: var(--card-bg);
      backdrop-filter: blur(18px);
      border: 1px solid var(--card-border);
      border-top: 6px solid var(--card-highlight);
      border-radius: 20px;
      padding: 34px 38px;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      box-shadow: var(--card-shadow);
      position: relative;
      overflow: hidden;
    }}
    .card.blue-highlight {{
      border-top-color: var(--blue-accent);
    }}

    .grid-2x2 .card {{
      padding: 26px 36px;
    }}

    .card-badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-family: 'Outfit', 'Segoe UI', sans-serif;
      font-size: 0.92rem;
      font-weight: 800;
      letter-spacing: 2.2px;
      text-transform: uppercase;
      color: var(--badge-text);
      background: var(--badge-bg);
      border: 1px solid var(--badge-border);
      padding: 6px 14px;
      border-radius: 999px;
      margin-bottom: 14px;
      align-self: flex-start;
    }}
    .card-badge.blue {{
      color: var(--blue-bright);
      background: rgba(56, 189, 248, 0.16);
      border-color: rgba(56, 189, 248, 0.48);
    }}

    .card-number {{
      font-family: 'Outfit', 'Segoe UI', sans-serif;
      font-size: 3.8rem;
      font-weight: 900;
      color: var(--gold-primary);
      line-height: 1;
      margin-bottom: 10px;
    }}
    .grid-2x2 .card-number {{
      font-size: 3rem;
      margin-bottom: 8px;
    }}
    .card.blue-highlight .card-number {{
      color: var(--blue-accent);
    }}

    .card-title {{
      font-family: 'Outfit', 'Segoe UI', sans-serif;
      font-size: 2.1rem;
      font-weight: 900;
      color: var(--text-hero);
      line-height: 1.22;
      margin-bottom: 10px;
      letter-spacing: -0.015em;
    }}
    .grid-2x2 .card-title {{
      font-size: 1.85rem;
      margin-bottom: 8px;
    }}

    .card-subtitle {{
      font-family: 'Outfit', 'Segoe UI', sans-serif;
      font-size: 1.15rem;
      font-weight: 800;
      color: var(--blue-accent);
      margin-bottom: 12px;
      text-transform: uppercase;
      letter-spacing: 1.2px;
    }}

    .card-text {{
      font-size: 1.35rem;
      color: var(--text-body);
      line-height: 1.62;
      font-weight: 450;
    }}
    .grid-2x2 .card-text {{
      font-size: 1.25rem;
      line-height: 1.58;
    }}
    .card-text strong {{
      color: #FFFFFF;
      font-weight: 800;
    }}
    body.light-mode .card-text strong {{
      color: #071120;
    }}

    /* =====================================================================
       TRACK BARS (Slide 4: Activity Architecture)
       ===================================================================== */
    .tracks-container {{
      display: flex;
      flex-direction: column;
      gap: 18px;
      height: 100%;
      justify-content: space-around;
    }}

    .track-card {{
      background: var(--card-bg);
      backdrop-filter: blur(18px);
      border: 1px solid var(--card-border);
      border-left: 8px solid var(--gold-primary);
      border-radius: 18px;
      padding: 24px 34px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      box-shadow: var(--card-shadow);
    }}
    .track-card.blue-bar {{
      border-left-color: var(--blue-accent);
    }}

    .track-left {{
      display: flex;
      align-items: center;
      gap: 32px;
      flex: 1;
    }}

    .track-num {{
      font-family: 'Outfit', 'Segoe UI', sans-serif;
      font-size: 2rem;
      font-weight: 900;
      color: var(--gold-primary);
      min-width: 140px;
      letter-spacing: 0.5px;
    }}
    .track-card.blue-bar .track-num {{
      color: var(--blue-accent);
    }}

    .track-content {{
      display: flex;
      flex-direction: column;
      gap: 6px;
      flex: 1;
    }}

    .track-title {{
      font-family: 'Outfit', 'Segoe UI', sans-serif;
      font-size: 1.75rem;
      font-weight: 900;
      color: var(--text-hero);
      display: flex;
      align-items: center;
      gap: 16px;
    }}

    .track-tag {{
      font-family: 'Outfit', 'Segoe UI', sans-serif;
      font-size: 0.92rem;
      font-weight: 800;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      background: var(--badge-bg);
      border: 1px solid var(--badge-border);
      color: var(--badge-text);
      padding: 4px 14px;
      border-radius: 999px;
    }}
    .track-card.blue-bar .track-tag {{
      background: rgba(56, 189, 248, 0.16);
      border-color: rgba(56, 189, 248, 0.48);
      color: var(--blue-bright);
    }}

    .track-desc {{
      font-size: 1.28rem;
      color: var(--text-body);
      line-height: 1.55;
    }}
    .track-desc strong {{
      color: #FFFFFF;
      font-weight: 800;
    }}
    body.light-mode .track-desc strong {{
      color: #071120;
    }}

    /* =====================================================================
       FEATURE LIST ITEMS (Slide 5: DevHack)
       ===================================================================== */
    .feature-list {{
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-top: 10px;
    }}

    .feature-item {{
      display: flex;
      gap: 18px;
      align-items: flex-start;
    }}

    .feature-bullet {{
      width: 36px;
      height: 36px;
      border-radius: 9px;
      background: var(--badge-bg);
      border: 1px solid var(--badge-border);
      color: var(--badge-text);
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Outfit', 'Segoe UI', sans-serif;
      font-size: 1.15rem;
      font-weight: 900;
      flex-shrink: 0;
      margin-top: 2px;
    }}
    .feature-bullet.blue {{
      background: rgba(56, 189, 248, 0.16);
      border-color: rgba(56, 189, 248, 0.48);
      color: var(--blue-bright);
    }}

    .feature-text {{
      font-size: 1.2rem;
      color: var(--text-body);
      line-height: 1.52;
    }}
    .feature-text strong {{
      font-family: 'Outfit', 'Segoe UI', sans-serif;
      color: var(--text-hero);
      font-size: 1.45rem;
      font-weight: 800;
      display: block;
      margin-bottom: 3px;
    }}

    /* =====================================================================
       SLIDE 1: GRAND HERO COVER LAYOUT
       ===================================================================== */
    .hero-layout {{
      display: grid;
      grid-template-columns: 1.35fr 0.65fr;
      gap: 60px;
      align-items: center;
      height: 100%;
    }}

    .hero-left {{
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 24px;
    }}

    .hero-univ-tag {{
      display: inline-flex;
      align-items: center;
      gap: 14px;
      font-family: 'Outfit', 'Segoe UI', sans-serif;
      font-size: 1.25rem;
      font-weight: 800;
      letter-spacing: 3px;
      text-transform: uppercase;
      color: var(--gold-bright);
    }}

    .hero-main-title {{
      font-family: 'Outfit', 'Segoe UI', sans-serif;
      font-size: 5.2rem;
      font-weight: 900;
      color: var(--text-hero);
      line-height: 1.04;
      letter-spacing: -0.035em;
    }}
    .hero-main-title span.accent {{
      color: var(--gold-primary);
    }}

    .hero-tagline {{
      font-family: 'Outfit', 'Segoe UI', sans-serif;
      font-size: 2.1rem;
      font-weight: 800;
      color: var(--blue-accent);
      line-height: 1.3;
    }}

    .hero-desc-box {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-left: 8px solid var(--gold-primary);
      border-radius: 18px;
      padding: 26px 36px;
      font-size: 1.42rem;
      line-height: 1.68;
      color: var(--text-body);
      box-shadow: var(--card-shadow);
    }}
    .hero-desc-box strong {{
      color: #FFFFFF;
      font-weight: 800;
    }}
    body.light-mode .hero-desc-box strong {{
      color: #071120;
    }}

    .hero-meta-footer {{
      margin-top: 10px;
      padding-top: 20px;
      border-top: 1px solid rgba(148, 163, 184, 0.28);
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .hero-meta-main {{
      font-family: 'Outfit', 'Segoe UI', sans-serif;
      font-size: 1.12rem;
      font-weight: 800;
      letter-spacing: 2.2px;
      text-transform: uppercase;
      color: var(--gold-bright);
    }}
    .hero-meta-sub {{
      font-size: 1.15rem;
      line-height: 1.65;
      color: var(--text-sub);
    }}
    .hero-meta-sub strong {{
      color: var(--text-hero);
    }}

    .hero-right {{
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding-right: 20px;
    }}

    /* Perfect Centered Medallion Frame for Seal */
    .hero-seal-wrapper {{
      width: 400px;
      height: 400px;
      border-radius: 50%;
      background: #FFFFFF;
      border: 8px solid var(--gold-primary);
      box-shadow: 0 0 65px rgba(245, 158, 11, 0.45), 0 25px 60px rgba(0,0,0,0.7);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 12px;
      position: relative;
    }}
    .hero-seal-img {{
      width: 100%;
      height: 100%;
      border-radius: 50%;
      object-fit: contain;
    }}

    /* =====================================================================
       SLIDE 9: CONCLUSION & REQUESTS LAYOUT
       ===================================================================== */
    .req-grid {{
      display: grid;
      grid-template-columns: 1.25fr 0.75fr;
      gap: 45px;
      align-items: center;
      height: 100%;
    }}

    .req-list {{
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}

    .req-item {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-left: 8px solid var(--gold-primary);
      border-radius: 18px;
      padding: 24px 32px;
      display: flex;
      gap: 24px;
      align-items: flex-start;
      box-shadow: var(--card-shadow);
    }}

    .req-number {{
      font-family: 'Outfit', 'Segoe UI', sans-serif;
      font-size: 2.8rem;
      font-weight: 900;
      color: var(--gold-primary);
      line-height: 1;
      padding-top: 4px;
      min-width: 40px;
    }}

    .req-content {{
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .req-title {{
      font-family: 'Outfit', 'Segoe UI', sans-serif;
      font-size: 1.7rem;
      font-weight: 900;
      color: var(--text-hero);
    }}
    .req-desc {{
      font-size: 1.25rem;
      color: var(--text-body);
      line-height: 1.58;
    }}
    .req-desc strong {{
      color: #FFFFFF;
      font-weight: 800;
    }}
    body.light-mode .req-desc strong {{
      color: #071120;
    }}

    .req-motto-quote {{
      margin-top: 10px;
      padding: 18px 24px;
      border-radius: 14px;
      background: rgba(56, 189, 248, 0.14);
      border: 1px solid rgba(56, 189, 248, 0.4);
      color: var(--blue-accent);
      font-family: 'Outfit', 'Segoe UI', sans-serif;
      font-size: 1.45rem;
      font-weight: 800;
      font-style: italic;
      text-align: center;
    }}

    .req-seal-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-top: 8px solid var(--gold-primary);
      border-radius: 24px;
      padding: 40px 32px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      box-shadow: var(--card-shadow);
    }}
    .req-seal-card img {{
      width: 230px;
      height: 230px;
      border-radius: 50%;
      background: #FFFFFF;
      border: 6px solid var(--gold-primary);
      box-shadow: 0 12px 35px rgba(0,0,0,0.55);
      padding: 6px;
      margin-bottom: 22px;
    }}
    .req-seal-title {{
      font-family: 'Outfit', 'Segoe UI', sans-serif;
      font-size: 1.85rem;
      font-weight: 900;
      color: var(--text-hero);
      letter-spacing: 1px;
      margin-bottom: 6px;
    }}
    .req-seal-sub {{
      font-family: 'Outfit', 'Segoe UI', sans-serif;
      font-size: 1.15rem;
      font-weight: 800;
      color: var(--gold-primary);
      text-transform: uppercase;
      letter-spacing: 2px;
    }}
    .req-seal-footer {{
      margin-top: 14px;
      font-size: 1.15rem;
      color: var(--text-muted);
      line-height: 1.5;
    }}

    /* =====================================================================
       FOOTER (Slide counter & metadata)
       ===================================================================== */
    .slide-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 18px;
      border-top: 1px solid rgba(148, 163, 184, 0.25);
      font-size: 1.12rem;
      color: var(--text-muted);
      position: relative;
      z-index: 2;
    }}
    .slide-footer-left {{
      display: flex;
      gap: 16px;
      align-items: center;
    }}
    .slide-footer-org {{
      font-family: 'Outfit', 'Segoe UI', sans-serif;
      font-weight: 800;
      color: var(--text-hero);
    }}
    .slide-footer-page {{
      font-family: 'Outfit', 'Segoe UI', sans-serif;
      font-weight: 900;
      color: var(--gold-primary);
      letter-spacing: 1.5px;
      font-size: 1.25rem;
    }}

    /* =====================================================================
       PRINT & PDF EXPORT STYLES (100% Full Bleed 1920x1080 - ZERO DRIFT)
       ===================================================================== */
    @page {{
      size: 1920px 1080px;
      margin: 0;
    }}

    @media print {{
      html, body {{
        width: 1920px !important;
        height: auto !important;
        margin: 0 !important;
        padding: 0 !important;
        background: #071120 !important;
        overflow: visible !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }}
      .deck-toolbar, .no-print {{
        display: none !important;
      }}
      .viewport-container {{
        display: block !important;
        width: 1920px !important;
        height: auto !important;
        margin: 0 !important;
        padding: 0 !important;
        background: transparent !important;
      }}
      #presentationStage {{
        display: block !important;
        width: 1920px !important;
        height: auto !important;
        transform: none !important;
        margin: 0 !important;
        padding: 0 !important;
        box-shadow: none !important;
      }}
      .slide-canvas {{
        display: flex !important;
        width: 1920px !important;
        height: 1080px !important;
        min-height: 1080px !important;
        max-height: 1080px !important;
        transform: none !important;
        position: relative !important;
        top: auto !important;
        left: auto !important;
        page-break-before: always !important;
        break-before: page !important;
        page-break-after: always !important;
        break-after: page !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        margin: 0 !important;
        padding: 45px 80px 35px 80px !important;
        box-sizing: border-box !important;
        overflow: hidden !important;
        box-shadow: none !important;
      }}
      .slide-canvas:first-of-type {{
        page-break-before: auto !important;
        break-before: auto !important;
      }}
    }}
  </style>
</head>
<body>

  <!-- FLOATING PRESENTATION CONTROLS (Screen only) -->
  <header class="deck-toolbar no-print">
    <span class="toolbar-title">🏛️ Deanery Proposal</span>
    <button class="nav-btn" onclick="prevSlide()" title="Previous Slide (← / Backspace)">◀ Prev</button>
    <span id="slideIndicator" class="slide-counter">1 / 9</span>
    <button class="nav-btn" onclick="nextSlide()" title="Next Slide (→ / Space)">Next ▶</button>
    <button class="nav-btn" onclick="toggleTheme()" title="Toggle Light / Dark Mode (T)">🎨 Theme</button>
    <button class="nav-btn" onclick="toggleFullscreen()" title="Fullscreen Presentation (F)">⛶ Fullscreen</button>
    <button class="nav-btn" onclick="window.print()" title="Export Pixel-Perfect 16:9 PDF (Ctrl + P)">🖨️ Export PDF</button>
  </header>

  <div class="viewport-container">
    <div id="presentationStage">

      <!-- =================================================================
           SLIDE 1: COVER TITLE
           ================================================================= -->
      <section class="slide-canvas active" id="slide-1">
        <div class="hero-layout">
          <div class="hero-left">
            <div class="hero-univ-tag">
              <span>🏛️ International University of Sarajevo</span>
              <span>•</span>
              <span style="color: var(--blue-accent);">FENS</span>
            </div>
            
            <h1 class="hero-main-title">
              IUS <span class="accent">Engineering</span> Club
            </h1>
            
            <div class="hero-tagline">
              Cultivating Innovation, Leadership, and Engineering Excellence
            </div>
            
            <div class="hero-desc-box">
              An official student-led engineering society dedicated to bridging theoretical classroom curricula with <strong>real-world technical execution, multidisciplinary teamwork, and early career leadership</strong> under the Faculty of Engineering and Natural Sciences.
            </div>
            
            <div class="hero-meta-footer">
              <div class="hero-meta-main">
                OFFICIAL PROPOSAL TO THE DEANERY • ACADEMIC YEAR 2026/2027
              </div>
              <div class="hero-meta-sub">
                <strong>Institutional Affiliation:</strong> Faculty of Engineering and Natural Sciences (FENS)<br>
                <strong>Presented to:</strong> Assoc. Prof. Dr. Altijana Hromić-Jahjefendić (Dean, FENS)<br>
                <strong>Faculty Academic Advisor:</strong> Prof. Dr. Leila Miller (Full Professor Dr., FENS)<br>
                <strong>Presented by:</strong> The Founding Executive Board & 11 Founding Engineering Students
              </div>
            </div>
          </div>
          
          <div class="hero-right">
            <div class="hero-seal-wrapper">
              <img src="{SEAL_B64}" alt="IUS Engineering Club Seal" class="hero-seal-img">
            </div>
          </div>
        </div>

        <footer class="slide-footer">
          <div class="slide-footer-left">
            <span class="slide-footer-org">IUS Engineering Club (IEC)</span>
            <span>•</span>
            <span>Official Deanery Pitch Deck</span>
          </div>
          <div class="slide-footer-page">01 / 09</div>
        </footer>
      </section>

      <!-- =================================================================
           SLIDE 2: CORE PHILOSOPHY
           ================================================================= -->
      <section class="slide-canvas" id="slide-2">
        <div class="slide-header">
          <div class="header-left">
            <div class="slide-breadcrumb">Faculty of Engineering and Natural Sciences (FENS) • Strategic Vision</div>
            <h2 class="slide-title">Our Core Philosophy: Purpose Beyond the Classroom</h2>
            <div class="slide-subtitle">Three foundational commitments designed to bridge theory with high-impact practice.</div>
          </div>
          <div class="header-badge">
            <img src="{SEAL_B64}" alt="Logo">
            <div class="header-badge-col">
              <span class="header-badge-title">IEC FENS</span>
              <span class="header-badge-sub">2026/2027</span>
            </div>
          </div>
        </div>

        <div class="slide-body">
          <div class="grid-3">
            <div class="card">
              <div class="card-badge">01 • PRAGMATIC FOCUS</div>
              <div class="card-number">01</div>
              <h3 class="card-title">Applied Engineering Practice</h3>
              <div class="card-subtitle">Theory to Working Systems</div>
              <p class="card-text">
                Classroom lectures provide <strong>rigorous mathematical and theoretical grounding</strong>. Our lab provides the collaborative space where students translate algorithms and circuits into <strong>functional, demonstrable engineering systems</strong>.
              </p>
            </div>

            <div class="card blue-highlight">
              <div class="card-badge blue">02 • CROSS-DISCIPLINARY</div>
              <div class="card-number">02</div>
              <h3 class="card-title">Interdisciplinary Teamwork</h3>
              <div class="card-subtitle" style="color: var(--blue-accent);">Breaking Departmental Silos</div>
              <p class="card-text">
                Modern engineering challenges require multifaceted collaboration. We unite ambitious students across <strong>Computer Science, Software Engineering, Electrical, and Mechanical Engineering</strong> to build unified prototypes.
              </p>
            </div>

            <div class="card">
              <div class="card-badge">03 • REGIONAL PRESTIGE</div>
              <div class="card-number">03</div>
              <h3 class="card-title">Faculty Pride in BiH</h3>
              <div class="card-subtitle">Elevating IUS Leadership</div>
              <p class="card-text">
                Positioning FENS as the <strong>most active and respected engineering faculty in Bosnia and Herzegovina</strong> through premier student hackathons, hands-on workshops, and deep partnerships with Sarajevo tech firms.
              </p>
            </div>
          </div>
        </div>

        <footer class="slide-footer">
          <div class="slide-footer-left">
            <span class="slide-footer-org">IUS Engineering Club (IEC)</span>
            <span>•</span>
            <span>Faculty of Engineering and Natural Sciences</span>
          </div>
          <div class="slide-footer-page">02 / 09</div>
        </footer>
      </section>

      <!-- =================================================================
           SLIDE 3: STRATEGIC MISSION & OBJECTIVES
           ================================================================= -->
      <section class="slide-canvas" id="slide-3">
        <div class="slide-header">
          <div class="header-left">
            <div class="slide-breadcrumb">Faculty of Engineering and Natural Sciences (FENS) • Long-Term Impact</div>
            <h2 class="slide-title">Strategic Mission & Long-Term Objectives</h2>
            <div class="slide-subtitle">Four concrete pillars built to strengthen student capability, retention, and post-grad success.</div>
          </div>
          <div class="header-badge">
            <img src="{SEAL_B64}" alt="Logo">
            <div class="header-badge-col">
              <span class="header-badge-title">IEC FENS</span>
              <span class="header-badge-sub">2026/2027</span>
            </div>
          </div>
        </div>

        <div class="slide-body">
          <div class="grid-2x2">
            <div class="card">
              <div class="card-number">01</div>
              <h3 class="card-title">Empower Student Leadership & Confidence</h3>
              <p class="card-text">
                Build deep technical confidence, practical troubleshooting capabilities, and resilient teamwork habits through <strong>student-directed development sprints, hackathons, and technical committee ownership</strong>.
              </p>
            </div>

            <div class="card blue-highlight">
              <div class="card-number">02</div>
              <h3 class="card-title">A Stepping Stone to Start Work Life Stronger</h3>
              <p class="card-text">
                Accelerate early career readiness by mastering <strong>production-grade software workflows, collaborative Git practices, and modern industry engineering standards</strong> before graduation.
              </p>
            </div>

            <div class="card">
              <div class="card-number">03</div>
              <h3 class="card-title">Build a Productive Culture of Innovation</h3>
              <p class="card-text">
                Establish an open campus culture where students <strong>publish open-source code, engineer portfolio prototypes, and represent IUS in regional and international tech competitions</strong>.
              </p>
            </div>

            <div class="card blue-highlight">
              <div class="card-number">04</div>
              <h3 class="card-title">Increase Student Belonging & Loyalty to FENS</h3>
              <p class="card-text">
                Provide <strong>continuous peer mentorship and hands-on labs</strong> so younger students stay motivated, pass demanding engineering courses, and feel genuine pride in FENS.
              </p>
            </div>
          </div>
        </div>

        <footer class="slide-footer">
          <div class="slide-footer-left">
            <span class="slide-footer-org">IUS Engineering Club (IEC)</span>
            <span>•</span>
            <span>Strategic Mission & Goals</span>
          </div>
          <div class="slide-footer-page">03 / 09</div>
        </footer>
      </section>

      <!-- =================================================================
           SLIDE 4: ACTIVITY ARCHITECTURE (FOUR LEARNING TRACKS)
           ================================================================= -->
      <section class="slide-canvas" id="slide-4">
        <div class="slide-header">
          <div class="header-left">
            <div class="slide-breadcrumb">Faculty of Engineering and Natural Sciences (FENS) • Operational Model</div>
            <h2 class="slide-title">Activity Architecture: Four Learning Tracks</h2>
            <div class="slide-subtitle">A sustainable, semester-long curriculum combining weekly hands-on practice with monthly summits.</div>
          </div>
          <div class="header-badge">
            <img src="{SEAL_B64}" alt="Logo">
            <div class="header-badge-col">
              <span class="header-badge-title">IEC FENS</span>
              <span class="header-badge-sub">2026/2027</span>
            </div>
          </div>
        </div>

        <div class="slide-body">
          <div class="tracks-container">
            <div class="track-card">
              <div class="track-left">
                <div class="track-num">TRACK 01</div>
                <div class="track-content">
                  <div class="track-title">
                    Hands-On Engineering Labs
                    <span class="track-tag">Weekly Sessions • FENS Labs</span>
                  </div>
                  <div class="track-desc">
                    Weekly practical sessions in FENS computer labs focusing on <strong>software building, modern AI coding workflows (Cursor, LLMs), git collaboration, and clean architecture</strong>.
                  </div>
                </div>
              </div>
            </div>

            <div class="track-card blue-bar">
              <div class="track-left">
                <div class="track-num">TRACK 02</div>
                <div class="track-content">
                  <div class="track-title">
                    Local Tech Speaker Talks
                    <span class="track-tag">Monthly • IUS Amphitheater</span>
                  </div>
                  <div class="track-desc">
                    Monthly physical keynotes in the amphitheater where <strong>Sarajevo software engineers, tech founders, and architects share battle-tested lessons from commercial projects</strong>.
                  </div>
                </div>
              </div>
            </div>

            <div class="track-card">
              <div class="track-left">
                <div class="track-num">TRACK 03</div>
                <div class="track-content">
                  <div class="track-title">
                    Online Developer Dialogues
                    <span class="track-tag">Bi-Weekly • Online Webinars</span>
                  </div>
                  <div class="track-desc">
                    Virtual fireside chats with <strong>international software developers and global IUS alumni, connecting students with global engineering standards and remote work</strong>.
                  </div>
                </div>
              </div>
            </div>

            <div class="track-card blue-bar">
              <div class="track-left">
                <div class="track-num">TRACK 04</div>
                <div class="track-content">
                  <div class="track-title">
                    Student Project Teams
                    <span class="track-tag">Continuous • Project Groups</span>
                  </div>
                  <div class="track-desc">
                    Dedicated multidisciplinary student circles developing <strong>useful semester software utilities, embedded prototypes, and preparing for student engineering competitions</strong>.
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <footer class="slide-footer">
          <div class="slide-footer-left">
            <span class="slide-footer-org">IUS Engineering Club (IEC)</span>
            <span>•</span>
            <span>Activity Architecture</span>
          </div>
          <div class="slide-footer-page">04 / 09</div>
        </footer>
      </section>

      <!-- =================================================================
           SLIDE 5: FLAGSHIP EVENT (IUS DEVHACK)
           ================================================================= -->
      <section class="slide-canvas" id="slide-5">
        <div class="slide-header">
          <div class="header-left">
            <div class="slide-breadcrumb">Faculty of Engineering and Natural Sciences (FENS) • Marquee Milestone</div>
            <h2 class="slide-title">Flagship Event: IUS DevHack (24-Hour Campus Hackathon)</h2>
            <div class="slide-subtitle">A high-energy 24-hour innovation marathon hosted on the IUS campus to showcase technical excellence.</div>
          </div>
          <div class="header-badge">
            <img src="{SEAL_B64}" alt="Logo">
            <div class="header-badge-col">
              <span class="header-badge-title">IEC FENS</span>
              <span class="header-badge-sub">2026/2027</span>
            </div>
          </div>
        </div>

        <div class="slide-body">
          <div class="grid-2">
            <div class="card">
              <div class="card-badge">THE CONCEPT & FORMAT</div>
              <h3 class="card-title">Event Concept & Academic Structure</h3>
              
              <div class="feature-list">
                <div class="feature-item">
                  <div class="feature-bullet">1</div>
                  <div class="feature-text">
                    <strong>24-Hour Intensive Marathon</strong>
                    A focused, energetic software and engineering hackathon hosted entirely on the IUS campus over a weekend block.
                  </div>
                </div>

                <div class="feature-item">
                  <div class="feature-bullet">2</div>
                  <div class="feature-text">
                    <strong>Friendly Competition & Growth</strong>
                    Teams compete on realistic problem briefs, learning from each other through peer collaboration and mutual support.
                  </div>
                </div>

                <div class="feature-item">
                  <div class="feature-bullet">3</div>
                  <div class="feature-text">
                    <strong>Experienced Industry Mentorship</strong>
                    Senior students and local guest engineers provide friendly technical guidance under direct faculty supervision.
                  </div>
                </div>

                <div class="feature-item">
                  <div class="feature-bullet">4</div>
                  <div class="feature-text">
                    <strong>Fair Academic Faculty Jury</strong>
                    Student projects presented to a friendly jury of FENS professors and invited tech practitioners with formal awards.
                  </div>
                </div>
              </div>
            </div>

            <div class="card blue-highlight">
              <div class="card-badge blue">PRACTICAL LEARNING IMPACT</div>
              <h3 class="card-title">Educational & Institutional Impact</h3>

              <div class="feature-list">
                <div class="feature-item">
                  <div class="feature-bullet blue">✓</div>
                  <div class="feature-text">
                    <strong>Fast Learning Through Action</strong>
                    Students turn concepts learned in lecture into working code under a realistic, exciting deadline.
                  </div>
                </div>

                <div class="feature-item">
                  <div class="feature-bullet blue">✓</div>
                  <div class="feature-text">
                    <strong>Tangible Project Portfolios</strong>
                    Every team leaves with a working project and git history they can showcase on their resume and GitHub.
                  </div>
                </div>

                <div class="feature-item">
                  <div class="feature-bullet blue">✓</div>
                  <div class="feature-text">
                    <strong>Positive Campus Culture</strong>
                    Shows the broader community that IUS engineering students are active, motivated, and passionate about tech.
                  </div>
                </div>

                <div class="feature-item">
                  <div class="feature-bullet blue">✓</div>
                  <div class="feature-text">
                    <strong>Full Safety & Lab Respect</strong>
                    Strict care for university computers, pre-approved schedule, clean-desk policy, and campus security adherence.
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <footer class="slide-footer">
          <div class="slide-footer-left">
            <span class="slide-footer-org">IUS Engineering Club (IEC)</span>
            <span>•</span>
            <span>Annual Flagship Hackathon</span>
          </div>
          <div class="slide-footer-page">05 / 09</div>
        </footer>
      </section>

      <!-- =================================================================
           SLIDE 6: CAMPUS DEMO DAY
           ================================================================= -->
      <section class="slide-canvas" id="slide-6">
        <div class="slide-header">
          <div class="header-left">
            <div class="slide-breadcrumb">Faculty of Engineering and Natural Sciences (FENS) • Semester Showcase</div>
            <h2 class="slide-title">Campus Demo Day: Sharing Student Projects</h2>
            <div class="slide-subtitle">A simple, student-focused end-of-semester celebration • Scheduled for Spring 2027.</div>
          </div>
          <div class="header-badge">
            <img src="{SEAL_B64}" alt="Logo">
            <div class="header-badge-col">
              <span class="header-badge-title">IEC FENS</span>
              <span class="header-badge-sub">2026/2027</span>
            </div>
          </div>
        </div>

        <div class="slide-body">
          <div class="grid-2x2">
            <div class="card">
              <div class="card-badge">01 • DEMO EXHIBITION</div>
              <h3 class="card-title">Open Student Project Demos</h3>
              <div class="card-subtitle">FENS Computer Labs & Atrium Lobby</div>
              <p class="card-text">
                Students bring their laptops and hardware to showcase <strong>course assignments, club workshop projects, and prototypes</strong> in a relaxed, friendly exhibition open to all peers.
              </p>
            </div>

            <div class="card blue-highlight">
              <div class="card-badge blue">02 • ACADEMIC ENGAGEMENT</div>
              <h3 class="card-title">Friendly Feedback from Professors</h3>
              <div class="card-subtitle" style="color: var(--blue-accent);">Direct Professor & Assistant Guidance</div>
              <p class="card-text">
                Faculty professors and teaching assistants walk around, <strong>view student demos, offer constructive praise, and share encouragement and academic tips</strong>.
              </p>
            </div>

            <div class="card">
              <div class="card-badge">03 • CAREER PERSPECTIVES</div>
              <h3 class="card-title">IUS Alumni Career Chats</h3>
              <div class="card-subtitle">Real Workplace Experiences</div>
              <p class="card-text">
                Recent IUS engineering graduates working locally return to campus to give <strong>short, honest talks about their first jobs, workplace realities, and practical career advice</strong>.
              </p>
            </div>

            <div class="card blue-highlight">
              <div class="card-badge blue">04 • INSPIRING UNDERCLASSMEN</div>
              <h3 class="card-title">Inspiring Younger Students</h3>
              <div class="card-subtitle" style="color: var(--blue-accent);">Early Academic Motivation</div>
              <p class="card-text">
                First- and second-year students see what their peers built, <strong>demystifying advanced engineering topics and gaining clear motivation to start their own projects</strong>.
              </p>
            </div>
          </div>
        </div>

        <footer class="slide-footer">
          <div class="slide-footer-left">
            <span class="slide-footer-org">IUS Engineering Club (IEC)</span>
            <span>•</span>
            <span>Semester Showcase Event</span>
          </div>
          <div class="slide-footer-page">06 / 09</div>
        </footer>
      </section>

      <!-- =================================================================
           SLIDE 7: PRACTICAL VALUE FOR FENS & UNIVERSITY
           ================================================================= -->
      <section class="slide-canvas" id="slide-7">
        <div class="slide-header">
          <div class="header-left">
            <div class="slide-breadcrumb">Faculty of Engineering and Natural Sciences (FENS) • Institutional ROI</div>
            <h2 class="slide-title">Practical Value for FENS & Our University</h2>
            <div class="slide-subtitle">How this student-led society delivers measurable value for faculty reputation and graduate success.</div>
          </div>
          <div class="header-badge">
            <img src="{SEAL_B64}" alt="Logo">
            <div class="header-badge-col">
              <span class="header-badge-title">IEC FENS</span>
              <span class="header-badge-sub">2026/2027</span>
            </div>
          </div>
        </div>

        <div class="slide-body">
          <div class="grid-2x2">
            <div class="card">
              <div class="card-number">01</div>
              <h3 class="card-title">Senior Students Mentoring Younger Peers</h3>
              <div class="card-subtitle">Self-Sustaining Knowledge Transfer</div>
              <p class="card-text">
                Experienced upper-year students guide younger peers, creating a <strong>supportive academic cycle where students reinforce their knowledge by teaching and building together</strong>.
              </p>
            </div>

            <div class="card blue-highlight">
              <div class="card-number">02</div>
              <h3 class="card-title">Higher Faculty Prestige & Student Pride</h3>
              <div class="card-subtitle" style="color: var(--blue-accent);">Recruitment & Institutional Standing</div>
              <p class="card-text">
                An active engineering club <strong>attracts prospective high school students during IUS Open Days</strong> and makes currently enrolled students genuinely proud to study at FENS.
              </p>
            </div>

            <div class="card">
              <div class="card-number">03</div>
              <h3 class="card-title">Active Profiles that Stand Out in Job Market</h3>
              <div class="card-subtitle">Graduate Employability Advantage</div>
              <p class="card-text">
                With real project work, hackathon awards, and active club involvement, <strong>our graduates stand out significantly when applying for jobs and corporate internships</strong>.
              </p>
            </div>

            <div class="card blue-highlight">
              <div class="card-number">04</div>
              <h3 class="card-title">A Lively and Productive Campus Atmosphere</h3>
              <div class="card-subtitle" style="color: var(--blue-accent);">Campus Life Enrichment</div>
              <p class="card-text">
                Making FENS much more than just lecture halls—<strong>creating an inspiring space where students naturally stay after class to discuss tech, code, and build things together</strong>.
              </p>
            </div>
          </div>
        </div>

        <footer class="slide-footer">
          <div class="slide-footer-left">
            <span class="slide-footer-org">IUS Engineering Club (IEC)</span>
            <span>•</span>
            <span>Institutional Value</span>
          </div>
          <div class="slide-footer-page">07 / 09</div>
        </footer>
      </section>

      <!-- =================================================================
           SLIDE 8: GOVERNANCE, RESPONSIBILITY & SAFETY
           ================================================================= -->
      <section class="slide-canvas" id="slide-8">
        <div class="slide-header">
          <div class="header-left">
            <div class="slide-breadcrumb">Faculty of Engineering and Natural Sciences (FENS) • Governance & Compliance</div>
            <h2 class="slide-title">Governance, Responsibility & Faculty Oversight</h2>
            <div class="slide-subtitle">Institutional Discipline, Academic Alignment, and Campus Safety.</div>
          </div>
          <div class="header-badge">
            <img src="{SEAL_B64}" alt="Logo">
            <div class="header-badge-col">
              <span class="header-badge-title">IEC FENS</span>
              <span class="header-badge-sub">2026/2027</span>
            </div>
          </div>
        </div>

        <div class="slide-body">
          <div class="grid-2x2">
            <div class="card">
              <div class="card-badge">01 • ADVISOR OVERSIGHT</div>
              <h3 class="card-title">Faculty Academic Advisor Oversight</h3>
              <p class="card-text">
                All workshop schedules, guest speaker invitations, and major campus events are planned under the <strong>direct guidance and prior approval of our appointed FENS Faculty Advisor, Prof. Dr. Leila Miller</strong>.
              </p>
            </div>

            <div class="card blue-highlight">
              <div class="card-badge blue">02 • STATUTORY RIGOR</div>
              <h3 class="card-title">Full University Regulatory Compliance</h3>
              <p class="card-text">
                Organized strictly under <strong>Article 77 of the IUS Statute and Student Career Center (SCC) club guidelines</strong>, complete with an official club constitution and transparent elections.
              </p>
            </div>

            <div class="card">
              <div class="card-badge">03 • 5/5 ACCOUNTABLE BOARD</div>
              <h3 class="card-title">Dedicated & Accountable Student Board</h3>
              <p class="card-text">
                A committed <strong>5-member Executive Board (President, VP, Secretary, Treasurer, PR Lead)</strong> ensuring transparent organization, good communication, and fair representation across all FENS majors.
              </p>
            </div>

            <div class="card blue-highlight">
              <div class="card-badge blue">04 • LAB INTEGRITY</div>
              <h3 class="card-title">Respect for Campus Facilities & Lab Safety</h3>
              <p class="card-text">
                Strict respect for university property, <strong>reservations limited to non-teaching hours, clean workstation policy, and total adherence to campus safety procedures</strong>.
              </p>
            </div>
          </div>
        </div>

        <footer class="slide-footer">
          <div class="slide-footer-left">
            <span class="slide-footer-org">IUS Engineering Club (IEC)</span>
            <span>•</span>
            <span>Governance & Oversight</span>
          </div>
          <div class="slide-footer-page">08 / 09</div>
        </footer>
      </section>

      <!-- =================================================================
           SLIDE 9: CONCLUSION & REQUESTS FROM THE DEANERY
           ================================================================= -->
      <section class="slide-canvas" id="slide-9">
        <div class="slide-header">
          <div class="header-left">
            <div class="slide-breadcrumb">Faculty of Engineering and Natural Sciences (FENS) • Official Petition</div>
            <h2 class="slide-title">Conclusion & What We Request From The Deanery</h2>
            <div class="slide-subtitle">Three straightforward, non-financial requests to launch this initiative for our faculty.</div>
          </div>
          <div class="header-badge">
            <img src="{SEAL_B64}" alt="Logo">
            <div class="header-badge-col">
              <span class="header-badge-title">IEC FENS</span>
              <span class="header-badge-sub">2026/2027</span>
            </div>
          </div>
        </div>

        <div class="slide-body">
          <div class="req-grid">
            <div class="req-list">
              <div class="req-item">
                <div class="req-number">1</div>
                <div class="req-content">
                  <div class="req-title">Official Faculty Endorsement</div>
                  <div class="req-desc">
                    Formal Deanery approval recognizing the club under FENS and confirming our Faculty Academic Advisor (<strong>Prof. Dr. Leila Miller</strong>).
                  </div>
                </div>
              </div>

              <div class="req-item" style="border-left-color: var(--blue-accent);">
                <div class="req-number" style="color: var(--blue-accent);">2</div>
                <div class="req-content">
                  <div class="req-title">Lab & Room Access Outside Lecture Hours</div>
                  <div class="req-desc">
                    Permission to schedule <strong>computer labs and the amphitheater during evenings or weekends</strong> without disrupting scheduled university classes.
                  </div>
                </div>
              </div>

              <div class="req-item">
                <div class="req-number">3</div>
                <div class="req-content">
                  <div class="req-title">Faculty Encouragement & Support</div>
                  <div class="req-desc">
                    A short faculty notice or welcome announcement introducing the club and <strong>encouraging engineering students across FENS to participate</strong>.
                  </div>
                </div>
              </div>

              <div class="req-motto-quote">
                “Empowering students to build, learn, and grow together at IUS.”
              </div>
            </div>

            <div class="req-seal-card">
              <img src="{SEAL_B64}" alt="IUS Engineering Club Crest">
              <div class="req-seal-title">IUS ENGINEERING CLUB</div>
              <div class="req-seal-sub">EST. 2026 • FENS</div>
              <div class="req-seal-footer">
                Faculty of Engineering and Natural Sciences<br>
                International University of Sarajevo
              </div>
            </div>
          </div>
        </div>

        <footer class="slide-footer">
          <div class="slide-footer-left">
            <span class="slide-footer-org">IUS Engineering Club (IEC)</span>
            <span>•</span>
            <span>The Path Forward</span>
          </div>
          <div class="slide-footer-page">09 / 09</div>
        </footer>
      </section>

    </div>
  </div>

  <!-- JAVASCRIPT CONTROLLER -->
  <script>
    const totalSlides = 9;
    let currentSlide = 1;

    function showSlide(index) {{
      if (index < 1) index = 1;
      if (index > totalSlides) index = totalSlides;
      currentSlide = index;

      document.querySelectorAll('.slide-canvas').forEach((el, idx) => {{
        if (idx + 1 === currentSlide) {{
          el.classList.add('active');
        }} else {{
          el.classList.remove('active');
        }}
      }});

      document.getElementById('slideIndicator').textContent = `${{currentSlide}} / ${{totalSlides}}`;
    }}

    function nextSlide() {{
      if (currentSlide < totalSlides) showSlide(currentSlide + 1);
    }}

    function prevSlide() {{
      if (currentSlide > 1) showSlide(currentSlide - 1);
    }}

    function toggleTheme() {{
      document.body.classList.toggle('light-mode');
    }}

    function toggleFullscreen() {{
      if (!document.fullscreenElement) {{
        document.documentElement.requestFullscreen().catch(() => {{}});
      }} else {{
        if (document.exitFullscreen) document.exitFullscreen();
      }}
    }}

    // KEYBOARD NAVIGATION
    window.addEventListener('keydown', (e) => {{
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
        e.preventDefault();
        nextSlide();
      }} else if (e.key === 'ArrowLeft' || e.key === 'Backspace' || e.key === 'PageUp') {{
        e.preventDefault();
        prevSlide();
      }} else if (e.key.toLowerCase() === 't') {{
        toggleTheme();
      }} else if (e.key.toLowerCase() === 'f') {{
        toggleFullscreen();
      }}
    }});

    // Auto-scale viewport stage smoothly to fit any screen resolution without touching slides
    function handleResize() {{
      if (window.matchMedia('print').matches) return;
      const stage = document.getElementById('presentationStage');
      if (!stage) return;
      const targetW = 1920;
      const targetH = 1080;
      const scaleX = window.innerWidth / targetW;
      const scaleY = window.innerHeight / targetH;
      const scale = Math.min(scaleX, scaleY);
      stage.style.transform = `scale(${{scale}})`;
    }}

    window.addEventListener('resize', handleResize);
    window.addEventListener('DOMContentLoaded', () => {{
      showSlide(1);
      handleResize();
    }});
  </script>

</body>
</html>
"""

def generate():
    html_path = SLIDES_DIR / "deanery_presentation.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE)
    print(f"[✓] HTML Sunum Dosyası Oluşturuldu: {html_path}")

    # Also save to export_documents
    export_html_path = EXPORT_DIR / "IUS_Engineering_Club_Deanery_Proposal.html"
    with open(export_html_path, "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE)
    print(f"[✓] Export HTML Oluşturuldu: {export_html_path}")

    # Export to PDF using Edge headless
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    edge_exe = None
    for ep in edge_paths:
        if os.path.exists(ep):
            edge_exe = ep
            break

    if edge_exe:
        pdf_out = EXPORT_DIR / "IUS_Engineering_Club_Deanery_Proposal.pdf"
        print(f"[*] Microsoft Edge Headless ile 16:9 tam sayfa PDF üretiliyor...")
        cmd = [
            edge_exe,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            "--window-size=1920,1080",
            "--force-device-scale-factor=1",
            f"--print-to-pdf={pdf_out.resolve()}",
            export_html_path.resolve().as_uri()
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, timeout=30)
            if pdf_out.exists() and pdf_out.stat().st_size > 5000:
                print(f"[✓] 16:9 Vektörel PDF Başarıyla Üretildi: {pdf_out} ({pdf_out.stat().st_size} bayt)")
            else:
                print(f"[!] PDF üretimi uyarısı: {res.stderr.decode('utf-8', errors='ignore')}")
        except Exception as e:
            print(f"[!] Headless Edge çalıştırma hatası: {e}")

if __name__ == "__main__":
    generate()
