import os
import re
import ast
import json
import uuid
import difflib
import hashlib
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime
import random
import shutil

class AICodeAnalyzer:
    """Advanced AI-powered code analysis and optimization engine"""
    
    @staticmethod
    def detect_code_smells(code: str) -> Dict[str, List[str]]:
        """Detect potential code quality issues"""
        issues = {
            'complexity': [],
            'performance': [],
            'security': [],
            'best_practices': []
        }
        
        try:
            # Parse the code to AST
            tree = ast.parse(code)
            
            # Complexity analysis
            complexity = AICodeAnalyzer._calculate_cyclomatic_complexity(tree)
            if complexity > 10:
                issues['complexity'].append(f"High cyclomatic complexity: {complexity}")
            
            # Security checks
            security_checks = AICodeAnalyzer._perform_security_scan(code)
            issues['security'].extend(security_checks)
            
            # Performance suggestions
            performance_issues = AICodeAnalyzer._analyze_performance(tree)
            issues['performance'].extend(performance_issues)
            
            # Best practices
            best_practice_issues = AICodeAnalyzer._check_best_practices(tree)
            issues['best_practices'].extend(best_practice_issues)
        
        except SyntaxError:
            issues['complexity'].append("Invalid syntax detected")
        
        return {k: v for k, v in issues.items() if v}
    
    @staticmethod
    def _calculate_cyclomatic_complexity(tree):
        """Calculate cyclomatic complexity of the code"""
        complexity = 1
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.Try, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity
    
    @staticmethod
    def _perform_security_scan(code: str) -> List[str]:
        """Perform basic security vulnerability detection"""
        security_issues = []
        
        # Check for potential security risks
        risky_patterns = [
            (r'eval\(.*\)', 'Potential code injection risk'),
            (r'exec\(.*\)', 'Potential remote code execution'),
            (r'input\(.*\)', 'Potential input validation required'),
            (r'os\.system\(.*\)', 'Potential command injection'),
        ]
        
        for pattern, message in risky_patterns:
            if re.search(pattern, code):
                security_issues.append(message)
        
        return security_issues
    
    @staticmethod
    def _analyze_performance(tree) -> List[str]:
        """Detect potential performance bottlenecks"""
        performance_issues = []
        
        # Check for inefficient list comprehensions
        for node in ast.walk(tree):
            if isinstance(node, ast.ListComp):
                performance_issues.append("Complex list comprehension - consider generator")
        
        return performance_issues
    
    @staticmethod
    def _check_best_practices(tree) -> List[str]:
        """Check for Python best practices"""
        best_practice_issues = []
        
        # Check for deep nesting
        max_nesting = 3
        current_nesting = 0
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.If, ast.For, ast.While)):
                current_nesting += 1
                if current_nesting > max_nesting:
                    best_practice_issues.append(f"Deep nesting detected (level {current_nesting})")
        
        return best_practice_issues
    
    @staticmethod
    def suggest_optimizations(code: str) -> Dict[str, List[str]]:
        """Provide code optimization suggestions"""
        optimizations = {
            'refactoring': [],
            'performance_improvements': []
        }
        
        # Example suggestions (can be expanded)
        suggestions = [
            ("for i in range(len(x))", "Use enumerate() or direct iteration"),
            ("if condition == True", "Simplify to 'if condition'"),
            ("except Exception as e: pass", "Log or handle exceptions properly"),
        ]
        
        for pattern, suggestion in suggestions:
            if re.search(pattern, code):
                optimizations['refactoring'].append(suggestion)
        
        return optimizations

@dataclass
class CodeReview:
    """Comprehensive code review tracking"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    code_snippet: str = ""
    file_path: str = ""
    analysis_results: Dict[str, List[str]] = field(default_factory=dict)
    optimization_suggestions: Dict[str, List[str]] = field(default_factory=dict)
    severity_score: float = 0.0

    def to_dict(self):
        """Convert CodeReview to dictionary for serialization"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'code_snippet': self.code_snippet,
            'file_path': self.file_path,
            'analysis_results': self.analysis_results,
            'optimization_suggestions': self.optimization_suggestions,
            'severity_score': self.severity_score
        }

    @classmethod
    def from_dict(cls, data):
        """Create CodeReview from dictionary"""
        review = cls()
        review.id = data['id']
        review.timestamp = datetime.fromisoformat(data['timestamp'])
        review.code_snippet = data['code_snippet']
        review.file_path = data['file_path']
        review.analysis_results = data['analysis_results']
        review.optimization_suggestions = data['optimization_suggestions']
        review.severity_score = data['severity_score']
        return review

    def interactive_menu(self):
        """Enhanced interactive CLI for CodeSync"""
        while True:
            print("\n--- CodeSync: AI-Powered Code Analysis ---")
            print("1. Create Repository")
            print("2. List Repositories")
            print("3. Analyze Repository")
            print("4. View Project Health Report")
            print("5. Remove Repository")
            print("6. Exit")
            
            choice = input("Enter your choice: ")
            
            try:
                if choice == '1':
                    name = input("Enter repository name: ")
                    path = input("Enter repository path: ")
                    self.create_repository(name, path)
                    print(f"Repository {name} created successfully!")
                
                elif choice == '2':
                    if not self.repositories:
                        print("No repositories found.")
                    else:
                        print("\nCreated Repositories:")
                        for name, repo in self.repositories.items():
                            print(f"- {name} (Path: {repo.path})")
                
                elif choice == '3':
                    if not self.repositories:
                        print("No repositories. Create one first!")
                        continue
                    
                    print("Available Repositories:")
                    for repo_name in self.repositories:
                        print(repo_name)
                    
                    repo_name = input("Enter repository name to analyze: ")
                    result = self.analyze_repository(repo_name)
                    print("\nAnalysis Results:")
                    print(f"Total Files Analyzed: {result['total_files_analyzed']}")
                    print("\nDetailed Project Report:")
                    report = result['project_report']
                    print(f"Total Code Reviews: {report['total_reviews']}")
                    print(f"Average Severity Score: {report['average_severity']:.2f}")
                    print("Critical Files:")
                    for file in report['critical_files']:
                        print(f"  - {file}")
                    print(f"Optimization Opportunities: {report['optimization_opportunities']}")
                
                elif choice == '4':
                    if not self.repositories:
                        print("No repositories. Create one first!")
                        continue
                    
                    print("Available Repositories:")
                    for repo_name in self.repositories:
                        print(repo_name)
                    
                    repo_name = input("Enter repository name: ")
                    report = self.repositories[repo_name].generate_project_health_report()
                    
                    print("\n--- Project Health Report ---")
                    print(f"Total Code Reviews: {report['total_reviews']}")
                    print(f"Average Severity Score: {report['average_severity']:.2f}")
                    print("Critical Files:")
                    for file in report['critical_files']:
                        print(f"  - {file}")
                    print(f"Optimization Opportunities: {report['optimization_opportunities']}")
                
                elif choice == '5':
                    if not self.repositories:
                        print("No repositories to remove!")
                        continue
                    
                    print("Available Repositories:")
                    for repo_name in self.repositories:
                        print(repo_name)
                    
                    repo_name = input("Enter repository name to remove: ")
                    confirm = input(f"Are you sure you want to remove repository '{repo_name}'? (y/N): ")
                    
                    if confirm.lower() == 'y':
                        delete_files = input("Do you want to delete repository files? (y/N): ").lower() == 'y'
                        self.remove_repository(repo_name, delete_files)
                        print(f"Repository '{repo_name}' removed successfully!")
                
                elif choice == '6':
                    print("Exiting CodeSync. Goodbye!")
                    break
                
                else:
                    print("Invalid choice. Try again.")
            
            except Exception as e:
                print(f"Error: {e}")

def main():
    print("Welcome to CodeSync: AI-Powered Code Analysis Tool")
    cli = CodeSyncCLI()
    cli.interactive_menu()

if __name__ == "__main__":
    main()