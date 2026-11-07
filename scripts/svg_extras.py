#!/usr/bin/env python3
"""
Extra animated assets for the profile: pixel mascots, typewriter role line,
scrolling skills marquee and a pulse divider. Imported by generate_svgs.py.
"""
import math
import xml.sax.saxutils as saxutils

P = 10  # pixel size of the mascot grid


def esc(text):
    return "" if text is None else saxutils.escape(str(text))


# ─── Pixel mascots ────────────────────────────────────────────────────────────

PAL = {
    "B": "#1e4fa3", "D": "#143a7a",          # headphones
    "O": "#f4794a", "L": "#ff9a6b",          # body, highlight
    "K": "#2a1a14",                          # eyes
    "W": "#f4f1ec", "G": "#d3cfc8",          # chef hat
    "H": "#3a3a3a", "A": "#1f1f1f",          # pan handle, pan
    "S": "#000000",                          # shadow (faded via opacity)
}

HEADPHONES = [
    "....BBBBBBBBBBBBBB....",
    "...BBOOOOOOOOOOOOBB...",
    "...BBOOLLOOOOOOOOBB...",
    "..BBBOOLOOOOOOOOOBBB..",
    "..BDBOOOOOOOOOOOOBDB..",
    "..BDBOOOOOOOOOOOOBDB..",
    "..BDBOOOOOOOOOOOOBDB..",
    "..BBBOOOOOOOOOOOOBBB..",
    "..OOOOOOOOOOOOOOOOOO..",
    "OOOOOOOOOOOOOOOOOOOOOO",
    ".OOOOOOOOOOOOOOOOOOOO.",
    "..OOOOOOOOOOOOOOOOOO..",
    "..OO.OOO..OOOO..OOO.OO",
    "..OO.OOO..OOOO..OOO.OO",
    "..OO.OO...OOOO...OO.OO",
]
HEADPHONES_EYES = [(7, 6), (8, 6), (13, 6), (14, 6)]

CHEF = [
    "........WWWWWWWW..............",
    ".......WWWWWWWWWW.............",
    ".......WWWWWWWWWW.............",
    "........GGGGGGGG..............",
    "........OOOOOOOO..............",
    ".......OOOOOOOOOO.............",
    ".......OOLLOOOOOO.............",
    ".......OOOOOOOOOO.............",
    ".......OOOOOOOOOO.......AAAAAA",
    "..OOOOOOOOOOOOOOOOOOHHHHAAAAAA",
    "..OOOOOOOOOOOOOOOOOO....AAAAAA",
    "....OOOOOOOOOOOOOO............",
    "....OO.OOO..OOOO.OO...........",
    "....OO.OOO..OOOO.OO...........",
    "....OO.OO...OOOO..OO..........",
]
CHEF_EYES = [(9, 7), (10, 7), (13, 7), (14, 7)]
CHEF_FOOD = [(25, 3), (27, 2), (26, 5)]  # sparks flipping over the pan


def mascot_css():
    return """
    @keyframes m-bob { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-7px); } }
    @keyframes m-blink { 0%,90%,100% { transform: scaleY(1); } 94% { transform: scaleY(0.1); } }
    @keyframes m-rise { 0% { transform: translateY(0); opacity: 0; } 20% { opacity: 1; } 100% { transform: translateY(-46px); opacity: 0; } }
    @keyframes m-flip { 0%,100% { transform: translateY(0) rotate(0deg); } 50% { transform: translateY(-30px) rotate(200deg); } }
    @keyframes m-shadow { 0%,100% { opacity: 1; } 50% { opacity: 0.45; } }
    .m-bob { animation: m-bob 2.2s ease-in-out infinite; }
    .m-eyes { transform-box: fill-box; transform-origin: center; animation: m-blink 4.2s infinite; }
    .m-note { animation: m-rise 3s ease-out infinite; opacity: 0; }
    .m-flip { transform-box: fill-box; transform-origin: center; animation: m-flip 1.5s ease-in-out infinite; }
    .m-shadow { animation: m-shadow 2.2s ease-in-out infinite; }
    """


def _rect(x, y, c, p=P):
    return f'<rect x="{x * p}" y="{y * p}" width="{p}" height="{p}" fill="{PAL.get(c, c)}"/>'


def _body(art):
    out = []
    for y, row in enumerate(art):
        for x, ch in enumerate(row):
            if ch != "." and ch in PAL:
                out.append(_rect(x, y, ch))
    return "".join(out)


def _shadow(x0, x1, y):
    return f'<rect x="{x0 * P}" y="{y * P}" width="{(x1 - x0) * P}" height="{P}" fill="#000000" fill-opacity="0.15"/>'


def _note(x, y, delay, color):
    return (f'<g class="m-note" style="animation-delay:{delay}s"><g transform="translate({x},{y})" fill="{color}">'
            f'<rect x="8" y="0" width="3" height="16"/><rect x="0" y="13" width="9" height="6"/>'
            f'<rect x="11" y="0" width="7" height="4"/></g></g>')


def octopus_headphones(x, y, scale=1.0, delay=0.0):
    eyes = "".join(_rect(ex, ey, "K") for ex, ey in HEADPHONES_EYES)
    notes = _note(-18, 6, delay, "#f97316") + _note(222, -12, delay + 1.2, "#3b82f6") + _note(-8, -34, delay + 2.1, "#fbbf24")
    return (f'<g transform="translate({x},{y}) scale({scale})">'
            f'<g class="m-shadow">{_shadow(3, 20, 15)}</g>'
            f'<g class="m-bob" style="animation-delay:{delay}s">{_body(HEADPHONES)}<g class="m-eyes">{eyes}</g></g>'
            f'{notes}</g>')


def octopus_chef(x, y, scale=1.0, delay=0.0):
    eyes = "".join(_rect(ex, ey, "K") for ex, ey in CHEF_EYES)
    food = "".join(
        f'<g class="m-flip" style="animation-delay:{delay + i * 0.35}s">{_rect(fx, fy, "#f5c518")}</g>'
        for i, (fx, fy) in enumerate(CHEF_FOOD)
    )
    return (f'<g transform="translate({x},{y}) scale({scale})">'
            f'<g class="m-shadow">{_shadow(4, 20, 15)}</g>'
            f'<g class="m-bob" style="animation-delay:{delay}s">{_body(CHEF)}<g class="m-eyes">{eyes}</g></g>'
            f'{food}</g>')


def generate_mascot_duo(write_svg):
    """Standalone duo scene used in the README intro (theme neutral)."""
    bubble_font = "'Courier New',monospace"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 250" width="640" height="250" shape-rendering="crispEdges">
  <style>{mascot_css()}
    @keyframes b-pop {{ 0%,8% {{ opacity: 0; transform: translateY(6px); }} 14%,46% {{ opacity: 1; transform: translateY(0); }} 54%,100% {{ opacity: 0; }} }}
    @keyframes b-pop2 {{ 0%,50% {{ opacity: 0; transform: translateY(6px); }} 58%,92% {{ opacity: 1; transform: translateY(0); }} 100% {{ opacity: 0; }} }}
    .b1 {{ animation: b-pop 8s infinite; opacity: 0; }}
    .b2 {{ animation: b-pop2 8s infinite; opacity: 0; }}
  </style>
  <g class="b1" shape-rendering="geometricPrecision">
    <rect x="30" y="8" width="200" height="30" rx="8" fill="#f97316" opacity="0.15" stroke="#f97316" stroke-width="1"/>
    <text x="130" y="28" text-anchor="middle" fill="#f97316" font-family="{bubble_font}" font-size="13" font-weight="700">cooking APIs fresh...</text>
  </g>
  <g class="b2" shape-rendering="geometricPrecision">
    <rect x="400" y="8" width="210" height="30" rx="8" fill="#3b82f6" opacity="0.15" stroke="#3b82f6" stroke-width="1"/>
    <text x="505" y="28" text-anchor="middle" fill="#3b82f6" font-family="{bubble_font}" font-size="13" font-weight="700">debugging to lo-fi beats</text>
  </g>
  {octopus_chef(20, 70, 0.95, 0.0)}
  {octopus_headphones(390, 60, 1.0, 0.6)}
  <rect x="20" y="226" width="600" height="2" fill="#94a3b8" opacity="0.35"/>
</svg>'''
    write_svg("mascot/octopus-duo.svg", svg)


# ─── Typewriter role line ─────────────────────────────────────────────────────

def typewriter_roles(roles, color, cx, y, uid, slot=3.4, size=13, spacing=4):
    """Types each role in, holds, erases it, with a blinking block cursor."""
    n = len(roles)
    cycle = n * slot
    adv = size * 0.6 + spacing
    f = slot / cycle
    defs, body = "", ""
    for i, role in enumerate(roles):
        w = round(len(role) * adv, 1)
        left = round(cx - w / 2, 1)
        kt = [0.0, i * f, i * f + 0.38 * f, i * f + 0.82 * f, (i + 1) * f, 1.0]
        kt = [min(1.0, round(k, 4)) for k in kt]
        kts = ";".join(str(k) for k in kt)
        widths = f"0;0;{w};{w};0;0"
        xs = f"{left};{left};{round(left + w, 1)};{round(left + w, 1)};{left};{left}"
        vis = "0;0;1;1;0;0"
        defs += (f'<clipPath id="tw_{uid}_{i}"><rect x="{left}" y="{y - size - 2}" width="0" height="{size + 10}">'
                 f'<animate attributeName="width" values="{widths}" keyTimes="{kts}" dur="{cycle}s" repeatCount="indefinite"/>'
                 f'</rect></clipPath>')
        body += (f'<text x="{cx}" y="{y}" text-anchor="middle" fill="{color}" font-family="\'Courier New\',monospace" '
                 f'font-size="{size}" font-weight="700" letter-spacing="{spacing}" clip-path="url(#tw_{uid}_{i})">{esc(role)}</text>'
                 f'<g opacity="0"><animate attributeName="opacity" values="{vis}" keyTimes="{kts}" dur="{cycle}s" repeatCount="indefinite"/>'
                 f'<rect x="{left}" y="{y - size + 1}" width="7" height="{size + 1}" fill="{color}">'
                 f'<animate attributeName="x" values="{xs}" keyTimes="{kts}" dur="{cycle}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="1;0.15;1" dur="0.8s" repeatCount="indefinite"/></rect></g>')
    return f"<defs>{defs}</defs>{body}"


# ─── Skills marquee ───────────────────────────────────────────────────────────

def generate_skills_marquee(groups, t, suffix, write_svg):
    W, row_h, pitch, top = 900, 30, 44, 46
    height = top + len(groups) * pitch + 8
    speed = 36.0  # px per second
    css, rows, legend = "", "", ""
    lx = 28
    for gi, g in enumerate(groups):
        col = t[g.get("color", "cyan")]
        items = g["items"]
        chips, x = [], 0.0
        for it in items:
            cw = len(it) * 7.0 + 32
            chips.append((it, x, cw))
            x += cw + 10
        S = x
        copies = int(math.ceil((W + 60) / S)) + 1
        group_svg = ""
        for c in range(copies):
            for it, cx0, cw in chips:
                ox = cx0 + c * S
                group_svg += (f'<g transform="translate({ox:.1f},0)">'
                              f'<rect width="{cw:.1f}" height="{row_h}" rx="15" fill="{t["bg2"]}" stroke="{col}" stroke-width="1" opacity="0.95"/>'
                              f'<circle cx="13" cy="{row_h / 2}" r="2.6" fill="{col}"/>'
                              f'<text x="22" y="{row_h / 2 + 3.6}" fill="{t["text"]}" font-family="\'Courier New\',monospace" font-size="10.5" font-weight="600">{esc(it)}</text></g>')
        dur = round(S / speed, 1)
        direction = "reverse" if gi % 2 else "normal"
        css += (f"@keyframes mq{gi} {{ from {{ transform: translateX(0); }} to {{ transform: translateX({-S:.1f}px); }} }}\n"
                f".mq{gi} {{ animation: mq{gi} {dur}s linear infinite; animation-direction: {direction}; }}\n")
        y = top + gi * pitch
        rows += f'<g transform="translate(0,{y})"><g class="mq{gi}">{group_svg}</g></g>'
        label = g["label"]
        legend += (f'<circle cx="{lx}" cy="24" r="3.5" fill="{col}"/>'
                   f'<text x="{lx + 10}" y="27.5" fill="{t["muted"]}" font-family="\'Courier New\',monospace" font-size="8.5" letter-spacing="1.5">{esc(label)}</text>')
        lx += len(label) * 7.4 + 34

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height}" width="{W}" height="{height}">
  <defs>
    <clipPath id="mqClip_{suffix}"><rect x="0" y="{top - 4}" width="{W}" height="{height - top}"/></clipPath>
    <linearGradient id="fadeL_{suffix}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t['bg']}" stop-opacity="1"/><stop offset="1" stop-color="{t['bg']}" stop-opacity="0"/></linearGradient>
    <linearGradient id="fadeR_{suffix}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t['bg']}" stop-opacity="0"/><stop offset="1" stop-color="{t['bg']}" stop-opacity="1"/></linearGradient>
  </defs>
  <style>
    {css}
  </style>
  <rect width="{W}" height="{height}" rx="10" fill="{t['bg']}" stroke="{t['border']}" stroke-width="0.6"/>
  {legend}
  <g clip-path="url(#mqClip_{suffix})">{rows}</g>
  <rect x="1" y="{top - 4}" width="70" height="{height - top - 2}" fill="url(#fadeL_{suffix})"/>
  <rect x="{W - 71}" y="{top - 4}" width="70" height="{height - top - 2}" fill="url(#fadeR_{suffix})"/>
</svg>'''
    write_svg(f"tech/skills-marquee-{suffix}.svg", svg)


# ─── Pulse divider ────────────────────────────────────────────────────────────

def generate_divider(write_svg):
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 18" width="900" height="18">
  <defs>
    <linearGradient id="dv" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#8B5CF6" stop-opacity="0"/>
      <stop offset="0.25" stop-color="#8B5CF6" stop-opacity="0.8"/>
      <stop offset="0.5" stop-color="#00B8D9" stop-opacity="0.9"/>
      <stop offset="0.75" stop-color="#3B82F6" stop-opacity="0.8"/>
      <stop offset="1" stop-color="#3B82F6" stop-opacity="0"/>
    </linearGradient>
    <filter id="dvGlow" x="-50%" y="-300%" width="200%" height="700%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect x="0" y="8" width="900" height="2" rx="1" fill="url(#dv)"/>
  <g filter="url(#dvGlow)">
    <circle cy="9" r="3" fill="#00B8D9"><animate attributeName="cx" values="-10;910" dur="5s" repeatCount="indefinite"/></circle>
    <circle cy="9" r="2" fill="#8B5CF6"><animate attributeName="cx" values="910;-10" dur="7s" repeatCount="indefinite"/></circle>
  </g>
  <rect x="445" y="4" width="10" height="10" transform="rotate(45 450 9)" fill="none" stroke="#00B8D9" stroke-width="1.2">
    <animate attributeName="opacity" values="0.4;1;0.4" dur="2.4s" repeatCount="indefinite"/>
  </rect>
</svg>'''
    write_svg("divider/pulse.svg", svg)
