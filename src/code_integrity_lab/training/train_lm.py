"""Train a decoder-only Transformer from random initialization on an authorized corpus.

The model weights start randomly initialized. This is base language-model pretraining,
not a supervised vulnerability detector.
"""
from __future__ import annotations

import argparse
import inspect
import json
import math
import os
from itertools import chain
from pathlib import Path
from typing import Any

import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    GPT2Config,
    GPT2LMHeadModel,
    Trainer,
    TrainingArguments,
    default_data_collator,
    set_seed,
)

SIZES: dict[str, dict[str, int]] = {
    "tiny": {"layers": 4, "heads": 4, "width": 256, "context": 512},
    "small": {"layers": 8, "heads": 8, "width": 512, "context": 1024},
    "medium": {"layers": 12, "heads": 12, "width": 768, "context": 1024},
    "large": {"layers": 24, "heads": 16, "width": 1024, "context": 2048},
    "xl": {"layers": 32, "heads": 20, "width": 1280, "context": 2048},
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", required=True, help="Path to a UTF-8 .txt code corpus")
    parser.add_argument("--tokenizer", required=True, help="Directory made by the tokenizer trainer")
    parser.add_argument("--out", default="artifacts/model", help="Checkpoint and final output directory")
    parser.add_argument("--size", choices=tuple(SIZES), default="small")
    parser.add_argument("--epochs", type=float, default=1.0)
    parser.add_argument("--batch-size", type=int, default=2, help="Per-device batch size")
    parser.add_argument("--grad-accum", type=int, default=16)
    parser.add_argument("--learning-rate", type=float, default=3e-4)
    parser.add_argument("--max-steps", type=int, default=-1, help="-1 uses epochs; positive sets a step budget")
    parser.add_argument("--save-steps", type=int, default=500)
    parser.add_argument("--logging-steps", type=int, default=10)
    parser.add_argument("--block-size", type=int, default=0, help="0 uses preset context length")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--resume", action="store_true", help="Resume from the latest valid checkpoint")
    return parser


def _group_texts(batch: dict[str, list[list[int]]], block_size: int) -> dict[str, list[list[int]]]:
    """Pack tokenized documents into fixed-size blocks without quadratic list concatenation."""
    joined = {key: list(chain.from_iterable(values)) for key, values in batch.items()}
    if "input_ids" not in joined:
        return {"input_ids": [], "attention_mask": [], "labels": []}
    total_length = (len(joined["input_ids"]) // block_size) * block_size
    if total_length == 0:
        return {"input_ids": [], "attention_mask": [], "labels": []}

    result = {key: values[:total_length] for key, values in joined.items()}
    chunks = {
        key: [values[i : i + block_size] for i in range(0, total_length, block_size)]
        for key, values in result.items()
    }
    chunks["labels"] = [ids.copy() for ids in chunks["input_ids"]]
    return chunks


def _latest_checkpoint(output_dir: Path) -> Path | None:
    candidates: list[tuple[int, Path]] = []
    for path in output_dir.glob("checkpoint-*"):
        try:
            step = int(path.name.rsplit("-", 1)[1])
        except (IndexError, ValueError):
            continue
        if path.is_dir():
            candidates.append((step, path))
    return max(candidates, key=lambda item: item[0])[1] if candidates else None


def _training_args_kwargs(**values: Any) -> dict[str, Any]:
    """Map evaluation strategy to the name used by the installed Transformers release."""
    parameters = inspect.signature(TrainingArguments.__init__).parameters
    evaluation_key = "eval_strategy" if "eval_strategy" in parameters else "evaluation_strategy"
    values[evaluation_key] = "steps"
    return values


def main() -> None:
    args = build_parser().parse_args()
    corpus = Path(args.corpus)
    tokenizer_dir = Path(args.tokenizer)
    output_dir = Path(args.out)

    if not corpus.is_file():
        raise SystemExit(f"Corpus file not found: {corpus}")
    if corpus.stat().st_size == 0:
        raise SystemExit(f"Corpus file is empty: {corpus}")
    if not (tokenizer_dir / "tokenizer.json").exists():
        raise SystemExit(f"tokenizer.json not found in {tokenizer_dir}; train a tokenizer first")
    if not torch.cuda.is_available():
        raise SystemExit(
            "No CUDA GPU detected. Run this command in a GPU cloud environment; "
            "CPU training is disabled by this entry point."
        )
    if args.batch_size < 1 or args.grad_accum < 1:
        raise SystemExit("--batch-size and --grad-accum must be positive")
    if args.learning_rate <= 0 or args.epochs <= 0:
        raise SystemExit("--learning-rate and --epochs must be positive")
    if args.max_steps == 0 or args.max_steps < -1:
        raise SystemExit("--max-steps must be -1 or a positive integer")
    if args.save_steps < 1 or args.logging_steps < 1:
        raise SystemExit("--save-steps and --logging-steps must be positive")

    preset = SIZES[args.size]
    block_size = args.block_size or preset["context"]
    if block_size < 16:
        raise SystemExit("--block-size must be at least 16")

    set_seed(args.seed)
    tokenizer = AutoTokenizer.from_pretrained(str(tokenizer_dir), use_fast=True, local_files_only=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token or tokenizer.unk_token
    if tokenizer.pad_token_id is None:
        raise SystemExit("Tokenizer needs a pad_token_id, eos_token_id, or unk_token_id")

    config = GPT2Config(
        vocab_size=len(tokenizer),
        n_positions=block_size,
        n_ctx=block_size,
        n_embd=preset["width"],
        n_layer=preset["layers"],
        n_head=preset["heads"],
        bos_token_id=tokenizer.bos_token_id,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.pad_token_id,
        use_cache=False,
    )
    # New configuration + model constructor means random initialization; no pretrained weights load.
    model = GPT2LMHeadModel(config)
    model.gradient_checkpointing_enable()
    model.config.use_cache = False
    parameter_count = sum(parameter.numel() for parameter in model.parameters())
    gpu_names = [torch.cuda.get_device_name(index) for index in range(torch.cuda.device_count())]
    print(
        f"Model size: {args.size}; parameters: {parameter_count:,}; context: {block_size}; "
        f"GPU(s): {gpu_names}; seed: {args.seed}"
    )

    raw = load_dataset("text", data_files={"train": str(corpus)}, split="train")
    if len(raw) < 2:
        raise SystemExit(
            "Corpus must contain at least two non-empty line-delimited documents for a train/validation split."
        )
    validation_rows = max(1, min(len(raw) - 1, math.ceil(len(raw) * 0.01)))
    split = raw.train_test_split(test_size=validation_rows, seed=args.seed)

    def tokenize_batch(batch: dict[str, list[str]]) -> dict[str, Any]:
        return tokenizer(batch["text"], add_special_tokens=True, truncation=False)

    tokenized = split.map(
        tokenize_batch,
        batched=True,
        remove_columns=split["train"].column_names,
        desc="Tokenizing corpus",
    )
    lm = tokenized.map(
        lambda batch: _group_texts(batch, block_size),
        batched=True,
        batch_size=1000,
        desc="Packing token sequences",
    )
    if len(lm["train"]) == 0 or len(lm["test"]) == 0:
        raise SystemExit(
            "Not enough tokens to create both train and validation blocks at this context length. "
            "Add a larger corpus or use --block-size with a smaller value."
        )

    use_bf16 = torch.cuda.is_bf16_supported()
    output_dir.mkdir(parents=True, exist_ok=True)
    training_kwargs: dict[str, Any] = {
        "output_dir": str(output_dir),
        "overwrite_output_dir": False,
        "num_train_epochs": args.epochs,
        "max_steps": args.max_steps,
        "per_device_train_batch_size": args.batch_size,
        "per_device_eval_batch_size": args.batch_size,
        "gradient_accumulation_steps": args.grad_accum,
        "learning_rate": args.learning_rate,
        "lr_scheduler_type": "cosine",
        "warmup_ratio": 0.03,
        "weight_decay": 0.1,
        "logging_steps": args.logging_steps,
        "save_steps": args.save_steps,
        "eval_steps": args.save_steps,
        "save_strategy": "steps",
        "save_total_limit": 3,
        "fp16": not use_bf16,
        "bf16": use_bf16,
        "gradient_checkpointing": True,
        "dataloader_num_workers": min(4, os.cpu_count() or 1),
        "report_to": "none",
        "logging_dir": str(output_dir / "logs"),
        "seed": args.seed,
        "data_seed": args.seed,
        "load_best_model_at_end": False,
    }
    train_args = TrainingArguments(**_training_args_kwargs(**training_kwargs))

    trainer_parameters = inspect.signature(Trainer.__init__).parameters
    trainer_kwargs: dict[str, Any] = {
        "model": model,
        "args": train_args,
        "train_dataset": lm["train"],
        "eval_dataset": lm["test"],
        "data_collator": default_data_collator,
    }
    if "processing_class" in trainer_parameters:
        trainer_kwargs["processing_class"] = tokenizer
    else:
        trainer_kwargs["tokenizer"] = tokenizer
    trainer = Trainer(**trainer_kwargs)

    resume_from: str | None = None
    if args.resume:
        checkpoint = _latest_checkpoint(output_dir)
        if checkpoint is not None:
            resume_from = str(checkpoint)
            print(f"Resuming from checkpoint: {resume_from}")
        else:
            print("No checkpoint found; starting from random initialization.")

    trainer.train(resume_from_checkpoint=resume_from)
    metrics = trainer.evaluate()
    if "eval_loss" in metrics:
        try:
            metrics["perplexity"] = math.exp(metrics["eval_loss"])
        except OverflowError:
            metrics["perplexity"] = float("inf")
    trainer.save_model(str(output_dir / "final"))
    tokenizer.save_pretrained(output_dir / "final")
    trainer.log_metrics("eval", metrics)
    trainer.save_metrics("eval", metrics)
    metadata = {
        "project": "Code Integrity Research Lab",
        "historical_codename": "AI Hacker",
        "model_size_preset": args.size,
        "parameter_count": parameter_count,
        "context_length": block_size,
        "seed": args.seed,
        "tokenizer_path": str(tokenizer_dir),
        "corpus_path": str(corpus),
        "training_args": {
            "epochs": args.epochs,
            "batch_size": args.batch_size,
            "gradient_accumulation": args.grad_accum,
            "learning_rate": args.learning_rate,
            "max_steps": args.max_steps,
        },
        "evaluation_metrics": metrics,
        "claim_limit": "Language-model metrics do not measure vulnerability-detection performance.",
    }
    (output_dir / "final" / "experiment.json").write_text(
        json.dumps(metadata, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    print(f"Training complete. Final artifacts: {(output_dir / 'final').resolve()}")


if __name__ == "__main__":
    main()
