"""Train a decoder-only Transformer from random initialization on a local code corpus.

Expected corpus: UTF-8 .txt, one or more documents separated by newlines. Train the tokenizer
first with train_tokenizer.py. This script never downloads pretrained model weights.
"""
from __future__ import annotations

import argparse
import math
import os
from pathlib import Path

import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    GPT2Config,
    GPT2LMHeadModel,
    Trainer,
    TrainingArguments,
    default_data_collator,
)


SIZES = {
    "tiny":   {"layers": 4,  "heads": 4,  "width": 256,  "context": 512},
    "small":  {"layers": 8,  "heads": 8,  "width": 512,  "context": 1024},
    "medium": {"layers": 12, "heads": 12, "width": 768,  "context": 1024},
    "large":  {"layers": 24, "heads": 16, "width": 1024, "context": 2048},
    "xl":     {"layers": 32, "heads": 20, "width": 1280, "context": 2048},
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--corpus", required=True, help="Path to a UTF-8 .txt code corpus")
    p.add_argument("--tokenizer", required=True, help="Directory created by train_tokenizer.py")
    p.add_argument("--out", default="artifacts/model")
    p.add_argument("--size", choices=SIZES, default="small")
    p.add_argument("--epochs", type=float, default=1.0)
    p.add_argument("--batch-size", type=int, default=2, help="Per-device batch size")
    p.add_argument("--grad-accum", type=int, default=16)
    p.add_argument("--learning-rate", type=float, default=3e-4)
    p.add_argument("--max-steps", type=int, default=-1, help="-1 uses epochs; set positive for a step budget")
    p.add_argument("--save-steps", type=int, default=500)
    p.add_argument("--logging-steps", type=int, default=10)
    p.add_argument("--block-size", type=int, default=0, help="0 uses the selected model context length")
    p.add_argument("--resume", action="store_true", help="Resume from the latest checkpoint in --out")
    p.add_argument("--trust-dataset", action="store_true", help="Allow remote dataset scripts (normally unnecessary)")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    corpus = Path(args.corpus)
    tokenizer_dir = Path(args.tokenizer)
    out = Path(args.out)
    if not corpus.is_file():
        raise SystemExit(f"Corpus file not found: {corpus}")
    if not (tokenizer_dir / "tokenizer.json").exists():
        raise SystemExit(f"tokenizer.json not found in {tokenizer_dir}; train tokenizer first")
    if args.batch_size < 1 or args.grad_accum < 1:
        raise SystemExit("--batch-size and --grad-accum must be positive")
    if not torch.cuda.is_available():
        raise SystemExit("No CUDA GPU detected. Run this on a GPU cloud instance; CPU training is intentionally disabled.")

    preset = SIZES[args.size]
    block_size = args.block_size or preset["context"]
    tokenizer = AutoTokenizer.from_pretrained(str(tokenizer_dir), use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token or tokenizer.unk_token
    vocab_size = len(tokenizer)

    config = GPT2Config(
        vocab_size=vocab_size,
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
    # This constructor initializes new random weights; no pretrained checkpoint is loaded.
    model = GPT2LMHeadModel(config)
    model.gradient_checkpointing_enable()
    model.config.use_cache = False
    params = sum(p.numel() for p in model.parameters())
    print(f"Model size: {args.size}; parameters: {params:,}; context: {block_size}; GPU(s): {torch.cuda.device_count():,}")

    raw = load_dataset("text", data_files={"train": str(corpus)}, split="train")
    split = raw.train_test_split(test_size=0.01, seed=42)
    def tokenize_batch(batch):
        return tokenizer(batch["text"], add_special_tokens=True, truncation=False)
    tokenized = split.map(tokenize_batch, batched=True, remove_columns=split["train"].column_names)
    def group_texts(batch):
        joined = {k: sum(batch[k], []) for k in batch.keys()}
        total = (len(joined["input_ids"]) // block_size) * block_size
        if total == 0:
            return {"input_ids": [], "attention_mask": [], "labels": []}
        result = {k: v[:total] for k, v in joined.items()}
        chunks = {k: [v[i:i + block_size] for i in range(0, total, block_size)] for k, v in result.items()}
        chunks["labels"] = [x[:] for x in chunks["input_ids"]]
        return chunks
    lm = tokenized.map(group_texts, batched=True, batch_size=1000)
    if len(lm["train"]) == 0 or len(lm["test"]) == 0:
        raise SystemExit("Not enough corpus text to form train and validation blocks. Add more text.")
    use_bf16 = torch.cuda.is_bf16_supported()
    train_args = TrainingArguments(
        output_dir=str(out),
        overwrite_output_dir=False,
        num_train_epochs=args.epochs,
        max_steps=args.max_steps,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.learning_rate,
        lr_scheduler_type="cosine",
        warmup_ratio=0.03,
        weight_decay=0.1,
        logging_steps=args.logging_steps,
        save_steps=args.save_steps,
        eval_steps=args.save_steps,
        evaluation_strategy="steps",
        save_strategy="steps",
        save_total_limit=3,
        fp16=not use_bf16,
        bf16=use_bf16,
        gradient_checkpointing=True,
        dataloader_num_workers=min(4, os.cpu_count() or 1),
        report_to="none",
        logging_dir=str(out / "logs"),
        load_best_model_at_end=False,
    )
    trainer = Trainer(
        model=model,
        args=train_args,
        train_dataset=lm["train"],
        eval_dataset=lm["test"],
        data_collator=default_data_collator,
        processing_class=tokenizer,
    )
    resume_from = None
    if args.resume:
        checkpoints = sorted(out.glob("checkpoint-*"), key=lambda p: int(p.name.split("-")[-1]))
        if checkpoints:
            resume_from = str(checkpoints[-1])
            print(f"Resuming from {resume_from}")
        else:
            print("No checkpoint found; starting from random initialization.")
    trainer.train(resume_from_checkpoint=resume_from)
    metrics = trainer.evaluate()
    if "eval_loss" in metrics:
        try:
            metrics["perplexity"] = math.exp(metrics["eval_loss"])
        except OverflowError:
            metrics["perplexity"] = float("inf")
    trainer.save_model(str(out / "final"))
    tokenizer.save_pretrained(str(out / "final"))
    trainer.log_metrics("eval", metrics)
    trainer.save_metrics("eval", metrics)
    print(f"Training complete. Final model and tokenizer: {(out / 'final').resolve()}")


if __name__ == "__main__":
    main()
