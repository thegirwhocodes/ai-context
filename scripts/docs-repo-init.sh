#!/bin/bash
# Turn a non-git project folder into a private GitHub repo: docs/code only — no secrets, media, archives, nested repos or >50MB files.
set -e
DIR="$1"; NAME="$2"; cd "$DIR"
[ -e .git ] && { echo "$DIR already a repo"; exit 1; }
cat >> .gitignore <<'IGN'
# --- docs-repo-init: secrets, media, archives, caches ---
.env*
!.env.example
*[Cc]redential*
*[Ss]ecret*
*.pem
*.key
*.p12
*.mov
*.MOV
*.mp4
*.m4a
*.wav
*.mp3
*.aiff
*.aif
*.flac
*.zip
*.dmg
*.jsonl
*.sqlite
*.db
node_modules/
.venv/
venv/
__pycache__/
.next/
.DS_Store
.claude-sessions*
.Rhistory
.aider*
IGN
# nested git repos and big files
find . -mindepth 2 -name .git -not -path './.git/*' 2>/dev/null | sed 's#^\./##; s#/\.git$#/#' >> .gitignore
git init -q -b main
git add -A
git ls-files -z | xargs -0 stat -f '%z %N' 2>/dev/null | awk '$1>50000000{sub(/^[0-9]+ /,""); print}' | while read -r f; do echo "$f" >> .gitignore; git rm -q --cached "$f"; done
git add .gitignore
PAT='sk-ant-[A-Za-z0-9_-]{16,}|sk-[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|(sk|rk)_live_[A-Za-z0-9]{16,}|sbp_[a-f0-9]{30,}|re_[A-Za-z0-9]{6,}_[A-Za-z0-9]{12,}|AKIA[A-Z0-9]{16}|-----BEGIN [A-Z ]*PRIVATE KEY|xox[baprs]-[A-Za-z0-9-]{10,}|AIza[A-Za-z0-9_-]{30,}|eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.'
HITS=$(git grep -IlE "$PAT" --cached 2>/dev/null || true)
if [ -n "$HITS" ]; then echo "SECRET CANDIDATES — excluding:"; echo "$HITS"; echo "$HITS" | while read -r f; do echo "$f" >> .gitignore; git rm -q --cached "$f"; done; git add .gitignore; fi
echo "files=$(git ls-files | wc -l | tr -d ' ') size=$(git ls-files -z | xargs -0 stat -f%z 2>/dev/null | awk '{s+=$1}END{printf "%.0fMB", s/1e6}')"
# create private repo + push
TOKEN=$(printf 'protocol=https\nhost=github.com\n\n' | git credential fill | sed -n 's/^password=//p')
code=$(curl -s -o /dev/null -w '%{http_code}' -H "Authorization: Bearer $TOKEN" "https://api.github.com/repos/thegirwhocodes/$NAME")
if [ "$code" = 404 ]; then
  curl -sf -X POST -H "Authorization: Bearer $TOKEN" https://api.github.com/user/repos \
    -d "{\"name\":\"$NAME\",\"private\":true,\"description\":\"Docs and planning for $(basename "$DIR") (synced from Naomi's Mac)\"}" >/dev/null
fi
git -c user.name="$(git config --global user.name)" commit -q -m "Initial import of $(basename "$DIR") project folder

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
git remote add origin "https://github.com/thegirwhocodes/$NAME.git"
git push -q -u origin main && echo "PUSHED $NAME"
