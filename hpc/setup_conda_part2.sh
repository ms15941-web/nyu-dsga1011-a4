#!/bin/bash
# Create Part 2 conda env (run once on interactive CPU node).
set -euo pipefail
source "${HOME}/miniconda3/bin/activate"
conda create -y -n dsga1011-hw4-part2 python=3.11
conda activate dsga1011-hw4-part2
pip install -r /scratch/${USER}/nyu-dsga1011-a4/part2/requirements.txt
echo "Part2 conda env ready: dsga1011-hw4-part2"
