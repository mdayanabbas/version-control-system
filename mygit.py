import os
import json
import hashlib
import uuid
from datetime import datetime
from typing import Dict, List, Callable, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path

class Utilities:
    @staticmethod
    def generate_sha256(input_string: str) -> str:
        """Generate SHA-256 hash for a given input."""
        return hashlib.sha256(input_string.encode()).hexdigest()

    @staticmethod
    def generate_diff(old_content: List[str], new_content: List[str]) -> List[str]:
        """Generate a diff between two lists of content."""
        diff_result = []
        
        for i in range(max(len(old_content), len(new_content))):
            if i >= len(old_content):
                diff_result.append(f"+ {new_content[i]}")
            elif i >= len(new_content):
                diff_result.append(f"- {old_content[i]}")
            elif old_content[i] != new_content[i]:
                diff_result.append(f"- {old_content[i]}")
                diff_result.append(f"+ {new_content[i]}")
        
        return diff_result

@dataclass
class User:
    """Advanced User Management Class"""
    username: str
    email: str
    public_key: Optional[str] = None
    _password_hash: Optional[str] = None

    def authenticate(self, password: str) -> bool:
        """User authentication method."""
        if not self._password_hash:
            # First time password set
            self._password_hash = Utilities.generate_sha256(password)
            return True
        
        # Verify existing password
        return self._password_hash == Utilities.generate_sha256(password)

    def generate_signature(self, commit_content: str) -> str:
        """Generate a user signature for a commit."""
        return Utilities.generate_sha256(f"{self.username}{commit_content}")

@dataclass
class Commit:
    """Advanced Commit Class with Comprehensive Tracking"""
    hash: str = field(default_factory=lambda: str(uuid.uuid4()))
    message: str = ""
    author: Optional[User] = None
    timestamp: datetime = field(default_factory=datetime.now)
    file_changes: Dict[str, List[str]] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def verify(self) -> bool:
        """Verify commit integrity."""
        reconstructed_hash = Utilities.generate_sha256(
            f"{self.message}{self.author.username}{self.timestamp}"
        )
        return reconstructed_hash == self.hash

    def analyze(self) -> Dict[str, Any]:
        """Perform advanced commit analysis."""
        analysis = {
            'lines_added': 0,
            'lines_removed': 0,
            'impacted_files': [],
            'file_change_count': {}
        }

        for filename, changes in self.file_changes.items():
            file_analysis = {
                'additions': sum(1 for change in changes if change.startswith('+')),
                'deletions': sum(1 for change in changes if change.startswith('-'))
            }
            
            analysis['lines_added'] += file_analysis['additions']
            analysis['lines_removed'] += file_analysis['deletions']
            analysis['impacted_files'].append(filename)
            analysis['file_change_count'][filename] = len(changes)

        return analysis

class Branch:
    """Advanced Branch Management"""
    def __init__(self, name: str):
        self.name = name
        self.commits: List[Commit] = []
        self.base_commit_hash: Optional[str] = None

    def detect_merge_conflicts(self, other_branch: 'Branch') -> bool:
        """Detect potential merge conflicts."""
        conflict_files = set()
        
        for other_commit in other_branch.commits:
            for filename in other_commit.file_changes:
                # Check for overlapping file modifications
                for local_commit in self.commits:
                    if filename in local_commit.file_changes:
                        conflict_files.add(filename)
        
        return bool(conflict_files)

    def merge(self, other_branch: 'Branch', merge_user: User) -> 'Branch':
        """Advanced merge strategy with conflict detection."""
        if self.detect_merge_conflicts(other_branch):
            raise ValueError("Merge conflicts detected!")

        # Create a new merged branch
        merged_branch = Branch(f"{self.name}_merged_{other_branch.name}")
        
        # Combine commits maintaining order
        merged_branch.commits = sorted(
            self.commits + other_branch.commits, 
            key=lambda commit: commit.timestamp
        )

        # Create merge commit
        merge_commit = Commit(
            message=f"Merged branch {other_branch.name}",
            author=merge_user,
            file_changes={}  # Merge commit typically doesn't change files
        )
        merged_branch.commits.append(merge_commit)

        return merged_branch

class Repository:
    """Advanced Repository Management"""
    def __init__(self, name: str, path: Path):
        self.name = name
        self.path = path
        self.branches: Dict[str, Branch] = {}
        self.collaborators: Dict[str, User] = {}

        # Create repository directory
        path.mkdir(parents=True, exist_ok=True)
        
        # Initialize main branch
        self.branches['main'] = Branch('main')

    def create_branch(self, branch_name: str, base_branch: str = 'main') -> Branch:
        """Create a new branch."""
        if branch_name in self.branches:
            raise ValueError(f"Branch {branch_name} already exists!")

        base = self.branches.get(base_branch)
        if not base:
            raise ValueError(f"Base branch {base_branch} not found!")

        new_branch = Branch(branch_name)
        new_branch.commits = base.commits.copy()
        self.branches[branch_name] = new_branch
        return new_branch

    def commit(self, branch: Branch, author: User, message: str, changes: Dict[str, List[str]]) -> Commit:
        """Commit changes to a specific branch."""
        # Create new commit
        commit = Commit(
            message=message,
            author=author,
            file_changes=changes
        )

        # Update branch with new commit
        branch.commits.append(commit)

        # Persist commit
        self._persist_commit(commit)

        return commit

    def _persist_commit(self, commit: Commit):
        """Persist commit to filesystem."""
        commit_dir = self.path / '.vcs' / commit.hash
        commit_dir.mkdir(parents=True, exist_ok=True)

        # Write commit metadata
        metadata_path = commit_dir / 'commit.json'
        with open(metadata_path, 'w') as f:
            json.dump({
                'hash': commit.hash,
                'author': commit.author.username,
                'message': commit.message,
                'timestamp': commit.timestamp.isoformat()
            }, f, indent=2)

        # Persist file changes
        for filename, changes in commit.file_changes.items():
            file_path = commit_dir / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w') as f:
                f.write('\n'.join(changes))

    def search_commits(self, filter_func: Callable[[Commit], bool]) -> List[Commit]:
        """Search commits across all branches."""
        matched_commits = []
        
        for branch in self.branches.values():
            matched_commits.extend(
                commit for commit in branch.commits if filter_func(commit)
            )
        
        return matched_commits

    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive repository report."""
        report = {
            'total_commits': 0,
            'total_branches': len(self.branches),
            'commits_by_author': {},
            'active_branches': []
        }

        for branch_name, branch in self.branches.items():
            report['total_commits'] += len(branch.commits)
            
            # Track commits by author
            for commit in branch.commits:
                author = commit.author.username if commit.author else 'unknown'
                report['commits_by_author'][author] = \
                    report['commits_by_author'].get(author, 0) + 1

            # Track active branches
            if branch.commits:
                report['active_branches'].append(branch_name)

        return report

    def add_collaborator(self, user: User):
        """Add a collaborator to the repository."""
        self.collaborators[user.username] = user

class AdvancedVersionControlSystem:
    """Top-level Version Control System Management"""
    def __init__(self):
        self.repositories: Dict[str, Repository] = {}
        self.users: Dict[str, User] = {}

    def create_repository(self, repo_name: str, path: Optional[Path] = None) -> Repository:
        """Create a new repository."""
        if repo_name in self.repositories:
            raise ValueError(f"Repository {repo_name} already exists!")

        # Use current directory if no path provided
        repo_path = path or Path.cwd() / repo_name
        
        repository = Repository(repo_name, repo_path)
        self.repositories[repo_name] = repository
        return repository

    def register_user(self, username: str, email: str) -> User:
        """Register a new user."""
        if username in self.users:
            raise ValueError(f"User {username} already exists!")

        user = User(username=username, email=email)
        self.users[username] = user
        return user

    def demonstrate_advanced_features(self):
        """Demonstrate comprehensive VCS features."""
        # Create users
        alice = self.register_user("alice", "alice@example.com")
        bob = self.register_user("bob", "bob@example.com")

        # Create repository
        project_repo = self.create_repository(
            "advanced_project", 
            Path.cwd() / "advanced_project"
        )

        # Add collaborators
        project_repo.add_collaborator(alice)
        project_repo.add_collaborator(bob)

        # Create develop branch
        develop_branch = project_repo.create_branch("develop")

        # Simulate commits
        first_commit = project_repo.commit(
            develop_branch, 
            alice, 
            "Initial project setup", 
            {
                "README.md": ["+ # Advanced Project", "+ Initial setup"],
                "src/main.py": ["+ def main():", "+     pass"]
            }
        )

        # Search commits by author
        alice_commits = project_repo.search_commits(
            lambda commit: commit.author.username == "alice"
        )

        # Generate repository report
        report = project_repo.generate_report()

        # Print report details
        print("Repository Report:")
        print(f"Total Commits: {report['total_commits']}")
        print(f"Total Branches: {report['total_branches']}")
        print(f"Active Branches: {', '.join(report['active_branches'])}")
        print("\nCommits by Author:")
        for author, count in report['commits_by_author'].items():
            print(f"{author}: {count} commits")

def main():
    try:
        vcs = AdvancedVersionControlSystem()
        vcs.demonstrate_advanced_features()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
    