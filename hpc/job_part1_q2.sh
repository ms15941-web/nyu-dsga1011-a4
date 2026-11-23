#!/bin/bash
#SBATCH -J a4_p1_q2
#SBATCH -p c12m85-a100-1
#SBATCH -A ds_ga_1011-2026fa
#SBATCH --gres=gpu:1
#SBATCH -t 00:30:00
#SBATCH -c 4
#SBATCH --mem=32G
#SBATCH -o logs/part1_q2_%j.out
#SBATCH -e logs/part1_q2_%j.err

set -euo pipefail
source "${HOME}/miniconda3/bin/activate"
conda activate dsga1011-hw4-part1

REPO_DIR="/scratch/${USER}/nyu-dsga1011-a4"
mkdir -p "${REPO_DIR}/logs"
cd "${REPO_DIR}/part1"

python main.py --eval_transformed
