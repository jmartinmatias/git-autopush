#!/usr/bin/env python3
"""
Git AutoPush - Automatically push projects to GitHub

Checks if a folder is already on GitHub, and if not, handles all the setup:
- Initialize Git repository
- Create .gitignore
- Make initial commit
- Add GitHub remote
- Push to GitHub
- Generate detailed documentation

All with detailed logging and explanations at each step.
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import json


class Colors:
    """ANSI color codes for terminal output"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'

    @staticmethod
    def success(text):
        return f"{Colors.GREEN}✓ {text}{Colors.RESET}"

    @staticmethod
    def error(text):
        return f"{Colors.RED}✗ {text}{Colors.RESET}"

    @staticmethod
    def warning(text):
        return f"{Colors.YELLOW}⚠ {text}{Colors.RESET}"

    @staticmethod
    def info(text):
        return f"{Colors.CYAN}ℹ {text}{Colors.RESET}"

    @staticmethod
    def step(num, total, text):
        return f"{Colors.BOLD}{Colors.BLUE}[STEP {num}/{total}] {text}{Colors.RESET}"


class Logger:
    """Handles both console and file logging"""

    def __init__(self, log_file="autopush.log"):
        self.log_file = log_file
        self.logs = []

    def log(self, message, level="INFO", color_func=None):
        """Log message to both console and file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.logs.append(log_entry)

        # Console output with colors
        if color_func:
            print(color_func(message))
        else:
            print(message)

    def step(self, num, total, text):
        """Log a step header"""
        message = f"STEP {num}/{total}: {text}"
        self.log(message, "STEP", lambda m: Colors.step(num, total, text))

    def success(self, text):
        """Log success message"""
        self.log(text, "SUCCESS", Colors.success)

    def error(self, text):
        """Log error message"""
        self.log(text, "ERROR", Colors.error)

    def warning(self, text):
        """Log warning message"""
        self.log(text, "WARNING", Colors.warning)

    def info(self, text):
        """Log info message"""
        self.log(text, "INFO", Colors.info)

    def detail(self, text):
        """Log detail (indented)"""
        message = f"  → {text}"
        self.log(message, "DETAIL")
        print(f"  → {text}")

    def save(self):
        """Save logs to file"""
        with open(self.log_file, 'w') as f:
            f.write('\n'.join(self.logs))
        print(f"\n{Colors.info(f'Log saved to: {self.log_file}')}")


class GitAutoPush:
    """Main autopush functionality"""

    def __init__(self, target_dir=None):
        self.target_dir = Path(target_dir or os.getcwd()).resolve()
        self.logger = Logger(self.target_dir / "autopush.log")
        self.total_steps = 8
        self.current_step = 0
        self.actions_taken = []

    def run_command(self, cmd, check=True, capture=True):
        """Run shell command and return result"""
        self.logger.detail(f"Running: {cmd}")
        try:
            if capture:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    check=check,
                    capture_output=True,
                    text=True,
                    cwd=self.target_dir
                )
                return result.stdout.strip(), result.returncode
            else:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    check=check,
                    cwd=self.target_dir
                )
                return "", result.returncode
        except subprocess.CalledProcessError as e:
            return e.stderr.strip() if capture else "", e.returncode

    def step(self, text):
        """Log current step"""
        self.current_step += 1
        self.logger.step(self.current_step, self.total_steps, text)

    def check_git_installed(self):
        """Verify Git is installed"""
        self.logger.info("Checking if Git is installed...")
        output, code = self.run_command("git --version")
        if code != 0:
            self.logger.error("Git is not installed!")
            self.logger.detail("Install Git: sudo apt install git (Linux) or https://git-scm.com/downloads")
            return False
        self.logger.detail(f"Found: {output}")
        return True

    def check_is_git_repo(self):
        """Check if current directory is a Git repository"""
        self.step("Checking if folder is a Git repository")
        self.logger.detail("Searching for .git directory...")

        git_dir = self.target_dir / ".git"
        if git_dir.exists():
            self.logger.detail("Found: .git directory exists")
            self.logger.success("This is already a Git repository")
            return True
        else:
            self.logger.detail("Not found: .git directory does not exist")
            self.logger.warning("This is NOT a Git repository")
            return False

    def check_remote_exists(self):
        """Check if GitHub remote is configured"""
        self.step("Checking for GitHub remote connection")
        output, code = self.run_command("git remote -v")

        if code == 0 and output:
            self.logger.detail(f"Remotes found:\n{output}")
            if 'origin' in output and 'github.com' in output:
                # Extract GitHub URL
                for line in output.split('\n'):
                    if 'origin' in line and 'github.com' in line:
                        url = line.split()[1]
                        self.logger.success(f"Already connected to GitHub: {url}")
                        return True, url
            self.logger.warning("Remote exists but not GitHub origin")
            return False, None
        else:
            self.logger.detail("No remotes configured")
            self.logger.warning("Not connected to any remote")
            return False, None

    def check_uncommitted_changes(self):
        """Check if there are uncommitted changes"""
        output, code = self.run_command("git status --porcelain")
        if output:
            self.logger.detail(f"Found uncommitted changes:\n{output}")
            return True
        return False

    def initialize_git(self):
        """Initialize Git repository"""
        self.step("Initializing Git repository")
        self.logger.detail("Running: git init")

        output, code = self.run_command("git init")
        if code == 0:
            self.logger.success("Git repository initialized")
            self.actions_taken.append("Initialized Git repository with `git init`")

            # Rename to main
            self.logger.detail("Renaming default branch to 'main'")
            self.run_command("git branch -m main")
            self.logger.success("Default branch set to 'main'")
            self.actions_taken.append("Set default branch to 'main'")
            return True
        else:
            self.logger.error(f"Failed to initialize Git: {output}")
            return False

    def create_gitignore(self):
        """Create .gitignore file"""
        self.step("Creating .gitignore file")

        gitignore_path = self.target_dir / ".gitignore"

        if gitignore_path.exists():
            self.logger.info(".gitignore already exists")
            # Add autopush files to existing .gitignore
            with open(gitignore_path, 'r') as f:
                content = f.read()

            additions = []
            if 'autopush.log' not in content:
                additions.append('autopush.log')
            if 'AUTOPUSH_GUIDE.pdf' not in content:
                additions.append('AUTOPUSH_GUIDE.pdf')

            if additions:
                with open(gitignore_path, 'a') as f:
                    f.write('\n# Git AutoPush generated files\n')
                    for item in additions:
                        f.write(f'{item}\n')
                self.logger.success(f"Added {', '.join(additions)} to .gitignore")
                self.actions_taken.append(f"Updated .gitignore to exclude {', '.join(additions)}")
            return True

        # Create new .gitignore from template
        template_path = Path(__file__).parent / "templates" / "default_gitignore.txt"

        if template_path.exists():
            with open(template_path, 'r') as f:
                template = f.read()
        else:
            # Default template
            template = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*~

# OS
.DS_Store
Thumbs.db

# Git AutoPush
autopush.log
AUTOPUSH_GUIDE.pdf
"""

        with open(gitignore_path, 'w') as f:
            f.write(template)

        self.logger.success("Created .gitignore file")
        self.logger.detail(f"Location: {gitignore_path}")
        self.actions_taken.append("Created .gitignore file from template")
        return True

    def make_initial_commit(self):
        """Create initial commit"""
        self.step("Making initial commit")

        # Stage all files
        self.logger.detail("Staging all files...")
        self.run_command("git add .")

        # Check what's staged
        output, _ = self.run_command("git diff --cached --name-only")
        files = output.split('\n') if output else []
        self.logger.detail(f"Staged {len(files)} files")

        # Commit
        commit_message = f"Initial commit: {self.target_dir.name}"
        self.logger.detail(f"Creating commit: '{commit_message}'")

        output, code = self.run_command(f'git commit -m "{commit_message}"')

        if code == 0:
            self.logger.success("Initial commit created")
            self.actions_taken.append(f"Created initial commit with message: '{commit_message}'")
            return True
        else:
            self.logger.error(f"Failed to commit: {output}")
            return False

    def get_github_info(self):
        """Get GitHub repository information from user"""
        self.step("Getting GitHub repository information")

        print(f"\n{Colors.BOLD}GitHub Repository Setup{Colors.RESET}")
        print("=" * 50)

        # Get username
        username = input(f"{Colors.CYAN}GitHub username: {Colors.RESET}").strip()
        if not username:
            self.logger.error("Username is required")
            return None

        # Get repo name (default to folder name)
        default_repo = self.target_dir.name
        repo_name = input(f"{Colors.CYAN}Repository name [{default_repo}]: {Colors.RESET}").strip()
        if not repo_name:
            repo_name = default_repo

        # License choice
        print(f"\n{Colors.CYAN}Choose a license:{Colors.RESET}")
        print("  1. MIT (recommended - most permissive)")
        print("  2. Apache 2.0 (permissive with patent grant)")
        print("  3. GPL v3 (copyleft - derivatives must be open source)")
        print("  4. None (no license)")

        license_choice = input(f"{Colors.CYAN}License [1]: {Colors.RESET}").strip() or "1"
        license_map = {
            "1": "MIT",
            "2": "Apache-2.0",
            "3": "GPL-3.0",
            "4": None
        }
        license_type = license_map.get(license_choice, "MIT")

        info = {
            'username': username,
            'repo_name': repo_name,
            'license': license_type,
            'url': f"https://github.com/{username}/{repo_name}.git"
        }

        self.logger.detail(f"Repository: {username}/{repo_name}")
        self.logger.detail(f"URL: {info['url']}")
        self.logger.detail(f"License: {license_type or 'None'}")

        return info

    def add_remote(self, github_info):
        """Add GitHub remote"""
        self.step("Adding GitHub remote")

        # Check if remote already exists
        output, _ = self.run_command("git remote -v")
        if 'origin' in output:
            self.logger.warning("Remote 'origin' already exists")
            # Remove it
            self.logger.detail("Removing existing remote...")
            self.run_command("git remote remove origin")

        # Add new remote
        self.logger.detail(f"Adding remote: {github_info['url']}")
        output, code = self.run_command(f"git remote add origin {github_info['url']}")

        if code == 0:
            self.logger.success(f"Remote 'origin' added: {github_info['url']}")
            self.actions_taken.append(f"Added GitHub remote: {github_info['url']}")

            # Verify
            output, _ = self.run_command("git remote -v")
            self.logger.detail(f"Verification:\n{output}")
            return True
        else:
            self.logger.error(f"Failed to add remote: {output}")
            return False

    def check_gh_cli(self):
        """Check if GitHub CLI is installed and authenticated"""
        # Check if gh is installed
        output, code = self.run_command("gh --version", check=False)
        if code != 0:
            return False, "not_installed"

        # Check if authenticated
        output, code = self.run_command("gh auth status", check=False)
        if code != 0:
            return False, "not_authenticated"

        return True, "authenticated"

    def create_repo_with_gh_cli(self, github_info):
        """Create GitHub repository using GitHub CLI"""
        self.logger.info("Attempting to create repository using GitHub CLI...")

        # Build gh repo create command
        cmd = f"gh repo create {github_info['repo_name']} --public"

        # Add license if specified
        if github_info['license']:
            # Map license names to gh CLI format
            license_map = {
                'MIT': 'mit',
                'Apache-2.0': 'apache-2.0',
                'GPL-3.0': 'gpl-3.0'
            }
            license_arg = license_map.get(github_info['license'])
            if license_arg:
                cmd += f" --license {license_arg}"

        # Don't clone, don't add README/gitignore (we have them)
        cmd += " --disable-wiki --confirm"

        self.logger.detail(f"Running: {cmd}")
        output, code = self.run_command(cmd, check=False)

        if code == 0:
            self.logger.success(f"Repository created on GitHub: {github_info['repo_name']}")
            self.actions_taken.append(f"Created GitHub repository using gh CLI")

            # Update remote URL to use the created repo
            repo_url = f"https://github.com/{github_info['username']}/{github_info['repo_name']}.git"
            self.run_command("git remote remove origin", check=False)
            self.run_command(f"git remote add origin {repo_url}")

            return True
        else:
            self.logger.warning(f"Failed to create repository with gh CLI: {output}")
            return False

    def push_to_github(self, github_info):
        """Push to GitHub"""
        self.step("Creating GitHub repository and pushing")

        # Try GitHub CLI first
        gh_available, gh_status = self.check_gh_cli()

        if gh_available and gh_status == "authenticated":
            self.logger.success("GitHub CLI detected and authenticated!")

            # Ask if user wants to use it
            print(f"\n{Colors.BOLD}GitHub Repository Creation{Colors.RESET}")
            print("=" * 50)
            print(f"{Colors.GREEN}✓ GitHub CLI (gh) is installed and authenticated{Colors.RESET}")
            print(f"\nI can automatically create the repository for you!")
            print()

            choice = input(f"{Colors.CYAN}Create repository automatically? [Y/n]: {Colors.RESET}").strip().lower()

            if choice in ('', 'y', 'yes'):
                if self.create_repo_with_gh_cli(github_info):
                    # Repository created successfully, proceed to push
                    self.push_changes(github_info)
                    return True
                else:
                    # Fall back to manual creation
                    self.logger.warning("Falling back to manual repository creation")
                    self.manual_repo_creation_instructions(github_info)
                    self.push_changes(github_info)
                    return True
            else:
                # User chose manual creation
                self.manual_repo_creation_instructions(github_info)
                self.push_changes(github_info)
                return True

        elif gh_available and gh_status == "not_authenticated":
            # gh is installed but not authenticated
            print(f"\n{Colors.BOLD}GitHub CLI Detected{Colors.RESET}")
            print("=" * 50)
            print(f"{Colors.YELLOW}⚠ GitHub CLI (gh) is installed but not authenticated{Colors.RESET}")
            print(f"\nTo enable automatic repository creation:")
            print(f"  1. Run: {Colors.CYAN}gh auth login{Colors.RESET}")
            print(f"  2. Follow the prompts to authenticate")
            print(f"  3. Run git-autopush again")
            print()

            choice = input(f"{Colors.CYAN}Authenticate now? [y/N]: {Colors.RESET}").strip().lower()

            if choice in ('y', 'yes'):
                self.logger.info("Launching GitHub CLI authentication...")
                self.run_command("gh auth login", check=False, capture=False)

                # Check if authentication succeeded
                gh_available, gh_status = self.check_gh_cli()
                if gh_available and gh_status == "authenticated":
                    if self.create_repo_with_gh_cli(github_info):
                        self.push_changes(github_info)
                        return True
                    else:
                        self.manual_repo_creation_instructions(github_info)
                        self.push_changes(github_info)
                        return True
                else:
                    self.logger.warning("Authentication unsuccessful, using manual creation")
                    self.manual_repo_creation_instructions(github_info)
                    self.push_changes(github_info)
                    return True
            else:
                self.manual_repo_creation_instructions(github_info)
                self.push_changes(github_info)
                return True

        else:
            # gh CLI not installed
            print(f"\n{Colors.BOLD}GitHub CLI Not Installed{Colors.RESET}")
            print("=" * 50)
            print(f"{Colors.YELLOW}⚠ GitHub CLI (gh) is not installed{Colors.RESET}")
            print(f"\nFor automatic repository creation, install GitHub CLI:")
            print(f"  Ubuntu/Debian: {Colors.CYAN}sudo apt install gh{Colors.RESET}")
            print(f"  macOS: {Colors.CYAN}brew install gh{Colors.RESET}")
            print(f"  Or visit: {Colors.CYAN}https://cli.github.com/{Colors.RESET}")
            print(f"\nContinuing with manual repository creation...")
            print()

            self.manual_repo_creation_instructions(github_info)
            self.push_changes(github_info)
            return True

    def push_changes(self, github_info):
        """Push changes to GitHub"""
        # Set merge strategy
        self.logger.detail("Setting pull strategy to merge")
        self.run_command("git config pull.rebase false")

        # Pull license if added
        if github_info['license']:
            self.logger.detail("Pulling LICENSE file from GitHub...")
            output, code = self.run_command("git pull origin main --allow-unrelated-histories", check=False)
            if code == 0:
                self.logger.success("Pulled LICENSE from GitHub")
                self.actions_taken.append("Pulled LICENSE file from GitHub and merged")
            else:
                self.logger.warning(f"Pull returned: {output}")

        # Push
        self.logger.detail("Pushing to GitHub...")
        output, code = self.run_command("git push -u origin main", check=False, capture=False)

        if code == 0:
            self.logger.success("Successfully pushed to GitHub!")
            self.actions_taken.append("Pushed all commits to GitHub")
            return True
        else:
            self.logger.error("Failed to push to GitHub")
            self.logger.detail("Common issues:")
            self.logger.detail("- Using GitHub password instead of Personal Access Token")
            self.logger.detail("- Repository doesn't exist on GitHub")
            self.logger.detail("- Network connectivity issues")
            return False

    def manual_repo_creation_instructions(self, github_info):
        """Show manual repository creation instructions"""
        print(f"\n{Colors.BOLD}Manual GitHub Repository Setup{Colors.RESET}")
        print("=" * 50)
        print(f"Please create the repository manually:")
        print(f"\n1. Go to: {Colors.CYAN}https://github.com/new{Colors.RESET}")
        print(f"2. Repository name: {Colors.GREEN}{github_info['repo_name']}{Colors.RESET}")
        print(f"3. Options:")
        print(f"   {Colors.RED}☐ Don't{Colors.RESET} check 'Add a README file'")
        print(f"   {Colors.RED}☐ Don't{Colors.RESET} check 'Add .gitignore'")
        if github_info['license']:
            print(f"   {Colors.GREEN}☑{Colors.RESET} Choose a license: {Colors.GREEN}{github_info['license']}{Colors.RESET}")
        else:
            print(f"   {Colors.YELLOW}☐{Colors.RESET} Choose a license: None")
        print(f"4. Click 'Create repository'")
        print()

        input(f"{Colors.CYAN}Press ENTER when you've created the repository on GitHub...{Colors.RESET}")

    def generate_documentation(self, github_info):
        """Generate detailed documentation of what was done"""
        self.logger.info("Generating documentation...")

        doc_content = f"""# Git AutoPush Report

**Project:** {self.target_dir.name}
**Location:** {self.target_dir}
**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**GitHub Repository:** https://github.com/{github_info['username']}/{github_info['repo_name']}

---

## Summary

This document explains all the steps taken to push this project to GitHub.

---

## Actions Taken

"""
        for i, action in enumerate(self.actions_taken, 1):
            doc_content += f"{i}. {action}\n"

        doc_content += f"""

---

## Detailed Explanation of Each Action

### 1. Git Repository Initialization

**Command:** `git init`

**What it does:**
- Creates a hidden `.git` folder in your project directory
- This folder stores all version control information
- Marks the folder as a Git repository

**Why needed:**
Git needs this folder to track changes to your files over time.

**Branch renamed to 'main':**
- Modern Git uses 'main' instead of 'master' as the default branch name
- A branch is a timeline of commits (snapshots of your code)

### 2. .gitignore File Creation

**What it is:**
A configuration file that tells Git which files to ignore.

**Why needed:**
Some files shouldn't be tracked:
- `__pycache__/` - Python's compiled bytecode (regenerated automatically)
- `venv/` - Virtual environment (too large, user-specific)
- `autopush.log` - Log files (generated, not source code)
- `*.pdf` - Generated documents (if from source)

**Content:**
Your .gitignore file excludes common temporary and generated files.

### 3. Initial Commit

**Command:** `git commit -m "Initial commit: {self.target_dir.name}"`

**What it does:**
- Creates a snapshot of all your files at this moment
- Assigns it a unique ID (hash)
- Records who made the commit and when
- Adds a message describing the commit

**Technical details:**
- All files were first staged with `git add .`
- Staging area = files ready to be committed
- Commit = permanent snapshot in Git history

**Commit message:**
- "Initial commit" indicates this is the first snapshot
- Good messages help you understand project history

### 4. GitHub Remote Added

**Command:** `git remote add origin {github_info['url']}`

**What it does:**
- Creates a link named 'origin' pointing to your GitHub repository
- This tells Git where to push/pull from

**Technical terms:**
- **Remote** = A reference to a repository on another computer (GitHub's servers)
- **origin** = Standard name for the primary remote
- You can have multiple remotes (origin, upstream, etc.)

**Verification:**
You can see all remotes with: `git remote -v`

### 5. GitHub Repository Created

**Manual step on GitHub website:**
1. Created repository: {github_info['repo_name']}
2. Selected license: {github_info['license'] or 'None'}
3. Did NOT add README or .gitignore (we have them locally)

**Why manually:**
Creating repos requires authentication and permissions that are easier to handle via web interface.

**License added:**
- {github_info['license'] or 'No license'} gives legal permission for others to use your code
- GitHub automatically creates a LICENSE file
"""

        if github_info['license']:
            doc_content += f"""
### 6. Pulled LICENSE from GitHub

**Command:** `git pull origin main --allow-unrelated-histories`

**What it does:**
- Downloads the LICENSE file from GitHub
- Merges it with your local code
- Creates a merge commit combining both histories

**Why needed:**
GitHub has commits (LICENSE) that your local repository doesn't have.
You need to synchronize before pushing.

**Technical details:**
- `pull` = `fetch` (download) + `merge` (combine)
- `--allow-unrelated-histories` - Merges two repos with no common ancestor
- Only needed when combining separate histories for the first time
"""

        doc_content += f"""
### 7. Pushed to GitHub

**Command:** `git push -u origin main`

**What it does:**
- Uploads your local commits to GitHub
- Sets up tracking between local 'main' and remote 'main'

**Breaking it down:**
- `push` - Send commits to remote repository
- `-u` - Set upstream tracking (only needed first time)
- `origin` - The remote name (your GitHub repo)
- `main` - The branch name

**Authentication:**
- Username: {github_info['username']}
- Password: Personal Access Token (not GitHub password!)

**After first push:**
Future pushes are simpler: just `git push` (Git remembers where to push)

---

## Git Workflow Going Forward

### Daily Development Cycle

1. **Make changes** to your code
   ```bash
   # Edit files with your editor
   ```

2. **Check status**
   ```bash
   git status
   ```
   Shows what files changed.

3. **Review changes**
   ```bash
   git diff filename.py
   ```
   Shows exactly what changed in files.

4. **Stage changes**
   ```bash
   git add .              # Stage all changes
   git add file1.py       # Stage specific file
   ```

5. **Commit changes**
   ```bash
   git commit -m "Add feature X"
   ```
   Create a snapshot with descriptive message.

6. **Push to GitHub**
   ```bash
   git push
   ```
   Upload your commits to GitHub.

### Example Session

```bash
# Navigate to project
cd {self.target_dir}

# Make changes
nano README.md

# Check what changed
git status
git diff README.md

# Stage and commit
git add README.md
git commit -m "Update README with new examples"

# Push to GitHub
git push

# Done! Your changes are now on GitHub
```

---

## Understanding Key Concepts

### Repository (Repo)
A folder that Git is tracking. Contains:
- Your actual files (working directory)
- .git folder (Git's database of all history)

### Commit
A snapshot of your project at a specific moment in time.
- Has unique ID (SHA hash like a3f5b2c...)
- Contains: author, timestamp, message, file contents
- Forms a chain (each commit points to its parent)

### Branch
An independent line of development.
- `main` - The primary stable branch
- Feature branches for experimental work
- You can have multiple branches and switch between them

### Remote
A link to a repository on another computer.
- `origin` - Your GitHub repository
- Lets you push (upload) and pull (download) changes

### Staging Area
A middle ground between your working files and repository.
- Lets you choose exactly what to commit
- Stage with `git add`
- Commit stages files, not all changed files

### HEAD
A pointer to your current position in the commit history.
- Usually points to the latest commit on your current branch
- Moves forward when you make new commits

---

## Common Git Commands

```bash
# Check status
git status

# View commit history
git log
git log --oneline

# See changes
git diff                    # Unstaged changes
git diff --cached           # Staged changes

# Stage files
git add filename.py         # Specific file
git add .                   # All changes

# Commit
git commit -m "message"     # With inline message
git commit                  # Opens editor for message

# Push/Pull
git push                    # Upload to GitHub
git pull                    # Download from GitHub

# Branches
git branch                  # List branches
git branch feature-x        # Create branch
git checkout feature-x      # Switch to branch
git checkout -b feature-x   # Create and switch

# Remotes
git remote -v               # List remotes
git remote add name url     # Add remote
git remote remove name      # Remove remote

# Undo changes
git checkout -- file.py     # Discard changes to file
git reset HEAD file.py      # Unstage file
git reset --soft HEAD~1     # Undo last commit (keep changes)
```

---

## Your Project Details

**Local path:** {self.target_dir}
**GitHub URL:** https://github.com/{github_info['username']}/{github_info['repo_name']}
**Remote name:** origin
**Branch:** main
**License:** {github_info['license'] or 'None'}

**Git configuration:**
```bash
# View your Git identity
git config user.name
git config user.email

# View this project's Git config
git config --list
```

---

## Troubleshooting

### Authentication Failed
**Problem:** Can't push to GitHub

**Solution:**
1. Make sure you're using a Personal Access Token, not your password
2. Create token at: https://github.com/settings/tokens
3. Select `repo` scope
4. Use token as password when pushing

### Merge Conflicts
**Problem:** Git can't automatically merge changes

**Solution:**
```bash
# Pull changes first
git pull

# If conflict, Git marks conflict areas in files
# Edit files to resolve conflicts
# Stage resolved files
git add .

# Complete merge
git commit
```

### Accidentally Committed Large File
**Problem:** Pushed a large file that should be ignored

**Solution:**
```bash
# Add to .gitignore
echo "largefile.zip" >> .gitignore

# Remove from Git but keep locally
git rm --cached largefile.zip

# Commit the removal
git commit -m "Remove large file from Git"
git push
```

---

## Next Steps

1. **Continue developing** - Make changes, commit often
2. **Use meaningful commit messages** - Future you will thank you
3. **Push regularly** - Don't wait too long between pushes
4. **Learn branching** - Use feature branches for new features
5. **Explore GitHub** - Issues, Pull Requests, Actions, Pages

---

## Resources

**Git Documentation:**
- Official docs: https://git-scm.com/doc
- Interactive tutorial: https://learngitbranching.js.org/

**GitHub:**
- Guides: https://guides.github.com/
- Personal Access Tokens: https://github.com/settings/tokens

**This Project:**
- Repository: https://github.com/{github_info['username']}/{github_info['repo_name']}
- View commits: https://github.com/{github_info['username']}/{github_info['repo_name']}/commits/main
- View code: https://github.com/{github_info['username']}/{github_info['repo_name']}/tree/main

---

**Generated by Git AutoPush on {datetime.now().strftime("%Y-%m-%d at %H:%M:%S")}**
"""

        # Save markdown
        md_path = self.target_dir / "AUTOPUSH_GUIDE.md"
        with open(md_path, 'w') as f:
            f.write(doc_content)
        self.logger.success(f"Documentation saved: {md_path}")

        # Convert to PDF using md2pdf if available
        md2pdf_script = Path(__file__).parent.parent / "md2pdf" / "md2pdf.py"
        if md2pdf_script.exists():
            self.logger.detail("Converting to PDF...")
            pdf_path = self.target_dir / "AUTOPUSH_GUIDE.pdf"
            cmd = f"python {md2pdf_script} {md_path} {pdf_path}"
            output, code = self.run_command(cmd, check=False)
            if code == 0:
                self.logger.success(f"PDF generated: {pdf_path}")
            else:
                self.logger.warning("PDF conversion failed (md2pdf not available)")

        return md_path

    def run(self):
        """Main execution flow"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}   Git AutoPush - Automatic GitHub Repository Setup{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

        self.logger.info(f"Target directory: {self.target_dir}")
        self.logger.info(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Check Git is installed
        if not self.check_git_installed():
            return False

        print()

        # Step 1: Check if Git repo
        is_repo = self.check_is_git_repo()
        print()

        if not is_repo:
            # Initialize Git
            if not self.initialize_git():
                return False
            print()

        # Step 2: Check for remote
        has_remote, remote_url = self.check_remote_exists()
        print()

        if has_remote:
            self.logger.info(f"Project is already on GitHub: {remote_url}")
            print(f"\n{Colors.GREEN}{'='*60}{Colors.RESET}")
            print(f"{Colors.GREEN}  ✓ This project is already on GitHub!{Colors.RESET}")
            print(f"{Colors.GREEN}{'='*60}{Colors.RESET}\n")
            print(f"Repository URL: {Colors.CYAN}{remote_url}{Colors.RESET}")
            print(f"\nNo action needed. Use normal Git workflow:")
            print(f"  {Colors.YELLOW}git add .{Colors.RESET}")
            print(f"  {Colors.YELLOW}git commit -m \"message\"{Colors.RESET}")
            print(f"  {Colors.YELLOW}git push{Colors.RESET}")
            return True

        # Step 3: Create .gitignore
        self.create_gitignore()
        print()

        # Step 4: Check for uncommitted changes
        if is_repo and self.check_uncommitted_changes():
            self.logger.warning("Found uncommitted changes")
            self.make_initial_commit()
            print()
        elif not is_repo:
            # Make initial commit
            self.make_initial_commit()
            print()

        # Step 5: Get GitHub info
        github_info = self.get_github_info()
        if not github_info:
            return False
        print()

        # Step 6: Add remote
        if not self.add_remote(github_info):
            return False
        print()

        # Step 7: Push to GitHub
        if not self.push_to_github(github_info):
            self.logger.warning("Push failed - you may need to complete manually")
        print()

        # Step 8: Generate documentation
        self.generate_documentation(github_info)
        print()

        # Save logs
        self.logger.save()

        # Success summary
        print(f"\n{Colors.GREEN}{'='*60}{Colors.RESET}")
        print(f"{Colors.GREEN}  ✓ Successfully pushed to GitHub!{Colors.RESET}")
        print(f"{Colors.GREEN}{'='*60}{Colors.RESET}\n")
        print(f"Repository: {Colors.CYAN}https://github.com/{github_info['username']}/{github_info['repo_name']}{Colors.RESET}")
        print(f"Documentation: {Colors.CYAN}AUTOPUSH_GUIDE.md{Colors.RESET}")
        print(f"Log file: {Colors.CYAN}autopush.log{Colors.RESET}")
        print()

        return True


def main():
    """Entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Automatically push a project to GitHub",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Push current directory
  python git_autopush.py

  # Push specific directory
  python git_autopush.py /path/to/project

  # Run from anywhere
  cd /path/to/your/project
  python /path/to/git_autopush.py
        """
    )
    parser.add_argument(
        'target_dir',
        nargs='?',
        default=None,
        help='Target directory (default: current directory)'
    )

    args = parser.parse_args()

    autopush = GitAutoPush(args.target_dir)
    success = autopush.run()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
