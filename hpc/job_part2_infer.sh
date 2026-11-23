#!/bin/bash
#SBATCH -J a4_p2_infer
#SBATCH -p c12m85-a100-1
#SBATCH -A ds_ga_1011-2026fa
#SBATCH --gres=gpu:1
#SBATCH -t 02:00:00
#SBATCH -c 4
#SBATCH --mem=48G
#SBATCH -o logs/part2_infer_%j.out
#SBATCH -e logs/part2_infer_%j.err

set -euo pipefail
source "${HOME}/miniconda3/etc/profile.d/conda.sh"
conda activate dsga1011-hw4-part2

REPO_DIR="${SLURM_SUBMIT_DIR}"
mkdir -p "${REPO_DIR}/logs" "${REPO_DIR}/part2/results" "${REPO_DIR}/part2/records"
cd "${REPO_DIR}/part2"

# Reuse trained best checkpoint; only regenerate dev/test predictions
python train_t5.py --finetune --experiment_name experiment --infer_only
