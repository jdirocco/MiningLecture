# Running on SLURM Cluster with GPU

## Setup (one-time)

1. **Create conda environment** (on login node):
```bash
conda env create -f environment.yml
```

This will create the `met_cuda_env` environment with all dependencies.

## Testing CUDA on GPU node

Before running the full training, test that CUDA works on the GPU node:

```bash
sbatch just_lunch2.bash test_cuda_on_gpu_node.py
```

Check the output:
```bash
cat testGPU.out
```

You should see:
- `cuda available: True`
- GPU device name
- Successful CUDA computation

## Running the full pipeline

Submit the job to SLURM:

```bash
sbatch just_lunch2.bash main.py
```

### With options:

Skip preprocessing (if already done):
```bash
sbatch just_lunch2.bash main.py --skip-preprocessing
```

Skip training (only evaluate):
```bash
sbatch just_lunch2.bash main.py --skip-preprocessing --skip-training
```

## Check job status

```bash
squeue -u $USER
```

## View output

```bash
tail -f testGPU.out
```

## Important notes

- The `just_lunch2.bash` script activates the `met_cuda_env` conda environment automatically
- CUDA is only available on GPU nodes (partition `cuda`), not on login nodes
- The script requests a `gpu:fat` resource - adjust if needed based on your cluster configuration
- Don't use `nvidia-smi` or test CUDA on login nodes - it won't work

## Troubleshooting

### If CUDA is not available on GPU node:

1. Check SLURM output: `cat testGPU.out`
2. Verify GPU was allocated: `grep -i gpu testGPU.out` (should show GPU device)
3. Check conda environment activated: `grep -i "met_cuda_env" testGPU.out`
4. Contact cluster admin if GPU node has driver issues

### If imports fail:

Re-create environment:
```bash
conda env remove -n met_cuda_env
conda env create -f environment.yml
```

## 🧪 Running the simple prompt script (inference only)

This project includes a lightweight inference script `simple_prompt_local_llm.py` that loads a Hugging Face model and generates text. The script will download the model automatically if you pass a HF model id (for example `meta-llama/Llama-2-7b-hf`).

### 1) Run locally (login node or workstation with GPU)

Activate the conda environment and run the script. If the model requires access, export your Hugging Face token first.

```bash
conda activate met_cuda_env
# If the model requires authentication (Llama2), set your HF token
export HUGGINGFACE_HUB_TOKEN="hf_xxx..."

# Run a single prompt (will download model if needed)
python simple_prompt_local_llm.py --model-path meta-llama/Llama-2-7b-hf --prompt "Write a short summary about cats."
```

Notes:
- The first run will download model files into the HF cache (e.g. `~/.cache/huggingface/`), which can be large.
- If you prefer to pre-download the model to a local folder (recommended if compute nodes have no internet), see the next section.

### 2) Pre-download model to a local/shared directory (recommended for clusters)

On a login node with network access, download the model into a shared folder accessible from compute nodes:

```bash
conda activate met_cuda_env
python - <<'PY'
from huggingface_hub import snapshot_download
snapshot_download("meta-llama/Llama-2-7b-hf", cache_dir="./llama2-finetuned", repo_type="model")
print("Downloaded to ./llama2-finetuned")
PY

# Then run inference pointing to the local directory
python simple_prompt_local_llm.py --model-path ./llama2-finetuned --prompt "Write a short summary about cats."
```

### 3) Run on a GPU node via SLURM

Use your SLURM wrapper `just_lunch2.bash` (it activates `met_cuda_env`). If the model is large, prefer the pre-downloaded local folder.

Run (download-on-demand):
```bash
sbatch just_lunch2.bash simple_prompt_local_llm.py --model-path meta-llama/Llama-2-7b-hf --prompt "Write a short summary about cats."
```

Run (pre-downloaded model):
```bash
sbatch just_lunch2.bash simple_prompt_local_llm.py --model-path ./llama2-finetuned --prompt "Write a short summary about cats."
```

If the compute nodes have no internet, make sure the folder `./llama2-finetuned` is on shared storage accessible by the compute nodes (NFS, Lustre, etc.).

### 4) Interactive REPL on a GPU node

For interactive usage on a GPU node, either use an interactive allocation or salloc, then run the script in REPL mode:

```bash
# Allocate an interactive GPU shell (example)
salloc --gres=gpu:1 --cpus-per-task=8 --time=01:00:00 --partition=cuda
conda activate met_cuda_env
python simple_prompt_local_llm.py --model-path ./llama2-finetuned --interactive
```

### 5) Troubleshooting model downloads and auth

- If download fails with a permissions error, make sure you have accepted the model license on Hugging Face and set `HUGGINGFACE_HUB_TOKEN` (or run `huggingface-cli login`).
- If the model is too large for the GPU or you get OOM, use a smaller model (for testing try `TinyLlama/TinyLlama-1.1B-Chat-v1.0`) or run inference on CPU.
- To force CPU-only loading, run:

```bash
python simple_prompt_local_llm.py --model-path meta-llama/Llama-2-7b-hf --prompt "Hi" --device cpu
```

### 6) Example SLURM job for small model (included)

There is an example job `run_with_small_model.bash` that runs `main.py` with a small model; you can adapt it to call `simple_prompt_local_llm.py` instead:

```bash
sbatch run_with_small_model.bash
```

---

End of SLURM usage tips.
