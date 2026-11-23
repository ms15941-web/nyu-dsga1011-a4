#!/bin/bash
#SBATCH --job-name=a4_p1_q1
#SBATCH --output=logs/part1_q1_%j.out
#SBATCH --error=logs/part1_q1_%j.err
#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --gres=gpu:a100:1
#SBATCH --partition=c12m85-a100-1
#SBATCH --account=cfg3

set -euo pipefail
source "${SLURM_SUBMIT_DIR}/hpc/env_config.sh"
mkdir -p "${REPO_DIR}/logs"
cd "${REPO_DIR}/part1"

singularity exec --nv \
  --overlay "${OVERLAY_PART1}:ro" \
  "${SIF}" /bin/bash -lc '
    source /ext3/env.sh
    conda activate dsga1011-hw4-part1
    # debug first (optional): python main.py --train --eval --debug_train
    python main.py --train --eval
  '
