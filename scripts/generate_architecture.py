#!/usr/bin/env python3
"""
ROSHAN // ENGINEERING SYSTEM — Architecture Diagram Generator
=============================================================
Generates all system design, AI lab, RAG, Agentic, Voice AI, IoT,
DevOps, and project architecture diagrams.
"""

import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from generate_svgs import (
    generate_ai_lab,
    generate_rag_pipeline,
    generate_agent_architecture,
    generate_system_design,
    generate_devops_pipeline,
    generate_voice_ai,
    generate_iot_system,
    generate_all_project_archs,
    generate_engineering_pipeline,
    generate_tech_constellation,
)

def main():
    print("=========================================================")
    print("  ROSHAN // ARCHITECTURE DIAGRAM ENGINE                  ")
    print("=========================================================")
    for theme, suffix in [("dark", "dark"), ("light", "light")]:
        print(f"  ▸ Rendering {theme.upper()} architecture diagrams...")
        generate_ai_lab(theme, suffix)
        generate_rag_pipeline(theme, suffix)
        generate_agent_architecture(theme, suffix)
        generate_system_design(theme, suffix)
        generate_devops_pipeline(theme, suffix)
        generate_voice_ai(theme, suffix)
        generate_iot_system(theme, suffix)
        generate_all_project_archs(theme, suffix)
        generate_engineering_pipeline(theme, suffix)
        generate_tech_constellation(theme, suffix)
    print("  [+] All architecture diagrams rendered successfully.")

if __name__ == "__main__":
    main()
