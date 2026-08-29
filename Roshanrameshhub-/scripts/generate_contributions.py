#!/usr/bin/env python3
"""
ROSHAN // ENGINEERING SYSTEM — Contribution Visualization Generator
===================================================================
Generates contribution skyline and activity pulse visualizations
from active commit data and GitHub contribution feeds.
"""

import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from generate_svgs import generate_skyline, generate_activity_pulse, generate_language_dna, generate_scoreboard

def main():
    print("=========================================================")
    print("  ROSHAN // CONTRIBUTION VISUALIZATION ENGINE            ")
    print("=========================================================")
    for theme, suffix in [("dark", "dark"), ("light", "light")]:
        generate_skyline(theme, suffix)
        generate_activity_pulse(theme, suffix)
        generate_language_dna(theme, suffix)
        generate_scoreboard(theme, suffix)
    print("  [+] Contribution visuals generated successfully.")

if __name__ == "__main__":
    main()
