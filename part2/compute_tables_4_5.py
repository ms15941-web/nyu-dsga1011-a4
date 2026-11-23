"""
Generate Part 2 Q6 Table 4 (metrics) and Table 5 (error analysis) on the dev set.

Usage (from part2/):
  python compute_tables_4_5.py
  python compute_tables_4_5.py \
      --pred_sql results/t5_ft_experiment_dev.sql \
      --pred_records records/t5_ft_experiment_dev.pkl

Test-set numbers are not available locally (hidden labels). Paste Gradescope
test metrics into Table 4 manually when printing finishes.
"""

from __future__ import annotations

import argparse
import re
from collections import defaultdict

from load_data import load_lines
from utils import compute_metrics, load_queries_and_records


def city_names(sql: str):
    return set(re.findall(r"city_name\s*=\s*'([^']+)'", sql, flags=re.I))


def airline_codes(sql: str):
    return set(re.findall(r"airline_code\s*=\s*'([^']+)'", sql, flags=re.I))


def classify_error(gt_sql, pred_sql, gt_rec, pred_rec, err_msg):
    """
    Return a list of error type tags for one example.
    An example can receive multiple tags; for Table 5 we also track primary.
    """
    tags = []

    if err_msg:
        tags.append("sql_execution_error")

    if pred_sql.strip() == gt_sql.strip():
        return tags  # exact SQL match (may still have empty tags)

    # Record-level issues (only if both executed somehow / comparable)
    gt_set = set(gt_rec)
    pred_set = set(pred_rec)

    if not err_msg:
        if gt_set != pred_set:
            if len(pred_set) == 0 and len(gt_set) > 0:
                tags.append("empty_result_but_gold_nonempty")
            elif len(pred_set) > 0 and len(gt_set) == 0:
                tags.append("nonempty_result_but_gold_empty")
            elif pred_set.isdisjoint(gt_set) and (gt_set or pred_set):
                tags.append("record_set_mismatch_disjoint")
            else:
                tags.append("record_set_partial_overlap")

    # Entity / constraint mistakes visible in SQL text
    if city_names(pred_sql) != city_names(gt_sql):
        tags.append("wrong_city_grounding")
    if airline_codes(pred_sql) != airline_codes(gt_sql):
        tags.append("wrong_airline_code")

    # Structural: SELECT target / join shape differs a lot
    gt_select = re.findall(r"SELECT\s+(.*?)\s+FROM", gt_sql, flags=re.I | re.S)
    pred_select = re.findall(r"SELECT\s+(.*?)\s+FROM", pred_sql, flags=re.I | re.S)
    if gt_select and pred_select and gt_select[0].strip() != pred_select[0].strip():
        tags.append("wrong_select_clause")

    if not tags and pred_sql.strip() != gt_sql.strip():
        # SQL string differs but records matched (paraphrase) — not counted as error for Table 5 focus
        tags.append("sql_paraphrase_same_records")

    return tags


ERROR_DESCRIPTIONS = {
    "sql_execution_error": (
        "Generated SQL is syntactically invalid or otherwise fails when executed "
        "against the flight database (non-empty DB error message)."
    ),
    "wrong_city_grounding": (
        "The predicted query uses different city_name constraints than the gold SQL "
        "(wrong origin/destination or missing/extra city filter)."
    ),
    "wrong_airline_code": (
        "The predicted query disagrees with gold on airline_code constraints."
    ),
    "empty_result_but_gold_nonempty": (
        "The predicted SQL runs but returns no rows, while the gold query returns "
        "one or more records."
    ),
    "record_set_partial_overlap": (
        "Both queries return non-empty record sets that partially overlap but are "
        "not identical (extra/missing flights)."
    ),
    "record_set_mismatch_disjoint": (
        "Both queries return records, but the predicted and gold record sets are disjoint."
    ),
    "wrong_select_clause": (
        "The SELECT clause differs from gold (e.g., different projected columns / distinct pattern)."
    ),
    "nonempty_result_but_gold_empty": (
        "Predicted SQL returns rows while gold returns an empty set."
    ),
    "sql_paraphrase_same_records": (
        "SQL text differs from gold but execution yields the same records "
        "(not a semantic error; listed for completeness)."
    ),
}


def primary_tag(tags):
    """Prefer the most report-worthy tag for Table 5 examples."""
    priority = [
        "sql_execution_error",
        "wrong_city_grounding",
        "wrong_airline_code",
        "empty_result_but_gold_nonempty",
        "record_set_mismatch_disjoint",
        "record_set_partial_overlap",
        "wrong_select_clause",
        "nonempty_result_but_gold_empty",
    ]
    for p in priority:
        if p in tags:
            return p
    return tags[0] if tags else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pred_sql", default="results/t5_ft_experiment_dev.sql")
    parser.add_argument("--pred_records", default="records/t5_ft_experiment_dev.pkl")
    parser.add_argument("--gt_sql", default="data/dev.sql")
    parser.add_argument("--gt_records", default="records/ground_truth_dev.pkl")
    parser.add_argument("--nl", default="data/dev.nl")
    parser.add_argument(
        "--test_f1",
        type=float,
        default=60.10,
        help="Test Record F1 from Gradescope (percent or fraction). Default=60.10",
    )
    parser.add_argument(
        "--test_em",
        type=float,
        default=53.47,
        help="Test Record EM from Gradescope (percent). Default=53.47",
    )
    parser.add_argument(
        "--test_sql_em",
        type=float,
        default=0.0,
        help="Test SQL EM from Gradescope (percent). Default=0.0",
    )
    args = parser.parse_args()

    sql_em, record_em, record_f1, error_msgs = compute_metrics(
        args.gt_sql, args.pred_sql, args.gt_records, args.pred_records
    )

    gt_sqls, gt_records, _ = load_queries_and_records(args.gt_sql, args.gt_records)
    pred_sqls, pred_records, _ = load_queries_and_records(args.pred_sql, args.pred_records)
    nls = load_lines(args.nl)

    n = len(gt_sqls)
    assert len(pred_sqls) == n

    # --- Table 4 ---
    # Accept test metrics as percent (60.10) or fraction (0.601)
    def as_pct(x):
        return x * 100 if x <= 1.0 else x

    test_f1 = as_pct(args.test_f1)
    test_em = as_pct(args.test_em)
    test_sql_em = as_pct(args.test_sql_em)

    print("\n" + "=" * 72)
    print("TABLE 4 — Quantitative results")
    print("=" * 72)
    print(f"{'System':<40} {'Query EM':>10} {'Record EM':>10} {'F1':>10}")
    print("-" * 72)
    print("Dev Results")
    print(
        f"{'T5 fine-tuned (Full model)':<40} "
        f"{sql_em*100:10.2f} {record_em*100:10.2f} {record_f1*100:10.2f}"
    )
    print("Test Results")
    print(
        f"{'T5 fine-tuning':<40} "
        f"{test_sql_em:10.2f} {test_em:10.2f} {test_f1:10.2f}"
    )
    print(
        "\nNote: Assignment Table 4 shows Query EM and F1; Record EM included here for debugging."
    )
    print(f"Dev SQL execution error rate: {sum(1 for m in error_msgs if m)/n*100:.2f}% "
          f"({sum(1 for m in error_msgs if m)}/{n})")

    # --- Error analysis ---
    buckets = defaultdict(list)  # tag -> list of example indices
    for i in range(n):
        tags = classify_error(
            gt_sqls[i], pred_sqls[i], gt_records[i], pred_records[i], error_msgs[i]
        )
        # Only count true errors for Table 5 (exclude pure paraphrases with same records)
        tags = [t for t in tags if t != "sql_paraphrase_same_records"]
        if not tags:
            continue
        # record under all tags for prevalence; keep primary for example display
        for t in set(tags):
            buckets[t].append(i)

    # Prefer 3 strong categories present in data
    preferred = [
        "sql_execution_error",
        "wrong_city_grounding",
        "empty_result_but_gold_nonempty",
        "record_set_partial_overlap",
        "wrong_airline_code",
        "record_set_mismatch_disjoint",
        "wrong_select_clause",
    ]
    chosen = [t for t in preferred if buckets.get(t)]
    # ensure at least 3 if possible
    for t, idxs in sorted(buckets.items(), key=lambda kv: -len(kv[1])):
        if t not in chosen:
            chosen.append(t)
        if len(chosen) >= 3:
            break
    chosen = chosen[: max(3, min(5, len(chosen)))]

    print("\n" + "=" * 72)
    print("TABLE 5 — Qualitative error analysis (dev set)")
    print("=" * 72)

    # Denominator choices:
    # - for sql_execution_error: all queries
    # - for others: queries that are not exact record match (semantic failures)
    hard = [
        i
        for i in range(n)
        if set(gt_records[i]) != set(pred_records[i]) or error_msgs[i]
    ]
    print(f"Total dev examples: {n}")
    print(f"Examples with record mismatch or SQL error: {len(hard)}")

    for tag in chosen:
        idxs = buckets[tag]
        # TOTAL: all queries for execution errors; else #incorrect-record examples
        total = n if tag == "sql_execution_error" else max(len(hard), 1)
        count = len(idxs)
        ex_i = idxs[0]
        nl_snip = nls[ex_i] if ex_i < len(nls) else ""
        pred_snip = pred_sqls[ex_i]
        gold_snip = gt_sqls[ex_i]
        if len(pred_snip) > 180:
            pred_snip = pred_snip[:177] + "..."
        if len(gold_snip) > 180:
            gold_snip = gold_snip[:177] + "..."

        print("\n" + "-" * 72)
        print(f"Error name: {tag}")
        print(f"Statistics: {count}/{total}")
        print(f"Description: {ERROR_DESCRIPTIONS.get(tag, tag)}")
        print(f"Example NL: {nl_snip}")
        print(f"Example predicted SQL: {pred_snip}")
        print(f"Example gold SQL: {gold_snip}")
        if error_msgs[ex_i]:
            print(f"DB error: {error_msgs[ex_i]}")

    print("\nDone. Copy the printed rows into your report tables.")
    print(
        "Tip: if you retrain (v2/EC), rerun with the matching --pred_sql/--pred_records "
        "and update --test_f1 from Gradescope."
    )


if __name__ == "__main__":
    main()
