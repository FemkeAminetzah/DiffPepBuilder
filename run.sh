uv run python run_diffpepbuilder.py \
  --pdb examples/receptor_data/5HO6_cMET_only.pdb \
  --hotspots "A1106,A1159,A1180,A1184" \
  --min_length 12 \
  --max_length 16 \
  --samples_per_length 4 \
  --build_ss_bond