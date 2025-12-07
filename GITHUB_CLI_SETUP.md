# GitHub CLI Setup for git-autopush

## What is GitHub CLI?

GitHub CLI (`gh`) is the official command-line tool from GitHub that lets you create and manage repositories without using the web browser.

**With GitHub CLI, git-autopush can:**
✅ Automatically create repositories on GitHub
✅ No manual browser steps needed
✅ Set license automatically
✅ Complete end-to-end automation!

---

## Installation

### Ubuntu/Debian/WSL

```bash
# Method 1: Official repository (recommended)
type -p curl >/dev/null || (sudo apt update && sudo apt install curl -y)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
&& sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
&& sudo apt update \
&& sudo apt install gh -y

# Method 2: From Ubuntu repository (may be older version)
sudo apt install gh
```

### macOS

```bash
brew install gh
```

### Windows

Download from: https://github.com/cli/cli/releases

Or use Chocolatey:
```powershell
choco install gh
```

---

## Authentication

After installing, authenticate with GitHub:

```bash
gh auth login
```

### Interactive Prompts:

```
? What account do you want to log into?
  > GitHub.com

? What is your preferred protocol for Git operations?
  > HTTPS

? Authenticate Git with your GitHub credentials?
  > Yes

? How would you like to authenticate GitHub CLI?
  > Login with a web browser
```

Then:
1. Copy the one-time code shown
2. Press ENTER to open browser
3. Paste the code
4. Authorize GitHub CLI
5. Done!

### Verify Authentication

```bash
gh auth status
```

Should show:
```
✓ Logged in to github.com as jmartinmatias
✓ Git operations for github.com configured to use https protocol.
✓ Token: *******************
```

---

## Using with git-autopush

Once GitHub CLI is installed and authenticated:

```bash
cd /home/xenhp/code/lab/git-autopush
python git_autopush.py
```

### Workflow:

```
[STEP 7/8] Creating GitHub repository and pushing

GitHub Repository Creation
==================================================
✓ GitHub CLI (gh) is installed and authenticated

I can automatically create the repository for you!

Create repository automatically? [Y/n]: y

ℹ Attempting to create repository using GitHub CLI...
  → Running: gh repo create git-autopush --public --license mit --disable-wiki --confirm
✓ Repository created on GitHub: git-autopush

  → Pushing to GitHub...
✓ Successfully pushed to GitHub!

============================================================
  ✓ Successfully pushed to GitHub!
============================================================
```

**No browser needed! Completely automated!** 🚀

---

## Quick Install & Setup

One-line setup for Ubuntu/WSL:

```bash
# Install GitHub CLI
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null && sudo apt update && sudo apt install gh -y

# Authenticate
gh auth login

# Verify
gh auth status

# Use git-autopush
cd ~/code/lab/git-autopush
python git_autopush.py
```

---

## Benefits

### Before (Manual):
1. Run git-autopush
2. **Pause and go to browser**
3. **Navigate to GitHub**
4. **Fill in form**
5. **Click create**
6. **Go back to terminal**
7. Press ENTER
8. Push completes

**Time:** 2-3 minutes

### After (With GitHub CLI):
1. Run git-autopush
2. Press 'y' when asked
3. Done!

**Time:** 10 seconds

---

## Troubleshooting

### "gh: command not found"

GitHub CLI is not installed. Follow installation instructions above.

### "gh auth status" shows not authenticated

Run:
```bash
gh auth login
```

### "failed to create repository"

Possible issues:
- Repository already exists: `gh repo delete username/repo-name` (careful!)
- Invalid repository name: Use lowercase, hyphens, no spaces
- No permission: Check authentication

### Want to see what gh CLI can do?

```bash
gh --help
gh repo --help
gh repo create --help
```

---

## Alternative: Personal Access Token

If you don't want to use GitHub CLI, git-autopush falls back to manual repository creation. You'll need a Personal Access Token for pushing:

1. Go to: https://github.com/settings/tokens
2. Generate new token (classic)
3. Select `repo` scope
4. Use as password when pushing

---

## Summary

**Install GitHub CLI:**
```bash
# Ubuntu/Debian
sudo apt install gh

# macOS
brew install gh
```

**Authenticate:**
```bash
gh auth login
```

**Use git-autopush:**
```bash
cd any-project
python /home/xenhp/code/lab/git-autopush/git_autopush.py
```

**Result:** Completely automated repository creation and push! 🎉

---

**Recommended:** Install GitHub CLI for the best git-autopush experience!
