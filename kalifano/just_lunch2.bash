#!/bin/bash -l
#SBATCH -s
#SBATCH -n 1
#SBATCH -o testGPU.out
#SBATCH -J MyJobName
#SBATCH -p cuda
#SBATCH -c 8
#SBATCH --gres=gpu:fat

export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}
export OPENBLAS_NUM_THREADS=${SLURM_CPUS_PER_TASK}
export MKL_NUM_THREADS=${SLURM_CPUS_PER_TASK}
export VECLIB_MAXIMUM_THREADS=${SLURM_CPUS_PER_TASK}
export NUMEXPR_NUM_THREADS=${SLURM_CPUS_PER_TASK}
export HUGGINGFACE_HUB_TOKEN="YOUR HF TOKEN HERE"
# Activate conda environment
source $(conda info --base)/etc/profile.d/conda.sh
conda activate ai4MDE

# Run the script
srun python "$@"