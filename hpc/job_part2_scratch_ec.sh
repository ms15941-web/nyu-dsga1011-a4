#!/bin/bash
#SBATCH -J a4_p2_ec
#SBATCH -p c12m85-a100-1
#SBATCH -A ds_ga_1011-2026fa
#SBATCH --gres=gpu:1
#SBATCH -t 16:00:00
#SBATCH -c 4
#SBATCH --mem=48G
#SBATCH -o logs/part2_ec_%j.out
#SBATCH -e logs/part2_ec_%j.err

set -euo pipefail
source "${HOME}/miniconda3/etc/profile.d/conda.sh"
conda activate dsga1011-hw4-part2

REPO_DIR="${SLURM_SUBMIT_DIR}"
mkdir -p "${REPO_DIR}/logs" "${REPO_DIR}/part2/results" "${REPO_DIR}/part2/records" "${REPO_DIR}/part2/checkpoints"
cd "${REPO_DIR}/part2"

# Extra credit: train T5-small from scratch (no --finetune)
export USE_SCHEMA_HINT=1
python train_t5.py \
  --experiment_name experiment_ec \
  --learning_rate 1e-3 \
  --max_n_epochs 60 \
  --patience_epochs 8 \
  --num_warmup_epochs 2 \
  --num_beams 5 \
  --batch_size 16 \
  --test_batch_size 8

# Gradescope expects t5_ft_experiment_ec_test.* even for scratch models
cp -f results/t5_scr_experiment_ec_test.sql results/t5_ft_experiment_ec_test.sql
cp -f records/t5_scr_experiment_ec_test.pkl records/t5_ft_experiment_ec_test.pkl
echo "Copied EC test outputs to t5_ft_experiment_ec_test.*"
