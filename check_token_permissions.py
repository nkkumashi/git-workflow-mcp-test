#!/usr/bin/env python3
"""Check exact token permissions."""

import requests


def check_token_permissions():
    """Check what permissions the token actually has."""
    print("🔍 Checking Token Permissions")
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
    
    # Check token permissions via API
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Get token info
    response = requests.get('https://api.github.com/user', headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        print(f"✅ Token valid for user: {user_data['login']}")
    else:
        print(f"❌ Token validation failed: {response.status_code}")
        return
    
    # Check repository-specific permissions
    repo_url = 'https://api.github.com/repos/nkkumashi/git-workflow-mcp-test'
    response = requests.get(repo_url, headers=headers)
    
    if response.status_code == 200:
        repo_data = response.json()
        permissions = repo_data.get('permissions', {})
        print(f"\n📋 Repository Permissions:")
        for perm, value in permissions.items():
            status = "✅" if value else "❌"
            print(f"   {status} {perm}: {value}")
    else:
        print(f"❌ Repository access failed: {response.status_code}")
    
    # Test PR creation endpoint specifically
    print(f"\n🧪 Testing PR Creation Endpoint:")
    pr_data = {
        'title': 'Test PR Permission Check',
        'body': 'Testing permissions',
        'head': 'feature/20251028-100500',
        'base': 'main',
        'draft': True  # Create as draft to avoid spam
    }
    
    response = requests.post(
        f'{repo_url}/pulls',
        headers=headers,
        json=pr_data
    )
    
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        print("   ✅ PR Creation: SUCCESS!")
        pr_data = response.json()
        print(f"   🎉 Draft PR created: {pr_data['html_url']}")
        
        # Clean up - close the draft PR
        pr_number = pr_data['number']
        close_response = requests.patch(
            f'{repo_url}/pulls/{pr_number}',
            headers=headers,
            json={'state': 'closed'}
        )
        if close_response.status_code == 200:
            print("   🧹 Draft PR closed automatically")
            
    elif response.status_code == 403:
        print("   ❌ PR Creation: 403 Forbidden")
        error_data = response.json()
        print(f"   Error: {error_data.get('message', 'Unknown error')}")
        print("\n💡 Your token needs 'Pull requests: Read and write' permission")
    else:
        print(f"   ❌ PR Creation: {response.status_code}")
        print(f"   Response: {response.text[:200]}")


if __name__ == "__main__":
    check_token_permissions()