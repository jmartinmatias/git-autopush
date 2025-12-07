# Git AutoPush - Automatic GitHub Repository Setup

Automatically check if your project is on GitHub, and if not, handle all the setup with detailed explanations at each step.

## What It Does

Git AutoPush automates the entire process of pushing a project to GitHub:

1. ✅ **Checks if folder is a Git repository**
2. ✅ **Checks if already connected to GitHub**
3. ✅ **Initializes Git if needed**
4. ✅ **Creates .gitignore from template**
5. ✅ **Makes initial commit**
6. ✅ **Adds GitHub remote**
7. ✅ **Pushes to GitHub**
8. ✅ **Generates detailed documentation** (MD + PDF)
9. ✅ **Logs every step with explanations**

All with color-coded output and detailed logging!

## Features

### Intelligent Detection
- Detects if folder is already a Git repository
- Checks for existing GitHub remote
- Handles uncommitted changes
- Skips unnecessary steps

### Detailed Logging
- Color-coded console output
- Timestamped log file (`autopush.log`)
- Explains what each command does
- Technical but beginner-friendly

### Auto-Documentation
- Generates `AUTOPUSH_GUIDE.md` explaining everything
- Converts to PDF automatically
- Includes complete Git workflow guide
- Lists all actions taken

### Smart .gitignore
- Uses template for Python projects
- Automatically excludes:
  - Python cache files
  - Virtual environments
  - IDE files
  - OS files
  - Generated logs and PDFs

## Quick Start

### Option 1: From Any Directory

```bash
cd /path/to/your/project
python /home/xenhp/code/lab/git-autopush/git_autopush.py
```

### Option 2: Specify Target Directory

```bash
python /home/xenhp/code/lab/git-autopush/git_autopush.py /path/to/project
```

### Option 3: Make It Executable

```bash
chmod +x /home/xenhp/code/lab/git-autopush/git_autopush.py
/home/xenhp/code/lab/git-autopush/git_autopush.py
```

## Usage

### Interactive Prompts

The script will ask you:

```
GitHub username: jmartinmatias
Repository name [project-name]: my-awesome-project
Choose a license:
  1. MIT (recommended - most permissive)
  2. Apache 2.0 (permissive with patent grant)
  3. GPL v3 (copyleft - derivatives must be open source)
  4. None (no license)
License [1]: 1
```

Then it will:
1. Initialize Git (if needed)
2. Create .gitignore
3. Commit all files
4. Guide you to create GitHub repository
5. Push to GitHub
6. Generate documentation

### Example Session

```bash
$ cd ~/code/my-new-project
$ python ~/code/lab/git-autopush/git_autopush.py

============================================================
   Git AutoPush - Automatic GitHub Repository Setup
============================================================

[STEP 1/8] Checking if folder is a Git repository
  → Searching for .git directory...
  → Not found: .git directory does not exist
⚠ This is NOT a Git repository

[STEP 2/8] Initializing Git repository
  → Running: git init
  → Renaming default branch to 'main'
✓ Git repository initialized
✓ Default branch set to 'main'

[STEP 3/8] Creating .gitignore file
  → Location: /home/user/code/my-new-project/.gitignore
✓ Created .gitignore file

[STEP 4/8] Making initial commit
  → Staging all files...
  → Staged 15 files
  → Creating commit: 'Initial commit: my-new-project'
✓ Initial commit created

[STEP 5/8] Getting GitHub repository information

GitHub Repository Setup
==================================================
GitHub username: jmartinmatias
Repository name [my-new-project]:
License [1]: 1

[STEP 6/8] Adding GitHub remote
  → Adding remote: https://github.com/jmartinmatias/my-new-project.git
✓ Remote 'origin' added

[STEP 7/8] Pushing to GitHub

Important: GitHub Repository Setup
==================================================
Before pushing, you need to create the repository on GitHub:
1. Go to: https://github.com/new
2. Repository name: my-new-project
3. Options:
   ☐ Don't check 'Add a README file'
   ☐ Don't check 'Add .gitignore'
   ☑ Choose a license: MIT
4. Click 'Create repository'

Press ENTER when you've created the repository...

✓ Successfully pushed to GitHub!

ℹ Generating documentation...
✓ Documentation saved: AUTOPUSH_GUIDE.md
✓ PDF generated: AUTOPUSH_GUIDE.pdf

============================================================
  ✓ Successfully pushed to GitHub!
============================================================

Repository: https://github.com/jmartinmatias/my-new-project
Documentation: AUTOPUSH_GUIDE.md
Log file: autopush.log
```

## Output Files

### autopush.log
Detailed timestamped log of all operations:

```
[2024-12-07 19:00:00] [INFO] Target directory: /home/user/project
[2024-12-07 19:00:01] [STEP] STEP 1/8: Checking if folder is a Git repository
[2024-12-07 19:00:01] [DETAIL]   → Searching for .git directory...
[2024-12-07 19:00:01] [SUCCESS] Git repository initialized
...
```

**Note:** Automatically excluded from Git via .gitignore

### AUTOPUSH_GUIDE.md
Comprehensive documentation including:
- Summary of all actions taken
- Detailed explanation of each step
- Git workflow guide for continuing development
- Common Git commands reference
- Troubleshooting section
- Links to resources

### AUTOPUSH_GUIDE.pdf
PDF version of the guide (generated using md2pdf if available)

**Note:** Automatically excluded from Git via .gitignore

## How It Works

### Detection Logic

```
Is .git folder present?
  ├─ NO → Initialize Git repository
  └─ YES → Already a Git repo
         │
         Is remote 'origin' configured?
           ├─ NO → Need to add remote
           └─ YES → Is it GitHub?
                  ├─ NO → Not a GitHub remote
                  └─ YES → Already on GitHub! (done)
```

### Step-by-Step Process

1. **Check Git Installation**
   - Verifies `git` command is available
   - Shows version information

2. **Check Repository Status**
   - Looks for `.git` directory
   - Checks for remote configuration
   - Detects uncommitted changes

3. **Initialize Git (if needed)**
   - Runs `git init`
   - Renames branch to `main`
   - Logs what happened and why

4. **Create .gitignore**
   - Uses template from `templates/default_gitignore.txt`
   - Excludes common unnecessary files
   - Adds autopush-generated files to ignore list

5. **Make Initial Commit**
   - Stages all files with `git add .`
   - Creates commit with project name
   - Records author and timestamp

6. **Get GitHub Information**
   - Prompts for username
   - Suggests repository name (folder name)
   - Offers license choices
   - Builds GitHub URL

7. **Add Remote**
   - Runs `git remote add origin <url>`
   - Verifies remote was added
   - Logs the GitHub URL

8. **Push to GitHub**
   - Guides user to create GitHub repository
   - Pulls LICENSE if selected
   - Pushes with `git push -u origin main`
   - Handles authentication

9. **Generate Documentation**
   - Creates detailed MD file
   - Converts to PDF (if md2pdf available)
   - Documents every action taken

## Technical Details

### Requirements

- **Git:** Must be installed and in PATH
- **Python 3.6+:** For running the script
- **md2pdf:** Optional, for PDF generation

### Dependencies

None! This script uses only Python standard library:
- `subprocess` - Running Git commands
- `pathlib` - File system operations
- `datetime` - Timestamps
- `json` - Data handling (not currently used but available)

### Color Codes

Uses ANSI escape codes for terminal colors:
- 🟢 Green: Success messages
- 🔴 Red: Error messages
- 🟡 Yellow: Warning messages
- 🔵 Blue: Step headers
- 🔵 Cyan: Information

### Command Execution

All Git commands are executed via `subprocess.run()`:
- `capture_output=True` - Captures stdout/stderr
- `text=True` - Returns strings, not bytes
- `cwd=target_dir` - Runs in project directory
- `check=False` - Doesn't raise exception on failure (we handle it)

### Error Handling

- Checks return codes of all Git commands
- Provides helpful error messages
- Suggests solutions for common problems
- Continues where possible, fails gracefully when not

## Comparison with Manual Process

### Manual Process (12 steps)

```bash
# 1. Check if Git repo
ls -la .git

# 2. Initialize
git init
git branch -m main

# 3. Create .gitignore
nano .gitignore
# ... type content ...

# 4. Stage files
git add .

# 5. Commit
git commit -m "Initial commit"

# 6. Go to GitHub website
# Click through UI to create repository

# 7. Copy repository URL

# 8. Add remote
git remote add origin https://github.com/user/repo.git

# 9. Pull license
git config pull.rebase false
git pull origin main --allow-unrelated-histories

# 10. Push
git push -u origin main
# Enter username and token

# 11. Create documentation
nano README.md
# ... explain what you did ...

# 12. Commit documentation
git add README.md
git commit -m "Add documentation"
git push
```

**Time:** 10-15 minutes

### With Git AutoPush (1 command)

```bash
python git_autopush.py
```

Answer 3 questions, press ENTER once, enter GitHub credentials.

**Time:** 2-3 minutes

**Bonus:** Automatically generates complete documentation explaining every step!

## Use Cases

### 1. New Project

```bash
mkdir my-new-app
cd my-new-app
# ... create some files ...
python ~/code/lab/git-autopush/git_autopush.py
```

### 2. Existing Project (No Git)

```bash
cd ~/old-project-without-git
python ~/code/lab/git-autopush/git_autopush.py
```

### 3. Git Repo (No GitHub)

```bash
cd ~/local-git-repo
python ~/code/lab/git-autopush/git_autopush.py
```

### 4. Already on GitHub

```bash
cd ~/github-project
python ~/code/lab/git-autopush/git_autopush.py
# Detects it's already on GitHub, does nothing
```

## Configuration

### Custom .gitignore Template

Edit `templates/default_gitignore.txt` to customize the default .gitignore:

```bash
nano /home/xenhp/code/lab/git-autopush/templates/default_gitignore.txt
```

Add your commonly ignored files/folders.

### Default License

Currently prompts for license choice. To auto-select:

```python
# In git_autopush.py, modify get_github_info():
license_type = "MIT"  # Skip prompt, use MIT
```

## Troubleshooting

### "Git is not installed"

Install Git:
```bash
# Ubuntu/Debian
sudo apt install git

# macOS
brew install git

# Windows
# Download from https://git-scm.com/downloads
```

### "Authentication failed"

Make sure you're using a Personal Access Token, not your GitHub password:

1. Go to https://github.com/settings/tokens
2. Generate new token (classic)
3. Select `repo` scope
4. Copy token and use as password

### "Repository not found"

Make sure you created the repository on GitHub before pushing:
- The script pauses and tells you to create it
- Don't skip this step!

### "Permission denied"

Check:
- GitHub username is correct
- Repository name matches what you created
- You own the repository or have write access

### "Can't find md2pdf"

PDF generation is optional. If you want it:

```bash
# Make sure md2pdf exists
ls /home/xenhp/code/lab/md2pdf/md2pdf.py

# Or edit git_autopush.py to point to correct location
```

## Advanced Usage

### Batch Processing

Push multiple projects:

```bash
#!/bin/bash
for dir in ~/code/projects/*/; do
    echo "Processing $dir"
    python ~/code/lab/git-autopush/git_autopush.py "$dir"
done
```

### Alias

Add to your `~/.bashrc`:

```bash
alias autopush='python /home/xenhp/code/lab/git-autopush/git_autopush.py'
```

Then:
```bash
cd ~/my-project
autopush
```

### Non-Interactive Mode

For automation, you could modify the script to accept command-line arguments:

```python
parser.add_argument('--username', help='GitHub username')
parser.add_argument('--repo', help='Repository name')
parser.add_argument('--license', choices=['MIT', 'Apache-2.0', 'GPL-3.0', 'None'])
```

## Future Enhancements

Potential features to add:

- [ ] GitHub CLI (`gh`) integration for automatic repo creation
- [ ] Support for GitLab, Bitbucket
- [ ] Automatic Personal Access Token handling
- [ ] Branch protection setup
- [ ] GitHub Actions workflow templates
- [ ] Automatic README generation
- [ ] Support for monorepos
- [ ] Dry-run mode (show what would happen)
- [ ] Rollback capability
- [ ] Email notifications on completion

## Architecture

### File Structure

```
git-autopush/
├── git_autopush.py              # Main script (500+ lines)
│   ├── Colors class             # ANSI color codes
│   ├── Logger class             # Dual console/file logging
│   └── GitAutoPush class        # Main logic
│       ├── check_git_installed()
│       ├── check_is_git_repo()
│       ├── check_remote_exists()
│       ├── initialize_git()
│       ├── create_gitignore()
│       ├── make_initial_commit()
│       ├── get_github_info()
│       ├── add_remote()
│       ├── push_to_github()
│       └── generate_documentation()
├── templates/
│   └── default_gitignore.txt   # Template .gitignore
├── README.md                    # This file
├── requirements.txt             # Dependencies (none!)
└── .gitignore                   # Exclude logs/PDFs
```

### Class Hierarchy

```
GitAutoPush
  ├─ Logger
  │   ├─ log()
  │   ├─ success()
  │   ├─ error()
  │   ├─ warning()
  │   └─ save()
  └─ Colors (static)
      ├─ success()
      ├─ error()
      ├─ warning()
      └─ step()
```

## License

MIT License - Free to use and modify

## Contributing

This is a personal tool, but improvements welcome:

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## Author

Created to automate the repetitive process of pushing projects to GitHub.

**Repository:** https://github.com/jmartinmatias/git-autopush (if you pushed it!)

## Changelog

### v1.0.0 (2024-12-07)
- Initial release
- Automatic Git initialization
- GitHub remote setup
- Detailed logging
- Auto-documentation generation
- PDF conversion support

---

**Happy pushing! 🚀**
