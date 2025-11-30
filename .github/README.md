# GitHub Configuration

This directory contains GitHub-specific configuration for CI/CD, issue templates, and contribution guidelines.

## Contents

### Workflows (`workflows/`)

| Workflow | File | Purpose | Triggers |
|----------|------|---------|----------|
| CI | `ci.yml` | Test across platforms, coverage, build | Push, PR |
| Code Quality | `code-quality.yml` | Lint, type check, security scan | Push, PR |
| Pull Request | `pr.yml` | PR-specific automation | PR events |

### Issue Templates (`ISSUE_TEMPLATE/`)

- **`bug_report.md`**: Template for reporting bugs
- **`feature_request.md`**: Template for suggesting features

### Templates

- **`pull_request_template.md`**: Default PR template with checklist

### Configuration

- **`dependabot.yml`**: Automated dependency updates
- **`CONTRIBUTING.md`**: Contribution guidelines
- **`CI.md`**: Detailed CI/CD documentation

## Quick Links

- [Contributing Guidelines](CONTRIBUTING.md)
- [CI/CD Documentation](CI.md)
- [Actions Dashboard](../../actions)

## Setup Checklist

After pushing this configuration:

- [ ] Enable GitHub Actions in repository settings
- [ ] Add `CODECOV_TOKEN` secret for coverage reporting (optional)
- [ ] Review and adjust Dependabot settings if needed
- [ ] Verify workflows run successfully
- [ ] Check that badges display correctly in README

## Workflow Status

Check the status of all workflows:
- [CI Workflow](../../actions/workflows/ci.yml)
- [Code Quality Workflow](../../actions/workflows/code-quality.yml)
- [PR Workflow](../../actions/workflows/pr.yml)

## Need Help?

- Review [CI.md](CI.md) for detailed documentation
- Check [CONTRIBUTING.md](CONTRIBUTING.md) for development workflow
- Open an issue if you encounter problems
