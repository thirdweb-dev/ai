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
5. Select "Dry run" option (default: true) to test without publishing
6. Click "Run workflow"

### Testing with Dry Run Mode

The workflow includes a "dry run" option that allows testing the entire release process without publishing to PyPI:

1. When "Dry run" is enabled:
   - A new branch is created with pattern `dry-run/release-{version}-test`
   - Version numbers include a `-test` suffix
   - Tags are prefixed with `dry-run/`
   - Packages are built but not published to PyPI
   - Build artifacts are uploaded to GitHub Actions artifacts
   - A summary report is generated as an artifact

2. Review the dry run results:
   - Check the generated branch and tags
   - Download and inspect the package artifacts
   - Verify version numbers and dependencies are updated correctly
   - Review the summary report

3. When ready for a real release:
   - Run the workflow again with "Dry run" disabled

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

3. **Building and Publishing**
   - Builds thirdweb-ai package
   - In dry run: uploads artifacts
   - In real release: publishes to PyPI
   - Builds thirdweb-mcp package
   - In dry run: uploads artifacts
   - In real release: publishes to PyPI
   - Creates a GitHub release with release notes (real release only)

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
   - Git permission issues

3. For dry run branch cleanup:
   ```bash
   # Delete local dry run branch
   git branch -D dry-run/release-x.y.z-test
   
   # Delete remote dry run branch
   git push origin --delete dry-run/release-x.y.z-test
   
   # Delete dry run tags
   git tag -d dry-run/thirdweb-ai-vx.y.z-test
   git tag -d dry-run/thirdweb-mcp-vx.y.z-test
   git push --delete origin dry-run/thirdweb-ai-vx.y.z-test
   git push --delete origin dry-run/thirdweb-mcp-vx.y.z-test
   ```

For persistent issues, contact the repository maintainers.