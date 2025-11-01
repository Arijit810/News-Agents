from tools.quality_tool import quality_score
from tools.factual_tool import factual_alignment_score
from langsmith.evaluation import evaluate

def evaluator_node(state):
    summary = state["summary"]
    topic = state["topic"]
    source = state.get("search_results", "")

    print("🧩 Evaluating quality and factual accuracy...")

    # Evaluate both quality & factuality
    q_eval = quality_score(summary)
    f_eval = factual_alignment_score(summary, source)

    # ---- Safe handling for both dict or float return types ----
    if isinstance(q_eval, dict):
        quality_val = q_eval.get("quality_score", 0.0)
        q_remarks = q_eval.get("remarks", "")
    else:
        quality_val = float(q_eval)
        q_remarks = ""

    if isinstance(f_eval, dict):
        factual_val = f_eval.get("factual_score", 0.0)
        f_remarks = f_eval.get("remarks", "")
    else:
        factual_val = float(f_eval)
        f_remarks = ""

    # ---- Compute overall weighted score ----
    overall = round((0.6 * quality_val + 0.4 * factual_val), 2)
    verdict = "excellent" if overall > 0.8 else "average" if overall > 0.6 else "poor"

    evaluation = {
        "overall_score": overall,
        "quality_score": quality_val,
        "factual_score": factual_val,
        "remarks": f"{q_remarks} | {f_remarks}".strip(" |"),
        "verdict": verdict,
    }

    # ---- Optional: Log to LangSmith ----
    try:
        evaluate(
            run_type="news_summary_eval",
            inputs={"topic": topic, "summary": summary},
            outputs={"evaluation": evaluation},
            evaluation_name="summary_quality_factuality",
            metrics={
                "quality": quality_val,
                "factuality": factual_val,
                "overall": overall,
            },
        )
    except Exception as e:
        print(f"⚠️ LangSmith logging skipped: {e}")

    # ---- Print nicely ----
    print(f"\n📊 Evaluation Results:")
    print(f"   Quality: {quality_val:.2f} | Factual: {factual_val:.2f} | Overall: {overall:.2f} ({verdict})")
    print(f"   Remarks: {evaluation['remarks']}\n")

    # ✅ Return updates instead of mutating state
    return {"evaluation": evaluation}
