from mygit import AdvancedVersionControlSystem
from pathlib import Path

vcs = AdvancedVersionControlSystem()

alice = vcs.register_user("Abbas", "alice@example.com")
bob = vcs.register_user("Aman
", "bob@example.com")

repo = vcs.create_repository("sample_project", Path.cwd() / "sample_project")
repo.add_collaborator(alice)
repo.add_collaborator(bob)

develop_branch = repo.create_branch("hhahahahaha")

changes = {"README.md": ["+ # Sample Project", "+ Initial setup"]}
commit = repo.commit(develop_branch, alice, "Added README", changes)

report = repo.generate_report()
print(report)
