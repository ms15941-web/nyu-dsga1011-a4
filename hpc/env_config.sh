#!/bin/bash
# Shared paths for NYU HPC with home Miniconda (no singularity overlay).

export ACCOUNT="ds_ga_1011-2026fa"
export PARTITION="c12m85-a100-1"
export NETID="${USER}"

export REPO_DIR="/scratch/${NETID}/nyu-dsga1011-a4"
export CONDA_ACTIVATE="${HOME}/miniconda3/bin/activate"
export ENV_PART1="dsga1011-hw4-part1"
export ENV_PART2="dsga1011-hw4-part2"
