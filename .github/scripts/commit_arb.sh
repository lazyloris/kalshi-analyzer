#!/usr/bin/env bash
# Commit scanner output to the current branch, retrying on push races.
git config user.name "kalshi-paper-bot"
git config user.email "kalshi-paper-bot@users.noreply.github.com"
git add data/arb
git diff --cached --quiet && exit 0
git commit -qm "arb scan data $(date -u +%Y-%m-%dT%H:%MZ)"
for i in 1 2 3 4; do git pull -q --rebase && git push -q && exit 0; sleep $((i * 5)); done
exit 1
