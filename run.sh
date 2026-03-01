uv run python run_diffpepbuilder.py \
  --pdb examples/receptor_data/alk1.pdb \
  --hotspots "B40, B58-59, B71-72, B87" \
  --min_length 12 \
  --max_length 16 \
  --samples_per_length 4 \
  --build_ss_bond