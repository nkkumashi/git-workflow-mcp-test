#!/usr/bin/env python3
"""Test all scenarios for the enhanced git-workflow-cli."""

import sys
import os
from pathlib import Path

# Add the git_workflow_cli to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "git-workflow-cli"))

from git_workflow_cli.main import cli
from git_workflow_cli.validator import CommitValidator
from git_workflow_cli.workflow import GitWorkflow
from rich.console import Console
import click
from click.testing import CliRunner

console = Console()

def test_validation_scenarios():
    """Test various validation scenarios."""
    
    console.print("🧪 Testing Validation Scenarios", style="blue bold")
    console.print("="*50, style="blue")
    
    test_cases = [
        # Positive cases
        ("feat: add user dashboard", "✅ Should trigger MINOR release"),
        ("fix(api): resolve timeout issue", "✅ Should trigger PATCH release"),
        ("docs: update README with examples", "✅ Should NOT trigger release"),
        ("perf: optimize database queries", "✅ Should trigger PATCH release"),
        ("chore: update dependencies", "✅ Should NOT trigger release"),
        
        # Breaking change cases (need to escape ! in shell)
        ("feat: redesign authentication system\n\nBREAKING CHANGE: API endpoints changed", "✅ Should trigger MAJOR release"),
        
        # Negative cases
        ("invalid message format", "❌ Should fail validation"),
        ("feat:", "❌ Should fail - no description"),
        ("feat: A", "❌ Should fail - description too short"),
        ("feat: Add new feature.", "❌ Should fail - ends with period"),
        ("feat: Add New Feature", "❌ Should fail - starts with uppercase"),
        ("unknown: some change", "❌ Should fail - invalid type"),
    ]
    
    validator = CommitValidator()
    
    for message, expected in test_cases:
        console.print(f"\n📝 Testing: '{message[:50]}{'...' if len(message) > 50 else ''}'", style="cyan")
        console.print(f"   Expected: {expected}", style="dim")
        
        result = validator.validate(message)
        
        if result.is_valid:
            console.print("✅ Valid commit message", style="green")
            console.print(f"   Type: {result.type}")
            if result.scope:
                console.print(f"   Scope: {result.scope}")
            
            # Enhanced release information
            if result.breaking_change:
                console.print("   Release Impact: MAJOR (Breaking Change)", style="red bold")
            elif result.release_type.value == "minor":
                console.print("   Release Impact: MINOR (New Feature)", style="yellow")
            elif result.release_type.value == "patch":
                console.print("   Release Impact: PATCH (Bug Fix)", style="green")
            else:
                console.print("   Release Impact: NONE (No Release)", style="dim")
        else:
            console.print("❌ Invalid commit message", style="red")
            for error in result.errors:
                console.print(f"   • {error}")

def test_workflow_info():
    """Test workflow information display."""
    
    console.print("\n\n🔄 Testing Workflow Information", style="blue bold")
    console.print("="*50, style="blue")
    
    try:
        workflow = GitWorkflow()
        validator = CommitValidator()
        
        test_messages = [
            "feat: add user authentication",
            "fix: resolve critical bug",
            "docs: update API documentation", 
            "ci: update GitHub Actions workflow",
            "test: add unit tests for auth module"
        ]
        
        for message in test_messages:
            console.print(f"\n📝 Message: '{message}'", style="cyan")
            result = validator.validate(message)
            
            if result.is_valid:
                release_info = workflow._get_release_info(result)
                console.print(f"   Release Impact: {release_info['level']}", style=release_info['style'])
                
                workflow_info = workflow._get_workflow_info(result)
                if workflow_info['will_trigger_workflows']:
                    console.print("   🔄 GitHub Workflows:", style="blue")
                    for wf in workflow_info['workflows']:
                        console.print(f"     • {wf}")
                
                if result.release_type.value != "none" or result.breaking_change:
                    console.print("   ⚠️  Would prompt user for confirmation", style="yellow")
                    
    except Exception as e:
        console.print(f"⚠️  Workflow test limited (repo context): {e}", style="yellow")

def test_cli_runner():
    """Test CLI using Click's test runner."""
    
    console.print("\n\n🖥️  Testing CLI Commands", style="blue bold")
    console.print("="*50, style="blue")
    
    runner = CliRunner()
    
    # Test validation mode
    console.print("\n📋 Testing --validate flag:", style="blue")
    
    test_cases = [
        "feat: add new feature",
        "fix(api): resolve bug", 
        "invalid message"
    ]
    
    for message in test_cases:
        console.print(f"\n   Testing: '{message}'", style="cyan")
        result = runner.invoke(cli, ['--validate', message])
        
        # Show first few lines of output
        output_lines = result.output.strip().split('\n')[:5]
        for line in output_lines:
            console.print(f"   {line}")
        
        if len(result.output.strip().split('\n')) > 5:
            console.print("   ...")

def main():
    """Run all tests."""
    
    console.print("🎯 Enhanced Git Workflow CLI - Comprehensive Testing", style="green bold")
    console.print("="*60, style="green")
    
    # Change to the test repo directory
    os.chdir(Path(__file__).parent)
    
    try:
        test_validation_scenarios()
        test_workflow_info() 
        test_cli_runner()
        
        console.print("\n\n🎉 All Tests Complete!", style="green bold")
        console.print("\n📋 Summary of Enhanced Features:", style="blue")
        console.print("• ✅ Detailed release impact information")
        console.print("• ✅ GitHub workflow predictions")
        console.print("• ✅ User confirmation prompts for releases")
        console.print("• ✅ Comprehensive validation messages")
        console.print("• ✅ Enhanced error reporting")
        
    except Exception as e:
        console.print(f"\n❌ Test failed: {e}", style="red")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()