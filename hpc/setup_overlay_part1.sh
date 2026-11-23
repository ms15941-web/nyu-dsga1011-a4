#!/bin/bash
# ONE-TIME setup for Part 1 conda env inside singularity overlay.
# Run on a compute node (interactive or short sbatch), NOT on login node if possible.
set -euo pipefail
source "$(dirname "$0")/env_config.sh"

mkdir -p "${OVERLAY_DIR}" "${REPO_DIR}"
cd "${OVERLAY_DIR}"

if [[ ! -f "${OVERLAY_PART1}" ]]; then
  cp -n /share/apps/overlay-fs-ext3/overlay-15GB-500K.ext3.gz .
  gunzip -c overlay-15GB-500K.ext3.gz > "${OVERLAY_PART1}"
fi

# Enter overlay in read-write mode and install miniconda + deps
singularity exec --fakeroot --nv \
  --overlay "${OVERLAY_PART1}:rw" \
  "${SIF}" /bin/bash <<'EOF'
set -euo pipefail
if [[ ! -d /ext3/miniconda3 ]]; then
  cd /tmp
  wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
  bash Miniconda3-latest-Linux-x86_64.sh -b -p /ext3/miniconda3
  rm -f Miniconda3-latest-Linux-x86_64.sh
fi

cat > /ext3/env.sh <<'ENV'
#!/bin/bash
unset -f which
source /ext3/miniconda3/etc/profile.d/conda.sh
export PATH=/ext3/miniconda3/bin:$PATH
ENV

source /ext3/env.sh
conda create -y -n dsga1011-hw4-part1 python=3.11
conda activate dsga1011-hw4-part1
pip install -r /scratch/$USER/nyu-dsga1011-a4/part1/requirements.txt
python - <<'PY'
import nltk
nltk.download('wordnet')
nltk.download('punkt')
PY
echo "Part1 overlay ready."
EOF
