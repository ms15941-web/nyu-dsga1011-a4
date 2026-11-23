#!/bin/bash
#SBATCH -J a4_p1_q1
#SBATCH -p c12m85-a100-1
#SBATCH -A ds_ga_1011-2026fa
#SBATCH --gres=gpu:1
#SBATCH -t 02:00:00
#SBATCH -c 4
#SBATCH --mem=32G
#SBATCH -o logs/part1_q1_%j.out
#SBATCH -e logs/part1_q1_%j.err

set -euo pipefail

source "${HOME}/miniconda3/etc/profile.d/conda.sh"
conda activate dsga1011-hw4-part1

# Directory from which you ran `sbatch` (should be the repo root)
REPO_DIR="${SLURM_SUBMIT_DIR}"
mkdir -p "${REPO_DIR}/logs"
cd "${REPO_DIR}/part1"

echo "REPO_DIR=${REPO_DIR}"
echo "hostname=$(hostname)"
echo "pwd=$(pwd)"
echo "which python=$(which python)"
python -c "import torch; print('cuda:', torch.cuda.is_available(), 'gpus:', torch.cuda.device_count())"

python main.py --train --eval
