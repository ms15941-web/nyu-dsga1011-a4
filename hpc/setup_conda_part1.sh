#!/bin/bash
# Create Part 1 conda env (run once on interactive CPU node).
set -euo pipefail
source "${HOME}/miniconda3/bin/activate"
conda create -y -n dsga1011-hw4-part1 python=3.11
conda activate dsga1011-hw4-part1
pip install -r /scratch/${USER}/nyu-dsga1011-a4/part1/requirements.txt
python - <<'PY'
import nltk
nltk.download('wordnet')
nltk.download('punkt')
PY
echo "Part1 conda env ready: dsga1011-hw4-part1"
