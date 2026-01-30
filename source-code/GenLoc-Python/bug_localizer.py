import csv
from datasets import load_dataset
from collections import defaultdict
from datetime import datetime
from bug_report_processor import BugReportProcessor
import concurrent.futures
import threading

lock = threading.Lock()

def extract_fixed_files(patch: str):
    files = set()
    for line in patch.splitlines():
        if line.startswith("diff --git"):
            parts = line.split()
            # diff --git a/foo/bar.py b/foo/bar.py
            file_path = parts[2][2:]  # remove "a/"
            files.add(file_path)
    return sorted(files)

def process_bug(bug, project, output_file):
    bug_report_processor = BugReportProcessor(
        project, bug['bug_id'], str(bug['problem_statement'] or 'N/A')
    )
    result = bug_report_processor.rank_files()
    
    with lock:
        with open(output_file, 'a', newline="", encoding='utf-8', errors='ignore') as output_csv:
            writer = csv.writer(output_csv)
            writer.writerow([bug['bug_id'], result, bug['fixed_files']])


def process_bugs_parallelly(bugs, project, output_file):
    with open(output_file, 'w', newline="", encoding='utf-8', errors='ignore') as output_csv:
        writer = csv.writer(output_csv)
        writer.writerow(['bug_id', 'suspicious_files', 'fixed_files'])

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(lambda bug: process_bug(bug, project, output_file), bugs)


if __name__ == "__main__":
    start_time = datetime.now()

    dataset = load_dataset("princeton-nlp/SWE-bench_Lite", split="test")
    

    project_groups = defaultdict(list)
    for issue in dataset:
        project_name = issue['repo']
        project_groups[project_name].append(issue)

    for project, issues in project_groups.items():
        bug_data = []
        sorted_issues = sorted(issues, key=lambda x: datetime.fromisoformat(x['created_at'].replace('Z', '')))
        for issue in sorted_issues:
            bug_data_entry = {
                'bug_id': issue['instance_id'],
                'fixed_files': extract_fixed_files(issue["patch"]),
                'problem_statement': issue['problem_statement']
            }
            bug_data.append(bug_data_entry)
            
        output_file = project + '-ranking-using-function-call.csv'

        process_bugs_parallelly(bug_data, project, output_file)
        
    end_time = datetime.now()
    print("total time", end_time-start_time)