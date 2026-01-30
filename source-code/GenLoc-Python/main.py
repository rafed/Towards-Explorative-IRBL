from pydriller import Git
from config import Config
from file_processor import *
from db_handler import initialize_db
from file_parser import initialize_parser
from collection_handler import get_suspicious_files
from datetime import datetime
from datasets import load_dataset
from collections import defaultdict


def main():
    start_time = datetime.now()
    dataset = load_dataset("princeton-nlp/SWE-bench_Lite", split="test")

    # Group by project (repo)
    project_groups = defaultdict(list)
    for issue in dataset:
        project_name = issue['repo']
        project_groups[project_name].append(issue)

    for project, issues in project_groups.items():
        config = Config()
        config.set_project(project)
        config.set_embedding_type('openai')
        sorted_issues = sorted(issues, key=lambda x: datetime.fromisoformat(x['created_at'].replace('Z', '')))

        initialize_parser()
        initialize_db()

        prev_commit = ""
        repo_path = '../swe_lite_repos/' + project.split('/')[1]
        git_repo = Git(repo_path)

        for issue in sorted_issues:
            print(issue['instance_id'], issue['base_commit'])
            manage_file_processing(git_repo, issue['instance_id'], prev_commit, f"{issue['base_commit']}")
            get_suspicious_files(issue['instance_id'], issue['problem_statement'])
            prev_commit = f"{issue['base_commit']}"
        # break
    end_time = datetime.now()
    print('total time', end_time - start_time)
    print("*********************************************************************************************")


if __name__ == "__main__":
    main()