#!/bin/bash
# Shared paths for NYU Torch HPC. Edit ACCOUNT after running: my_slurm_accounts

export ACCOUNT="cfg3"
export PARTITION="c12m85-a100-1"
export NETID="${USER}"

export REPO_DIR="/scratch/${NETID}/nyu-dsga1011-a4"
export OVERLAY_DIR="/scratch/${NETID}/overlays"

# Part1 / Part2 need separate overlays (incompatible package pins)
export OVERLAY_PART1="${OVERLAY_DIR}/a4_part1.ext3"
export OVERLAY_PART2="${OVERLAY_DIR}/a4_part2.ext3"

# Pick a CUDA singularity image available on the cluster:
#   ls /share/apps/images/ | grep -i cuda
export SIF="/share/apps/images/cuda11.8.86-cudnn8.7-devel-ubuntu22.04.2.sif"

# Helper: run a command inside an overlay (read-only, for jobs)
run_in_overlay() {
  local overlay="$1"
  shift
  singularity exec --nv \
    --overlay "${overlay}:ro" \
    "${SIF}" \
    /bin/bash -lc "source /ext3/env.sh; $*"
}
