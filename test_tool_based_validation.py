#!/usr/bin/env python3
"""Test the tool-based commit validation using commitlint and semantic-release."""

import asyncio
import sys
import os

# Add the parent directory to the path to import our MCP server
sys.path.append('../git-workflow-mcp')

from git_workflow_mcp.server import GitWorkflowMCPServer


async def test_tool_based_validation():
    """Test the tool-based commit validation."""
    print("🔧 Testing Tool-Based Commit Validation")
    print("=" * 60)
    
    server = GitWorkflowMCPServer()
    await server._initialize_workflow_engine()
    
    if not server.workflow_engine:
        print("❌ Failed to initialize workflow engine")
        return
    
    print("✅ MCP Server initialized successfully")
    
    # Step 1: Check current tool status
    print("\n1️⃣ Checking current validation tools status...")
    tools_status = server.workflow_engine.commit_validator.get_tools_status()
    print(f"   Tools available: {tools_status}")
    
    # Step 2: Set up tools if needed
    if not all(tools_status.values()):
        print("\n2️⃣ Setting up validation tools...")
        setup_result = await server.workflow_engine.setup_validation_tools()
        print(f"   Setup status: {setup_result.status.value}")
        print(f"   Setup message: {setup_result.message}")
        
        if setup_result.data:
            print(f"   Setup results: {setup_result.data}")
        
        if setup_result.errors:
            print(f"   Setup errors: {setup_result.errors}")
    else:
        print("\n2️⃣ All validation tools already available!")
    
    # Step 3: Test validation with different commit messages
    test_commits = [
        {
            "message": "feat: add user authentication system",
            "description": "Valid conventional commit (should pass)"
        },
        {
            "message": "Fix: resolve memory leak in parser",
            "description": "Invalid case (should fail with commitlint)"
        },
        {
            "message": "feat(auth)!: redesign authentication API\n\nBREAKING CHANGE: This changes the login flow completely",
            "description": "Breaking change with body (should trigger MAJOR)"
        },
        {
            "message": "docs: update API documentation",
            "description": "Documentation change (should not trigger release)"
        },
        {
            "message": "Add some new feature without proper format",
            "description": "Invalid format (should fail validation)"
        }
    ]
    
    print(f"\n3️⃣ Testing validation with {len(test_commits)} different commit messages:")
    
    for i, test_commit in enumerate(test_commits, 1):
        print(f"\n   {i}. {test_commit['description']}")
        print(f"      Message: '{test_commit['message'][:50]}{'...' if len(test_commit['message']) > 50 else ''}'")
        
        try:
            validation_result = await server.workflow_engine.commit_validator.validate_commit_message(
                test_commit['message']
            )
            
            if validation_result.is_valid:
                print(f"      ✅ Valid: {validation_result.commit_type} - {validation_result.description}")
                print(f"      📦 Release: {validation_result.release_type.value.upper()}")
                if validation_result.breaking_change:
                    print(f"      ⚠️  Breaking change detected!")
            else:
                print(f"      ❌ Invalid: {', '.join(validation_result.errors)}")
                if validation_result.suggestions:
                    print(f"      💡 Suggestions: {validation_result.suggestions[0]}")
            
            # Show tool output if available
            if validation_result.tool_output:
                print(f"      🔧 Used external tools for validation")
                
        except Exception as e:
            print(f"      ❌ Exception: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Tool-based validation testing completed!")
    print("\n📋 Benefits of using external tools:")
    print("   ✅ Industry-standard validation (commitlint)")
    print("   ✅ Comprehensive rule sets")
    print("   ✅ Configurable validation rules")
    print("   ✅ Integration with semantic-release")
    print("   ✅ Better error messages and suggestions")
    print("   ✅ Community-maintained and battle-tested")
    print("\n💡 Fallback to built-in validation when tools unavailable")


if __name__ == "__main__":
    asyncio.run(test_tool_based_validation())