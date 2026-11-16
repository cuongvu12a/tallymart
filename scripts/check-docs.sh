#!/usr/bin/env bash
# scripts/check-docs.sh
# Reports docs whose `related_code` paths changed while the doc itself did not.
#
# Usage:
#   bash scripts/check-docs.sh                 # working tree vs HEAD (+ staged + untracked)
#   bash scripts/check-docs.sh --staged        # staged files only  -> husky pre-commit
#   bash scripts/check-docs.sh --hook          # Claude Code Stop hook (reads JSON on stdin)
#   bash scripts/check-docs.sh origin/main...HEAD   # a commit range -> CI
#
# Exit codes: 0 = ok, 1 = stale docs (normal modes), 2 = stale docs (--hook, fed back to Claude).
# Works with macOS bash 3.2 (no globstar).

set -u
MODE="${1:-}"
DOCS_DIR="docs"

case "$MODE" in
  --hook)
    # Claude Code sends JSON on stdin. If we already blocked once this turn, let Claude stop.
    input="$(cat)"
    if printf '%s' "$input" | grep -q '"stop_hook_active"[[:space:]]*:[[:space:]]*true'; then
      exit 0
    fi
    changed="$( { git diff --name-only HEAD 2>/dev/null; git diff --name-only --cached 2>/dev/null;
                  git ls-files --others --exclude-standard; } | sort -u )"
    FAIL_CODE=2 ;;
  --staged)
    changed="$(git diff --name-only --cached | sort -u)"
    FAIL_CODE=1 ;;
  "")
    changed="$( { git diff --name-only HEAD 2>/dev/null; git diff --name-only --cached 2>/dev/null;
                  git ls-files --others --exclude-standard; } | sort -u )"
    FAIL_CODE=1 ;;
  *)
    changed="$(git diff --name-only "$MODE" | sort -u)"
    FAIL_CODE=1 ;;
esac

[ -z "$changed" ] && exit 0
[ -d "$DOCS_DIR" ] || exit 0

# Print the `related_code:` list items from a file's frontmatter, one path per line.
related_paths() {
  awk '
    /^---[[:space:]]*$/ { n++; if (n >= 2) exit; next }
    n == 1 && /^related_code:/ { f = 1; next }
    n == 1 && f && /^[[:space:]]+-[[:space:]]/ {
      sub(/^[[:space:]]+-[[:space:]]+/, ""); sub(/[[:space:]]+#.*$/, "")
      gsub(/["\047]/, ""); sub(/[[:space:]]+$/, "")
      if ($0 != "") print; next
    }
    { f = 0 }
  ' "$1"
}

stale=""
while IFS= read -r doc; do
  # The doc itself was changed -> considered updated.
  printf '%s\n' "$changed" | grep -qxF "$doc" && continue
  while IFS= read -r path; do
    [ -z "$path" ] && continue
    if printf '%s\n' "$changed" | awk -v p="$path" 'index($0, p) == 1 { f = 1 } END { exit !f }'; then
      stale="${stale}- ${doc} (code changed under: ${path})"$'\n'
      break
    fi
  done <<EOF
$(related_paths "$doc")
EOF
done <<EOF
$(find "$DOCS_DIR" -type f -name '*.md' | sort)
EOF

if [ -n "$stale" ]; then
  {
    echo "Code changed, but these docs were not updated:"
    printf '%s' "$stale"
    echo "-> Update the doc (and its last_verified), OR state why no doc change is needed (e.g. pure refactor)."
  } >&2
  exit "$FAIL_CODE"
fi
exit 0