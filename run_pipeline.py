"""Runs every stage in order: python3 run_pipeline.py"""
import subprocess, sys
for step in ["generate_dataset.py", "clean_data.py", "build_db.py", "queries.py", "metrics_engine.py",
             "draft_report.py", "make_memo.py", "review_gate.py"]:
    print(f"\n===== {step} =====", flush=True)
    subprocess.run([sys.executable, step], check=True)
print("\nPipeline complete. Now run: streamlit run app.py")
