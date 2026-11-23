#!/bin/bash
#SBATCH -J a4_p2_t5
#SBATCH -p c12m85-a100-1
#SBATCH -A ds_ga_1011-2026fa
#SBATCH --gres=gpu:1
#SBATCH -t 08:00:00
#SBATCH -c 4
#SBATCH --mem=48G
#SBATCH -o logs/part2_t5_%j.out
#SBATCH -e logs/part2_t5_%j.err

set -euo pipefail
source "${HOME}/miniconda3/bin/activate"
conda activate dsga1011-hw4-part2

REPO_DIR="/scratch/${USER}/nyu-dsga1011-a4"
mkdir -p "${REPO_DIR}/logs" "${REPO_DIR}/part2/results" "${REPO_DIR}/part2/records" "${REPO_DIR}/part2/checkpoints"
cd "${REPO_DIR}/part2"

python train_t5.py --finetune --experiment_name experiment
