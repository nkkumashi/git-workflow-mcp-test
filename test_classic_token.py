#!/usr/bin/env python3
"""Test classic GitHub token for PR creation."""

import os
import sys
sys.path.append('../git-workflow-mcp')

from github import Github


def test_classic_token():
    """Test if classic token can create PRs."""
    print("🔑 Testing Classic GitHub Token")
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
    
    if not token or token == 'your_classic_github_token_here':
        print("❌ Please update the GITHUB_TOKEN in .env file with your classic token")
        print("   Token should start with 'ghp_'")
        return
    
    print(f"✅ Token loaded")
    
    # Check token type
    if token.startswith('ghp_'):
        print("✅ Classic token detected (ghp_)")
    elif token.startswith('github_pat_'):
        print("⚠️  Fine-grained token detected - may not work for PR creation")
    else:
        print("⚠️  Unknown token format")
    
    try:
        github = Github(token)
        user = github.get_user()
        print(f"✅ GitHub API access successful")
        print(f"   User: {user.login}")
        
        # Test repository access
        repo = github.get_repo("nkkumashi/git-workflow-mcp-test")
        print(f"✅ Repository access successful")
        print(f"   Permissions: {repo.permissions}")
        
        # Check if we can access pulls endpoint
        try:
            pulls = list(repo.get_pulls(state='all'))
            print(f"✅ Pull requests access successful")
            print(f"   Existing PRs: {len(pulls)}")
            
            print("\n🎯 Token appears ready for PR creation!")
            print("   You can now run the full workflow test.")
            
        except Exception as e:
            print(f"❌ Pull requests access failed: {e}")
            
    except Exception as e:
        print(f"❌ GitHub API access failed: {e}")


if __name__ == "__main__":
    test_classic_token()