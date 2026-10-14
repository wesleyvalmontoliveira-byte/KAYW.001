#!/usr/bin/env bash
# Regenera todo o kit (miolos, imposição A4, capas, extras, mockups e guia).
# Requisitos: python3 + pip install reportlab pillow pymupdf pypdf
set -euo pipefail
cd "$(dirname "$0")/src"
python3 build_miolo.py all
python3 impose_a4.py ../produto/miolo/Planner-2027-Miolo-A5-Delicada.pdf ../produto/miolo/Planner-2027-Miolo-A5-Neutra.pdf
python3 build_capas.py
python3 build_extras.py
python3 build_mockups.py
python3 build_guia.py
echo "✔ kit completo em $(cd ../produto && pwd)"
