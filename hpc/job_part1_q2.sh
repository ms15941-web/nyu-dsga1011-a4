#!/bin/bash
#SBATCH --job-name=a4_p1_q2
#SBATCH --output=logs/part1_q2_%j.out
#SBATCH --error=logs/part1_q2_%j.err
#SBATCH --time=00:30:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --gres=gpu:1
#SBATCH --account=REPLACE_WITH_YOUR_SLURM_ACCOUNT

set -euo pipefail
source "${SLURM_SUBMIT_DIR}/hpc/env_config.sh"
mkdir -p "${REPO_DIR}/logs"
cd "${REPO_DIR}/part1"

# Requires ./out from Q1
singularity exec --nv \
  --overlay "${OVERLAY_PART1}:ro" \
  "${SIF}" /bin/bash -lc '
    source /ext3/env.sh
    conda activate dsga1011-hw4-part1
    python main.py --eval_transformed
  '
