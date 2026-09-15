# cs-agent-hiver
# AppleSupport AI Customer Support Agent

Built for the Hiver SDE Intern assignment — classifies customer support 
tweets by intent, drafts grounded replies based on historical AppleSupport 
resolution patterns, and decides whether to auto-handle or escalate to a human.

## Setup
1. Clone this repo
2. Install dependencies: `pip install -r requirements.txt`
3. Get a free Gemini API key: https://aistudio.google.com/apikey
4. Set it as an environment variable:
   - Windows: `setx GEMINI_API_KEY "your-key-here"` (then open a new terminal)
   - Mac/Linux: `export GEMINI_API_KEY=your-key-here`
5. Download `twcs.csv` from Kaggle (`thoughtvector/customer-support-on-twitter`), 
   place it in a `data/` folder in the repo root.

## Reproduce headline results (~10-15 min)
Run these in order:
python src/step1_subsample.py
python src/step2_build_threads.py
python src/step2c_filter_threads.py
python src/step3_clean.py
python src/step5_retrieval.py
python src/agent.py

To run the full evaluation:
python src/step9_run_eval.py
python src/step10_metrics.py

## Project structure
- `src/` — pipeline scripts (data processing, classification, drafting, routing, evaluation)
- `eval/` — intent taxonomy (`intent_spec.md`), labeled sample (`intent_sample.csv`), golden evaluation set
- `report.md` — full report: problem framing, baselines, failure analysis, decision log

## Brand
AppleSupport (chosen for high tweet volume and clear multi-turn resolution patterns)

## Model
Google Gemini (gemini-3.6-flash) via free-tier API
