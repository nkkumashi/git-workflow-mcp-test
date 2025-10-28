#!/usr/bin/env python3
"""Test the workflow-gated PR creation functionality."""

import asyncio
import sys
import os

# Add the parent directory to the path to import our MCP server
sys.path.append('../git-workflow-mcp')

from git_workflow_mcp.server import GitWorkflowMCPServer


async def test_workflow_gated_pr():
    """Test the complete workflow-gated PR creation process."""
    print("🚀 Testing Workflow-Gated PR Creation")
    print("=" * 60)
    
    server = GitWorkflowMCPServer()
    await server._initialize_workflow_engine()
    
    if not server.workflow_engine:
        print("❌ Failed to initialize workflow engine")
        return
    
    if not server.workflow_engine.github_actions:
        print("❌ GitHub Actions integration not available")
        return
    
    print("✅ MCP Server and GitHub Actions integration ready")
    
    # Step 1: List available workflows
    print("\n1️⃣ Discovering available workflows...")
    result = await server.workflow_engine.list_available_workflows()
    if result.data:
        workflows = result.data.get("workflows", [])
        print(f"   Found {len(workflows)} workflows:")
        for workflow in workflows:
            print(f"     - {workflow['name']} ({workflow['state']})")
    
    # Step 2: Check current repository state
    print("\n2️⃣ Checking repository state...")
    result = await server.workflow_engine.validate_repository_state()
    print(f"   Status: {result.status.value}")
    if result.data:
        print(f"   Current branch: {result.data.get('current_branch')}")
        print(f"   Is clean: {result.data.get('is_clean')}")
        print(f"   Uncommitted files: {len(result.data.get('uncommitted_files', []))}")
        print(f"   Untracked files: {len(result.data.get('untracked_files', []))}")
    
    # Step 3: Execute workflow-gated PR creation
    print("\n3️⃣ Creating workflow-gated PR...")
    print("   This will:")
    print("   - Commit the current changes")
    print("   - Create a feature branch")
    print("   - Trigger all GitHub Actions workflows")
    print("   - Wait for all workflows to complete")
    print("   - Create PR only if all workflows pass")
    print("")
    
    # Auto-confirm for testing
    print("   Auto-confirming for testing...")
    response = 'y'
    
    print("\n   🚀 Starting workflow-gated PR creation...")
    print("   ⏳ This may take 1-2 minutes...")
    
    try:
        result = await server.workflow_engine.execute_workflow_gated_pr(
            commit_message="Add test application and update documentation",
            workflows_to_run=["CI", "Lint", "Security"],  # Specify our workflows
            timeout_per_workflow=300  # 5 minutes per workflow
        )
        
        print(f"\n   Status: {result.status.value}")
        print(f"   Message: {result.message}")
        
        if result.status.value == "success":
            print("   🎉 SUCCESS! Workflow-gated PR created!")
            if result.pr_url:
                print(f"   📋 PR URL: {result.pr_url}")
            if result.data:
                print(f"   🔄 Workflows run: {result.data.get('workflows_run', 0)}")
                print(f"   🌿 Branch: {result.data.get('branch_name', 'unknown')}")
        else:
            print("   ❌ FAILED!")
            if result.errors:
                print("   Errors:")
                for error in result.errors:
                    print(f"     - {error}")
            
            # Show workflow results if available
            if result.data and "workflow_results" in result.data:
                print("   Workflow Results:")
                for workflow_result in result.data["workflow_results"]:
                    name = workflow_result["workflow_name"]
                    status = workflow_result["result"].status.value
                    print(f"     - {name}: {status}")
    
    except Exception as e:
        print(f"   ❌ Exception occurred: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Test completed!")


if __name__ == "__main__":
    asyncio.run(test_workflow_gated_pr())