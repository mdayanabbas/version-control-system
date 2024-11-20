from mygit import AdvancedVersionControlSystem
from pathlib import Path

# Create an instance of the VCS
vcs = AdvancedVersionControlSystem()

# Register users
alice = vcs.register_user("Abbas", "alice@example.com")
bob = vcs.register_user("Aman", "bob@example.com")

# Create a repository
repo = vcs.create_repository("sample_project", Path.cwd() / "sample_project")
repo.add_collaborator(alice)
repo.add_collaborator(bob)

# Create a branch
develop_branch = repo.create_branch("hhahahahaha")

# Make a commit
changes = {"README.md": ["+ # Sample Project", "+ Initial setup"]}
commit = repo.commit(develop_branch, alice, "Added README", changes)

# Generate a report
report = repo.generate_report()
print(report)
