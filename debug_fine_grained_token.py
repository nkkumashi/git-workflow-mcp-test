#!/usr/bin/env python3
"""Debug fine-grained token permissions and fix the issue."""

import os
import sys
sys.path.append('../git-workflow-mcp')

from github import Github
import requests


def debug_fine_grained_token():
    """Debug fine-grained token permissions."""
    print("🔍 Debugging Fine-Grained Token Permissions")
    print("=" * 50)
    
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
    
    print(f"✅ Token loaded (type: {'fine-grained' if token.startswith('github_pat_') else 'classic'})")
    
    # Test basic API access
    try:
        github = Github(token)
        user = github.get_user()
        print(f"✅ Basic API access: {user.login}")
        
        # Test repository access
        repo = github.get_repo("nkkumashi/git-workflow-mcp-test")
        print(f"✅ Repository access: {repo.full_name}")
        
        # Check what permissions we have
        permissions = repo.permissions
        print(f"\n📋 Current Repository Permissions:")
        print(f"   • Admin: {permissions.admin}")
        print(f"   • Push: {permissions.push}")
        print(f"   • Pull: {permissions.pull}")
        print(f"   • Maintain: {permissions.maintain}")
        print(f"   • Triage: {permissions.triage}")
        
        # Test specific operations
        print(f"\n🧪 Testing Specific Operations:")
        
        # Test 1: Can we list PRs?
        try:
            pulls = list(repo.get_pulls(state='all'))
            print(f"   ✅ List PRs: Success ({len(pulls)} PRs found)")
        except Exception as e:
            print(f"   ❌ List PRs: Failed - {e}")
        
        # Test 2: Can we get branches?
        try:
            branches = [b.name for b in repo.get_branches()]
            print(f"   ✅ List branches: Success ({len(branches)} branches)")
        except Exception as e:
            print(f"   ❌ List branches: Failed - {e}")
        
        # Test 3: Direct API call to create PR (to see exact error)
        print(f"\n🔬 Testing Direct PR Creation API Call:")
        
        # Check if we have the right branches
        if 'feature/20251028-100500' in branches and 'main' in branches:
            headers = {
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3+json',
                'X-GitHub-Api-Version': '2022-11-28'
            }
            
            pr_data = {
                'title': '🧪 Test PR - Fine-grained Token',
                'body': 'Testing fine-grained token PR creation',
                'head': 'feature/20251028-100500',
                'base': 'main'
            }
            
            response = requests.post(
                f'https://api.github.com/repos/nkkumashi/git-workflow-mcp-test/pulls',
                headers=headers,
                json=pr_data
            )
            
            print(f"   Status Code: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
            if response.status_code == 201:
                print("   ✅ PR Creation: SUCCESS!")
                pr_data = response.json()
                print(f"   🎉 PR #{pr_data['number']} created: {pr_data['html_url']}")
            elif response.status_code == 403:
                print("   ❌ PR Creation: 403 Forbidden")
                print("   💡 This means the token lacks specific permissions")
                print("\n🔧 SOLUTION:")
                print("   Go to your fine-grained token settings and ensure these permissions:")
                print("   • Pull requests: Read and write")
                print("   • Contents: Read and write")
                print("   • Metadata: Read")
                print("   • Actions: Read (for workflow access)")
            else:
                print(f"   ❌ PR Creation: {response.status_code} - {response.text}")
        else:
            print("   ⚠️  Required branches not found for PR test")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print(f"\n" + "=" * 50)
    print("💡 Fine-grained tokens are more secure and preferred!")
    print("   Just need to configure the right permissions.")


if __name__ == "__main__":
    debug_fine_grained_token()