# Implementation and Default Configurations

This document describes the implementation details and default configuration choices of **GenLoc**, as used in all experiments unless stated otherwise. The goal is to ensure transparency and reproducibility of the reported results.

---

## Implementation Overview

GenLoc currently supports **Java and Python** and can be easily extended to other programming languages, as it leverages the **Tree-sitter** library for source code parsing, which supports over ten programming languages.


---

## Configuration of Semantic Retrieval

### Embedding Model and Similarity Metric

To compute semantic similarity between bug reports and source code files, GenLoc employs OpenAI’s `text-embedding-3-small` model as the default embedding model due to its cost-effectiveness ($0.02 per 1M tokens).  

The similarity between bug report embeddings and source code embeddings is computed using **cosine similarity**, following prior work [1].

---

### Chunking Strategy

Following Amazon Bedrock’s chunking recommendation [2], source code files are divided into chunks of **300 tokens** by default. This choice balances granularity and contextual completeness, allowing GenLoc to capture relevant code segments while preserving sufficient surrounding context for meaningful semantic comparison.

To evaluate the robustness of this choice, we conduct a **sensitivity analysis** using smaller (100 tokens) and larger (500 tokens) chunk sizes. Each configuration is evaluated on the Ye et al. dataset using **retrieval coverage**, defined as the percentage of bugs for which at least one ground-truth fixed file appears among the top-50 retrieved candidates.

### Chunk Size Sensitivity Results

| Chunk Size (tokens) | 100   | 300   | 500   |
|--------------------|-------|-------|-------|
| Coverage (%)       | 80.94 | **81.28** | 79.76 |

The 300-token configuration achieves the highest retrieval coverage and is therefore adopted as GenLoc’s default chunk size.



### Number of Retrieved Candidate Files

After embedding all chunks, GenLoc retrieves the top-ranked candidate files for each bug report. Using the Ye et al. dataset, we analyze how retrieval coverage changes as the number of retrieved candidates increases from 1 to 100.

We observe steep gains in the early stages (e.g., 1 → 10 → 20), followed by diminishing returns beyond the top-50 candidates. Increasing the retrieval window from 50 to 100 candidates yields only a **4.26% increase in retrieval coverage**, while substantially increasing noise and computational overhead.

Therefore, retrieving the **top 50 candidate files** is adopted as GenLoc’s default setting.

**Figure:** Retrieval coverage for varying numbers of candidate files on the Ye et al. dataset.  
![Retrieval coverage vs number of candidates](../img/candidates.png)


### Embedding Storage and Incremental Updates

To minimize embedding cost, GenLoc stores all source-code chunk embeddings in **ChromaDB** when processing the first bug of a project.  

Since different bugs correspond to different software versions, embeddings are updated incrementally: for each subsequent bug, only files that have been **added, modified, deleted, or renamed** across versions are re-embedded and updated in the database.

---

## Configuration of the LLM

### Default LLM Choice

GenLoc uses OpenAI’s `GPT-4o-mini` as its default LLM for reasoning due to its favorable cost-effectiveness ($0.15 per 1M input tokens and $0.60 per 1M output tokens).

---

### Temperature Setting

The temperature parameter is left at its default value (**1.0**) rather than being set to 0. This allows for diverse reasoning paths during inference [3,4]. A temperature of 0 significantly reduces variability by consistently selecting the highest-probability tokens, which can lead the model to overlook less obvious but relevant files. 

Our preliminary analysis shows that the performance remained mostly unchanged regardless of the temperature setting. This aligns with prior findings that changes in temperature between 0.0 and 1.0 do not have a significant effect on LLM's performance for problem-solving tasks [5].

---

### Handling Non-Determinism

To account for LLM non-determinism, all experiments are executed **three times**, and the **average results** are reported, as followed in prior work [6].

---


## References

[1] Jiang, Z., Lo, D., & Liu, Z. (2025). Agentic Software Issue Resolution with Large Language Models: A Survey. arXiv preprint arXiv:2512.22256.

[2] AWS Blogs, URL: https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-knowledge-bases-now-supports-advanced-parsing-chunking-and-query-reformulation-giving-greater-control-of-accuracy-in-rag-based-applications/

[3] Kang, S., Yoon, J., & Yoo, S. (2023, May). Large language models are few-shot testers: Exploring llm-based general bug reproduction. In 2023 IEEE/ACM 45th International Conference on Software Engineering (ICSE) (pp. 2312-2323). IEEE.

[4] Zhu, Y., Li, J., Li, G., Zhao, Y., Jin, Z., & Mei, H. (2024, March). Hot or cold? adaptive temperature sampling for code generation with large language models. In Proceedings of the AAAI Conference on Artificial Intelligence (Vol. 38, No. 1, pp. 437-445).

[5] Renze, M. (2024, November). The effect of sampling temperature on problem solving in large language models. In Findings of the association for computational linguistics: EMNLP 2024 (pp. 7346-7356).

[6] Zhang, Y., Ruan, H., Fan, Z., & Roychoudhury, A. (2024, September). Autocoderover: Autonomous program improvement. In Proceedings of the 33rd ACM SIGSOFT International Symposium on Software Testing and Analysis (pp. 1592-1604).