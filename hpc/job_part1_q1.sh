#!/bin/bash
#SBATCH --job-name=a4_p1_q1
#SBATCH --output=logs/part1_q1_%j.out
#SBATCH --error=logs/part1_q1_%j.err
#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --gres=gpu:a100:1
#SBATCH --partition=c12m85-a100-1
#SBATCH --account=ds_ga_1011-2026fa

set -euo pipefail
source "${HOME}/miniconda3/bin/activate"
conda activate dsga1011-hw4-part1

REPO_DIR="/scratch/${USER}/nyu-dsga1011-a4"
mkdir -p "${REPO_DIR}/logs"
cd "${REPO_DIR}/part1"

python main.py --train --eval
