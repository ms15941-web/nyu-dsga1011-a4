#!/bin/bash
#SBATCH -J a4_p2_beam8
#SBATCH -p c12m85-a100-1
#SBATCH -A ds_ga_1011-2026fa
#SBATCH --gres=gpu:1
#SBATCH -t 02:00:00
#SBATCH -c 4
#SBATCH --mem=48G
#SBATCH -o logs/part2_infer_beam8_%j.out
#SBATCH -e logs/part2_infer_beam8_%j.err

set -euo pipefail
source "${HOME}/miniconda3/etc/profile.d/conda.sh"
conda activate dsga1011-hw4-part2

REPO_DIR="${SLURM_SUBMIT_DIR}"
mkdir -p "${REPO_DIR}/logs"
cd "${REPO_DIR}/part2"

# Quick try: same checkpoint, stronger decoding (may lift F1 without retrain)
export USE_SCHEMA_HINT=0
python train_t5.py --finetune --experiment_name experiment --infer_only --num_beams 8
