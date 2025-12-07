# Git AutoPush - Quick Start Guide

## What Is This?

A tool that automatically pushes any project to GitHub with one command!

It:
- Checks if your project is already on GitHub
- If not, does **everything** to get it there
- Explains **every step** in detail
- Generates complete documentation

## How to Use

### Step 1: Navigate to Your Project

```bash
cd /path/to/your/project
```

### Step 2: Run AutoPush

```bash
python /home/xenhp/code/lab/git-autopush/git_autopush.py
```

### Step 3: Answer Questions

```
GitHub username: jmartinmatias
Repository name [project-name]:
License [1]: 1
```

### Step 4: Create GitHub Repo

When prompted, go to https://github.com/new and create the repository.

**Important settings:**
- ☐ **Don't** check "Add a README"
- ☐ **Don't** check "Add .gitignore"
- ☑ **Do** select a license (MIT recommended)

### Step 5: Done!

Press ENTER and your project is pushed to GitHub!

## What You Get

After running, you'll have:

1. **Your project on GitHub** - Fully pushed with all files
2. **AUTOPUSH_GUIDE.md** - Detailed explanation of everything
3. **AUTOPUSH_GUIDE.pdf** - PDF version of the guide
4. **autopush.log** - Complete log of all operations

## Example

```bash
$ cd ~/my-awesome-app
$ python ~/code/lab/git-autopush/git_autopush.py

============================================================
   Git AutoPush - Automatic GitHub Repository Setup
============================================================

[STEP 1/8] Checking if folder is a Git repository
⚠ This is NOT a Git repository

[STEP 2/8] Initializing Git repository
✓ Git repository initialized

[STEP 3/8] Creating .gitignore file
✓ Created .gitignore file

[STEP 4/8] Making initial commit
✓ Initial commit created

[STEP 5/8] Getting GitHub repository information
GitHub username: jmartinmatias
Repository name [my-awesome-app]:
License [1]: 1

[STEP 6/8] Adding GitHub remote
✓ Remote 'origin' added

[STEP 7/8] Pushing to GitHub
✓ Successfully pushed to GitHub!

============================================================
  ✓ Successfully pushed to GitHub!
============================================================

Repository: https://github.com/jmartinmatias/my-awesome-app
```

## Detailed Features

### Intelligent Detection

- **Already on GitHub?** → Does nothing, tells you it's done
- **Has Git but no remote?** → Just adds remote and pushes
- **No Git at all?** → Initializes everything from scratch

### Color-Coded Output

- 🟢 Green ✓ = Success
- 🔴 Red ✗ = Error
- 🟡 Yellow ⚠ = Warning
- 🔵 Blue [STEP X/8] = Progress

### Complete Documentation

The generated `AUTOPUSH_GUIDE.md` includes:

- Summary of all actions taken
- Detailed explanation of each Git command
- Complete Git workflow guide
- Common commands reference
- Troubleshooting section
- Links to resources

Perfect for learning what actually happened!

## Common Questions

### Q: Will it overwrite my existing Git setup?

No! If your project is already on GitHub, it detects this and does nothing.

### Q: What if I don't want to use MIT license?

You'll be prompted to choose: MIT, Apache, GPL, or None.

### Q: Can I use this for non-Python projects?

Yes! It works for any project. The .gitignore template is Python-focused but you can customize it.

### Q: What if something goes wrong?

Check `autopush.log` for detailed information about what happened. The script logs every command and its output.

### Q: Do I need to install anything?

No! It uses only Python standard library. Just needs Git to be installed on your system.

## Tips

### Make an Alias

Add to `~/.bashrc`:

```bash
alias autopush='python /home/xenhp/code/lab/git-autopush/git_autopush.py'
```

Then just:
```bash
cd ~/my-project
autopush
```

### Batch Process

Push multiple projects:

```bash
for dir in ~/projects/*/; do
    python git_autopush.py "$dir"
done
```

## Troubleshooting

### "Git is not installed"

```bash
sudo apt install git
```

### "Authentication failed"

Use a Personal Access Token, not your GitHub password:
1. https://github.com/settings/tokens
2. Generate new token (classic)
3. Check `repo` scope
4. Use token as password

### "Repository not found"

Make sure you created the repository on GitHub when prompted!

## Next Steps

After pushing:

1. Visit your repository on GitHub
2. Read the generated `AUTOPUSH_GUIDE.md`
3. Continue developing with normal Git workflow:
   ```bash
   git add .
   git commit -m "Add new feature"
   git push
   ```

---

**That's it! Happy pushing! 🚀**
