Create a new private repository in pamam-apps organization, then push the current code to it.

Name(optional): $ARGUMENTS

(if no name provided, use the project dir name)

Steps:
1. Get the current directory name for the repo name (if needed)
2. Verify work account (sstitt_pam) is active in GitHub CLI
3. Create private repo: `gh repo create pamam-apps/REPO-NAME --private --description "Brief description"`
4. Add remote origin: `git remote add origin git@github-pamam:pamam-apps/REPO-NAME.git`
5. Push code: `git push -u origin main`

Notes:
- Enterprise accounts only allow private repos
- Use git@github-pamam: prefix for pamam-apps repos (matches SSH config)
- Switch accounts if needed: `gh auth switch --user sstitt_pam`