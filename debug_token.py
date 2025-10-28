#!/usr/bin/env python3
"""Debug GitHub token permissions."""

import os
import sys
sys.path.append('../git-workflow-mcp')

from github import Github


def debug_token():
    """Debug GitHub token permissions and access."""
    print("🔍 Debugging GitHub Token")
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
    
    if not token or token == 'your_new_github_pat_here':
        print("❌ No valid GitHub token found in .env file")
        return
    
    print(f"✅ Token loaded (length: {len(token)})")
    print(f"   Token prefix: {token[:10]}...")
    
    # Test GitHub API access
    try:
        github = Github(token)
        user = github.get_user()
        print(f"✅ GitHub API access successful")
        print(f"   User: {user.login}")
        print(f"   Name: {user.name}")
        
        # Test repository access
        repo = github.get_repo("nkkumashi/git-workflow-mcp-test")
        print(f"✅ Repository access successful")
        print(f"   Repo: {repo.full_name}")
        print(f"   Permissions: {repo.permissions}")
        
        # Test if we can create a PR (dry run)
        print("\n🧪 Testing PR creation permissions...")
        try:
            # Get branches
            branches = list(repo.get_branches())
            print(f"   Available branches: {[b.name for b in branches[:5]]}")
            
            # Check if we have push access
            if repo.permissions.push:
                print("✅ Push permission: Yes")
            else:
                print("❌ Push permission: No")
                
            if repo.permissions.pull:
                print("✅ Pull permission: Yes")
            else:
                print("❌ Pull permission: No")
                
            # The actual issue might be that we need to check specific scopes
            print("\n💡 Token appears to have basic access.")
            print("   If PR creation fails, the token might need 'repo' scope.")
            
        except Exception as e:
            print(f"❌ Error testing PR permissions: {e}")
            
    except Exception as e:
        print(f"❌ GitHub API access failed: {e}")
        print("   Check if token is valid and has correct permissions")


if __name__ == "__main__":
    debug_token()