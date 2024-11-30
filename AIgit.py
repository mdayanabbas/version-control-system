import os
import re
import ast
import json
import uuid
import difflib
import hashlib
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import random

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

class CodeSyncRepository:
    """Advanced repository management with AI-powered insights"""
    
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path
        self.reviews: List[CodeReview] = []
        self.code_health_history: List[float] = []
    
    def analyze_file(self, file_path: str) -> CodeReview:
        """Perform comprehensive code analysis on a file"""
        try:
            with open(file_path, 'r') as f:
                code_content = f.read()
            
            # Perform AI-powered analysis
            code_smells = AICodeAnalyzer.detect_code_smells(code_content)
            optimizations = AICodeAnalyzer.suggest_optimizations(code_content)
            
            # Calculate severity score
            severity = self._calculate_severity(code_smells)
            
            # Create code review
            review = CodeReview(
                code_snippet=code_content,
                file_path=file_path,
                analysis_results=code_smells,
                optimization_suggestions=optimizations,
                severity_score=severity
            )
            
            self.reviews.append(review)
            self.code_health_history.append(severity)
            
            return review
        
        except Exception as e:
            print(f"Error analyzing file {file_path}: {e}")
            return None
    
    def _calculate_severity(self, code_smells: Dict[str, List[str]]) -> float:
        """Calculate severity score based on detected issues"""
        severity_map = {
            'complexity': 0.4,
            'security': 0.3,
            'performance': 0.2,
            'best_practices': 0.1
        }
        
        severity = 0.0
        for category, issues in code_smells.items():
            severity += len(issues) * severity_map.get(category, 0.1)
        
        return min(severity, 10.0)  # Cap at 10
    
    def generate_project_health_report(self) -> Dict[str, Any]:
        """Generate comprehensive project health report"""
        report = {
            'total_reviews': len(self.reviews),
            'average_severity': sum(self.code_health_history) / len(self.code_health_history) if self.code_health_history else 0,
            'critical_files': [],
            'optimization_opportunities': 0
        }
        
        # Identify critical files
        report['critical_files'] = [
            review.file_path for review in self.reviews 
            if review.severity_score > 5.0
        ]
        
        # Count optimization opportunities
        for review in self.reviews:
            report['optimization_opportunities'] += sum(
                len(suggestions) for suggestions in review.optimization_suggestions.values()
            )
        
        return report

class CodeSyncCLI:
    """Command-line interface for CodeSync"""
    
    def __init__(self):
        self.repositories: Dict[str, CodeSyncRepository] = {}
    
    def create_repository(self, name: str, path: str) -> CodeSyncRepository:
        """Create a new repository"""
        if name in self.repositories:
            raise ValueError(f"Repository {name} already exists!")
        
        repo = CodeSyncRepository(name, path)
        self.repositories[name] = repo
        return repo
    
    def analyze_repository(self, repo_name: str, recursive: bool = True) -> Dict[str, Any]:
        """Analyze entire repository or specific files"""
        repo = self.repositories.get(repo_name)
        if not repo:
            raise ValueError(f"Repository {repo_name} not found!")
        
        results = []
        
        # Walk through repository files
        for root, _, files in os.walk(repo.path):
            for file in files:
                if file.endswith('.py'):  # Focus on Python files
                    file_path = os.path.join(root, file)
                    review = repo.analyze_file(file_path)
                    if review:
                        results.append(review)
        
        return {
            'total_files_analyzed': len(results),
            'project_report': repo.generate_project_health_report()
        }
    
    def interactive_menu(self):
        """Interactive CLI for CodeSync"""
        while True:
            print("\n--- CodeSync: AI-Powered Code Analysis ---")
            print("1. Create Repository")
            print("2. Analyze Repository")
            print("3. View Project Health Report")
            print("4. Exit")
            
            choice = input("Enter your choice: ")
            
            try:
                if choice == '1':
                    name = input("Enter repository name: ")
                    path = input("Enter repository path: ")
                    self.create_repository(name, path)
                    print(f"Repository {name} created successfully!")
                
                elif choice == '2':
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
                
                elif choice == '3':
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
                
                elif choice == '4':
                    break
                
                else:
                    print("Invalid choice. Try again.")
            
            except Exception as e:
                print(f"Error: {e}")

def main():
    cli = CodeSyncCLI()
    cli.interactive_menu()

if __name__ == "__main__":
    main()