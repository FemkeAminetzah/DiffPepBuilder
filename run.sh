#!/bin/bash
#set -e  # Stop on first error

# uv run python run_diffpepbuilder.py \
#   --pdb examples/receptor_data/1SHY.pdb \
#   --lig_chain "A" \
#   --min_length 28 \
#   --max_length 30 \
#   --samples_per_length 8 \
#   --build_ss_bond \

uv run python run_diffpepbuilder.py \
  --pdb examples/receptor_data/4K3JMET.pdb \
  --lig_chain "A" \
  --min_length 12 \
  --max_length 30 \
  --samples_per_length 8 \
  --build_ss_bond \

# uv run python run_diffpepbuilder.py \
#   --pdb examples/receptor_data/6I04_cMET.pdb \
#   --hotspots "A159,A190,A124" \
#   --min_length 12 \
#   --max_length 30 \
#   --samples_per_length 8 \
#   --build_ss_bond \

# uv run python run_diffpepbuilder.py \
#   --pdb examples/receptor_data/7MO7_cMET.pdb \
#   --hotspots "E290,E323,E457" \
#   --min_length 12 \
#   --max_length 30 \
#   --samples_per_length 8 \
#   --build_ss_bond \

#echo "All three runs complete."