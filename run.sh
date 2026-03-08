uv run python run_diffpepbuilder.py \
  --pdb examples/receptor_data/1SHY_cMET.pdb \
  --hotspots "B124,B159,B190" \
  --min_length 12 \
  --max_length 30 \
  --samples_per_length 10 \
  --build_ss_bond \
  --amber_relax \
  --rosetta_relax