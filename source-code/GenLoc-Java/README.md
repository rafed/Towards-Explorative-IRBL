## ⚙️ Set-Up

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Place your OpenAI API key in a file named `api_key.txt` in the project root directory.

---

## 🔧 How to Run

execute the following steps:

```bash
# Step 1: Execute embedding-based retrieval
# Format: python main.py <project_name> <project_repo_path> <bug_report_xml> <embedding_model>
# Example:
python main.py aspectj ye_et_al_dataset/aspectj ye_et_al_dataset/aspectj.xml openai

# Step 2: Run the LLM-based analysis
# Format: python bug_localizer.py <project_name> <bug_report_xml>
# Example:
python bug_localizer.py aspectj ye_et_al_dataset/aspectj.xml

# Step 3: Perform post-processing
# Format: python post_processor.py <project_name>
# Example:
python post_processor.py aspectj

# Step 4: Evaluate performance using standard metrics
# Format: python evaluation_metric_calculator.py <project_name>
# Example:
python evaluation_metric_calculator.py aspectj
```

---
