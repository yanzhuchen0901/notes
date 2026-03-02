import argparse
import os
import sys
import inspect
from pathlib import Path

import evaluate
import numpy as np
from datasets import load_dataset
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    Trainer,
    TrainingArguments,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fine-tune BERT on GLUE MRPC")
    parser.add_argument("--checkpoint", type=str, default="bert-base-uncased")
    parser.add_argument("--output_dir", type=str, default="AI/test-trainer")
    parser.add_argument("--learning_rate", type=float, default=5e-5)
    parser.add_argument("--train_batch_size", type=int, default=16)
    parser.add_argument("--eval_batch_size", type=int, default=64)
    parser.add_argument("--num_train_epochs", type=float, default=3)
    parser.add_argument("--weight_decay", type=float, default=0.01)
    parser.add_argument("--max_train_samples", type=int, default=None)
    parser.add_argument("--max_eval_samples", type=int, default=None)
    parser.add_argument("--max_steps", type=int, default=-1)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def ensure_std_streams() -> None:
    if sys.stdout is None:
        sys.stdout = sys.__stdout__ or open(os.devnull, "w", encoding="utf-8")
    if sys.stderr is None:
        sys.stderr = sys.__stderr__ or open(os.devnull, "w", encoding="utf-8")


def main() -> None:
    ensure_std_streams()
    args = parse_args()

    raw_datasets = load_dataset("glue", "mrpc")
    tokenizer = AutoTokenizer.from_pretrained(args.checkpoint)

    def tokenize_function(examples):
        return tokenizer(examples["sentence1"], examples["sentence2"], truncation=True)

    tokenized_datasets = raw_datasets.map(tokenize_function, batched=True)

    train_dataset = tokenized_datasets["train"]
    eval_dataset = tokenized_datasets["validation"]

    if args.max_train_samples is not None:
        train_dataset = train_dataset.select(range(min(args.max_train_samples, len(train_dataset))))
    if args.max_eval_samples is not None:
        eval_dataset = eval_dataset.select(range(min(args.max_eval_samples, len(eval_dataset))))

    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
    model = AutoModelForSequenceClassification.from_pretrained(args.checkpoint, num_labels=2)
    metric = evaluate.load("glue", "mrpc")

    def compute_metrics(eval_preds):
        logits, labels = eval_preds
        predictions = np.argmax(logits, axis=-1)
        return metric.compute(predictions=predictions, references=labels)

    training_kwargs = {
        "output_dir": args.output_dir,
        "evaluation_strategy": "epoch",
        "eval_strategy": "epoch",
        "save_strategy": "epoch",
        "learning_rate": args.learning_rate,
        "per_device_train_batch_size": args.train_batch_size,
        "per_device_eval_batch_size": args.eval_batch_size,
        "num_train_epochs": args.num_train_epochs,
        "weight_decay": args.weight_decay,
        "logging_steps": 20,
        "max_steps": args.max_steps,
        "seed": args.seed,
        "load_best_model_at_end": True,
        "metric_for_best_model": "f1",
        "greater_is_better": True,
        "report_to": "none",
    }

    accepted = set(inspect.signature(TrainingArguments.__init__).parameters.keys())
    filtered_kwargs = {k: v for k, v in training_kwargs.items() if k in accepted}
    training_args = TrainingArguments(**filtered_kwargs)

    trainer_kwargs = {
        "model": model,
        "args": training_args,
        "train_dataset": train_dataset,
        "eval_dataset": eval_dataset,
        "tokenizer": tokenizer,
        "data_collator": data_collator,
        "compute_metrics": compute_metrics,
    }
    trainer_params = set(inspect.signature(Trainer.__init__).parameters.keys())
    trainer = Trainer(**{k: v for k, v in trainer_kwargs.items() if k in trainer_params})

    trainer.train()
    eval_metrics = trainer.evaluate()
    trainer.save_model(args.output_dir)

    output_path = Path(args.output_dir) / "eval_metrics.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(str(eval_metrics), encoding="utf-8")

    print("Training finished.")
    print(f"Model and metrics saved to: {args.output_dir}")
    print(eval_metrics)


if __name__ == "__main__":
    main()
