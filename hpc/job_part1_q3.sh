#!/bin/bash
#SBATCH -J a4_p1_q3
#SBATCH -p c12m85-a100-1
#SBATCH -A ds_ga_1011-2026fa
#SBATCH --gres=gpu:1
#SBATCH -t 02:30:00
#SBATCH -c 4
#SBATCH --mem=32G
#SBATCH -o logs/part1_q3_%j.out
#SBATCH -e logs/part1_q3_%j.err

set -euo pipefail
source "${HOME}/miniconda3/etc/profile.d/conda.sh"
conda activate dsga1011-hw4-part1

REPO_DIR="${SLURM_SUBMIT_DIR}"
mkdir -p "${REPO_DIR}/logs"
cd "${REPO_DIR}/part1"

python main.py --train_augmented --eval_transformed
python main.py --eval --model_dir out_augmented
python main.py --eval_transformed --model_dir out_augmented
