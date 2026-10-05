#!/usr/bin/env bash
# .ai/ctx.sh — régénère le bloc dynamique de .ai/STATE.md.
# Déterministe, aucun appel LLM. Portable : copiable tel quel dans n'importe quel repo.
# Usage : bash .ai/ctx.sh   (ou : .ai/ctx.sh si exécutable)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE="$SCRIPT_DIR/STATE.md"
START="<!-- CTX:AUTO:START"
END="<!-- CTX:AUTO:END"

[ -f "$STATE" ] || { echo "ctx.sh: introuvable: $STATE" >&2; exit 1; }
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "ctx.sh: pas un repo git" >&2; exit 1; }

branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '?')"
commits="$(git log --oneline -5 --no-decorate 2>/dev/null || true)"
dirty="$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')"

# Issues GitHub ouvertes (si gh est présent et authentifié), sinon on saute proprement.
issues=""
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  issues="$(gh issue list --state open --limit 8 \
              --json number,title -q '.[] | "- #\(.number) \(.title)"' 2>/dev/null || true)"
fi

TMP="$(mktemp)"
trap 'rm -f "$TMP" "$TMP.new"' EXIT
{
  echo "### 🔄 Snapshot auto — $(date '+%Y-%m-%d %H:%M')"
  echo
  echo "- **Branche** : \`$branch\` · **fichiers modifiés** : $dirty"
  echo
  echo "- **5 derniers commits** :"
  if [ -n "$commits" ]; then printf '%s\n' "$commits" | sed 's/^/  - /'; else echo "  - (aucun)"; fi
  echo
  if [ -n "$issues" ]; then
    echo "- **Issues ouvertes (8 max)** :"
    printf '%s\n' "$issues" | sed 's/^/  /'
  else
    echo "- **Issues** : (gh indisponible ou non authentifié — \`gh auth login\`)"
  fi
} > "$TMP"

awk -v f="$TMP" -v start="$START" -v end="$END" '
  index($0, start) { print; while ((getline line < f) > 0) print line; close(f); inblock=1; next }
  index($0, end)   { inblock=0 }
  !inblock         { print }
' "$STATE" > "$TMP.new" && mv "$TMP.new" "$STATE"

echo "ctx.sh: .ai/STATE.md mis à jour (branche=$branch, modifs=$dirty)."
