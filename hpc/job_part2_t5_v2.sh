#!/bin/bash
#SBATCH -J a4_p2_t5v2
#SBATCH -p c12m85-a100-1
#SBATCH -A ds_ga_1011-2026fa
#SBATCH --gres=gpu:1
#SBATCH -t 12:00:00
#SBATCH -c 4
#SBATCH --mem=48G
#SBATCH -o logs/part2_t5v2_%j.out
#SBATCH -e logs/part2_t5v2_%j.err

set -euo pipefail
source "${HOME}/miniconda3/etc/profile.d/conda.sh"
conda activate dsga1011-hw4-part2

REPO_DIR="${SLURM_SUBMIT_DIR}"
mkdir -p "${REPO_DIR}/logs" "${REPO_DIR}/part2/results" "${REPO_DIR}/part2/records" "${REPO_DIR}/part2/checkpoints"
cd "${REPO_DIR}/part2"

# Stronger finetune (schema hint + higher lr + longer training)
export USE_SCHEMA_HINT=1
python train_t5.py \
  --finetune \
  --experiment_name experiment_v2 \
  --learning_rate 3e-4 \
  --max_n_epochs 30 \
  --patience_epochs 6 \
  --num_beams 5 \
  --batch_size 16 \
  --test_batch_size 8

# Copy to Gradescope submission names if this run looks good
cp -f results/t5_ft_experiment_v2_test.sql results/t5_ft_experiment_test.sql
cp -f records/t5_ft_experiment_v2_test.pkl records/t5_ft_experiment_test.pkl
echo "Copied v2 test outputs to t5_ft_experiment_test.*"
