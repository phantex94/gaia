#!/usr/bin/env bash
set -euo pipefail

# qstack installer (managed in gaia) for Claude Code and optional .agents/skills symlink mode.
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGIN_DIR="$REPO_ROOT/plugins/qstack"
MODE="${1:-claude}"

case "$MODE" in
  claude)
    if command -v claude >/dev/null 2>&1; then
      echo "Installing qstack plugin into Claude Code from: $REPO_ROOT"
      claude plugin marketplace add "$REPO_ROOT" || true
      claude plugin install qstack@qstack
      echo "Done. Reload plugins in Claude Code (/reload-plugins) and try /qstack:why or /qstack:mode."
    else
      echo "claude CLI not found on PATH. Add $REPO_ROOT as a local marketplace in ~/.claude/settings.json." >&2
      exit 1
    fi
    ;;
  agents)
    TARGET="${2:-$HOME/.agents/skills/qstack}"
    mkdir -p "$(dirname "$TARGET")"
    ln -sfn "$PLUGIN_DIR" "$TARGET"
    echo "Linked $PLUGIN_DIR -> $TARGET"
    ;;
  *)
    echo "Usage: $0 [claude | agents [target_dir]]" >&2
    exit 2
    ;;
esac
