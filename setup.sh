#!/bin/bash
set -euo pipefail

# ============================================================
# Research Pipeline Setup
# Installs global Claude Code config and optionally initializes
# a new project from template.
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# ============================================================
# 1. Install Global Config
# ============================================================
install_global() {
    info "Installing global config to $CLAUDE_DIR ..."

    mkdir -p "$CLAUDE_DIR"/{agents,commands}

    # CLAUDE.md
    cp "$SCRIPT_DIR/global/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md"
    info "  → CLAUDE.md"

    # settings.json (merge if exists)
    if [ -f "$CLAUDE_DIR/settings.json" ]; then
        warn "  settings.json already exists. Backing up to settings.json.bak"
        cp "$CLAUDE_DIR/settings.json" "$CLAUDE_DIR/settings.json.bak"
    fi
    cp "$SCRIPT_DIR/global/settings.json" "$CLAUDE_DIR/settings.json"
    info "  → settings.json"

    # MCP global config
    if [ -f "$HOME/.claude.json" ]; then
        warn "  ~/.claude.json already exists. Backing up to ~/.claude.json.bak"
        cp "$HOME/.claude.json" "$HOME/.claude.json.bak"
    fi
    cp "$SCRIPT_DIR/global/mcp_global.json" "$HOME/.claude.json"
    info "  → ~/.claude.json (MCP servers: arxiv, wandb, context7)"

    # Agents
    for agent in "$SCRIPT_DIR"/global/agents/*.md; do
        cp "$agent" "$CLAUDE_DIR/agents/"
        info "  → agents/$(basename "$agent")"
    done

    # Commands
    for cmd in "$SCRIPT_DIR"/global/commands/*.md; do
        cp "$cmd" "$CLAUDE_DIR/commands/"
        info "  → commands/$(basename "$cmd")"
    done

    echo ""
    info "Global config installed successfully!"
    echo ""
    echo "  Installed to: $CLAUDE_DIR"
    echo "  Commands:     /go, /prereport, /analyze, /impl, /verify, /debug, /status"
    echo "               /paper, /exp, /repo"
    echo "  Agents:       @prereport, @analyzer, @implementer, @verifier, @debugger"
    echo "               @paper-fetcher, @experiment-fetcher, @repo-explorer"
    echo "  MCP servers:  arxiv, wandb, context7"
    echo ""
    echo "  MCP setup:"
    echo "    uv tool install arxiv-mcp-server"
    echo "    export WANDB_API_KEY='your-key'  (add to ~/.bashrc)"
    echo ""
}

# ============================================================
# 2. Initialize New Project
# ============================================================
init_project() {
    local target="$1"
    local project_name="$2"

    if [ -d "$target/docs/templates" ]; then
        warn "Project structure already exists at $target"
        read -p "Overwrite templates? (y/N) " -n 1 -r
        echo
        [[ ! $REPLY =~ ^[Yy]$ ]] && { info "Skipped."; return; }
    fi

    info "Initializing project at $target ..."

    # Create directory structure
    mkdir -p "$target"/{docs/{templates,progress,experiment,obsidian},analyze,experiments,src,scripts,cfgs,test}

    # Copy templates
    cp "$SCRIPT_DIR"/project_template/docs/templates/*.md "$target/docs/templates/"
    info "  → docs/templates/ (SUMMARY, ANALYSIS, DEV_GUIDELINE, EXP_MANAGEMENT, INTEGRITY_GATES)"

    # Copy project CLAUDE.md and substitute project name
    sed "s/<PROJECT_NAME>/$project_name/g" \
        "$SCRIPT_DIR/project_template/CLAUDE.md" > "$target/CLAUDE.md"
    info "  → CLAUDE.md (project-level)"

    # Copy project MCP config and substitute project name
    sed "s/YOUR_PROJECT/$project_name/g" \
        "$SCRIPT_DIR/project_template/.mcp.json" > "$target/.mcp.json"
    info "  → .mcp.json (project MCP — edit WANDB_ENTITY)"

    # Create .gitkeep files
    for dir in docs/progress docs/experiment docs/obsidian analyze experiments src scripts cfgs test; do
        touch "$target/$dir/.gitkeep"
    done

    # Create experiments registry
    if [ ! -f "$target/experiments/registry.csv" ]; then
        echo "exp_id,project,date,description,config,commit" > "$target/experiments/registry.csv"
        info "  → experiments/registry.csv"
    fi

    echo ""
    info "Project '$project_name' initialized at $target"
    echo ""
    echo "  Next steps:"
    echo "  1. Edit $target/CLAUDE.md with project-specific context"
    echo "  2. Add research docs to $target/docs/obsidian/"
    echo "  3. Start Claude Code in $target and run /status"
    echo ""
}

# ============================================================
# Main
# ============================================================
usage() {
    echo "Usage:"
    echo "  $0 install              Install global Claude Code config"
    echo "  $0 init <path> <name>   Initialize a new project from template"
    echo "  $0 all <path> <name>    Install global + initialize project"
    echo ""
    echo "Examples:"
    echo "  $0 install"
    echo "  $0 init ~/projects/fragfm3d FragFM3D"
    echo "  $0 all ~/projects/degpred DegPred"
}

case "${1:-}" in
    install)
        install_global
        ;;
    init)
        [ -z "${2:-}" ] && error "Missing project path. Usage: $0 init <path> <name>"
        [ -z "${3:-}" ] && error "Missing project name. Usage: $0 init <path> <name>"
        init_project "$2" "$3"
        ;;
    all)
        [ -z "${2:-}" ] && error "Missing project path. Usage: $0 all <path> <name>"
        [ -z "${3:-}" ] && error "Missing project name. Usage: $0 all <path> <name>"
        install_global
        init_project "$2" "$3"
        ;;
    *)
        usage
        ;;
esac
