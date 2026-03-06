#!/usr/bin/env python

import os
import json
import yaml
import argparse
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DPB_DIR = ROOT
CONFIG_PATH = DPB_DIR / "config" / "inference.yaml"


def write_receptor_json(pdb_path: Path, hotspots=None, motif=None, lig_chain=None):
    test_dir = ROOT / "test_case"
    test_dir.mkdir(parents=True, exist_ok=True)

    key = pdb_path.stem

    data = {}
    if lig_chain:
        data["lig_chain"] = lig_chain
    if hotspots:
        data["hotspots"] = hotspots.replace(",", "-")
    if motif:
        data["motif"] = motif.replace(",", "-")

    final_data = {key: data}

    json_path = test_dir / "de_novo_cases.json"
    with open(json_path, "w") as f:
        json.dump(final_data, f, indent=4)

    return test_dir, json_path


def update_inference_yaml(args):
    with open(CONFIG_PATH, "r") as f:
        yaml_data = yaml.safe_load(f)

    yaml_data["inference"]["denoising"]["num_t"] = args.denoising_steps
    yaml_data["inference"]["denoising"]["noise_scale"] = args.noise_scale
    yaml_data["inference"]["sampling"]["min_length"] = args.min_length
    yaml_data["inference"]["sampling"]["max_length"] = args.max_length
    yaml_data["inference"]["sampling"]["samples_per_length"] = args.samples_per_length
    yaml_data["inference"]["sampling"]["seq_temperature"] = args.seq_temperature
    yaml_data["inference"]["ss_bond"]["build_ss_bond"] = args.build_ss_bond
    yaml_data["inference"]["ss_bond"]["max_ss_bond"] = args.max_ss_bond
    yaml_data["inference"]["ss_bond"]["entropy_threshold"] = args.entropy_threshold

    with open(CONFIG_PATH, "w") as f:
        yaml.dump(yaml_data, f)


def run_process_receptor(test_dir, json_path):
    cmd = [
        "python",
        str(DPB_DIR / "experiments" / "process_receptor.py"),
        "--pdb_dir", str(test_dir),
        "--write_dir", str(test_dir),
        "--receptor_info_path", str(json_path),
    ]
    subprocess.run(cmd, check=True)


def run_inference():
    os.environ["BASE_PATH"] = str(DPB_DIR)

    cmd = [
        "torchrun",
        "--nproc-per-node=1",
        str(DPB_DIR / "experiments" / "run_inference.py"),
        "data.val_csv_path=test_case/metadata_test.csv",
        "experiment.use_ddp=False",
        "experiment.num_gpus=1",
        "experiment.num_loader_workers=1",
    ]

    subprocess.run(cmd, check=True)


def run_postprocess():
    cmd = [
        "python",
        str(DPB_DIR / "experiments" / "run_postprocess.py"),
    ]
    subprocess.run(cmd, check=True)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--pdb", required=True, help="Path to receptor PDB")
    parser.add_argument("--hotspots", default=None)
    parser.add_argument("--motif", default=None)
    parser.add_argument("--lig_chain", default=None)

    parser.add_argument("--denoising_steps", type=int, default=200)
    parser.add_argument("--noise_scale", type=float, default=1.0)
    parser.add_argument("--seq_temperature", type=float, default=0.1)

    parser.add_argument("--min_length", type=int, default=12)
    parser.add_argument("--max_length", type=int, default=16)
    parser.add_argument("--samples_per_length", type=int, default=4)

    parser.add_argument("--build_ss_bond", action="store_true")
    parser.add_argument("--max_ss_bond", type=int, default=2)
    parser.add_argument("--entropy_threshold", type=float, default=0.01)

    args = parser.parse_args()

    pdb_path = Path(args.pdb).resolve()
    if not pdb_path.exists():
        raise FileNotFoundError(pdb_path)

    test_dir, json_path = write_receptor_json(
        pdb_path,
        hotspots=args.hotspots,
        motif=args.motif,
        lig_chain=args.lig_chain,
    )

    # copy pdb into test_case
    dest = test_dir / pdb_path.name
    if not dest.exists():
        dest.write_bytes(pdb_path.read_bytes())

    update_inference_yaml(args)

    print("=== Preprocessing receptor ===")
    run_process_receptor(test_dir, json_path)

    print("=== Running inference ===")
    run_inference()

    print("=== Running postprocess ===")
    run_postprocess()

    print("Done.")


if __name__ == "__main__":
    main()