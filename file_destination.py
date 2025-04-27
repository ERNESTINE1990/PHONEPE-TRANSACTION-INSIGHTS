from git import Repo


repo_url = "https://github.com/PhonePe/pulse.git"
destination = "C:/Users/mosel/Documents/PYTHON/project/project_phonepe_transaction_insight/dataset/"

Repo.clone_from(repo_url, destination)