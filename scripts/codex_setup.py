#!/usr/bin/env python3
"""Generate and install the Codex research workflow (Python 3.11+).

Related progress log: docs/progress/260915_codex_migration.md.
Claude sources remain canonical; generated Codex files are committed for review.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import logging
import os
from pathlib import Path
import re
import shutil
import tomllib

ROOT = Path(__file__).resolve().parents[1]
LOG = logging.getLogger(__name__)
COMMANDS = ('go', 'prereport', 'analyze', 'impl', 'verify', 'debug', 'status', 'paper', 'exp', 'repo')
DESCRIPTIONS = {
    'go': 'Run the agreed full research cycle with analysis, implementation, verification and checkpoints.',
    'prereport': 'Synthesize research context into a pre-report before implementation.',
    'analyze': 'Investigate a research question with permanent, runnable analysis scripts and evidence.',
    'impl': 'Implement an approved research plan with integrity gates.',
    'verify': 'Verify research code against integrity gates and agreed success criteria.',
    'debug': 'Diagnose research code failures with reproductions and explicit hypotheses.',
    'status': 'Summarize the research project state from progress logs and evidence; not Codex usage status.',
    'paper': 'Search arXiv literature for a research topic using the configured arXiv MCP.',
    'exp': 'Read and compare experiment metrics using the configured W&B MCP.',
    'repo': 'Inspect an external repository for a specific research implementation question.',
}
ROLE_DESCRIPTIONS = {
    'prereport': 'Synthesize project evidence into a reviewable pre-report.',
    'analyzer': 'Run permanent research analyses with explicit judgment criteria.',
    'implementer': 'Implement approved research plans with integrity gates.',
    'verifier': 'Read and test changes, report failures without implementing fixes.',
    'debugger': 'Reproduce failures and test bounded diagnostic hypotheses.',
    'paper-fetcher': 'Retrieve arXiv papers and report grounded summaries.',
    'experiment-fetcher': 'Read experiment metrics without modifying or deleting runs.',
    'repo-explorer': 'Inspect external repository implementations without modifying upstream code.',
}
ROLES_BY_COMMAND = {
    'go': ('prereport', 'analyzer', 'implementer', 'verifier', 'debugger'),
    'prereport': ('prereport',),
    'analyze': ('analyzer',),
    'impl': ('implementer',),
    'verify': ('verifier',),
    'debug': ('debugger',),
    'status': (),
    'paper': ('paper-fetcher',),
    'exp': ('experiment-fetcher',),
    'repo': ('repo-explorer',),
}
RUNTIME = """## Codex execution conventions

Use the available native subagent tools for delegation. Role names below identify
custom agents installed in `~/.codex/agents/` (or `$CODEX_HOME/agents/`). Pass the
role's instructions, research context, file paths, previous results and constraints.
`Delegation brief(...)` examples are explanatory prompt text, not a tool or command.
If this client cannot select a custom role, load the matching playbook from
`references/agents/` in this skill and pass it to an available subagent. If delegation
is unavailable, perform the role inline and disclose that fallback. Keep role scope
and checkpoints. Do not claim a subagent ran when it did not. Independent subtasks
may run concurrently; dependent phases remain sequential. Inherit the user's model.
Read/Write/Edit/Bash/Grep/Glob are capability descriptions: use the actual available
file, shell and search tools. Never invoke a nonexistent Claude tool.

Use `$source-command-NAME` for these skills. Legacy `/NAME` labels below describe
the research workflow, not registered CLI slash commands. `/status` in Codex is a
built-in usage command; use `$source-command-status` for research status.
Honor existing user authorization; do not request the same approval again.
Do not undo work or delete files on a rejected checkpoint. Preserve and report state.
Stage only explicit task-owned paths. Push only when the user explicitly requests it.
"""
REMOTE = """\n## Remote compute and continuity

Determine the actual host, working directory and Python environment before execution.
macOS is for local work; CUDA training and MD run on the designated remote server.
Do not assume a local clone has the server's GPU, data, environment or checkpoints.
On a single-user multi-GPU server, inspect `nvidia-smi` and existing tmux sessions
before launching. Never interrupt existing experiments without authorization.
Use a named tmux session for long jobs and record host, repository commit, exact
command, environment, GPU IDs, session name, log path and checkpoint path in the
progress log. Preserve the user's existing scheduler/tmux workflow.
A saved Codex chat and a running training process have separate lifetimes.
"""


def adapt(text: str) -> str:
    """Translate platform references without changing scientific guidance."""
    text = text.replace('~/.claude.json', '~/.codex/config.toml')
    text = text.replace('<project>/.mcp.json', '<project>/.codex/config.toml')
    text = text.replace('CLAUDE.md', 'AGENTS.md').replace('Claude Code', 'Codex').replace('Claude', 'Codex')
    text = text.replace('~/.claude/', '~/.codex/').replace('~/.Codex/', '~/.codex/')
    text = text.replace('Task(', 'Delegation brief(')
    text = text.replace('Task (delegate', 'Native subagent tools (delegate')
    text = re.sub(r'@(' + '|'.join(map(re.escape, ROLE_DESCRIPTIONS)) + r')\b', r'\1', text)
    text = text.replace('rollback with `git checkout .`', 'stop and preserve the working tree; discuss any scoped undo')
    text = text.replace('git add docs/progress/ analyze/ src/ test/', 'git add -- <explicit-task-owned-file-paths>')
    text = re.sub(
        r'```bash\n\s*rm -rf [^\n]+\n\s*```',
        'Preserve the temporary clone and report its path; clean up only when explicitly authorized.',
        text,
    )
    text = re.sub(
        r'^- .*rm -rf.*$',
        '- Preserve temporary clones; clean up only when explicitly authorized.',
        text,
        flags=re.M,
    )
    text = text.replace('See `mcp_global.json` for full config.', 'See the installed MCP sections in `~/.codex/config.toml`; repository defaults are in `codex/mcp.toml`.')
    return '\n'.join(line.rstrip() for line in text.splitlines()) + '\n'


def generate() -> None:
    """Build the reviewable Codex distribution from the Claude source assets."""
    out = ROOT / 'codex'
    if out.exists():
        shutil.rmtree(out)
    out.mkdir()
    global_text = adapt((ROOT / 'global/CLAUDE.md').read_text())
    header = '# Codex research pipeline\n\nGenerated by `scripts/codex_setup.py generate` from repository sources.\n\n'
    (out / 'AGENTS.md').write_text(header + RUNTIME.replace('in this skill', 'in any installed source-command skill') + '\n' + global_text + REMOTE)
    roles = {p.stem: adapt(p.read_text()) for p in sorted((ROOT / 'global/agents').glob('*.md'))}
    (out / 'agents').mkdir(exist_ok=True)
    for name, instructions in roles.items():
        content = {'name': name, 'description': ROLE_DESCRIPTIONS[name], 'developer_instructions': RUNTIME + '\n' + instructions}
        # JSON basic strings are valid TOML basic strings for these text fields.
        (out / 'agents' / (name + '.toml')).write_text('\n'.join(f'{k} = {json.dumps(v, ensure_ascii=False)}' for k, v in content.items()) + '\n')
    for name in COMMANDS:
        folder = out / 'skills' / ('source-command-' + name)
        roles_for_command = ROLES_BY_COMMAND[name]
        refs = folder / 'references/agents'
        folder.mkdir(parents=True, exist_ok=True)
        if roles_for_command:
            refs.mkdir(parents=True)
        body = adapt((ROOT / 'global/commands' / (name + '.md')).read_text())
        role_section = ''
        if roles_for_command:
            links = '\n'.join(f'- [{role}](references/agents/{role}.md)' for role in roles_for_command)
            role_section = '\n## Role playbooks\n\nRead only the role needed for the current phase.\n\n' + links + '\n'
        text = f'---\nname: source-command-{name}\ndescription: {json.dumps(DESCRIPTIONS[name])}\n---\n\n' + RUNTIME + role_section + '\n' + body
        (folder / 'SKILL.md').write_text(adapt(text))
        for role in roles_for_command:
            instructions = roles[role]
            (refs / (role + '.md')).write_text(instructions)
    template = adapt((ROOT / 'project_template/CLAUDE.md').read_text())
    (out / 'PROJECT_AGENTS.md').write_text(template)
    (out / 'mcp.toml').write_text('''[mcp_servers.arxiv]
command = "uvx"
args = ["arxiv-mcp-server"]

[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]

[mcp_servers.wandb]
command = "uvx"
args = ["--from", "git+https://github.com/wandb/wandb-mcp-server", "wandb_mcp_server"]
env_vars = ["WANDB_API_KEY"]
''')
    (out / 'research.rules').write_text('''# Prompts preserve the user's ability to explicitly authorize these operations.
# These prefix rules are not a complete command firewall; sandbox policy still applies.
prefix_rule(pattern=["git", "push"], decision="prompt", justification="Push requires explicit user authorization.")
prefix_rule(pattern=["rm", "-rf"], decision="prompt", justification="Destructive cleanup requires explicit user authorization.")
prefix_rule(pattern=["sudo"], decision="prompt", justification="Privilege escalation requires explicit user authorization.")
''')
    LOG.info('Generated 10 skills and %d custom agents', len(roles))


class Installer:
    """Install changed files with unique, private backups."""

    def __init__(self, codex_home: Path, skills_home: Path) -> None:
        self.codex_home = codex_home
        self.skills_home = skills_home
        stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
        self.backup = codex_home / 'migration-backups' / stamp
        self.changes: list[str] = []

    def write(self, target: Path, data: bytes) -> None:
        """Back up changed destinations, then atomically replace the content."""
        if target.exists() and target.read_bytes() == data:
            return
        target.parent.mkdir(parents=True, exist_ok=True)
        mode = target.stat().st_mode & 0o777 if target.exists() else 0o600
        if target.exists():
            backup = self.backup / str(target.absolute()).lstrip('/')
            backup.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            shutil.copy2(target, backup)
            backup.chmod(0o600)
        # Write through a temporary sibling; an existing symlink is preserved.
        actual = target.resolve() if target.is_symlink() else target
        temp = actual.with_name(actual.name + '.research-pipeline.tmp')
        with temp.open('xb') as stream:
            os.chmod(temp, mode)
            stream.write(data)
        temp.replace(actual)
        self.changes.append(str(target))

    def prune_tree(self, target: Path, expected: set[Path]) -> None:
        """Back up and remove stale files from a pipeline-owned directory."""
        if not target.exists():
            return
        for path in sorted((item for item in target.rglob('*') if item.is_file()), reverse=True):
            if path.relative_to(target) in expected:
                continue
            backup = self.backup / str(path.absolute()).lstrip('/')
            backup.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            shutil.copy2(path, backup)
            backup.chmod(0o600)
            path.unlink()
            self.changes.append(str(path) + ' (removed)')
        for path in sorted((item for item in target.rglob('*') if item.is_dir()), reverse=True):
            try:
                path.rmdir()
            except OSError:
                pass

    def install(self) -> None:
        """Install only pipeline-owned assets and add missing config sections."""
        out = ROOT / 'codex'
        self.write(self.codex_home / 'AGENTS.md', (out / 'AGENTS.md').read_bytes())
        for kind, destination in [('agents', self.codex_home / 'agents'), ('skills', self.skills_home)]:
            for source in sorted((out / kind).rglob('*')):
                if source.is_file():
                    self.write(destination / source.relative_to(out / kind), source.read_bytes())
        for skill in sorted((out / 'skills').iterdir()):
            expected = {
                source.relative_to(skill)
                for source in skill.rglob('*')
                if source.is_file()
            }
            self.prune_tree(self.skills_home / skill.name, expected)
        self.write(self.codex_home / 'rules/research-pipeline.rules', (out / 'research.rules').read_bytes())
        path = self.codex_home / 'config.toml'
        text = path.read_text() if path.exists() else ''
        data = tomllib.loads(text)
        if data.get('project_doc_max_bytes', 32768) < 65536:
            # Root keys occur before the first table; never replace a nested key.
            root, sep, tables = text.partition('[')
            if re.search(r'^project_doc_max_bytes\s*=', root, re.M):
                root = re.sub(r'^project_doc_max_bytes\s*=.*$', 'project_doc_max_bytes = 65536', root, flags=re.M)
            else:
                root = 'project_doc_max_bytes = 65536\n' + root
            text = root + sep + tables
        defaults = (out / 'mcp.toml').read_text()
        for block in re.split(r'(?=^\[mcp_servers\.)', defaults, flags=re.M):
            if not block.strip():
                continue
            name = re.search(r'\[mcp_servers\.([^]]+)\]', block).group(1)
            if name not in data.get('mcp_servers', {}):
                text += '\n' + block
        tomllib.loads(text)  # Validate before touching user config.
        self.write(path, text.encode())
        LOG.info('Changed %d files; backups (if needed): %s', len(self.changes), self.backup)

    def adopt(self, project: Path) -> None:
        """Add Codex guidance while retaining the existing scientific content."""
        target = project / 'AGENTS.md'
        source = project / 'CLAUDE.md'
        if target.exists():
            # Existing Codex guidance wins; repair only known platform path spellings.
            old = target.read_text()
            new = old.replace('~/.Codex/AGENTS.md', '~/.codex/AGENTS.md').replace('~/.Codex.json', '~/.codex/config.toml')
        elif source.exists():
            new = adapt(source.read_text())
        else:
            raise ValueError(f'No existing AGENTS.md or CLAUDE.md in {project}; use init for new projects')
        self.write(target, new.encode())
        LOG.info('Adopted project: %s (existing research guidance preserved)', project)

    def init(self, project: Path, name: str) -> None:
        """Initialize a new project without overwriting existing files."""
        for source in (ROOT / 'project_template').rglob('*'):
            relative = source.relative_to(ROOT / 'project_template')
            if source.is_file() and relative.as_posix() not in ('CLAUDE.md', '.mcp.json'):
                target = project / relative
                if not target.exists():
                    self.write(target, source.read_bytes())
        target = project / 'AGENTS.md'
        if not target.exists():
            self.write(target, (ROOT / 'codex/PROJECT_AGENTS.md').read_text().replace('<PROJECT_NAME>', name).encode())
        registry = project / 'experiments/registry.csv'
        if not registry.exists():
            self.write(registry, b'exp_id,project,date,description,config,commit\n')


def main() -> None:
    """Dispatch generation or an explicit installation action."""
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['generate', 'install', 'adopt', 'init'])
    parser.add_argument('project', nargs='?', type=Path)
    parser.add_argument('name', nargs='?')
    parser.add_argument('--codex-home', type=Path, default=Path(os.environ.get('CODEX_HOME', Path.home() / '.codex')))
    parser.add_argument('--skills-home', type=Path, default=Path.home() / '.agents/skills')
    args = parser.parse_args()
    if args.action == 'generate':
        generate()
        return
    installer = Installer(args.codex_home.expanduser().absolute(), args.skills_home.expanduser().absolute())
    if args.action == 'install':
        installer.install()
    elif args.project is None:
        parser.error('project path required')
    elif args.action == 'adopt':
        installer.adopt(args.project.expanduser().resolve())
    elif not args.name:
        parser.error('project name required for init')
    else:
        installer.init(args.project.expanduser().resolve(), args.name)


if __name__ == '__main__':
    main()
