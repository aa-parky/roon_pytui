# CI/CD Setup Checklist

Use this checklist to ensure your CI/CD setup is fully configured and working.

## ✅ Pre-Push Checklist

- [x] All workflow files created in `.github/workflows/`
- [x] Dependabot configuration created
- [x] Issue and PR templates created
- [x] Documentation files created (CONTRIBUTING.md, CI.md)
- [x] Status badges added to README.md
- [x] CLAUDE.md updated with CI information

## 📤 Push to GitHub

```bash
# Review all changes
git status

# Add all CI files
git add .github/ README.md CLAUDE.md CI_SETUP_SUMMARY.md CI_CHECKLIST.md

# Commit with descriptive message
git commit -m "ci: Add comprehensive CI/CD infrastructure

- Add CI workflow for multi-platform testing (Python 3.8-3.12)
- Add code quality workflow (ruff, mypy, security scanning)
- Add PR automation workflow (size labeling, coverage comments)
- Configure Dependabot for automated dependency updates
- Add issue and PR templates
- Add comprehensive documentation (CONTRIBUTING.md, CI.md)
- Add status badges to README.md
- Update CLAUDE.md with CI information"

# Push to GitHub
git push origin main
```

## 🔍 Post-Push Verification

### 1. Check Workflow Runs
- [ ] Go to https://github.com/aa-parky/roon_pytui/actions
- [ ] Verify CI workflow is running or completed
- [ ] Verify Code Quality workflow is running or completed
- [ ] Check that all jobs show green checkmarks

### 2. Review Workflow Results
- [ ] All tests pass on all platforms
- [ ] Coverage is calculated (should show current coverage %)
- [ ] Package builds successfully
- [ ] Linting passes
- [ ] Type checking passes

### 3. Check Status Badges
- [ ] Go to https://github.com/aa-parky/roon_pytui
- [ ] Verify all 5 badges display correctly in README
- [ ] Click each badge to ensure links work
- [ ] Badges show current status (not "unknown" or "error")

### 4. Test PR Workflow
- [ ] Create a test branch: `git checkout -b test/ci-verification`
- [ ] Make a small change (e.g., update a comment)
- [ ] Push branch and open a PR
- [ ] Verify PR workflow runs
- [ ] Check that PR gets:
  - [ ] Size label (probably size/XS)
  - [ ] Summary comment
  - [ ] Coverage comment
- [ ] Close/delete the test PR

## 🔐 Optional: Codecov Setup

### 1. Sign Up for Codecov
- [ ] Go to https://codecov.io
- [ ] Sign in with GitHub
- [ ] Add your repository (aa-parky/roon_pytui)

### 2. Get Token
- [ ] Copy your `CODECOV_TOKEN` from Codecov dashboard
- [ ] Go to GitHub: Settings → Secrets and variables → Actions
- [ ] Click "New repository secret"
- [ ] Name: `CODECOV_TOKEN`
- [ ] Value: Paste your token
- [ ] Click "Add secret"

### 3. Verify Codecov
- [ ] Trigger a workflow run (push to main)
- [ ] Check that coverage uploads successfully
- [ ] View coverage report on Codecov dashboard
- [ ] Verify Codecov badge shows actual coverage percentage

## 🤖 Dependabot Verification

### 1. Enable Dependabot (if not auto-enabled)
- [ ] Go to Settings → Security → Dependabot
- [ ] Ensure "Dependabot alerts" is enabled
- [ ] Ensure "Dependabot security updates" is enabled
- [ ] Ensure "Dependabot version updates" is enabled

### 2. Wait for First Run
- [ ] Dependabot should run on first Monday after setup
- [ ] Check for PRs created by dependabot[bot]
- [ ] Review and merge (or close) Dependabot PRs

## 📋 Issue Template Verification

### 1. Test Bug Report Template
- [ ] Go to Issues → New Issue
- [ ] Verify "Bug Report" template appears
- [ ] Check that template has all sections
- [ ] Cancel (don't create)

### 2. Test Feature Request Template
- [ ] Go to Issues → New Issue
- [ ] Verify "Feature Request" template appears
- [ ] Check that template has all sections
- [ ] Cancel (don't create)

## 📝 PR Template Verification

### 1. Test PR Template
- [ ] Create a test PR (if not done above)
- [ ] Verify PR template auto-fills description
- [ ] Check that checklist appears
- [ ] Verify all sections are present

## 🛠️ Local Testing

### 1. Run All Checks Locally
```bash
# Format code
ruff format .

# Lint
ruff check .

# Type check
mypy src/roon_pytui

# Test with coverage
pytest --cov=roon_pytui --cov-report=html

# Build package
python -m build
twine check dist/*
```

- [ ] All commands run without errors
- [ ] Coverage meets 80% threshold

## 📚 Documentation Review

- [ ] Read through `.github/CONTRIBUTING.md`
- [ ] Read through `.github/CI.md`
- [ ] Verify all commands are correct
- [ ] Check for typos or errors

## 🎯 Success Criteria

Your CI/CD setup is complete when:

- ✅ All workflows run successfully
- ✅ Status badges display correctly
- ✅ PR automation works (size labels, comments)
- ✅ Coverage is tracked and reported
- ✅ Dependabot is enabled and configured
- ✅ All templates work correctly
- ✅ Documentation is accurate and complete

## 🚀 Next Steps

After completing this checklist:

1. **Start Development**
   - Create feature branches
   - Open PRs
   - See automation in action

2. **Monitor Workflows**
   - Check Actions tab regularly
   - Review Dependabot PRs
   - Track coverage trends

3. **Iterate and Improve**
   - Adjust workflows as needed
   - Add more checks if desired
   - Update documentation

## 📞 Troubleshooting

If you encounter issues, refer to:
- `.github/CI.md` - Detailed troubleshooting guide
- `.github/CONTRIBUTING.md` - Development workflow
- GitHub Actions logs - Detailed error messages

## 🎉 Congratulations!

Once all items are checked, your CI/CD infrastructure is fully operational!

---

**Created**: 2025-11-30
**Last Updated**: 2025-11-30
**Status**: Ready for verification
