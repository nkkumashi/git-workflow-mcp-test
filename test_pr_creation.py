#!/usr/bin/env python3
"""Test PR creation directly."""

import os
import sys
sys.path.append('../git-workflow-mcp')

from github import Github


def test_pr_creation():
    """Test creating a PR directly."""
    print("🧪 Testing Direct PR Creation")
    print("=" * 40)
    
    # Load token from .env
    token = None
    try:
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('GITHUB_TOKEN='):
                    token = line.split('=', 1)[1].strip()
                    break
    except Exception as e:
        print(f"❌ Error loading .env: {e}")
        return
    
    if not token:
        print("❌ No GitHub token found")
        return
    
    try:
        github = Github(token)
        repo = github.get_repo("nkkumashi/git-workflow-mcp-test")
        
        print(f"✅ Connected to repository: {repo.full_name}")
        
        # Check branches
        branches = [b.name for b in repo.get_branches()]
        print(f"   Available branches: {branches}")
        
        # Try to create a test PR
        head_branch = "feature/20251028-100500"
        base_branch = "main"
        
        if head_branch not in branches:
            print(f"❌ Head branch '{head_branch}' not found")
            return
            
        print(f"\n🚀 Attempting to create PR...")
        print(f"   Head: {head_branch}")
        print(f"   Base: {base_branch}")
        
        pr = repo.create_pull(
            title="🧪 Test PR from MCP Server",
            body="This is a test PR created by the Git Workflow MCP Server to verify functionality.\n\n✅ All workflows passed successfully!",
            head=head_branch,
            base=base_branch
        )
        
        print(f"🎉 SUCCESS! PR created!")
        print(f"   PR Number: #{pr.number}")
        print(f"   PR URL: {pr.html_url}")
        print(f"   Title: {pr.title}")
        
    except Exception as e:
        print(f"❌ Error creating PR: {e}")
        print(f"   Error type: {type(e).__name__}")
        
        # Check if it's a specific GitHub error
        if hasattr(e, 'status'):
            print(f"   HTTP Status: {e.status}")
        if hasattr(e, 'data'):
            print(f"   Error data: {e.data}")


if __name__ == "__main__":
    test_pr_creation()