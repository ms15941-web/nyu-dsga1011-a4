#!/bin/bash
# ONE-TIME setup for Part 2 conda env inside singularity overlay.
set -euo pipefail
source "$(dirname "$0")/env_config.sh"

mkdir -p "${OVERLAY_DIR}"
cd "${OVERLAY_DIR}"

if [[ ! -f "${OVERLAY_PART2}" ]]; then
  cp -n /share/apps/overlay-fs-ext3/overlay-15GB-500K.ext3.gz .
  gunzip -c overlay-15GB-500K.ext3.gz > "${OVERLAY_PART2}"
fi

singularity exec --fakeroot --nv \
  --overlay "${OVERLAY_PART2}:rw" \
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
conda create -y -n dsga1011-hw4-part2 python=3.11
conda activate dsga1011-hw4-part2
pip install -r /scratch/$USER/nyu-dsga1011-a4/part2/requirements.txt
echo "Part2 overlay ready."
EOF
