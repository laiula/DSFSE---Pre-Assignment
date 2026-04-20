from pydriller import Repository
from pydriller.domain.commit import ModificationType

repo_url = "https://github.com/apache/lucene"

issue_ids = ['LUCENE-12', 'LUCENE-17', 'LUCENE-701', 'LUCENE-1200', 'LUCENE-1799']
issue_ids = set(i.upper() for i in issue_ids)   # 🔥 faster lookup

total_commits = 0
total_dmm = 0
total_files_changed = 0

repo = Repository(
    repo_url,
    only_in_branch="main",     # 🔥 reduces history scope
)

for commit in repo.traverse_commits():

    msg = commit.msg.upper()

    # 🔥 faster than "any()"
    if not any(issue in msg for issue in issue_ids):
        continue

    total_commits += 1

    # DMM (avoid repeated attribute calls)
    size = commit.dmm_unit_size or 0
    complexity = commit.dmm_unit_complexity or 0
    interfacing = commit.dmm_unit_interfacing or 0

    total_dmm += (size + complexity + interfacing) / 3

    # 🔥 faster loop (avoid set lookup overhead inside loop)
    for f in commit.modified_files:
        if f.change_type in (ModificationType.ADD,
                              ModificationType.MODIFY,
                              ModificationType.DELETE):
            total_files_changed += 1


avg_files_changed = total_files_changed / total_commits if total_commits else 0
avg_dmm_metric = total_dmm / total_commits if total_commits else 0

print("Total commits analyzed:", total_commits)
print("Average Number of Files Changed:", avg_files_changed)
print("Average DMM Metric:", avg_dmm_metric)