#!/usr/bin/env python3
"""
Simple local LLM prompt script with CUDA support.

Usage examples:
  # activate conda env first
  conda activate met_cuda_env

  # Prompt once and exit
  python simple_prompt_local_llm.py --model-path ./llama2-finetuned --prompt "Write a short summary about cats."

  # Interactive REPL
  python simple_prompt_local_llm.py --model-path ./llama2-finetuned --interactive

Notes:
- Expects a Hugging Face style model directory (local or remote repo id).
- Tries to load model onto CUDA if available; otherwise falls back to CPU.
"""
import argparse
import sys
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


def load_model_and_tokenizer(model_path, device):
    print(f"Loading tokenizer and model from: {model_path}")
    # If model_path is a local directory, verify it contains files
    if os.path.isdir(model_path):
        files = os.listdir(model_path)
        if len(files) == 0:
            raise FileNotFoundError(
                f"Local model directory '{model_path}' is empty.\n"
                "Place the model and tokenizer files in this directory, or pass a Hugging Face model id (e.g. 'meta-llama/Llama-2-7b-hf')."
            )

    # Try slow tokenizer first for Llama-style models; fall back to fast if available
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
    except TypeError as e:
        # Catch errors like 'not a string' from sentencepiece and provide guidance
        raise RuntimeError(
            f"Failed to load tokenizer from '{model_path}': {e}\n"
            "This usually means the tokenizer files are missing or invalid.\n"
            "If you intended to use a local model folder, ensure it contains tokenizer files (e.g. tokenizer.model / spm.model).\n"
            "Alternatively, pass a Hugging Face model id to download the tokenizer automatically."
        )

    # Try to load onto GPU with fp16 if available; fall back to cpu if any error
    try:
        if device == "cuda":
            print("Attempting to load model on CUDA (fp16, device_map='auto')...")
            model = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.float16,
                device_map='auto',
                low_cpu_mem_usage=True,
            )
        else:
            print("Loading model on CPU (float32)...")
            model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float32)
    except Exception as e:
        print("Model load with device_map/FP16 failed, retrying on CPU:", e)
        model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float32)

    # Ensure tokenizer has pad token
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    return model, tokenizer


def generate_once(model, tokenizer, prompt, max_new_tokens=128, device_str="cuda"):
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    input_ids = inputs.input_ids.to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            input_ids,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            top_p=0.95,
            temperature=0.8,
            pad_token_id=tokenizer.eos_token_id,
        )
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return text


DEFAULT_MODEL_ID = "meta-llama/Llama-2-7b-hf"


def main():
    parser = argparse.ArgumentParser(description="Simple local LLM prompt with CUDA support")
    parser.add_argument(
        "--model-path",
        default=DEFAULT_MODEL_ID,
        help="Local model directory or HF repo id (default: meta-llama/Llama-2-7b-hf). If the model is not present locally it will be downloaded.",
    )
    parser.add_argument("--prompt", default=None, help="Prompt to send to the model (non-interactive)")
    parser.add_argument("--interactive", action="store_true", help="Start interactive prompt REPL")
    parser.add_argument("--max-new-tokens", type=int, default=128, help="Max new tokens to generate")
    args = parser.parse_args()

    # Determine device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # Load model (if `--model-path` is a local dir with files we'll use it; otherwise treat it as a HF id and download)
    model, tokenizer = load_model_and_tokenizer(args.model_path, device)

    # If using cuda and model is not on cuda, move it
    if device == "cuda":
        try:
            # If model uses device_map='auto', it is already loaded on correct devices
            # Otherwise try to move to cuda
            if next(model.parameters()).device.type != "cuda":
                model = model.to('cuda')
        except Exception:
            pass

    # Interactive REPL
    if args.interactive:
        print("Interactive mode (type 'exit' or Ctrl+C to quit)")
        while True:
            try:
                prompt = input("PROMPT> ")
                if prompt.strip().lower() in ["exit", "quit"]:
                    break
                out = generate_once(model, tokenizer, prompt, max_new_tokens=args.max_new_tokens)
                print("\n=== RESPONSE ===\n")
                print(out)
                print("\n================\n")
            except KeyboardInterrupt:
                print("Exiting interactive mode")
                break
    else:
        if args.prompt is None:
            print("No prompt provided. Use --prompt or --interactive")
            sys.exit(1)
        out = generate_once(model, tokenizer, args.prompt, max_new_tokens=args.max_new_tokens)
        print("\n=== RESPONSE ===\n")
        print(out)


if __name__ == '__main__':
    main()
