"""
Compute Part 2 Q4 data statistics (Table 1 / Table 2) with the T5 tokenizer.

Usage (from part2/):
  python compute_stats.py
  USE_SCHEMA_HINT=1 python compute_stats.py   # match v2/EC preprocessing
"""

from __future__ import annotations

import os
from collections import Counter

from transformers import T5TokenizerFast

from load_data import TASK_PREFIX, T5_CHECKPOINT, load_lines


def mean(xs):
    return sum(xs) / max(len(xs), 1)


def vocab_size_from_token_lists(token_lists):
    vocab = set()
    for toks in token_lists:
        vocab.update(toks)
    return len(vocab)


def summarize_split(name, nls, sqls, tokenizer, prefix=""):
    """Return stats dict for one split."""
    # Tokenize with T5 (add_special_tokens=True includes </s>)
    nl_toks = [tokenizer.encode(prefix + nl, add_special_tokens=True) for nl in nls]
    sql_toks = None
    if sqls is not None:
        sql_toks = [tokenizer.encode(sql, add_special_tokens=True) for sql in sqls]

    stats = {
        "split": name,
        "num_examples": len(nls),
        "mean_sentence_len": mean([len(t) for t in nl_toks]),
        "vocab_nl": vocab_size_from_token_lists(nl_toks),
    }
    if sql_toks is not None:
        stats["mean_sql_len"] = mean([len(t) for t in sql_toks])
        stats["vocab_sql"] = vocab_size_from_token_lists(sql_toks)
    else:
        stats["mean_sql_len"] = None
        stats["vocab_sql"] = None
    return stats


def print_table(title, train_stats, dev_stats):
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)
    rows = [
        ("Number of examples", "num_examples", "{}"),
        ("Mean sentence length (T5 tokens)", "mean_sentence_len", "{:.2f}"),
        ("Mean SQL query length (T5 tokens)", "mean_sql_len", "{:.2f}"),
        ("Vocabulary size (natural language)", "vocab_nl", "{}"),
        ("Vocabulary size (SQL)", "vocab_sql", "{}"),
    ]
    print(f"{'Statistics Name':<40} {'Train':>12} {'Dev':>12}")
    print("-" * 72)
    for label, key, fmt in rows:
        tr = train_stats[key]
        dv = dev_stats[key]
        tr_s = "N/A" if tr is None else fmt.format(tr)
        dv_s = "N/A" if dv is None else fmt.format(dv)
        print(f"{label:<40} {tr_s:>12} {dv_s:>12}")


def whitespace_vocab(lines):
    vocab = set()
    lengths = []
    for line in lines:
        toks = line.split()
        lengths.append(len(toks))
        vocab.update(toks)
    return mean(lengths), len(vocab)


def main():
    tokenizer = T5TokenizerFast.from_pretrained(T5_CHECKPOINT)
    data_folder = "data"

    train_nl = load_lines(os.path.join(data_folder, "train.nl"))
    train_sql = load_lines(os.path.join(data_folder, "train.sql"))
    dev_nl = load_lines(os.path.join(data_folder, "dev.nl"))
    dev_sql = load_lines(os.path.join(data_folder, "dev.sql"))
    test_nl = load_lines(os.path.join(data_folder, "test.nl"))

    print(f"Model / tokenizer: {T5_CHECKPOINT}")
    print(f"USE_SCHEMA_HINT={os.environ.get('USE_SCHEMA_HINT', '0')}")
    print(f"TASK_PREFIX = {TASK_PREFIX!r}")
    print(f"test examples (for reference): {len(test_nl)}")

    # ----- Table 1: before preprocessing (raw text → T5 tokens, no task prefix) -----
    t1_train = summarize_split("train", train_nl, train_sql, tokenizer, prefix="")
    t1_dev = summarize_split("dev", dev_nl, dev_sql, tokenizer, prefix="")
    print_table(
        "Table 1: BEFORE preprocessing (raw NL/SQL, T5 tokenizer, no task prefix)",
        t1_train,
        t1_dev,
    )

    # Optional: whitespace token stats (sometimes useful in writeup discussion)
    print("\n(Optional reference) whitespace-tokenized lengths / vocab:")
    for split, nls, sqls in [
        ("train", train_nl, train_sql),
        ("dev", dev_nl, dev_sql),
    ]:
        nl_len, nl_v = whitespace_vocab(nls)
        sql_len, sql_v = whitespace_vocab(sqls)
        print(
            f"  {split}: mean NL words={nl_len:.2f}, NL word-vocab={nl_v}, "
            f"mean SQL words={sql_len:.2f}, SQL word-vocab={sql_v}"
        )

    # ----- Table 2: after preprocessing (same as training encoder inputs) -----
    t2_train = summarize_split("train", train_nl, train_sql, tokenizer, prefix=TASK_PREFIX)
    t2_dev = summarize_split("dev", dev_nl, dev_sql, tokenizer, prefix=TASK_PREFIX)
    print_table(
        "Table 2: AFTER preprocessing (TASK_PREFIX + optional schema on NL; SQL unchanged)",
        t2_train,
        t2_dev,
    )

    # Combined train+dev vocab (sometimes people report corpus-level vocab)
    print("\nCorpus-level T5 token vocab (train+dev), raw NL/SQL:")
    all_nl = [tokenizer.encode(x, add_special_tokens=True) for x in train_nl + dev_nl]
    all_sql = [tokenizer.encode(x, add_special_tokens=True) for x in train_sql + dev_sql]
    print(f"  NL vocab: {vocab_size_from_token_lists(all_nl)}")
    print(f"  SQL vocab: {vocab_size_from_token_lists(all_sql)}")

    print("\nDone. Copy the Table 1 / Table 2 numbers into your report.")


if __name__ == "__main__":
    main()
