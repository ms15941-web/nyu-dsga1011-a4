#!/bin/bash
#SBATCH --job-name=a4_p2_t5
#SBATCH --output=logs/part2_t5_%j.out
#SBATCH --error=logs/part2_t5_%j.err
#SBATCH --time=08:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=48G
#SBATCH --gres=gpu:a100:1
#SBATCH --partition=c12m85-a100-1
#SBATCH --account=ds_ga_1011-2026fa

set -euo pipefail
source "${SLURM_SUBMIT_DIR}/hpc/env_config.sh"
mkdir -p "${REPO_DIR}/logs" "${REPO_DIR}/part2/results" "${REPO_DIR}/part2/records" "${REPO_DIR}/part2/checkpoints"
cd "${REPO_DIR}/part2"

singularity exec --nv \
  --overlay "${OVERLAY_PART2}:ro" \
  "${SIF}" /bin/bash -lc '
    source /ext3/env.sh
    conda activate dsga1011-hw4-part2
    python train_t5.py --finetune --experiment_name experiment
  '
