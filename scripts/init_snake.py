#!/usr/bin/env python3
"""
Generate initial neon contribution grid snake SVGs so local references resolve instantly
before the GitHub Action executes for the first time.
"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GITHUB_ASSETS = os.path.join(BASE_DIR, "assets", "github")
os.makedirs(GITHUB_ASSETS, exist_ok=True)

def make_snake_svg(theme="dark"):
    bg = "#0A0E1A" if theme == "dark" else "#F8FAFC"
    dot_empty = "#111827" if theme == "dark" else "#E2E8F0"
    dot_mid = "#3B82F6" if theme == "dark" else "#93C5FD"
    dot_high = "#8B5CF6" if theme == "dark" else "#60A5FA"
    snake_head = "#00E5FF" if theme == "dark" else "#0891B2"

    dots = ""
    import random
    random.seed(13)
    for col in range(52):
        for row in range(7):
            x = 15 + col * 14
            y = 15 + row * 14
            v = random.random()
            if v < 0.5:
                color = dot_empty
            elif v < 0.8:
                color = dot_mid
            else:
                color = dot_high
            dots += f'<rect x="{x}" y="{y}" width="10" height="10" rx="2" fill="{color}"/>'

    # Animated neon snake trail
    snake_path = ""
    for i in range(8):
        sx = 15 + (28 + i) * 14
        sy = 15 + 3 * 14
        op = round((i + 1) / 8, 2)
        fill = snake_head if i == 7 else dot_high
        snake_path += f'<rect x="{sx}" y="{sy}" width="10" height="10" rx="2.5" fill="{fill}" opacity="{op}"/>'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 130" width="760" height="130">
  <rect width="760" height="130" rx="8" fill="{bg}" stroke="{"rgba(0,229,255,0.15)" if theme=="dark" else "rgba(59,130,246,0.2)"}" stroke-width="0.5"/>
  <text x="380" y="122" text-anchor="middle" fill="{"#94A3B8" if theme=="dark" else "#64748B"}" font-family="'Courier New',monospace" font-size="7" letter-spacing="2">NEON CONTRIBUTION SNAKE // PIXEL TELEMETRY</text>
  {dots}
  {snake_path}
</svg>'''
    return svg

with open(os.path.join(GITHUB_ASSETS, "github-contribution-grid-snake-dark.svg"), "w", encoding="utf-8") as f:
    f.write(make_snake_svg("dark"))

with open(os.path.join(GITHUB_ASSETS, "github-contribution-grid-snake-light.svg"), "w", encoding="utf-8") as f:
    f.write(make_snake_svg("light"))

print("Created snake SVGs.")
