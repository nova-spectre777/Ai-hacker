"""Train a byte-level BPE tokenizer from an authorized text corpus."""
from __future__ import annotations

import argparse
from pathlib import Path

from tokenizers import Tokenizer, decoders, models, pre_tokenizers, trainers
from transformers import PreTrainedTokenizerFast


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", required=True, help="UTF-8 text corpus file")
    parser.add_argument("--out", default="artifacts/tokenizer", help="Tokenizer output directory")
    parser.add_argument("--vocab-size", type=int, default=32000)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    corpus = Path(args.corpus)
    if not corpus.is_file():
        raise SystemExit(f"Corpus file not found: {corpus}")
    if corpus.stat().st_size == 0:
        raise SystemExit(f"Corpus file is empty: {corpus}")
    if args.vocab_size < 1000:
        raise SystemExit("--vocab-size must be at least 1000")

    output_dir = Path(args.out)
    output_dir.mkdir(parents=True, exist_ok=True)

    tokenizer = Tokenizer(models.BPE(unk_token="<unk>"))
    tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
    tokenizer.decoder = decoders.ByteLevel()
    special_tokens = [
        "<pad>", "<unk>", "<s>", "</s>",
        "<|code|>", "<|language|>", "<|label|>",
    ]
    trainer = trainers.BpeTrainer(
        vocab_size=args.vocab_size,
        min_frequency=2,
        special_tokens=special_tokens,
        initial_alphabet=pre_tokenizers.ByteLevel.alphabet(),
        show_progress=True,
    )
    tokenizer.train([str(corpus)], trainer)
    tokenizer_json = output_dir / "tokenizer.json"
    tokenizer.save(str(tokenizer_json))

    fast_tokenizer = PreTrainedTokenizerFast(
        tokenizer_file=str(tokenizer_json),
        unk_token="<unk>",
        pad_token="<pad>",
        bos_token="<s>",
        eos_token="</s>",
        additional_special_tokens=["<|code|>", "<|language|>", "<|label|>"],
    )
    fast_tokenizer.save_pretrained(output_dir)
    print(f"Tokenizer saved to {output_dir.resolve()}")
    print(f"Vocabulary size: {len(fast_tokenizer):,}")


if __name__ == "__main__":
    main()
