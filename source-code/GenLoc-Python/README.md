
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
# Format: python main.py
# Example:
python main.py

# Step 2: Run the LLM-based analysis
# Format: python bug_localizer.py
# Example:
python bug_localizer.py

# Step 3: Perform post-processing
# Format: python post_processor.py <directory>
# Example:
python post_processor.py .

# Step 4: Evaluate performance using standard metrics
# Format: python evaluation_metric_calculator.py
# Example:
python evaluation_metric_calculator.py
```

---
