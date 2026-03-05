#!/bin/bash
#SBATCH --job-name=diffpepbuilder_run
#SBATCH --gpus-per-node=v100:1
#SBATCH --cpus-per-node:8
#SBATCH --mem=48G                # Request 48GB of RAM
#SBATCH --time=01:00:00          # Max run time (HH:MM:SS)
#SBATCH --output=logs/diffpepbuilder_run-%j.log     # Standard output and error log

mkdir -p logs

cd /scratch/s6771548/AI_Based_Peptide_Ligand_Design/DiffPepBuilder

eval "$(/home5/USER/.local/bin/micromamba shell hook --shell bash)"

micromamba activate ENVIRONMENT

python stuff.py
