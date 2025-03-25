# Publishing Workflow

This document outlines the workflow for simultaneously publishing the `thirdweb-ai` and `thirdweb-mcp` packages to PyPI.

## Overview

The publishing workflow is designed to:
1. Validate both packages
2. Synchronize version numbers
3. Update dependencies
4. Publish packages in the correct order
5. Create GitHub releases

## Workflow Details

### Triggering a Release

1. Go to the GitHub Actions tab in the repository
2. Select the "Publish Both Packages to PyPI" workflow
3. Click "Run workflow"
4. Choose a version increment type:
   - `patch` (e.g., 0.1.4 → 0.1.5) for bug fixes and small changes
   - `minor` (e.g., 0.1.4 → 0.2.0) for new features
   - `major` (e.g., 0.1.4 → 1.0.0) for breaking changes
5. Click "Run workflow"

### Workflow Process

The workflow executes the following steps automatically:

1. **Validation**
   - Runs linting checks (ruff)
   - Performs type checking (pyright)
   - Executes tests for thirdweb-ai

2. **Version Update**
   - Calculates new version numbers based on the selected increment
   - Updates version in `thirdweb-ai/src/thirdweb_ai/__init__.py`
   - Updates version in `thirdweb-mcp/src/mcp.py`
   - Updates the dependency on thirdweb-ai in `thirdweb-mcp/pyproject.toml`
   - Commits these changes to the repository
   - Creates Git tags for both packages

3. **Publishing**
   - Builds and publishes thirdweb-ai to PyPI
   - Waits for successful completion
   - Builds and publishes thirdweb-mcp to PyPI
   - Creates a GitHub release with release notes

## Versioning

Both packages follow [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality that's backward compatible
- **PATCH** version for backward compatible bug fixes

## Dependencies

The `thirdweb-mcp` package depends on `thirdweb-ai` with the `mcp` extra. When versions are updated, this dependency is automatically updated to reference the new version.

## Manual Publishing (Alternative)

If you need to publish the packages separately:

### thirdweb-ai Only
- Use the `publish_pypi_thirdweb_ai.yaml` workflow
- This will trigger on tags matching `thirdweb-ai-v*` or through manual dispatch

### thirdweb-mcp Only
- Use the `publish_pypi_thirdweb_mcp.yaml` workflow 
- This will trigger on tags matching `thirdweb-mcp-v*` or through manual dispatch

### Synchronizing Dependencies
- After publishing thirdweb-ai, the `sync_dependencies.yaml` workflow will automatically:
  - Update the thirdweb-ai dependency in thirdweb-mcp
  - Create a PR for this update

## Troubleshooting

If the workflow fails:

1. Check the GitHub Actions logs for specific error messages
2. Common issues include:
   - Failing tests or linting errors
   - PyPI authentication problems
   - Version conflicts

For persistent issues, contact the repository maintainers.
