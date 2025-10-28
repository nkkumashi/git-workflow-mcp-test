# git-workflow-mcp-test
Test repository for Git Workflow MCP Server

## 🚀 Testing Workflow-Gated PR Creation

This repository demonstrates the Git Workflow MCP Server's ability to:
- Create feature branches automatically
- Trigger GitHub Actions workflows
- Wait for all workflows to complete successfully
- Create pull requests only after all checks pass

## Workflows
- **CI**: Runs tests and builds (~20 seconds)
- **Lint**: Code quality checks (~11 seconds)  
- **Security**: Security audits (~17 seconds)

Total expected time: ~48 seconds

## Recent Updates
- Enhanced CLI to display PR URL when created successfully
- Fixed PR URL propagation from GitHub Actions to CLI output
- Added debug output to track PR URL flow
