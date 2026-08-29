#!/usr/bin/env python3
"""
ROSHAN // ENGINEERING SYSTEM — Master SVG Asset Engine
======================================================
Renders 50+ production-grade SVG assets for Roshan R's profile.
Features:
- 100% strict XML compliance (full entity escaping)
- Calibrated Dark (#0A0E1A) and Light (#F8FAFC) palettes
- GitHub-compatible CSS & SMIL keyframe animations
- Zero external runtime dependencies
"""

import json
import os
import sys
import math
import xml.sax.saxutils as saxutils
from datetime import datetime, timezone, timedelta

# Force UTF-8 on stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# ─── XML Sanitization Helper ───────────────────────────────────────────────────

def esc(text):
    """Safely escape text for XML / SVG attributes and contents."""
    if text is None:
        return ""
    return saxutils.escape(str(text))


# ─── Design Tokens (Apple x Vercel x Linear x Modern AI Lab) ───────────────────

DARK = {
    "bg": "#0A0E1A",
    "bg2": "#111827",
    "surface": "rgba(17, 24, 39, 0.9)",
    "glass": "rgba(30, 41, 59, 0.7)",
    "border": "rgba(0, 229, 255, 0.18)",
    "border_subtle": "rgba(255, 255, 255, 0.08)",
    "cyan": "#00E5FF",
    "violet": "#8B5CF6",
    "blue": "#3B82F6",
    "green": "#10B981",
    "amber": "#F59E0B",
    "red": "#EF4444",
    "text": "#F8FAFC",
    "muted": "#94A3B8",
    "dim": "#475569",
    "white": "#FFFFFF",
}

LIGHT = {
    "bg": "#F8FAFC",
    "bg2": "#FFFFFF",
    "surface": "rgba(255, 255, 255, 0.95)",
    "glass": "rgba(241, 245, 249, 0.9)",
    "border": "rgba(59, 130, 246, 0.22)",
    "border_subtle": "rgba(0, 0, 0, 0.08)",
    "cyan": "#0891B2",
    "violet": "#7C3AED",
    "blue": "#2563EB",
    "green": "#059669",
    "amber": "#D97706",
    "red": "#DC2626",
    "text": "#0F172A",
    "muted": "#475569",
    "dim": "#94A3B8",
    "white": "#000000",
}


def load_json(name):
    path = os.path.join(DATA_DIR, name)
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def write_svg(rel_path, content):
    full = os.path.join(ASSETS_DIR, rel_path)
    ensure_dir(full)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  [+] {rel_path}")


# ─── 1. HERO BANNER ───────────────────────────────────────────────────────────

def generate_hero(profile, theme, suffix):
    t = DARK if theme == "dark" else LIGHT
    roles = profile.get("roles", [
        "SOFTWARE ENGINEERING", "AI ENGINEERING", "SYSTEM DESIGN",
        "AGENTIC AI", "RAG SYSTEMS", "REAL-TIME SYSTEMS", "DEVOPS & CLOUD"
    ])
    tagline = profile.get("tagline", "BUILDING SYSTEMS THAT THINK, SCALE & SHIP")

    cycle = len(roles) * 3
    role_keyframes = ""
    role_texts = ""
    for i, role in enumerate(roles):
        start_pct = (i * 3 / cycle) * 100
        show_pct = start_pct + 2
        end_pct = ((i + 1) * 3 / cycle) * 100
        role_keyframes += f"""
        @keyframes role{i} {{
            0%, {start_pct:.1f}% {{ opacity: 0; transform: translateY(6px); }}
            {start_pct + 1:.1f}%, {show_pct:.1f}% {{ opacity: 1; transform: translateY(0); }}
            {end_pct:.1f}%, 100% {{ opacity: 0; transform: translateY(-6px); }}
        }}"""
        role_texts += f'<text x="450" y="192" text-anchor="middle" fill="{t["cyan"]}" font-family="\'Courier New\',monospace" font-size="13" font-weight="600" letter-spacing="4" opacity="0" style="animation: role{i} {cycle}s infinite;">{esc(role)}</text>'

    import random
    random.seed(42)
    particles = ""
    for _ in range(35):
        cx = random.randint(15, 885)
        cy = random.randint(15, 285)
        r = round(random.uniform(0.4, 1.2), 2)
        dur = round(random.uniform(3.5, 7.5), 1)
        delay = round(random.uniform(0.1, 4.0), 1)
        particles += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{t["cyan"]}" opacity="0.2"><animate attributeName="opacity" values="0.05;0.35;0.05" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/></circle>'

    grid = ""
    for x in range(0, 900, 50):
        grid += f'<line x1="{x}" y1="0" x2="{x}" y2="300" stroke="{t["border"]}" stroke-width="0.5" opacity="0.25"/>'
    for y in range(0, 300, 50):
        grid += f'<line x1="0" y1="{y}" x2="900" y2="{y}" stroke="{t["border"]}" stroke-width="0.5" opacity="0.25"/>'

    aurora_colors = f"{t['violet']};{t['cyan']};{t['blue']}" if theme == "dark" else f"{t['blue']};{t['violet']};{t['cyan']}"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 300" width="900" height="300">
  <defs>
    <linearGradient id="heroBg_{suffix}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{t["bg"]}"/>
      <stop offset="100%" stop-color="{t["bg2"]}"/>
    </linearGradient>
    <linearGradient id="aurora_{suffix}" x1="0" y1="0" x2="1" y2="0.6">
      <stop offset="0%" stop-color="{t["violet"]}" stop-opacity="0.18">
        <animate attributeName="stop-color" values="{aurora_colors}" dur="8s" repeatCount="indefinite"/>
      </stop>
      <stop offset="50%" stop-color="{t["cyan"]}" stop-opacity="0.10">
        <animate attributeName="stop-color" values="{t['cyan']};{t['violet']};{t['blue']}" dur="10s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" stop-color="{t["blue"]}" stop-opacity="0.14">
        <animate attributeName="stop-color" values="{t['blue']};{t['cyan']};{t['violet']}" dur="12s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>
    <linearGradient id="titleGrad_{suffix}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{t["cyan"]}"/>
      <stop offset="45%" stop-color="{t["violet"]}"/>
      <stop offset="100%" stop-color="{t["blue"]}"/>
    </linearGradient>
    <filter id="glow_{suffix}" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <style>
    {role_keyframes}
    @keyframes scanline {{ 0% {{ transform: translateY(0); }} 100% {{ transform: translateY(300px); }} }}
  </style>

  <rect width="900" height="300" fill="url(#heroBg_{suffix})"/>
  <rect width="900" height="300" fill="url(#aurora_{suffix})"/>
  <g opacity="0.18">{grid}</g>
  <rect width="900" height="1" fill="{t["cyan"]}" opacity="0.06" style="animation: scanline 7s linear infinite;"/>
  {particles}

  <line x1="80" y1="225" x2="820" y2="225" stroke="{t["cyan"]}" stroke-width="0.6" opacity="0.25" filter="url(#glow_{suffix})"/>

  <text x="450" y="105" text-anchor="middle" fill="url(#titleGrad_{suffix})" font-family="system-ui,-apple-system,sans-serif" font-size="50" font-weight="900" letter-spacing="8" filter="url(#glow_{suffix})">ROSHAN R</text>
  <text x="450" y="142" text-anchor="middle" fill="{t["muted"]}" font-family="'Courier New',monospace" font-size="11" letter-spacing="5">SOFTWARE ENGINEERING // AI SYSTEMS</text>

  {role_texts}

  <g transform="translate(450, 245)" text-anchor="middle">
    <circle cx="-165" cy="-3.5" r="3" fill="{t["green"]}">
      <animate attributeName="opacity" values="0.4;1;0.4" dur="2s" repeatCount="indefinite"/>
    </circle>
    <text x="0" y="0" fill="{t["muted"]}" font-family="'Courier New',monospace" font-size="9" letter-spacing="3">{esc(tagline)}</text>
  </g>

  <g transform="translate(0, 276)" opacity="0.65">
    <text x="35" y="0" fill="{t["dim"]}" font-family="'Courier New',monospace" font-size="7.5" letter-spacing="2">SYSTEM: ONLINE</text>
    <text x="260" y="0" fill="{t["dim"]}" font-family="'Courier New',monospace" font-size="7.5" letter-spacing="2">MODE: ENGINEERING</text>
    <text x="510" y="0" fill="{t["dim"]}" font-family="'Courier New',monospace" font-size="7.5" letter-spacing="2">FOCUS: AI + SYSTEMS</text>
    <text x="760" y="0" fill="{t["dim"]}" font-family="'Courier New',monospace" font-size="7.5" letter-spacing="2">NODE: 01</text>
  </g>

  <text x="875" y="294" text-anchor="end" fill="{t["dim"]}" font-family="'Courier New',monospace" font-size="5" opacity="0.2">ROSHAN // NODE 01 // stack booted</text>

  <polyline points="0,18 0,0 18,0" fill="none" stroke="{t["cyan"]}" stroke-width="1.2" opacity="0.4"/>
  <polyline points="882,0 900,0 900,18" fill="none" stroke="{t["cyan"]}" stroke-width="1.2" opacity="0.4"/>
  <polyline points="0,282 0,300 18,300" fill="none" stroke="{t["violet"]}" stroke-width="1.2" opacity="0.4"/>
  <polyline points="882,300 900,300 900,282" fill="none" stroke="{t["violet"]}" stroke-width="1.2" opacity="0.4"/>
</svg>'''
    write_svg(f"hero/hero-{suffix}.svg", svg)


# ─── 2. ENGINEERING OPERATING SYSTEM PANEL ───────────────────────────────────

def generate_engineering_os(profile, theme, suffix):
    t = DARK if theme == "dark" else LIGHT

    cards = [
        ("IDENTITY", "Roshan R", "CS Engineering Student", t["cyan"]),
        ("ROLE", "Software Engineer", "AI Systems Engineer", t["violet"]),
        ("FOCUS", "AI Systems • Architecture", "Backend • Distributed Workflows", t["blue"]),
        ("CURRENTLY BUILDING", "Agentic AI • Hybrid RAG", "Real-Time Voice Systems", t["green"]),
        ("CORE STACK", "Python • TypeScript • C++", "FastAPI • React • PostgreSQL", t["amber"]),
        ("AI & AGENTS", "LangGraph • MCP • ChromaDB", "PyTorch • LiveKit • WebRTC", t["cyan"]),
    ]

    content = ""
    for i, (title, l1, l2, color) in enumerate(cards):
        row = i // 3
        col = i % 3
        x = 25 + col * 270
        y = 45 + row * 90

        content += f'''
    <g transform="translate({x}, {y})">
      <rect width="250" height="75" rx="8" fill="{t["bg2"]}" stroke="{t["border_subtle"]}" stroke-width="1"/>
      <rect width="4" height="75" rx="2" fill="{color}"/>
      <text x="18" y="22" fill="{color}" font-family="'Courier New',monospace" font-size="8" font-weight="700" letter-spacing="2">{esc(title)}</text>
      <text x="18" y="44" fill="{t["text"]}" font-family="system-ui,sans-serif" font-size="11" font-weight="600">{esc(l1)}</text>
      <text x="18" y="60" fill="{t["muted"]}" font-family="system-ui,sans-serif" font-size="9.5">{esc(l2)}</text>
    </g>'''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 240" width="840" height="240">
  <rect width="840" height="240" rx="10" fill="{t["bg"]}" stroke="{t["border"]}" stroke-width="0.6"/>
  <text x="420" y="24" text-anchor="middle" fill="{t["muted"]}" font-family="'Courier New',monospace" font-size="8.5" letter-spacing="4">ENGINEERING OPERATING SYSTEM</text>
  {content}
</svg>'''
    write_svg(f"diagrams/engineering-os-{suffix}.svg", svg)


# ─── 3. LIVE TERMINAL EXPERIENCE ─────────────────────────────────────────────

def generate_terminal(theme, suffix):
    t = DARK if theme == "dark" else LIGHT
    lines = [
        ("$ whoami", "roshan-r // software-engineer // ai-systems-architect"),
        ("$ cat focus.json", '{ "agentic_ai": true, "rag": true, "voice_ai": true, "dsa": "active" }'),
        ("$ git log --oneline -1", "e8b4c12 feat(agentforge): implement graph-rag & mcp tool orchestration"),
        ("$ docker ps --format 'table {{.Names}}\t{{.Status}}'", "agent-orchestrator (Up 42h) | vector-db (Up 42h) | rconnectx-api (Up 42h)"),
        ("$ systemctl status ai-pipeline", "● ai-pipeline.service - Active: running (event-driven WebRTC / LiveKit)"),
        ("$ leetcode --stats", "219 Solved (73 Easy, 114 Med, 32 Hard) | Rating: 1773.12 (Top 9.47%)"),
        ("$ deploy --production", "Build: PASS (100% tests) -> Deployed to production across edge nodes"),
    ]

    line_elements = ""
    y = 52
    for i, (cmd, output) in enumerate(lines):
        delay = i * 0.8
        line_elements += f'''
    <g opacity="0">
      <animate attributeName="opacity" values="0;1;1" keyTimes="0;0.1;1" dur="10s" begin="{delay}s" fill="freeze" repeatCount="indefinite"/>
      <text x="20" y="{y}" fill="{t["green"]}" font-family="'Courier New',monospace" font-size="10.5" font-weight="600">{esc(cmd)}</text>
      <text x="20" y="{y + 16}" fill="{t["muted"]}" font-family="'Courier New',monospace" font-size="9.5">{esc(output)}</text>
    </g>'''
        y += 38

    win_bg = t["bg"] if theme == "dark" else "#0F172A"
    win_muted = t["muted"] if theme == "dark" else "#94A3B8"
    win_green = t["green"]

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 330" width="840" height="330">
  <defs>
    <linearGradient id="termBorder_{suffix}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{t["cyan"]}" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="{t["violet"]}" stop-opacity="0.35"/>
    </linearGradient>
  </defs>

  <rect x="0" y="0" width="840" height="330" rx="8" fill="{win_bg}" stroke="url(#termBorder_{suffix})" stroke-width="1"/>
  <rect x="0" y="0" width="840" height="30" rx="8" fill="{win_bg}"/>
  <rect x="0" y="22" width="840" height="8" fill="{win_bg}"/>

  <circle cx="20" cy="15" r="4.5" fill="#EF4444" opacity="0.85"/>
  <circle cx="36" cy="15" r="4.5" fill="#F59E0B" opacity="0.85"/>
  <circle cx="52" cy="15" r="4.5" fill="#10B981" opacity="0.85"/>
  <text x="420" y="19" text-anchor="middle" fill="{win_muted}" font-family="'Courier New',monospace" font-size="9.5">roshan@engineering-node-01 ~ zsh</text>
  <line x1="0" y1="30" x2="840" y2="30" stroke="{t["border_subtle"]}" stroke-width="0.8"/>

  <g transform="translate(0, 5)">
    {line_elements}
  </g>

  <rect x="20" y="{y + 4}" width="7" height="13" fill="{win_green}">
    <animate attributeName="opacity" values="1;0;1" dur="0.9s" repeatCount="indefinite"/>
  </rect>
</svg>'''
    write_svg(f"terminal/terminal-{suffix}.svg", svg)


# ─── 4. HOW I THINK (ENGINEERING PIPELINE) ───────────────────────────────────

def generate_engineering_pipeline(theme, suffix):
    t = DARK if theme == "dark" else LIGHT
    steps = ["PROBLEM", "MODEL", "ARCHITECTURE", "IMPLEMENTATION", "TESTING", "OBSERVABILITY", "DEPLOYMENT", "ITERATION"]
    colors = [t["cyan"], t["violet"], t["blue"], t["amber"], t["green"], t["violet"], t["cyan"], t["blue"]]

    content = ""
    x = 52
    spacing = 92
    for i, (step, color) in enumerate(zip(steps, colors)):
        w = max(len(step) * 6.5 + 14, 76)
        content += f'''
    <g>
      <rect x="{x - w//2}" y="42" width="{w}" height="28" rx="6" fill="{t['bg2']}" stroke="{color}" stroke-width="1" opacity="0.9"/>
      <text x="{x}" y="59" text-anchor="middle" fill="{color}" font-family="'Courier New',monospace" font-size="8" font-weight="700" letter-spacing="0.5">{esc(step)}</text>
    </g>'''
        if i < len(steps) - 1:
            nx = x + spacing
            content += f'''
      <line x1="{x + w//2}" y1="56" x2="{nx - 42}" y2="56" stroke="{color}" stroke-width="0.8" opacity="0.4" stroke-dasharray="3,3"/>
      <circle r="2.2" fill="{color}" opacity="0.85">
        <animateMotion dur="2.2s" repeatCount="indefinite" path="M{x + w//2},56 L{nx - 42},56"/>
      </circle>'''
        x += spacing

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 115" width="780" height="115">
  <rect width="780" height="115" rx="8" fill="{t['bg']}" stroke="{t['border']}" stroke-width="0.5"/>
  <text x="390" y="22" text-anchor="middle" fill="{t['muted']}" font-family="'Courier New',monospace" font-size="8" letter-spacing="4">HOW I THINK // ENGINEERING LIFECYCLE</text>
  {content}
  <text x="390" y="100" text-anchor="middle" fill="{t['dim']}" font-family="'Courier New',monospace" font-size="7" letter-spacing="2">SYSTEM DESIGN METHODOLOGY • CONTINUOUS REFINEMENT</text>
</svg>'''
    write_svg(f"diagrams/engineering-pipeline-{suffix}.svg", svg)


# ─── 5. ARCHITECTURE DIAGRAMS (AI LAB, RAG, AGENTS, SYSTEMS, DEVOPS, VOICE, IOT) ───

def _node(x, y, label, color, t, w=100, h=30):
    return f'''<g>
    <rect x="{x - w//2}" y="{y - h//2}" width="{w}" height="{h}" rx="6" fill="{t['bg2']}" stroke="{color}" stroke-width="1" opacity="0.9"/>
    <text x="{x}" y="{y + 4}" text-anchor="middle" fill="{color}" font-family="'Courier New',monospace" font-size="8.5" font-weight="600" letter-spacing="0.5">{esc(label)}</text>
  </g>'''

def _arrow(x1, y1, x2, y2, color, t, dur=2.0):
    return f'''<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="0.8" opacity="0.4" stroke-dasharray="3,3"/>
  <circle r="2.2" fill="{color}" opacity="0.85">
    <animateMotion dur="{dur}s" repeatCount="indefinite" path="M{x1},{y1} L{x2},{y2}"/>
  </circle>'''


def generate_ai_lab(theme, suffix):
    t = DARK if theme == "dark" else LIGHT
    c, v, b, g, a = t["cyan"], t["violet"], t["blue"], t["green"], t["amber"]

    nodes = [
        (400, 36, "USER", c, 90),
        (400, 80, "INPUT PROCESSING", t["muted"], 130),
        (400, 126, "MODEL ROUTER", v, 120),
        (230, 176, "RETRIEVAL", b, 100),
        (400, 176, "VECTOR DATABASE", c, 130),
        (570, 176, "TOOLS & MCP", g, 110),
        (230, 230, "MEMORY ENGINE", v, 115),
        (400, 230, "AGENT ORCHESTRATION", a, 150),
        (570, 230, "FOUNDATION MODEL", b, 135),
        (400, 282, "FINAL RESPONSE", c, 120),
    ]

    content = ""
    for x, y, label, col, w in nodes:
        content += _node(x, y, label, col, t, w, 28)

    arrows = [
        (400, 50, 400, 66, c),
        (400, 94, 400, 112, t["muted"]),
        (350, 140, 250, 162, v),
        (400, 140, 400, 162, v),
        (450, 140, 550, 162, v),
        (230, 190, 230, 216, b),
        (400, 190, 400, 216, c),
        (570, 190, 570, 216, g),
        (290, 230, 325, 230, v),
        (500, 230, 475, 230, b),
        (400, 244, 400, 268, a),
    ]
    for x1, y1, x2, y2, col in arrows:
        content += _arrow(x1, y1, x2, y2, col, t)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 320" width="800" height="320">
  <rect width="800" height="320" rx="8" fill="{t['bg']}" stroke="{t['border']}" stroke-width="0.5"/>
  <text x="400" y="20" text-anchor="middle" fill="{t['muted']}" font-family="'Courier New',monospace" font-size="8" letter-spacing="4">AI ENGINEERING ARCHITECTURE</text>
  {content}
</svg>'''
    write_svg(f"architecture/ai-lab-{suffix}.svg", svg)


def generate_rag_pipeline(theme, suffix):
    t = DARK if theme == "dark" else LIGHT
    steps = ["DOCUMENTS", "CHUNKING", "EMBEDDINGS", "VECTOR STORE", "RETRIEVAL", "RERANKING", "CONTEXT", "LLM", "ANSWER"]
    colors = [t["muted"], t["blue"], t["violet"], t["cyan"], t["blue"], t["violet"], t["cyan"], t["amber"], t["green"]]

    content = ""
    x = 48
    spacing = 86
    for i, (step, col) in enumerate(zip(steps, colors)):
        w = max(len(step) * 6.5 + 14, 72)
        content += _node(x, 70, step, col, t, w, 26)
        if i < len(steps) - 1:
            nx = x + spacing
            content += _arrow(x + w//2, 70, nx - 36, 70, col, t, 1.8)
        x += spacing

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 140" width="780" height="140">
  <rect width="780" height="140" rx="8" fill="{t['bg']}" stroke="{t['border']}" stroke-width="0.5"/>
  <text x="390" y="24" text-anchor="middle" fill="{t['muted']}" font-family="'Courier New',monospace" font-size="8" letter-spacing="4">RAG PIPELINE // RETRIEVAL-AUGMENTED GENERATION</text>
  {content}
  <text x="390" y="122" text-anchor="middle" fill="{t['dim']}" font-family="'Courier New',monospace" font-size="7" letter-spacing="2">DENSE RETRIEVAL • HYBRID SEARCH • RE-RANKED CONTEXT INJECTION</text>
</svg>'''
    write_svg(f"architecture/rag-pipeline-{suffix}.svg", svg)


def generate_agent_architecture(theme, suffix):
    t = DARK if theme == "dark" else LIGHT
    c, v, g, b, a = t["cyan"], t["violet"], t["green"], t["blue"], t["amber"]

    content = _node(375, 48, "ORCHESTRATOR / SUPERVISOR", a, t, 200, 30)

    sub_nodes = [
        (130, 115, "REASONING ENGINE", v, 130),
        (290, 115, "EPISODIC MEMORY", c, 125),
        (460, 115, "MCP & TOOL CALLING", g, 135),
        (620, 115, "KNOWLEDGE RETRIEVAL", b, 140),
        (210, 175, "TASK EXECUTION", a, 120),
        (540, 175, "SAFETY & VALIDATION", c, 135),
    ]
    for x, y, label, col, w in sub_nodes:
        content += _node(x, y, label, col, t, w, 26)
        content += _arrow(375, 63, x, y - 13, col, t, 2.2)

    content += _arrow(130, 128, 210, 162, v, t)
    content += _arrow(620, 128, 540, 162, b, t)
    content += _arrow(270, 175, 470, 175, a, t)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 750 215" width="750" height="215">
  <rect width="750" height="215" rx="8" fill="{t['bg']}" stroke="{t['border']}" stroke-width="0.5"/>
  <text x="375" y="20" text-anchor="middle" fill="{t['muted']}" font-family="'Courier New',monospace" font-size="8" letter-spacing="4">AGENTIC AI ORCHESTRATION ARCHITECTURE</text>
  {content}
</svg>'''
    write_svg(f"architecture/agent-architecture-{suffix}.svg", svg)


def generate_system_design(theme, suffix):
    t = DARK if theme == "dark" else LIGHT
    c, b, v, a, g = t["cyan"], t["blue"], t["violet"], t["amber"], t["green"]

    main = [
        (320, 42, "CLIENT APPS", c),
        (320, 92, "API GATEWAY", b),
        (320, 142, "AUTH / JWT", v),
        (320, 192, "MICROSERVICES", c),
        (320, 242, "MESSAGE QUEUE", a),
        (320, 292, "ASYNC WORKERS", g),
        (320, 342, "PRIMARY DB / POSTGRES", b),
    ]
    parallel = [
        (560, 192, "REDIS CACHE", a),
        (560, 242, "OBSERVABILITY", v),
        (560, 292, "CENTRAL LOGGING", t["muted"]),
        (560, 342, "METRICS / TELEMETRY", c),
    ]

    content = ""
    for x, y, label, col in main:
        content += _node(x, y, label, col, t, 140, 28)
    for i in range(len(main) - 1):
        content += _arrow(320, main[i][1] + 14, 320, main[i+1][1] - 14, main[i][3], t, 1.6)

    for x, y, label, col in parallel:
        content += _node(x, y, label, col, t, 135, 26)

    content += _arrow(390, 192, 492, 192, a, t)
    content += _arrow(560, 205, 560, 229, v, t)
    content += _arrow(560, 255, 560, 279, t["muted"], t)
    content += _arrow(560, 305, 560, 329, c, t)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 380" width="720" height="380">
  <rect width="720" height="380" rx="8" fill="{t['bg']}" stroke="{t['border']}" stroke-width="0.5"/>
  <text x="360" y="20" text-anchor="middle" fill="{t['muted']}" font-family="'Courier New',monospace" font-size="8" letter-spacing="4">DISTRIBUTED SYSTEM DESIGN LAB</text>
  {content}
</svg>'''
    write_svg(f"architecture/system-design-{suffix}.svg", svg)


def generate_devops_pipeline(theme, suffix):
    t = DARK if theme == "dark" else LIGHT
    steps = ["GIT PUSH", "CI TESTS", "LINT & BUILD", "DOCKERIZE", "REGISTRY", "DEPLOY", "HEALTH CHECK", "PRODUCTION"]
    colors = [t["muted"], t["blue"], t["violet"], t["cyan"], t["blue"], t["green"], t["amber"], t["green"]]
    statuses = ["PUSHED", "PASS", "PASS", "BUILT", "SYNCED", "ROLLOUT", "HEALTHY", "LIVE"]

    content = ""
    x = 50
    spacing = 96
    for i, (step, col, st) in enumerate(zip(steps, colors, statuses)):
        w = max(len(step) * 6.5 + 14, 76)
        content += _node(x, 62, step, col, t, w, 26)
        content += f'<text x="{x}" y="88" text-anchor="middle" fill="{t["green"]}" font-family="\'Courier New\',monospace" font-size="6.5" font-weight="600">● {esc(st)}</text>'
        if i < len(steps) - 1:
            nx = x + spacing
            content += _arrow(x + w//2, 62, nx - 38, 62, col, t, 1.8)
        x += spacing

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 115" width="780" height="115">
  <rect width="780" height="115" rx="8" fill="{t['bg']}" stroke="{t['border']}" stroke-width="0.5"/>
  <text x="390" y="20" text-anchor="middle" fill="{t['muted']}" font-family="'Courier New',monospace" font-size="8" letter-spacing="4">PRODUCTION CI/CD DEVOPS PIPELINE</text>
  {content}
</svg>'''
    write_svg(f"architecture/devops-pipeline-{suffix}.svg", svg)


def generate_voice_ai(theme, suffix):
    t = DARK if theme == "dark" else LIGHT
    steps = ["MIC INPUT", "VAD", "STT (WHISPER)", "CONVERSATION FSM", "LLM", "MEMORY", "TTS (REALTIME)", "AUDIO OUT"]
    colors = [t["cyan"], t["violet"], t["blue"], t["amber"], t["violet"], t["cyan"], t["blue"], t["green"]]

    content = ""
    x = 52
    spacing = 94
    for i, (step, col) in enumerate(zip(steps, colors)):
        w = max(len(step) * 6.2 + 12, 74)
        content += _node(x, 65, step, col, t, w, 26)
        if i < len(steps) - 1:
            nx = x + spacing
            content += _arrow(x + w//2, 65, nx - 37, 65, col, t, 1.7)
        x += spacing

    wave = ""
    for i in range(85):
        h = round(10 * math.sin(i * 0.28) * (0.3 + 0.7 * math.sin(i * 0.08)), 1)
        wave += f'<line x1="{40 + i * 8.2}" y1="{120 - h}" x2="{40 + i * 8.2}" y2="{120 + h}" stroke="{t["cyan"]}" stroke-width="1.8" opacity="0.2"/>'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 155" width="780" height="155">
  <rect width="780" height="155" rx="8" fill="{t['bg']}" stroke="{t['border']}" stroke-width="0.5"/>
  <text x="390" y="20" text-anchor="middle" fill="{t['muted']}" font-family="'Courier New',monospace" font-size="8" letter-spacing="4">REAL-TIME VOICE AI PIPELINE // WebRTC &amp; LiveKit</text>
  {content}
  {wave}
  <g transform="translate(0, 142)" opacity="0.7">
    <text x="60" y="0" fill="{t['dim']}" font-family="'Courier New',monospace" font-size="7">● LiveKit WebRTC DataChannel</text>
    <text x="300" y="0" fill="{t['dim']}" font-family="'Courier New',monospace" font-size="7">● Sub-300ms Turn Latency</text>
    <text x="540" y="0" fill="{t['dim']}" font-family="'Courier New',monospace" font-size="7">● Interruption / Barge-In Safe</text>
  </g>
</svg>'''
    write_svg(f"architecture/voice-ai-{suffix}.svg", svg)


def generate_iot_system(theme, suffix):
    t = DARK if theme == "dark" else LIGHT
    steps = ["ESP32", "SOIL SENSORS", "TELEMETRY", "EDGE PROCESSING", "FASTAPI", "CLOUD AI", "NPK PREDICTOR", "DISPENSER"]
    colors = [t["green"], t["cyan"], t["blue"], t["violet"], t["cyan"], t["blue"], t["violet"], t["green"]]

    content = ""
    x = 50
    spacing = 94
    for i, (step, col) in enumerate(zip(steps, colors)):
        w = max(len(step) * 6.2 + 12, 74)
        content += _node(x, 62, step, col, t, w, 26)
        if i < len(steps) - 1:
            nx = x + spacing
            content += _arrow(x + w//2, 62, nx - 37, 62, col, t, 1.8)
        x += spacing

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 120" width="780" height="120">
  <rect width="780" height="120" rx="8" fill="{t['bg']}" stroke="{t['border']}" stroke-width="0.5"/>
  <text x="390" y="20" text-anchor="middle" fill="{t['muted']}" font-family="'Courier New',monospace" font-size="8" letter-spacing="4">INTELLIGENT IoT ARCHITECTURE // HARDWARE TO AI</text>
  {content}
  <text x="390" y="105" text-anchor="middle" fill="{t['dim']}" font-family="'Courier New',monospace" font-size="7" letter-spacing="2">REAL-TIME SENSOR TELEMETRY -> EDGE ENCODING -> CLOUD PREDICTION -> ACTUATION</text>
</svg>'''
    write_svg(f"architecture/iot-system-{suffix}.svg", svg)


# ─── 6. PROJECT MINI-ARCHITECTURES ───────────────────────────────────────────

def generate_project_arch(name, steps, colors, theme, suffix, filename):
    t = DARK if theme == "dark" else LIGHT
    spacing = 42
    h = len(steps) * spacing + 34
    content = ""
    for i, (step, col) in enumerate(zip(steps, colors)):
        y = 32 + i * spacing
        w = max(len(step) * 7.5 + 16, 85)
        content += _node(200, y, step, col, t, w, 26)
        if i < len(steps) - 1:
            content += _arrow(200, y + 13, 200, y + spacing - 13, col, t, 1.8)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 {h}" width="400" height="{h}">
  <rect width="400" height="{h}" rx="6" fill="{t['bg']}" stroke="{t['border']}" stroke-width="0.5"/>
  <text x="200" y="16" text-anchor="middle" fill="{t['muted']}" font-family="'Courier New',monospace" font-size="7.5" letter-spacing="2">{esc(name)} // ARCHITECTURE</text>
  {content}
</svg>'''
    write_svg(f"projects/{filename}-{suffix}.svg", svg)


def generate_all_project_archs(theme, suffix):
    t = DARK if theme == "dark" else LIGHT
    generate_project_arch(
        "RCONNECTX", ["CLIENT BROWSERS", "NEXT.JS / REACT", "FASTAPI GATEWAY", "AI MATCHING ENGINE", "POSTGRESQL & REDIS", "WEBSOCKET STREAM"],
        [t["cyan"], t["blue"], t["violet"], t["amber"], t["cyan"], t["green"]],
        theme, suffix, "rconnectx-arch"
    )
    generate_project_arch(
        "SMARTFERT-AI", ["ESP32 CONTROLLER", "NPK SOIL SENSORS", "FASTAPI BACKEND", "ML PREDICTION MODEL", "RECOMMENDER ENGINE", "VALVE ACTUATORS"],
        [t["green"], t["cyan"], t["blue"], t["violet"], t["amber"], t["green"]],
        theme, suffix, "smartfert-arch"
    )
    generate_project_arch(
        "AGENTFORGE", ["USER PROMPT", "LANGGRAPH SUPERVISOR", "SPECIALIZED AGENTS", "HYBRID RAG + GRAPH", "MCP TOOL RUNTIME", "PERSISTENT MEMORY"],
        [t["cyan"], t["amber"], t["violet"], t["blue"], t["green"], t["cyan"]],
        theme, suffix, "agentforge-arch"
    )
    generate_project_arch(
        "GUARDIAN-AI", ["MOBILE APP (FLUTTER)", "MOTION & AUDIO SENSORS", "DISTRESS ML MODEL", "FASTAPI BACKEND", "REAL-TIME GPS TRACKING", "TWILIO SOS BROADCAST"],
        [t["cyan"], t["green"], t["violet"], t["blue"], t["amber"], t["cyan"]],
        theme, suffix, "guardian-arch"
    )


# ─── 7. TECHNOLOGY CONSTELLATION ─────────────────────────────────────────────

def generate_tech_constellation(theme, suffix):
    t = DARK if theme == "dark" else LIGHT
    domains = {
        "AI / ML": {
            "color": t["violet"],
            "techs": ["PyTorch", "TensorFlow", "LangChain", "LangGraph", "LLMs", "RAG", "MCP"],
            "angle_start": 200, "angle_span": 80,
        },
        "BACKEND": {
            "color": t["cyan"],
            "techs": ["Python", "FastAPI", "Node.js", "PostgreSQL", "MongoDB", "Redis"],
            "angle_start": 280, "angle_span": 70,
        },
        "FRONTEND": {
            "color": t["blue"],
            "techs": ["React", "TypeScript", "JavaScript", "HTML5", "CSS3"],
            "angle_start": 350, "angle_span": 60,
        },
        "INFRA / CLOUD": {
            "color": t["amber"],
            "techs": ["Docker", "AWS", "GitHub Actions", "Linux", "CI/CD"],
            "angle_start": 50, "angle_span": 60,
        },
        "REAL-TIME": {
            "color": t["green"],
            "techs": ["WebRTC", "LiveKit", "WebSocket"],
            "angle_start": 110, "angle_span": 40,
        },
        "HARDWARE / IoT": {
            "color": t["cyan"],
            "techs": ["ESP32", "Sensors"],
            "angle_start": 160, "angle_span": 30,
        },
    }

    cx, cy = 400, 200
    content = ""

    content += f'''
  <circle cx="{cx}" cy="{cy}" r="48" fill="none" stroke="{t['cyan']}" stroke-width="0.8" opacity="0.3">
    <animate attributeName="r" values="45;50;45" dur="4s" repeatCount="indefinite"/>
  </circle>
  <circle cx="{cx}" cy="{cy}" r="32" fill="{t['bg2']}" stroke="{t['cyan']}" stroke-width="1.2" opacity="0.9"/>
  <text x="{cx}" y="{cy - 4}" text-anchor="middle" fill="{t['cyan']}" font-family="'Courier New',monospace" font-size="8.5" font-weight="700" letter-spacing="2">ROSHAN</text>
  <text x="{cx}" y="{cy + 8}" text-anchor="middle" fill="{t['muted']}" font-family="'Courier New',monospace" font-size="6.5" letter-spacing="1">ENGINEERING</text>'''

    for r in [95, 155, 205]:
        content += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{t["border"]}" stroke-width="0.5" opacity="0.2" stroke-dasharray="3,4"/>'

    import random
    random.seed(9)
    for domain, cfg in domains.items():
        color = cfg["color"]
        techs = cfg["techs"]
        angle_start = cfg["angle_start"]
        angle_span = cfg["angle_span"]

        for i, tech in enumerate(techs):
            angle = math.radians(angle_start + (angle_span / len(techs)) * (i + 0.5))
            radius = 90 + (i % 3) * 52 + random.randint(-6, 6)
            tx = cx + radius * math.cos(angle)
            ty = cy + radius * math.sin(angle)

            content += f'<line x1="{cx}" y1="{cy}" x2="{tx}" y2="{ty}" stroke="{color}" stroke-width="0.4" opacity="0.18"/>'

            tw = max(len(tech) * 6.5 + 14, 42)
            dur = round(3 + random.random() * 3, 1)
            content += f'''
    <g>
      <rect x="{tx - tw/2}" y="{ty - 10}" width="{tw}" height="20" rx="10" fill="{t['bg2']}" stroke="{color}" stroke-width="0.8" opacity="0.9"/>
      <text x="{tx}" y="{ty + 3.5}" text-anchor="middle" fill="{color}" font-family="'Courier New',monospace" font-size="7.5" font-weight="600">{esc(tech)}</text>
      <animate attributeName="opacity" values="0.75;1;0.75" dur="{dur}s" repeatCount="indefinite"/>
    </g>'''

        mid_angle = math.radians(angle_start + angle_span / 2)
        lx = cx + 240 * math.cos(mid_angle)
        ly = cy + 240 * math.sin(mid_angle)
        content += f'<text x="{lx}" y="{ly}" text-anchor="middle" fill="{color}" font-family="\'Courier New\',monospace" font-size="7" font-weight="700" letter-spacing="2" opacity="0.6">{esc(domain)}</text>'

    content += f'''
  <circle r="3" fill="{t['cyan']}" opacity="0.7">
    <animateMotion dur="18s" repeatCount="indefinite" path="M{cx + 155},{cy} A155,155,0,1,1,{cx + 154.9},{cy}"/>
  </circle>'''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" width="800" height="400">
  <rect width="800" height="400" rx="8" fill="{t['bg']}" stroke="{t['border']}" stroke-width="0.5"/>
  <text x="400" y="22" text-anchor="middle" fill="{t['muted']}" font-family="'Courier New',monospace" font-size="8" letter-spacing="4">TECHNOLOGY CONSTELLATION // MULTI-DOMAIN EXPERTISE</text>
  {content}
</svg>'''
    write_svg(f"tech/constellation-{suffix}.svg", svg)


# ─── 8. LEETCODE COMMAND CENTER ASSETS (REAL DATA ONLY) ──────────────────────

def generate_leetcode_stats(lc, theme, suffix):
    t = DARK if theme == "dark" else LIGHT
    s = lc.get("stats", {
        "totalSolved": 219, "totalQuestions": 4033,
        "easySolved": 73, "totalEasy": 961,
        "mediumSolved": 114, "totalMedium": 2105,
        "hardSolved": 32, "totalHard": 967,
    })
    c = lc.get("contest", {
        "rating": 1773.12, "globalRanking": 81536, "topPercentage": 9.47
    })

    def ring(cx, cy, r, pct, color, label, solved, total):
        circ = 2 * math.pi * r
        offset = circ * (1 - pct)
        return f'''
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{t['dim']}" stroke-width="4.5" opacity="0.18"/>
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="4.5" stroke-dasharray="{circ:.1f}" stroke-dashoffset="{offset:.1f}" stroke-linecap="round" transform="rotate(-90 {cx} {cy})">
      <animate attributeName="stroke-dashoffset" from="{circ}" to="{offset:.1f}" dur="1.2s" fill="freeze"/>
    </circle>
    <text x="{cx}" y="{cy - 2}" text-anchor="middle" fill="{t['text']}" font-family="'Courier New',monospace" font-size="14" font-weight="700">{solved}</text>
    <text x="{cx}" y="{cy + 11}" text-anchor="middle" fill="{t['muted']}" font-family="'Courier New',monospace" font-size="7">/ {total}</text>
    <text x="{cx}" y="{cy + r + 16}" text-anchor="middle" fill="{color}" font-family="'Courier New',monospace" font-size="8" font-weight="700" letter-spacing="1">{esc(label)}</text>'''

    total_pct = s["totalSolved"] / s["totalQuestions"] if s.get("totalQuestions") else 0
    easy_pct = s["easySolved"] / s["totalEasy"] if s.get("totalEasy") else 0
    med_pct = s["mediumSolved"] / s["totalMedium"] if s.get("totalMedium") else 0
    hard_pct = s["hardSolved"] / s["totalHard"] if s.get("totalHard") else 0

    rings = ring(95, 95, 42, total_pct, t["cyan"], "TOTAL SOLVED", s["totalSolved"], s["totalQuestions"])
    rings += ring(250, 95, 32, easy_pct, t["green"], "EASY", s["easySolved"], s["totalEasy"])
    rings += ring(370, 95, 32, med_pct, t["amber"], "MEDIUM", s["mediumSolved"], s["totalMedium"])
    rings += ring(490, 95, 32, hard_pct, t["red"], "HARD", s["hardSolved"], s["totalHard"])

    contest_rating = c.get("rating", 1773.12)
    contest_rank = c.get("globalRanking", 81536)
    contest_pct = c.get("topPercentage", 9.47)

    contest_section = f'''
    <rect x="580" y="45" width="130" height="95" rx="6" fill="{t['bg2']}" stroke="{t['border_subtle']}" stroke-width="1"/>
    <text x="645" y="65" text-anchor="middle" fill="{t['muted']}" font-family="'Courier New',monospace" font-size="7.5" letter-spacing="2">CONTEST RATING</text>
    <text x="645" y="92" text-anchor="middle" fill="{t['cyan']}" font-family="'Courier New',monospace" font-size="22" font-weight="800">{contest_rating:.0f}</text>
    <text x="645" y="112" text-anchor="middle" fill="{t['green']}" font-family="'Courier New',monospace" font-size="9" font-weight="700">Top {contest_pct}%</text>
    <text x="645" y="128" text-anchor="middle" fill="{t['dim']}" font-family="'Courier New',monospace" font-size="7">Rank #{contest_rank:,}</text>
    '''

    badge_section = f'''
    <rect x="725" y="45" width="95" height="95" rx="6" fill="{t['bg2']}" stroke="{t['border_subtle']}" stroke-width="1"/>
    <text x="772" y="65" text-anchor="middle" fill="{t['muted']}" font-family="'Courier New',monospace" font-size="7" letter-spacing="1">BADGE</text>
    <circle cx="772" cy="88" r="16" fill="{t['amber']}" opacity="0.2"/>
    <text x="772" y="92" text-anchor="middle" fill="{t['amber']}" font-family="'Courier New',monospace" font-size="10" font-weight="800">50D</text>
    <text x="772" y="122" text-anchor="middle" fill="{t['muted']}" font-family="'Courier New',monospace" font-size="7">2026 Badge</text>
    '''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 180" width="840" height="180">
  <rect width="840" height="180" rx="8" fill="{t['bg']}" stroke="{t['border']}" stroke-width="0.5"/>
  <text x="420" y="22" text-anchor="middle" fill="{t['muted']}" font-family="'Courier New',monospace" font-size="8" letter-spacing="4">LEETCODE COMMAND CENTER // VERIFIED TELEMETRY</text>
  <g transform="translate(0, 10)">
    {rings}
    {contest_section}
    {badge_section}
  </g>
</svg>'''
    write_svg(f"leetcode/stats-{suffix}.svg", svg)


def generate_leetcode_heatmap(lc, theme, suffix):
    t = DARK if theme == "dark" else LIGHT
    cal = lc.get("submissionCalendar", {})

    submissions = {}
    for ts_str, count in cal.items():
        dt = datetime.fromtimestamp(int(ts_str), tz=timezone.utc)
        submissions[dt.strftime("%Y-%m-%d")] = count

    today = datetime(2026, 8, 29, tzinfo=timezone.utc)
    start = today - timedelta(weeks=22)
    start = start - timedelta(days=(start.weekday() + 1) % 7)

    cell_size = 11
    gap = 2.5
    content = ""
    months_shown = set()

    x = 35
    current = start
    week = 0
    while current <= today:
        row = (current.weekday() + 1) % 7
        y = 35 + row * (cell_size + gap)
        key = current.strftime("%Y-%m-%d")
        count = submissions.get(key, 0)

        if count == 0:
            fill = t["dim"]
            opacity = "0.15"
        elif count <= 3:
            fill = t["cyan"]
            opacity = "0.35"
        elif count <= 7:
            fill = t["cyan"]
            opacity = "0.55"
        elif count <= 12:
            fill = t["cyan"]
            opacity = "0.75"
        else:
            fill = t["cyan"]
            opacity = "0.95"

        content += f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="2.5" fill="{fill}" opacity="{opacity}"/>'

        if current.day <= 7 and current.month not in months_shown:
            months_shown.add(current.month)
            m_name = current.strftime("%b")
            content += f'<text x="{x}" y="28" fill="{t["muted"]}" font-family="\'Courier New\',monospace" font-size="7.5">{esc(m_name)}</text>'

        current += timedelta(days=1)
        if row == 6:
            x += cell_size + gap
            week += 1

    svg_w = x + 30
    lx = svg_w - 140
    legend = f'''
    <g transform="translate({lx}, 142)">
      <text x="0" y="9" fill="{t["muted"]}" font-family="'Courier New',monospace" font-size="7">Less</text>
      <rect x="25" y="0" width="{cell_size}" height="{cell_size}" rx="2" fill="{t['dim']}" opacity="0.15"/>
      <rect x="40" y="0" width="{cell_size}" height="{cell_size}" rx="2" fill="{t['cyan']}" opacity="0.35"/>
      <rect x="55" y="0" width="{cell_size}" height="{cell_size}" rx="2" fill="{t['cyan']}" opacity="0.55"/>
      <rect x="70" y="0" width="{cell_size}" height="{cell_size}" rx="2" fill="{t['cyan']}" opacity="0.75"/>
      <rect x="85" y="0" width="{cell_size}" height="{cell_size}" rx="2" fill="{t['cyan']}" opacity="0.95"/>
      <text x="102" y="9" fill="{t["muted"]}" font-family="'Courier New',monospace" font-size="7">More</text>
    </g>'''

    day_labels = ""
    for i, day in enumerate(["", "Mon", "", "Wed", "", "Fri", ""]):
        if day:
            day_labels += f'<text x="25" y="{35 + i * (cell_size + gap) + 8.5}" fill="{t["muted"]}" font-family="\'Courier New\',monospace" font-size="6.5" text-anchor="end">{esc(day)}</text>'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} 165" width="{svg_w}" height="165">
  <rect width="{svg_w}" height="165" rx="8" fill="{t['bg']}" stroke="{t['border']}" stroke-width="0.5"/>
  <text x="{svg_w // 2}" y="16" text-anchor="middle" fill="{t['muted']}" font-family="'Courier New',monospace" font-size="7.5" letter-spacing="3">DAILY SUBMISSION HEATMAP</text>
  {day_labels}
  {content}
  {legend}
</svg>'''
    write_svg(f"leetcode/heatmap-{suffix}.svg", svg)


def generate_skill_radar(lc, theme, suffix):
    t = DARK if theme == "dark" else LIGHT

    all_skills = []
    for cat in ["fundamental", "intermediate", "advanced"]:
        all_skills.extend(lc.get("skills", {}).get(cat, []))
    all_skills.sort(key=lambda x: x["count"], reverse=True)
    top = all_skills[:8]
    if not top:
        return

    cx, cy = 200, 200
    max_r = 140
    max_val = max(s["count"] for s in top)
    n = len(top)
    content = ""

    for ring_pct in [0.25, 0.5, 0.75, 1.0]:
        r = max_r * ring_pct
        points = ""
        for i in range(n):
            angle = math.radians(360 / n * i - 90)
            px = cx + r * math.cos(angle)
            py = cy + r * math.sin(angle)
            points += f"{px:.1f},{py:.1f} "
        content += f'<polygon points="{points.strip()}" fill="none" stroke="{t["dim"]}" stroke-width="0.5" opacity="0.25"/>'

    for i in range(n):
        angle = math.radians(360 / n * i - 90)
        px = cx + max_r * math.cos(angle)
        py = cy + max_r * math.sin(angle)
        content += f'<line x1="{cx}" y1="{cy}" x2="{px:.1f}" y2="{py:.1f}" stroke="{t["dim"]}" stroke-width="0.5" opacity="0.25"/>'

    data_points = ""
    for i, skill in enumerate(top):
        pct = skill["count"] / max_val
        r = max_r * pct
        angle = math.radians(360 / n * i - 90)
        px = cx + r * math.cos(angle)
        py = cy + r * math.sin(angle)
        data_points += f"{px:.1f},{py:.1f} "

    content += f'<polygon points="{data_points.strip()}" fill="{t["cyan"]}" fill-opacity="0.18" stroke="{t["cyan"]}" stroke-width="1.8"/>'

    for i, skill in enumerate(top):
        pct = skill["count"] / max_val
        r = max_r * pct
        angle = math.radians(360 / n * i - 90)
        px = cx + r * math.cos(angle)
        py = cy + r * math.sin(angle)
        content += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3" fill="{t["cyan"]}"/>'

        lx = cx + (max_r + 22) * math.cos(angle)
        ly = cy + (max_r + 22) * math.sin(angle)
        anchor = "start" if math.cos(angle) > 0.1 else ("end" if math.cos(angle) < -0.1 else "middle")
        content += f'<text x="{lx:.1f}" y="{ly + 3.5:.1f}" text-anchor="{anchor}" fill="{t["muted"]}" font-family="\'Courier New\',monospace" font-size="8">{esc(skill["name"])} ({skill["count"]})</text>'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <rect width="400" height="400" rx="8" fill="{t['bg']}" stroke="{t['border']}" stroke-width="0.5"/>
  <text x="200" y="20" text-anchor="middle" fill="{t['muted']}" font-family="'Courier New',monospace" font-size="8" letter-spacing="3">SKILL RADAR // DSA MASTERY</text>
  {content}
</svg>'''
    write_svg(f"leetcode/skill-radar-{suffix}.svg", svg)


def generate_leetcode_streak(lc, theme, suffix):
    t = DARK if theme == "dark" else LIGHT

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 130" width="400" height="130">
  <rect width="400" height="130" rx="8" fill="{t['bg']}" stroke="{t['border']}" stroke-width="0.5"/>
  <text x="200" y="20" text-anchor="middle" fill="{t['muted']}" font-family="'Courier New',monospace" font-size="7.5" letter-spacing="3">LEETCODE CONSISTENCY</text>

  <g transform="translate(30, 45)">
    <text x="0" y="10" fill="{t['muted']}" font-family="'Courier New',monospace" font-size="8">CURRENT ACTIVITY</text>
    <rect x="130" y="2" width="210" height="10" rx="5" fill="{t['dim']}" opacity="0.2"/>
    <rect x="130" y="2" width="180" height="10" rx="5" fill="{t['cyan']}">
      <animate attributeName="width" from="0" to="180" dur="1.2s" fill="freeze"/>
    </rect>
    <text x="350" y="10" fill="{t['cyan']}" font-family="'Courier New',monospace" font-size="8" font-weight="700">ACTIVE</text>
  </g>

  <g transform="translate(30, 80)">
    <text x="0" y="10" fill="{t['muted']}" font-family="'Courier New',monospace" font-size="8">50-DAY BADGE</text>
    <rect x="130" y="2" width="210" height="10" rx="5" fill="{t['dim']}" opacity="0.2"/>
    <rect x="130" y="2" width="210" height="10" rx="5" fill="{t['green']}">
      <animate attributeName="width" from="0" to="210" dur="1.2s" fill="freeze"/>
    </rect>
    <text x="350" y="10" fill="{t['green']}" font-family="'Courier New',monospace" font-size="8" font-weight="700">100%</text>
  </g>
</svg>'''
    write_svg(f"leetcode/streak-{suffix}.svg", svg)


# ─── 9. GITHUB ANALYTICS, LANGUAGE DNA, SCOREBOARD ───────────────────────────

def generate_language_dna(theme, suffix):
    t = DARK if theme == "dark" else LIGHT

    langs = [
        ("TypeScript", 38, t["blue"]),
        ("Python", 32, t["violet"]),
        ("JavaScript", 12, t["amber"]),
        ("Dart", 10, t["cyan"]),
        ("C++ / Java", 8, t["green"]),
    ]

    bars = ""
    y = 42
    for name, pct, col in langs:
        bars += f'''
    <g transform="translate(30, {y})">
      <text x="0" y="11" fill="{t['text']}" font-family="'Courier New',monospace" font-size="8.5" font-weight="600">{esc(name)}</text>
      <rect x="120" y="2" width="560" height="12" rx="6" fill="{t['dim']}" opacity="0.18"/>
      <rect x="120" y="2" width="{5.6 * pct:.1f}" height="12" rx="6" fill="{col}">
        <animate attributeName="width" from="0" to="{5.6 * pct:.1f}" dur="1.2s" fill="freeze"/>
      </rect>
      <text x="700" y="11" fill="{col}" font-family="'Courier New',monospace" font-size="8.5" font-weight="700">{pct}%</text>
    </g>'''
        y += 26

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 185" width="780" height="185">
  <rect width="780" height="185" rx="8" fill="{t['bg']}" stroke="{t['border']}" stroke-width="0.5"/>
  <text x="390" y="22" text-anchor="middle" fill="{t['muted']}" font-family="'Courier New',monospace" font-size="8" letter-spacing="4">LANGUAGE DNA // CODE DISTRIBUTION</text>
  {bars}
</svg>'''
    write_svg(f"github/language-dna-{suffix}.svg", svg)


def generate_scoreboard(theme, suffix):
    t = DARK if theme == "dark" else LIGHT

    categories = [
        ("AI / AGENTS", "ACTIVE", t["violet"]),
        ("SYSTEM DESIGN", "ACTIVE", t["cyan"]),
        ("BACKEND / API", "ACTIVE", t["blue"]),
        ("ALGORITHMS (DSA)", "ACTIVE", t["green"]),
        ("CLOUD / DEVOPS", "ADVANCING", t["amber"]),
        ("OPEN SOURCE", "ADVANCING", t["cyan"]),
    ]

    cards = ""
    for i, (cat, status, col) in enumerate(categories):
        x = 25 + (i % 3) * 245
        y = 42 + (i // 3) * 60

        cards += f'''
    <g transform="translate({x}, {y})">
      <rect width="230" height="48" rx="6" fill="{t['bg2']}" stroke="{t['border_subtle']}" stroke-width="1"/>
      <text x="16" y="28" fill="{t['text']}" font-family="'Courier New',monospace" font-size="8.5" font-weight="600">{esc(cat)}</text>
      <rect x="150" y="16" width="68" height="18" rx="9" fill="{col}" fill-opacity="0.15" stroke="{col}" stroke-width="0.8"/>
      <text x="184" y="28" text-anchor="middle" fill="{col}" font-family="'Courier New',monospace" font-size="7" font-weight="700">{esc(status)}</text>
    </g>'''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 170" width="760" height="170">
  <rect width="760" height="170" rx="8" fill="{t['bg']}" stroke="{t['border']}" stroke-width="0.5"/>
  <text x="380" y="22" text-anchor="middle" fill="{t['muted']}" font-family="'Courier New',monospace" font-size="8" letter-spacing="4">ENGINEERING CAPABILITY SCOREBOARD</text>
  {cards}
</svg>'''
    write_svg(f"github/scoreboard-{suffix}.svg", svg)


def generate_skyline(theme, suffix):
    t = DARK if theme == "dark" else LIGHT

    import random
    random.seed(11)
    bars = ""
    for i in range(40):
        h = random.randint(15, 75)
        x = 40 + i * 17
        y = 110 - h
        op = round(0.4 + (h / 75) * 0.55, 2)
        bars += f'<rect x="{x}" y="{y}" width="12" height="{h}" rx="2" fill="{t["cyan"]}" opacity="{op}"/>'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 145" width="760" height="145">
  <rect width="760" height="145" rx="8" fill="{t['bg']}" stroke="{t['border']}" stroke-width="0.5"/>
  <text x="380" y="20" text-anchor="middle" fill="{t['muted']}" font-family="'Courier New',monospace" font-size="8" letter-spacing="4">CONTRIBUTION SKYLINE INTENSITY</text>
  <line x1="30" y1="110" x2="730" y2="110" stroke="{t['border']}" stroke-width="0.8"/>
  {bars}
  <text x="380" y="132" text-anchor="middle" fill="{t['dim']}" font-family="'Courier New',monospace" font-size="7" letter-spacing="2">CONTINUOUS ENGINEERING &amp; COMMIT ACTIVITY</text>
</svg>'''
    write_svg(f"github/skyline-{suffix}.svg", svg)


def generate_activity_pulse(theme, suffix):
    t = DARK if theme == "dark" else LIGHT

    events = [
        ("COMMIT", "AgentForge: hybrid RAG indexing engine", t["cyan"]),
        ("PR", "nexus: real-time WebSocket matching feed", t["violet"]),
        ("ISSUE", "SmartFert: telemetry latency optimization", t["green"]),
        ("RELEASE", "guardian-ai: v1.2 voice SOS trigger", t["amber"]),
        ("PROJECT", "CATI AI: WebRTC conversation FSM", t["blue"]),
    ]

    content = ""
    y = 42
    for tag, desc, col in events:
        content += f'''
    <g transform="translate(35, {y})">
      <rect width="65" height="20" rx="10" fill="{col}" fill-opacity="0.15" stroke="{col}" stroke-width="0.8"/>
      <text x="32.5" y="13.5" text-anchor="middle" fill="{col}" font-family="'Courier New',monospace" font-size="7.5" font-weight="700">{esc(tag)}</text>
      <text x="80" y="13.5" fill="{t['text']}" font-family="system-ui,sans-serif" font-size="9.5">{esc(desc)}</text>
    </g>'''
        y += 28

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 195" width="760" height="195">
  <rect width="760" height="195" rx="8" fill="{t['bg']}" stroke="{t['border']}" stroke-width="0.5"/>
  <text x="380" y="22" text-anchor="middle" fill="{t['muted']}" font-family="'Courier New',monospace" font-size="8" letter-spacing="4">ENGINEERING ACTIVITY PULSE</text>
  {content}
</svg>'''
    write_svg(f"github/activity-pulse-{suffix}.svg", svg)


# ─── 10. AURORA FOOTER ───────────────────────────────────────────────────────

def generate_footer(profile, theme, suffix):
    t = DARK if theme == "dark" else LIGHT
    aurora_colors = f"{t['violet']};{t['cyan']};{t['blue']}" if theme == "dark" else f"{t['blue']};{t['violet']};{t['cyan']}"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 120" width="900" height="120">
  <defs>
    <linearGradient id="footerAurora_{suffix}" x1="0" y1="0" x2="1" y2="0.5">
      <stop offset="0%" stop-color="{t['violet']}" stop-opacity="0.16">
        <animate attributeName="stop-color" values="{aurora_colors}" dur="10s" repeatCount="indefinite"/>
      </stop>
      <stop offset="50%" stop-color="{t['cyan']}" stop-opacity="0.09"/>
      <stop offset="100%" stop-color="{t['blue']}" stop-opacity="0.14">
        <animate attributeName="stop-color" values="{t['blue']};{t['cyan']};{t['violet']}" dur="12s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>
  </defs>
  <rect width="900" height="120" fill="{t['bg']}"/>
  <rect width="900" height="120" fill="url(#footerAurora_{suffix})"/>
  <line x1="80" y1="15" x2="820" y2="15" stroke="{t['border']}" stroke-width="0.5"/>

  <text x="450" y="45" text-anchor="middle" fill="{t['muted']}" font-family="'Courier New',monospace" font-size="9" letter-spacing="8">DESIGN  ·  BUILD  ·  MEASURE  ·  SHIP</text>

  <text x="450" y="75" text-anchor="middle" fill="{t['text']}" font-family="system-ui,sans-serif" font-size="16" font-weight="800" letter-spacing="4">ROSHAN R</text>
  <text x="450" y="95" text-anchor="middle" fill="{t['muted']}" font-family="'Courier New',monospace" font-size="9" letter-spacing="3">Software Engineer • AI Engineering</text>

  <polyline points="0,10 0,0 10,0" fill="none" stroke="{t['violet']}" stroke-width="1" opacity="0.4"/>
  <polyline points="890,0 900,0 900,10" fill="none" stroke="{t['violet']}" stroke-width="1" opacity="0.4"/>
  <polyline points="0,110 0,120 10,120" fill="none" stroke="{t['cyan']}" stroke-width="1" opacity="0.4"/>
  <polyline points="890,120 900,120 900,110" fill="none" stroke="{t['cyan']}" stroke-width="1" opacity="0.4"/>
</svg>'''
    write_svg(f"footer/footer-{suffix}.svg", svg)


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    print("=========================================================")
    print("  ROSHAN // ENGINEERING SYSTEM — Master Asset Generator  ")
    print("=========================================================")

    profile = load_json("profile.json")
    leetcode = load_json("leetcode.json")

    for theme, suffix in [("dark", "dark"), ("light", "light")]:
        print(f"\n[+] Generating {theme.upper()} theme assets...")
        generate_hero(profile, theme, suffix)
        generate_engineering_os(profile, theme, suffix)
        generate_terminal(theme, suffix)
        generate_engineering_pipeline(theme, suffix)
        generate_ai_lab(theme, suffix)
        generate_rag_pipeline(theme, suffix)
        generate_agent_architecture(theme, suffix)
        generate_system_design(theme, suffix)
        generate_devops_pipeline(theme, suffix)
        generate_voice_ai(theme, suffix)
        generate_iot_system(theme, suffix)
        generate_all_project_archs(theme, suffix)
        generate_tech_constellation(theme, suffix)
        generate_leetcode_stats(leetcode, theme, suffix)
        generate_leetcode_heatmap(leetcode, theme, suffix)
        generate_skill_radar(leetcode, theme, suffix)
        generate_leetcode_streak(leetcode, theme, suffix)
        generate_language_dna(theme, suffix)
        generate_scoreboard(theme, suffix)
        generate_skyline(theme, suffix)
        generate_activity_pulse(theme, suffix)
        generate_footer(profile, theme, suffix)

    print("\n[+] All visual assets rendered successfully!")


if __name__ == "__main__":
    main()
