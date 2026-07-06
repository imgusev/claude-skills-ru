#!/usr/bin/env python3
"""Generate MkDocs documentation pages from SKILL.md files, agents, and commands.

Bilingual (en/ru) for skill, domain-index, agent, and command pages: every
page is always emitted in English from its source `<name>.md`; it is
additionally emitted in Russian (suffix `.ru.md`) if a `<name>.ru.md`
sibling already exists next to that source (created by
scripts/translate.py). Until a given agent/command is translated,
mkdocs-static-i18n's `fallback_to_default: true` serves the English page
under the `/ru/` URL for it — same mechanism already used for
not-yet-translated skills (ARCH-4, closed — see _meta/docs/ARCHITECTURE.md;
was English-only per §2.3 through iteration 3).
"""

import argparse
import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(REPO_ROOT, "docs")

# This fork's GitHub identity (ARCH-1, closed — see _meta/docs/BRANDING.md).
GITHUB_BASE = "https://github.com/imgusev/claude-skills-ru/tree/main"

LANGS = ("en", "ru")

# Domain mapping: directory prefix -> (sort order, icon, plugin_name)
DOMAINS = {
    "engineering-team": (1, ":material-code-braces:", "engineering-skills"),
    "engineering": (2, ":material-rocket-launch:", "engineering-advanced-skills"),
    "product-team": (3, ":material-lightbulb-outline:", "product-skills"),
    "marketing-skill": (4, ":material-bullhorn-outline:", "marketing-skills"),
    "project-management": (5, ":material-clipboard-check-outline:", "pm-skills"),
    "c-level-advisor": (6, ":material-account-tie:", "c-level-skills"),
    "ra-qm-team": (7, ":material-shield-check-outline:", "ra-qm-skills"),
    "business-growth": (8, ":material-trending-up:", "business-growth-skills"),
    "finance": (9, ":material-calculator-variant:", "finance-skills"),
    "productivity": (10, ":material-lightning-bolt-outline:", "productivity-skills"),
    "marketing": (11, ":material-web:", "marketing-top-level-skills"),
    "research": (12, ":material-magnify:", "research-skills"),
    "business-operations": (13, ":material-cog-outline:", "business-operations-skills"),
    "commercial": (14, ":material-handshake-outline:", "commercial-skills"),
    "research-ops": (15, ":material-flask-outline:", "research-ops-skills"),
    "compliance-os": (16, ":material-shield-lock-outline:", "compliance-os"),
    "markdown-html": (17, ":material-language-html5:", "markdown-html-skills"),
}

# Domain display names, per language (§2.4 ARCHITECTURE.md).
DOMAIN_NAMES: dict[str, dict[str, str]] = {
    "engineering-team": {"en": "Engineering - Core", "ru": "Инженерия — базовый уровень"},
    "engineering": {"en": "Engineering - POWERFUL", "ru": "Инженерия — уровень POWERFUL"},
    "product-team": {"en": "Product", "ru": "Продукт"},
    "marketing-skill": {"en": "Marketing", "ru": "Маркетинг"},
    "project-management": {"en": "Project Management", "ru": "Управление проектами"},
    "c-level-advisor": {"en": "C-Level Advisory", "ru": "C-level консультирование"},
    "ra-qm-team": {"en": "Regulatory & Quality", "ru": "Регуляторика и качество"},
    "business-growth": {"en": "Business & Growth", "ru": "Бизнес и рост"},
    "finance": {"en": "Finance", "ru": "Финансы"},
    "productivity": {"en": "Productivity", "ru": "Продуктивность"},
    "marketing": {"en": "Marketing (Top-Level)", "ru": "Маркетинг (лендинги)"},
    "research": {"en": "Research", "ru": "Исследования"},
    "business-operations": {"en": "Business Operations", "ru": "Бизнес-операции"},
    "commercial": {"en": "Commercial", "ru": "Коммерция"},
    "research-ops": {"en": "Research Operations", "ru": "Исследовательские операции"},
    "compliance-os": {"en": "Compliance OS", "ru": "Compliance OS"},
    "markdown-html": {"en": "Markdown to HTML", "ru": "Markdown → HTML"},
}

# UI strings shared by generated pages, per language.
UI_STRINGS: dict[str, dict[str, str]] = {
    "source": {"en": "Source", "ru": "Источник"},
    "install": {"en": "Install:", "ru": "Установить:"},
    "install_all": {"en": "Install all:", "ru": "Установить все:"},
    "agent_badge": {"en": "Agent", "ru": "Агент"},
    "slash_command_badge": {"en": "Slash Command", "ru": "Слэш-команда"},
    "skills_in_domain": {"en": "skills in this domain", "ru": "скиллов в этом домене"},
}

# Skills to skip (nested assets, samples, etc.)
SKIP_PATTERNS = [
    "assets/sample-skill",
    "medium-content-pro 2",  # duplicate with space
]


def find_skill_files():
    """Walk the repo and find all SKILL.md files, grouped by domain.

    Dedupes the dual-publish pattern: when a skill has both a bundled mirror
    at <domain>/skills/<name>/SKILL.md AND a standalone wrapper at
    <domain>/<name>/skills/<name>/SKILL.md, the standalone wrapper is skipped
    (the bundled location is canonical for docs). The two are kept in sync by
    scripts/sync_skill_bundles.py; rendering both creates duplicate pages.
    """
    # First pass: collect all SKILL.md paths grouped by domain.
    raw = {}
    for root, _dirs, files in os.walk(REPO_ROOT):
        if "SKILL.md" not in files:
            continue
        rel_path = os.path.relpath(root, REPO_ROOT).replace(os.sep, "/")
        if any(skip in rel_path for skip in SKIP_PATTERNS):
            continue
        parts = rel_path.split("/")
        domain_key = parts[0]
        if domain_key not in DOMAINS:
            continue
        raw.setdefault(domain_key, []).append((parts, root))

    # Second pass: build the bundled-name set per domain, then skip
    # standalone wrappers that mirror those bundled skills.
    skills = {}
    for domain_key, entries in raw.items():
        bundled_names = {parts[2] for parts, _ in entries if len(parts) == 3 and parts[1] == "skills"}
        for parts, root in entries:
            # Detect the dual-publish standalone wrapper:
            # <domain>/<name>/skills/<same-name>/SKILL.md (4 parts) where
            # the same <name> already exists in the bundled set.
            is_dual_publish_mirror = (
                len(parts) == 4 and parts[2] == "skills" and parts[1] == parts[3] and parts[1] in bundled_names
            )
            if is_dual_publish_mirror:
                continue

            skill_name = parts[-1]
            skill_path = os.path.join(root, "SKILL.md")
            if len(parts) >= 3 and parts[1] == "skills":
                is_sub_skill = False
                parent = None
            else:
                is_sub_skill = len(parts) > 2
                parent = parts[1] if len(parts) > 2 else None

            skills.setdefault(domain_key, []).append(
                {
                    "name": skill_name,
                    "path": skill_path,
                    "rel_path": os.path.relpath(root, REPO_ROOT).replace(os.sep, "/"),
                    "is_sub_skill": is_sub_skill,
                    "parent": parent,
                }
            )
    return skills


def extract_title(filepath):
    """Extract the first H1 heading from a SKILL.md file."""
    try:
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Skip YAML frontmatter
                if line == "---":
                    for line2 in f:
                        if line2.strip() == "---":
                            break
                    continue
                if line.startswith("# "):
                    return line[2:].strip()
    except Exception:
        pass
    return None


def extract_subtitle(filepath):
    """Extract the first non-empty line after the first H1 heading."""
    try:
        with open(filepath, encoding="utf-8") as f:
            found_h1 = False
            in_frontmatter = False
            for line in f:
                stripped = line.strip()
                if stripped == "---" and not in_frontmatter:
                    in_frontmatter = True
                    for line2 in f:
                        if line2.strip() == "---":
                            break
                    continue
                if stripped.startswith("# ") and not found_h1:
                    found_h1 = True
                    continue
                if found_h1 and stripped and not stripped.startswith("#"):
                    return stripped
    except Exception:
        pass
    return None


def _unescape_yaml_double_quoted(text):
    """Inverse of YAML double-quoted scalar escaping (backslash/quote only).

    Needed because a double-quoted description may itself contain an
    escaped `\\"` (e.g. a translated trigger phrase quoted inside the
    description, see DEF-1 in _meta/docs/QA-REPORT.md) — the raw regex
    match below intentionally keeps escape sequences as literal two-char
    sequences, so callers get the human-readable unescaped text.
    """
    result = []
    i = 0
    while i < len(text):
        if text[i] == "\\" and i + 1 < len(text) and text[i + 1] in "\\\"":
            result.append(text[i + 1])
            i += 2
        else:
            result.append(text[i])
            i += 1
    return "".join(result)


def extract_description_from_frontmatter(filepath):
    """Extract the description field from YAML frontmatter.

    Handles single-line, quoted, and multi-line (| or >) YAML descriptions.
    """
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        match = re.match(r"^---\n(.*?)---\n", content, re.DOTALL)
        if not match:
            return None
        fm = match.group(1)

        # Try quoted single-line: description: "text" or description: 'text'
        # (?:[^"\\]|\\.)* accounts for escaped \" inside the value — a plain
        # [^"]+ would stop at the FIRST quote, escaped or not, silently
        # truncating the description (DEF-1's visible symptom on the site).
        m = re.search(r'description:\s*"((?:[^"\\]|\\.)*)"', fm)
        if m:
            return _unescape_yaml_double_quoted(m.group(1).strip())
        m = re.search(r"description:\s*'([^']+)'", fm)
        if m:
            return m.group(1).strip()

        # Try multi-line block scalar: description: | or description: >
        m = re.search(r"description:\s*[|>]-?\s*\n((?:[ \t]+.+\n?)+)", fm)
        if m:
            lines = m.group(1).strip().splitlines()
            text = " ".join(line.strip() for line in lines)
            return text

        # Try unquoted single-line: description: text
        m = re.search(r"description:\s+([^\n\"'][^\n]+)", fm)
        if m:
            return m.group(1).strip()
    except Exception:
        pass
    return None


def slugify(name):
    """Convert a skill name to a URL-friendly slug."""
    return re.sub(r"[^a-z0-9-]", "-", name.lower()).strip("-")


# SEO keyword mapping: domain_key -> differentiating keywords for <title> tags,
# per language. site_name already carries "Claude Code Skills" on every page,
# so per-page suffixes emphasize complementary terms: agent skill, Codex, OpenClaw, domain
DOMAIN_SEO_SUFFIX: dict[str, dict[str, str]] = {
    "engineering-team": {"en": "Agent Skill & Codex Plugin", "ru": "Агентский скилл и плагин Codex"},
    "engineering": {"en": "Agent Skill for Codex & OpenClaw", "ru": "Агентский скилл для Codex и OpenClaw"},
    "product-team": {"en": "Agent Skill for Product Teams", "ru": "Агентский скилл для продуктовых команд"},
    "marketing-skill": {"en": "Agent Skill for Marketing", "ru": "Агентский скилл для маркетинга"},
    "project-management": {"en": "Agent Skill for PM", "ru": "Агентский скилл для управления проектами"},
    "c-level-advisor": {"en": "Agent Skill for Executives", "ru": "Агентский скилл для руководителей"},
    "ra-qm-team": {"en": "Agent Skill for Compliance", "ru": "Агентский скилл для комплаенса"},
    "business-growth": {"en": "Agent Skill for Growth", "ru": "Агентский скилл для роста"},
    "finance": {"en": "Agent Skill for Finance", "ru": "Агентский скилл для финансов"},
    "productivity": {"en": "Agent Skill for Personal Productivity", "ru": "Агентский скилл для личной продуктивности"},
    "marketing": {"en": "Agent Skill for Landing Pages", "ru": "Агентский скилл для лендингов"},
    "research": {"en": "Agent Skill for Research Workflows", "ru": "Агентский скилл для исследовательских процессов"},
    "markdown-html": {"en": "Agent Skill for HTML Output", "ru": "Агентский скилл для HTML-вывода"},
}
DOMAIN_SEO_SUFFIX_DEFAULT = {"en": "Claude Code Plugin & Agent Skill", "ru": "Плагин и агентский скилл для Claude Code"}

# Domain-specific description context for pages without frontmatter descriptions, per language.
DOMAIN_SEO_CONTEXT: dict[str, dict[str, str]] = {
    "engineering-team": {
        "en": "engineering agent skill and Claude Code plugin for code generation, DevOps, architecture, and testing",
        "ru": "инженерный агентский скилл и плагин Claude Code для генерации кода, DevOps, архитектуры и тестирования",
    },
    "engineering": {
        "en": "advanced agent-native skill and Claude Code plugin for AI agent design, infrastructure, and automation",
        "ru": "продвинутый агентно-нативный скилл и плагин Claude Code для дизайна AI-агентов, инфраструктуры и автоматизации",
    },
    "product-team": {
        "en": "product management agent skill and Claude Code plugin for PRDs, discovery, analytics, and roadmaps",
        "ru": "продуктовый агентский скилл и плагин Claude Code для PRD, дискавери, аналитики и дорожных карт",
    },
    "marketing-skill": {
        "en": "marketing agent skill and Claude Code plugin for content, SEO, CRO, and growth",
        "ru": "маркетинговый агентский скилл и плагин Claude Code для контента, SEO, CRO и роста",
    },
    "project-management": {
        "en": "project management agent skill and Claude Code plugin for sprints, Jira, and Confluence",
        "ru": "агентский скилл и плагин Claude Code для управления проектами — спринты, Jira и Confluence",
    },
    "c-level-advisor": {
        "en": "executive advisory agent skill and Claude Code plugin for strategic decisions and board meetings",
        "ru": "агентский скилл для executive-консультирования и плагин Claude Code для стратегических решений и совета директоров",
    },
    "ra-qm-team": {
        "en": "regulatory and quality management agent skill for ISO 13485, MDR, FDA, and GDPR compliance",
        "ru": "агентский скилл для регуляторики и управления качеством по ISO 13485, MDR, FDA и GDPR",
    },
    "business-growth": {
        "en": "business growth agent skill and Claude Code plugin for customer success, sales, and revenue ops",
        "ru": "агентский скилл для роста бизнеса и плагин Claude Code для customer success, продаж и revenue ops",
    },
    "finance": {
        "en": "finance agent skill and Claude Code plugin for DCF valuation, budgeting, and SaaS metrics",
        "ru": "агентский скилл для финансов и плагин Claude Code для DCF-оценки, бюджетирования и SaaS-метрик",
    },
    "productivity": {
        "en": "personal productivity agent skill and Claude Code plugin for brain-dump capture, email triage, and reflection",
        "ru": "агентский скилл для личной продуктивности и плагин Claude Code для брейн-дампа, триажа почты и рефлексии",
    },
    "marketing": {
        "en": "landing-page generator agent skill and Claude Code plugin for single-file HTML output with 4 design styles",
        "ru": "агентский скилл — генератор лендингов и плагин Claude Code для одностраничного HTML-вывода с 4 стилями дизайна",
    },
    "research": {
        "en": "research orchestrator agent skill and Claude Code plugin for hybrid routing across pulse, litreview, grants, dossier, patent, syllabus, and notebooklm specialists",
        "ru": "агентский скилл — исследовательский оркестратор и плагин Claude Code для гибридной маршрутизации между pulse, litreview, grants, dossier, patent, syllabus и notebooklm",
    },
    "business-operations": {
        "en": "business operations agent skill and Claude Code plugin for process mapping, vendor management, capacity planning, and internal comms",
        "ru": "агентский скилл для бизнес-операций и плагин Claude Code для маппинга процессов, управления вендорами, планирования мощностей и внутренних коммуникаций",
    },
    "commercial": {
        "en": "commercial agent skill and Claude Code plugin for pricing strategy, deal desk, partnerships, and RFP response",
        "ru": "коммерческий агентский скилл и плагин Claude Code для ценовой стратегии, deal desk, партнёрств и ответов на RFP",
    },
    "research-ops": {
        "en": "enterprise research operations agent skill and Claude Code plugin for clinical study design, R&D finance, market sizing, and product research",
        "ru": "корпоративный агентский скилл для исследовательских операций и плагин Claude Code для дизайна клинических исследований, R&D-финансов, оценки рынка и продуктовых исследований",
    },
    "compliance-os": {
        "en": "compliance readiness agent skill and Claude Code plugin for ISO 13485, ISO 27001, SOC 2, GDPR, FDA QSR, and EU AI Act audit prep",
        "ru": "агентский скилл для готовности к комплаенсу и плагин Claude Code для аудит-подготовки ISO 13485, ISO 27001, SOC 2, GDPR, FDA QSR и EU AI Act",
    },
    "markdown-html": {
        "en": "markdown-to-interactive-HTML converter agent skill and Claude Code plugin for single-file documents, code reviews, and slide decks",
        "ru": "агентский скилл — конвертер markdown в интерактивный HTML и плагин Claude Code для одностраничных документов, код-ревью и слайд-дек",
    },
}

# Agent domain folders (agents/<key>/) don't always match skill domain
# keys (agents/ is its own subtree, separate from the SKILL.md domain
# tree) — this reuses DOMAIN_NAMES above (single source of truth for
# en/ru domain labels) for the 10 domains agent pages have always shown,
# rather than duplicating a parallel translation. Anything outside this
# set (e.g. business-operations/commercial agents nested under a skill
# domain) falls back to a prettified key in agent_domain_label(), en-only
# — identical to the pre-i18n behavior, just no longer hand-duplicated
# per render call site.
AGENT_DOMAIN_LABELS: dict[str, dict[str, str]] = {
    "business-growth": DOMAIN_NAMES["business-growth"],
    "c-level": DOMAIN_NAMES["c-level-advisor"],
    "engineering-team": DOMAIN_NAMES["engineering-team"],
    "engineering": DOMAIN_NAMES["engineering"],
    "finance": DOMAIN_NAMES["finance"],
    "marketing": DOMAIN_NAMES["marketing-skill"],
    "product": DOMAIN_NAMES["product-team"],
    "project-management": DOMAIN_NAMES["project-management"],
    "ra-qm-team": DOMAIN_NAMES["ra-qm-team"],
    "markdown-html": DOMAIN_NAMES["markdown-html"],
}

AGENT_DOMAIN_ICONS: dict[str, str] = {
    "business-growth": ":material-trending-up:",
    "c-level": ":material-account-tie:",
    "engineering-team": ":material-code-braces:",
    "engineering": ":material-rocket-launch:",
    "finance": ":material-calculator-variant:",
    "marketing": ":material-bullhorn-outline:",
    "product": ":material-lightbulb-outline:",
    "project-management": ":material-clipboard-check-outline:",
    "ra-qm-team": ":material-shield-check-outline:",
    "markdown-html": ":material-language-html5:",
}

# <skill-domain>/agents/*.md or <skill-domain>/<plugin>/agents/*.md
# (Pass 2 of find_agent_files) map to one of the AGENT_DOMAIN_LABELS/
# AGENT_DOMAIN_ICONS keys above via this table.
SKILL_TO_AGENT_DOMAIN = {
    "c-level-advisor": "c-level",
    "engineering": "engineering",
    "engineering-team": "engineering-team",
    "marketing-skill": "marketing",
    "product-team": "product",
    "project-management": "project-management",
    "ra-qm-team": "ra-qm-team",
    "business-growth": "business-growth",
    "finance": "finance",
    "business-operations": "business-operations",
    "commercial": "commercial",
    "research-ops": "research-ops",
    "compliance-os": "compliance-os",
    "markdown-html": "markdown-html",
}


def agent_domain_label(domain_key, lang):
    """Return the (en/ru) display label for an agent-domain key.

    Falls back to a prettified key (identical string in both languages)
    for domains outside AGENT_DOMAIN_LABELS — matches the pre-existing
    fallback behavior, which was always en-only/untranslated for those.
    """
    names = AGENT_DOMAIN_LABELS.get(domain_key)
    return names[lang] if names else prettify(domain_key)


def agent_domain_icon(domain_key):
    return AGENT_DOMAIN_ICONS.get(domain_key, ":material-account:")


def find_agent_files():
    """Walk the repo and find all agent doc `<name>.md` files.

    Two discovery passes, same patterns main() used to walk inline before
    this was factored out (kept here so scripts/translate.py can reuse it
    via the same `_load_generate_docs()` dynamic-import trick already used
    for find_skill_files() — see tooling/translate.py):

      1. Top-level agents/<domain>/<name>.md
      2. Plugin-internal agents/ folders bundled inside a skill domain —
         <domain>/agents/<name>.md (v2.8.0 pattern) or
         <domain>/<plugin>/agents/<name>.md (legacy pattern: c-level-agents,
         agenthub, self-improving-agent, etc.)

    Returns a list of dicts: name, path, rel_path (repo-root-relative),
    domain_key (an AGENT_DOMAIN_LABELS/AGENT_DOMAIN_ICONS key, or — when
    unmapped — the raw domain/skill-domain folder name; see
    agent_domain_label()/agent_domain_icon()). `agents/CLAUDE.md` (a
    dev doc, not a page) is excluded structurally (it's a file, not a
    domain folder, so the isdir() check below already skips it) — the
    explicit filename check is defense in depth if a per-domain CLAUDE.md
    ever appears.
    """
    agents_dir = os.path.join(REPO_ROOT, "agents")
    entries = []
    seen_slugs = set()

    if os.path.isdir(agents_dir):
        for domain_folder in sorted(os.listdir(agents_dir)):
            domain_path = os.path.join(agents_dir, domain_folder)
            if not os.path.isdir(domain_path):
                continue
            for agent_file in sorted(os.listdir(domain_path)):
                if not agent_file.endswith(".md") or agent_file == "CLAUDE.md":
                    continue
                agent_name = agent_file.replace(".md", "")
                agent_path = os.path.join(domain_path, agent_file)
                entries.append(
                    {
                        "name": agent_name,
                        "path": agent_path,
                        "rel_path": os.path.relpath(agent_path, REPO_ROOT).replace(os.sep, "/"),
                        "domain_key": domain_folder,
                    }
                )
                seen_slugs.add(slugify(agent_name))

    for skill_domain in DOMAINS:
        skill_domain_path = os.path.join(REPO_ROOT, skill_domain)
        if not os.path.isdir(skill_domain_path):
            continue
        candidate_dirs = []
        domain_agents = os.path.join(skill_domain_path, "agents")
        if os.path.isdir(domain_agents):
            candidate_dirs.append(domain_agents)
        for plugin_name in sorted(os.listdir(skill_domain_path)):
            plugin_agents_dir = os.path.join(skill_domain_path, plugin_name, "agents")
            if os.path.isdir(plugin_agents_dir):
                candidate_dirs.append(plugin_agents_dir)
        agent_domain_key = SKILL_TO_AGENT_DOMAIN.get(skill_domain, skill_domain)
        for plugin_agents_dir in candidate_dirs:
            for agent_file in sorted(os.listdir(plugin_agents_dir)):
                if not agent_file.endswith(".md") or agent_file == "CLAUDE.md":
                    continue
                agent_name = agent_file.replace(".md", "")
                slug = slugify(agent_name)
                if slug in seen_slugs:
                    continue
                agent_path = os.path.join(plugin_agents_dir, agent_file)
                entries.append(
                    {
                        "name": agent_name,
                        "path": agent_path,
                        "rel_path": os.path.relpath(agent_path, REPO_ROOT).replace(os.sep, "/"),
                        "domain_key": agent_domain_key,
                    }
                )
                seen_slugs.add(slug)

    return entries


def find_command_files():
    """Walk the repo and find all slash-command `<name>.md` files.

    Two discovery passes (see find_agent_files() docstring for why this
    was factored out of main()):

      1. Top-level commands/<name>.md
      2. Domain-level and skill-internal commands/ folders —
         <domain>/commands/<name>.md (v2.8.0 pattern) or
         <domain>/<skill>/commands/<name>.md (v2.7.0 pattern: productivity,
         research, marketing top-level)

    Returns a list of dicts: name, path, rel_path (repo-root-relative).
    `CLAUDE.md` is excluded explicitly (no per-domain one exists today,
    but commands/ has no isdir() structural guard against it the way
    agents/ does, so the filename check does the real work here).
    """
    commands_dir = os.path.join(REPO_ROOT, "commands")
    entries = []
    seen_slugs = set()

    if os.path.isdir(commands_dir):
        for cmd_file in sorted(os.listdir(commands_dir)):
            if not cmd_file.endswith(".md") or cmd_file == "CLAUDE.md":
                continue
            cmd_name = cmd_file.replace(".md", "")
            cmd_path = os.path.join(commands_dir, cmd_file)
            entries.append(
                {
                    "name": cmd_name,
                    "path": cmd_path,
                    "rel_path": os.path.relpath(cmd_path, REPO_ROOT).replace(os.sep, "/"),
                }
            )
            seen_slugs.add(slugify(cmd_name))

    extra_cmd_dirs = []
    for skill_domain in DOMAINS:
        skill_domain_path = os.path.join(REPO_ROOT, skill_domain)
        if not os.path.isdir(skill_domain_path):
            continue
        domain_cmds = os.path.join(skill_domain_path, "commands")
        if os.path.isdir(domain_cmds):
            extra_cmd_dirs.append(domain_cmds)
        for entry in sorted(os.listdir(skill_domain_path)):
            if entry in {"skills", "agents", "commands", ".claude-plugin", ".codex-plugin"}:
                continue
            skill_cmds = os.path.join(skill_domain_path, entry, "commands")
            if os.path.isdir(skill_cmds):
                extra_cmd_dirs.append(skill_cmds)

    for cmd_dir in extra_cmd_dirs:
        for cmd_file in sorted(os.listdir(cmd_dir)):
            if not cmd_file.endswith(".md") or cmd_file == "CLAUDE.md":
                continue
            cmd_name = cmd_file.replace(".md", "")
            slug = slugify(cmd_name)
            if slug in seen_slugs:
                continue
            cmd_path = os.path.join(cmd_dir, cmd_file)
            entries.append(
                {
                    "name": cmd_name,
                    "path": cmd_path,
                    "rel_path": os.path.relpath(cmd_path, REPO_ROOT).replace(os.sep, "/"),
                }
            )
            seen_slugs.add(slug)

    return entries


def prettify(name):
    """Convert kebab-case to Title Case."""
    return name.replace("-", " ").title()


def strip_content(content):
    """Strip frontmatter and first H1 from content, handling edge cases."""
    # Strip YAML frontmatter
    content = re.sub(r"^---\n.*?---\n", "", content, flags=re.DOTALL)
    # Strip leading whitespace
    content = content.lstrip()
    # Remove the first H1 if it exists (avoid duplicate)
    content = re.sub(r"^#\s+.+\n", "", content, count=1)
    # Remove leading hr after title
    content = re.sub(r"^\s*---\s*\n", "", content)
    return content


def rewrite_skill_internal_links(content, skill_rel_path):
    """Rewrite skill-internal relative links to GitHub source URLs.

    SKILL.md files contain links like references/foo.md, scripts/bar.py,
    assets/template.md, README.md — these exist in the repo but not in docs/.
    Convert them to absolute GitHub URLs.
    """
    # Patterns that are skill-internal (not other docs pages)
    internal_prefixes = ("references/", "scripts/", "assets/", "templates/", "tools/")

    def resolve_internal(match):
        text = match.group(1)
        target = match.group(2)
        # Skip anchors, absolute URLs, and links to other docs pages
        if target.startswith(("#", "http://", "https://", "mailto:")):
            return match.group(0)
        # Rewrite skill-internal links
        if (
            target.startswith(internal_prefixes)
            or target == "README.md"
            or target.endswith((".py", ".json", ".yaml", ".yml", ".sh"))
        ):
            github_url = f"{GITHUB_BASE}/{skill_rel_path}/{target}"
            return f"[{text}]({github_url})"
        # Explicit ./ links and ALL-CAPS companion files (CONTEXT-FORMAT.md,
        # ADR-FORMAT.md, REFERENCE.md) are skill-folder siblings, not docs pages.
        bare = target[2:] if target.startswith("./") else target
        stem = bare.split("/")[0].split("#")[0].rsplit(".", 1)[0]
        if target.startswith("./") or (bare.endswith(".md") and "/" not in bare and stem and stem == stem.upper()):
            github_url = f"{GITHUB_BASE}/{skill_rel_path}/{bare}"
            return f"[{text}]({github_url})"
        return match.group(0)

    content = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", resolve_internal, content)
    return content


def rewrite_relative_links(content, source_rel_path):
    """Rewrite relative markdown links (../../, ../) to absolute GitHub URLs.

    Agent and command source files use relative paths like ../../product-team/SKILL.md
    which break when rendered in the docs site. Convert them to GitHub source links.
    """
    source_dir = os.path.dirname(source_rel_path)

    def resolve_link(match):
        text = match.group(1)
        rel_target = match.group(2)
        # Repo-root-relative links (e.g. engineering/grill-me/agents/cs-foo.md or
        # marketing-skill/skills/aeo/SKILL.md) exist in the repo but not in docs/ —
        # rewrite them to GitHub source URLs.
        if (
            not rel_target.startswith(("../", "#", "http://", "https://", "mailto:"))
            and "/" in rel_target
            and os.path.exists(os.path.join(REPO_ROOT, rel_target.split("#")[0]))
        ):
            return f"[{text}]({GITHUB_BASE}/{rel_target})"
        # Only rewrite relative paths that go up (../)
        if not rel_target.startswith("../"):
            return match.group(0)
        # Resolve against source directory
        resolved = os.path.normpath(os.path.join(source_dir, rel_target)).replace(os.sep, "/")
        # Keep links to sibling .md files in the same docs directory
        # e.g. agents/product/cs-foo.md linking to cs-bar.md (same-level agent docs)
        # These resolve to agents/product/cs-bar.md — only keep if they're
        # a docs page we generate (agent .md that isn't CLAUDE.md)
        if (
            resolved.startswith("agents/")
            and resolved.count("/") == 1
            and resolved.endswith(".md")
            and "CLAUDE" not in resolved
        ):
            # This is a sibling agent doc link — rewrite to flat docs slug
            sibling = os.path.basename(resolved).replace(".md", "") + ".md"
            return f"[{text}]({sibling})"
        return f"[{text}]({GITHUB_BASE}/{resolved})"

    content = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", resolve_link, content)

    # Also rewrite backtick code references like `../../product-team/foo/SKILL.md`
    # Convert to clickable GitHub links
    def resolve_backtick(match):
        rel_target = match.group(1)
        if not rel_target.startswith("../"):
            return match.group(0)
        resolved = os.path.normpath(os.path.join(source_dir, rel_target)).replace(os.sep, "/")
        # Make the path a clickable link to the GitHub source
        # Show parent/filename for context (e.g., product-analytics/SKILL.md)
        parts = resolved.split("/")
        display = "/".join(parts[-2:]) if len(parts) >= 2 else resolved
        return f"[`{display}`]({GITHUB_BASE}/{resolved})"

    content = re.sub(r"`(\.\./[^`]+)`", resolve_backtick, content)

    return content


def skill_source_path(skill, lang):
    """Return the source SKILL.md path to render for this skill in `lang`.

    lang="en" always returns skill["path"] (SKILL.md).
    lang="ru" returns the sibling SKILL.ru.md if it already exists next to
    the English source, else None (no translation yet — caller must not
    emit a .ru.md page for it).
    """
    if lang == "en":
        return skill["path"]
    ru_path = os.path.join(os.path.dirname(skill["path"]), "SKILL.ru.md")
    return ru_path if os.path.isfile(ru_path) else None


def flat_lang_source_path(md_path, lang):
    """Return the source path to render for a flat-named doc (agent or
    command `<name>.md`, unlike SKILL.md they don't share one filename per
    folder) in `lang`.

    lang="en" always returns md_path unchanged. lang="ru" returns the
    sibling "<name>.ru.md" next to it if a translation already exists,
    else None — caller must not emit a `.ru.md` page for it;
    mkdocs-static-i18n's fallback_to_default serves the English page at
    that URL instead (same contract as skill_source_path above).
    """
    if lang == "en":
        return md_path
    stem, ext = os.path.splitext(md_path)
    ru_path = f"{stem}.ru{ext}"
    return ru_path if os.path.isfile(ru_path) else None


def output_page_path(domain_key, slug, lang):
    """Return the docs-relative output path for a skill page in `lang`."""
    suffix = ".md" if lang == "en" else f".{lang}.md"
    return f"skills/{domain_key}/{slug}{suffix}"


def generate_skill_page(skill, domain_key, lang):
    """Generate a docs page for a single skill in the given language.

    Returns None (after printing a notice) when lang="ru" and no
    SKILL.ru.md sibling exists yet — the caller must skip emitting that
    page rather than fail the build (Wave A translates skills gradually).
    """
    skill_md_path = skill_source_path(skill, lang)
    if skill_md_path is None:
        print(f"  (skip {lang}) no translation yet: {skill['rel_path']}/SKILL.ru.md")
        return None

    with open(skill_md_path, encoding="utf-8") as f:
        content = f.read()

    # Extract title or generate one
    title = extract_title(skill_md_path) or prettify(skill["name"])
    # Clean title of markdown artifacts and strip domain labels
    title = re.sub(r"[*_`]", "", title)
    title = re.sub(r"\s*[-—]\s*(POWERFUL|Core|Advanced)\s*$", "", title, flags=re.IGNORECASE)

    _, domain_icon, plugin_name = DOMAINS[domain_key]
    domain_name = DOMAIN_NAMES[domain_key][lang]
    ui = {key: values[lang] for key, values in UI_STRINGS.items()}
    seo_suffix = DOMAIN_SEO_SUFFIX.get(domain_key, DOMAIN_SEO_SUFFIX_DEFAULT)[lang]
    seo_title = f"{title} — {seo_suffix}"

    fm_desc = extract_description_from_frontmatter(skill_md_path)
    desc_platforms = "Claude Code, Codex CLI, Gemini CLI, OpenClaw"
    agent_skill_for = "Agent skill for" if lang == "en" else "Агентский скилл для"
    if fm_desc:
        # Strip quotes and clean
        clean = fm_desc.strip("'\"").replace('"', "'")
        # Check if platform keywords already present
        has_platform = any(k in clean.lower() for k in ["claude code", "codex", "gemini"])
        if len(clean) > 150:
            # Truncate at last word boundary before 150 chars
            truncated = clean[:150].rsplit(" ", 1)[0].rstrip(".,;:—-")
            description = f"{truncated}." if has_platform else f"{truncated}. {agent_skill_for} {desc_platforms}."
        else:
            desc_text = clean.rstrip(".")
            description = f"{desc_text}." if has_platform else f"{desc_text}. {agent_skill_for} {desc_platforms}."
    else:
        seo_ctx = DOMAIN_SEO_CONTEXT.get(domain_key, {}).get(lang, f"{agent_skill_for.lower()} {domain_name}")
        works_with = "Works with" if lang == "en" else "Работает с"
        description = f"{title} — {seo_ctx}. {works_with} {desc_platforms}."

    # Build the page with design system
    page = f'''---
title: "{seo_title}"
description: "{description}"
---

# {title}

<div class="page-meta" markdown>
<span class="meta-badge">{domain_icon} {domain_name}</span>
<span class="meta-badge">:material-identifier: `{skill["name"]}`</span>
<span class="meta-badge">:material-github: <a href="{GITHUB_BASE}/{skill["rel_path"]}/SKILL.md">{ui["source"]}</a></span>
</div>

'''
    # Add install banner
    page += f"""<div class="install-banner" markdown>
<span class="install-label">{ui["install"]}</span> <code>claude /plugin install {plugin_name}</code>
</div>

"""

    content_clean = strip_content(content)
    content_clean = rewrite_skill_internal_links(content_clean, skill["rel_path"])
    content_clean = rewrite_relative_links(content_clean, os.path.join(skill["rel_path"], "SKILL.md"))
    page += content_clean

    return page


def generate_nav_entry(skills_by_domain):
    """Generate the nav section for mkdocs.yml (English labels only)."""
    nav_lines = []
    sorted_domains = sorted(skills_by_domain.items(), key=lambda x: DOMAINS[x[0]][0])

    for domain_key, skills in sorted_domains:
        domain_name = DOMAIN_NAMES[domain_key]["en"]
        # Group sub-skills under their parent
        top_level = [s for s in skills if not s["is_sub_skill"]]
        sub_skills = [s for s in skills if s["is_sub_skill"]]
        top_level.sort(key=lambda s: s["name"])

        nav_lines.append(f"    - {domain_name}:")
        for skill in top_level:
            slug = slugify(skill["name"])
            page_path = f"skills/{domain_key}/{slug}.md"
            title = extract_title(skill["path"]) or prettify(skill["name"])
            title = re.sub(r"[*_`]", "", title)
            nav_lines.append(f'      - "{title}": {page_path}')

            # Add sub-skills under parent
            children = [s for s in sub_skills if s["parent"] == skill["name"]]
            children.sort(key=lambda s: s["name"])
            for child in children:
                child_slug = slugify(child["name"])
                child_path = f"skills/{domain_key}/{slug}-{child_slug}.md"
                child_title = extract_title(child["path"]) or prettify(child["name"])
                child_title = re.sub(r"[*_`]", "", child_title)
                nav_lines.append(f'        - "{child_title}": {child_path}')

    return "\n".join(nav_lines)


def parse_args(argv=None):
    """Parse CLI arguments BEFORE any filesystem access.

    `--help` must be side-effect-free: argparse prints usage and exits 0
    without ever touching docs/. Default (no-arg) behavior is unchanged —
    the full docs/ tree is regenerated.
    """
    parser = argparse.ArgumentParser(
        description="Generate MkDocs documentation pages from SKILL.md files, "
        "agents, and commands. Running with no arguments rewrites "
        "the docs/ tree."
    )
    return parser.parse_args(argv)


def _domain_index_cards(top_level, sub_skills, lang):
    """Build the grid-card markdown listing a domain's top-level skills.

    Link targets stay unsuffixed (`{slug}.md`) in both languages — the
    i18n plugin resolves the matching localized file behind that same URL.
    """
    cards = ""
    sub_label = "sub-skills" if lang == "en" else "саб-скиллов"
    for skill in top_level:
        slug = slugify(skill["name"])
        src = skill_source_path(skill, lang) or skill["path"]
        title = re.sub(r"[*_`]", "", extract_title(src) or prettify(skill["name"]))
        subtitle = re.sub(r"[*_`\[\]]", "", extract_subtitle(src) or f"`{skill['name']}`")
        if len(subtitle) > 120:
            subtitle = subtitle[:117] + "..."
        children = [s for s in sub_skills if s["parent"] == skill["name"]]
        sub_text = f" + {len(children)} {sub_label}" if children else ""
        cards += f"""
-   **[{title}]({slug}.md)**{sub_text}

    ---

    {subtitle}
"""
    return cards


def generate_domain_index_page(domain_key, top_level, sub_skills, skill_count, lang):
    """Generate the docs/skills/<domain>/index page in the given language.

    Returns None for lang="ru" when no skill in the domain has a
    SKILL.ru.md translation yet — nothing to add over the English
    fallback the i18n plugin already serves for the whole domain.
    """
    if lang != "en" and not any(skill_source_path(s, lang) for s in (*top_level, *sub_skills)):
        return None

    _, domain_icon, plugin_name = DOMAINS[domain_key]
    domain_name = DOMAIN_NAMES[domain_key][lang]
    ui = {key: values[lang] for key, values in UI_STRINGS.items()}
    cards = _domain_index_cards(top_level, sub_skills, lang)

    fallback_ctx = f"{'agent skills for' if lang == 'en' else 'агентские скиллы для'} {domain_name}"
    domain_seo_ctx = DOMAIN_SEO_CONTEXT.get(domain_key, {}).get(lang, fallback_ctx)
    works_with = "Works with" if lang == "en" else "Работает с"

    return f'''---
title: "{domain_name} Skills — Agent Skills & Codex Plugins"
description: "{skill_count} {domain_name.lower()} skills — {domain_seo_ctx}. {works_with} Claude Code, Codex CLI, Gemini CLI, and OpenClaw."
---

<div class="domain-header" markdown>

# {domain_icon} {domain_name}

<p class="domain-count">{skill_count} {ui["skills_in_domain"]}</p>

</div>

<div class="install-banner" markdown>
<span class="install-label">{ui["install_all"]}</span> <code>claude /plugin install {plugin_name}</code>
</div>

<div class="grid cards" markdown>
{cards}
</div>
'''


def _write_skill_pages(skill, domain_key, out_slug):
    """Render and write a skill page in every language with content.

    `out_slug` is the file stem (without extension) under
    docs/skills/<domain_key>/. Returns the number of pages written
    (1 for en-only skills, 2 once a SKILL.ru.md sibling exists).
    """
    written = 0
    for lang in LANGS:
        content = generate_skill_page(skill, domain_key, lang)
        if content is None:
            continue
        rel_path = output_page_path(domain_key, out_slug, lang)
        with open(os.path.join(DOCS_DIR, rel_path), "w", encoding="utf-8") as f:
            f.write(content)
        written += 1
    return written


def render_agent_page(agent, lang):
    """Render one agent doc page (see find_agent_files()) in `lang`.

    Returns None if lang="ru" and no "<name>.ru.md" sibling exists yet
    next to the agent's source — caller must not emit a page for it;
    mkdocs-static-i18n's fallback_to_default serves the English page at
    that URL instead (same contract as skill pages/generate_skill_page).
    """
    src_path = flat_lang_source_path(agent["path"], lang)
    if src_path is None:
        return None

    title = extract_title(src_path) or prettify(agent["name"])
    title = re.sub(r"[*_`]", "", title)
    # If H1 is a raw slug (cs-foo-bar), prettify it
    if re.match(r"^cs-[a-z-]+$", title):
        title = prettify(title.removeprefix("cs-"))

    with open(src_path, encoding="utf-8") as f:
        content = f.read()

    content_clean = strip_content(content)
    content_clean = rewrite_relative_links(content_clean, agent["rel_path"])

    ui = {key: values[lang] for key, values in UI_STRINGS.items()}
    domain_label = agent_domain_label(agent["domain_key"], lang)
    domain_icon = agent_domain_icon(agent["domain_key"])
    seo_suffix = "AI Coding Agent & Codex Skill" if lang == "en" else "ИИ-агент для Claude Code и Codex"
    agent_seo_title = f"{title} — {seo_suffix}"
    agent_fm_desc = extract_description_from_frontmatter(src_path)
    if agent_fm_desc:
        agent_clean = agent_fm_desc.strip("'\"").replace('"', "'")
        if len(agent_clean) > 150:
            agent_clean = agent_clean[:150].rsplit(" ", 1)[0].rstrip(".,;:—-")
        orchestrator_for = "Agent-native orchestrator for" if lang == "en" else "Агентский оркестратор для"
        agent_desc = f"{agent_clean}. {orchestrator_for} Claude Code, Codex, Gemini CLI."
    else:
        native_for = "agent-native AI orchestrator for" if lang == "en" else "агентский ИИ-оркестратор для"
        works_with = "Works with" if lang == "en" else "Работает с"
        agent_desc = f"{title} — {native_for} {domain_label}. {works_with} Claude Code, Codex CLI, Gemini CLI, and OpenClaw."

    return f'''---
title: "{agent_seo_title}"
description: "{agent_desc}"
---

# {title}

<div class="page-meta" markdown>
<span class="meta-badge">:material-robot: {ui["agent_badge"]}</span>
<span class="meta-badge">{domain_icon} {domain_label}</span>
<span class="meta-badge">:material-github: <a href="{GITHUB_BASE}/{agent["rel_path"]}">{ui["source"]}</a></span>
</div>

{content_clean}'''


def _write_agent_pages(agent, agents_docs_dir):
    """Render and write an agent page in every language with content.

    Returns the number of pages written (1 while untranslated, 2 once a
    "<name>.ru.md" sibling exists next to the source).
    """
    slug = slugify(agent["name"])
    written = 0
    for lang in LANGS:
        page = render_agent_page(agent, lang)
        if page is None:
            continue
        suffix = ".md" if lang == "en" else f".{lang}.md"
        out_path = os.path.join(agents_docs_dir, f"{slug}{suffix}")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(page)
        written += 1
    return written


def render_command_page(cmd, lang):
    """Render one slash-command doc page (see find_command_files()) in
    `lang`. Returns None if lang="ru" and no "<name>.ru.md" sibling
    exists yet (see render_agent_page for the same fallback contract).
    """
    src_path = flat_lang_source_path(cmd["path"], lang)
    if src_path is None:
        return None

    title = extract_title(src_path) or prettify(cmd["name"])
    title = re.sub(r"[*_`]", "", title)

    with open(src_path, encoding="utf-8") as f:
        content = f.read()

    content_clean = strip_content(content)
    content_clean = rewrite_relative_links(content_clean, cmd["rel_path"])

    ui = {key: values[lang] for key, values in UI_STRINGS.items()}
    cmd_fm_desc = extract_description_from_frontmatter(src_path)
    if cmd_fm_desc:
        cmd_clean = cmd_fm_desc.strip("'\"").replace('"', "'")
        if len(cmd_clean) > 150:
            cmd_clean = cmd_clean[:150].rsplit(" ", 1)[0].rstrip(".,;:—-")
        slash_for = "Slash command for" if lang == "en" else "Слэш-команда для"
        cmd_desc = f"{cmd_clean}. {slash_for} Claude Code, Codex CLI, Gemini CLI."
    elif lang == "en":
        cmd_desc = (
            f"/{cmd['name']} — slash command for Claude Code, Codex CLI, and Gemini CLI. "
            "Run directly in your AI coding agent."
        )
    else:
        cmd_desc = (
            f"/{cmd['name']} — слэш-команда для Claude Code, Codex CLI и Gemini CLI. "
            "Запускается прямо в вашем ИИ-агенте для разработки."
        )

    seo_title = (
        f"/{cmd['name']} — Slash Command for AI Coding Agents"
        if lang == "en"
        else f"/{cmd['name']} — слэш-команда для ИИ-агентов разработки"
    )

    return f'''---
title: "{seo_title}"
description: "{cmd_desc}"
---

# /{cmd["name"]}

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: {ui["slash_command_badge"]}</span>
<span class="meta-badge">:material-github: <a href="{GITHUB_BASE}/{cmd["rel_path"]}">{ui["source"]}</a></span>
</div>

{content_clean}'''


def _write_command_pages(cmd, commands_docs_dir):
    """Render and write a command page in every language with content.

    Returns the number of pages written (1 while untranslated, 2 once a
    "<name>.ru.md" sibling exists next to the source).
    """
    slug = slugify(cmd["name"])
    written = 0
    for lang in LANGS:
        page = render_command_page(cmd, lang)
        if page is None:
            continue
        suffix = ".md" if lang == "en" else f".{lang}.md"
        out_path = os.path.join(commands_docs_dir, f"{slug}{suffix}")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(page)
        written += 1
    return written


def main():
    skills_by_domain = find_skill_files()

    # Create docs/skills/ directories
    for domain_key in skills_by_domain:
        os.makedirs(os.path.join(DOCS_DIR, "skills", domain_key), exist_ok=True)

    total = 0
    # Generate individual skill pages
    for domain_key, skills in skills_by_domain.items():
        top_level = [s for s in skills if not s["is_sub_skill"]]
        sub_skills = [s for s in skills if s["is_sub_skill"]]
        top_level_names = {s["name"] for s in top_level}

        for skill in top_level:
            slug = slugify(skill["name"])
            total += _write_skill_pages(skill, domain_key, slug)

            # Generate sub-skill pages
            children = [s for s in sub_skills if s["parent"] == skill["name"]]
            for child in children:
                child_slug = slugify(child["name"])
                total += _write_skill_pages(child, domain_key, f"{slug}-{child_slug}")

        # Render orphan sub-skills (sub-skills whose parent is a plugin folder,
        # not a top-level skill at <domain>/skills/<name>/). Without this,
        # standalone-only plugins like executive-mentor, agenthub, autoresearch-agent,
        # playwright-pro, self-improving-agent, c-level-agents, and llm-wiki have
        # their sub-skills silently dropped (~79 pages missing from the docs site).
        orphan_sub_skills = [s for s in sub_skills if s["parent"] not in top_level_names]
        # Group by plugin parent
        by_parent = {}
        for s in orphan_sub_skills:
            by_parent.setdefault(s["parent"], []).append(s)
        for parent, children in by_parent.items():
            parent_slug = slugify(parent)
            # If a child has the same name as parent, it's the plugin's index skill;
            # render as <parent>.md (preserves existing URLs like executive-mentor.md).
            index_sub = next((s for s in children if s["name"] == parent), None)
            if index_sub:
                total += _write_skill_pages(index_sub, domain_key, parent_slug)
            # Render non-index children as <parent>-<child>.md
            # (preserves existing URLs like executive-mentor-challenge.md).
            for child in children:
                if child["name"] == parent:
                    continue
                child_slug = slugify(child["name"])
                total += _write_skill_pages(child, domain_key, f"{parent_slug}-{child_slug}")

    # Generate domain index pages (bilingual)
    sorted_domains = sorted(skills_by_domain.items(), key=lambda x: DOMAINS[x[0]][0])
    for domain_key, skills in sorted_domains:
        top_level = sorted([s for s in skills if not s["is_sub_skill"]], key=lambda s: s["name"])
        sub_skills = [s for s in skills if s["is_sub_skill"]]
        skill_count = len(skills)

        for lang in LANGS:
            index_content = generate_domain_index_page(domain_key, top_level, sub_skills, skill_count, lang)
            if index_content is None:
                continue
            index_name = "index.md" if lang == "en" else f"index.{lang}.md"
            index_path = os.path.join(DOCS_DIR, "skills", domain_key, index_name)
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(index_content)

    # Generate agent pages (bilingual: en always, plus ru once a
    # "<name>.ru.md" sibling exists next to the source — see
    # find_agent_files()/render_agent_page()/_write_agent_pages()).
    agents_docs_dir = os.path.join(DOCS_DIR, "agents")
    os.makedirs(agents_docs_dir, exist_ok=True)
    agent_count = 0
    agent_entries = []

    for agent in find_agent_files():
        _write_agent_pages(agent, agents_docs_dir)
        agent_count += 1
        slug = slugify(agent["name"])
        title = extract_title(agent["path"]) or prettify(agent["name"])
        title = re.sub(r"[*_`]", "", title)
        if re.match(r"^cs-[a-z-]+$", title):
            title = prettify(title.removeprefix("cs-"))
        domain_label = agent_domain_label(agent["domain_key"], "en")
        domain_icon = agent_domain_icon(agent["domain_key"])
        agent_entries.append((title, slug, domain_label, domain_icon))

    # Generate agents index
    if agent_entries:
        agent_cards = ""
        for title, slug, domain, icon in agent_entries:
            agent_cards += f"""
-   {icon}{{ .lg .middle }} **[{title}]({slug}.md)**

    ---

    {domain}
"""

        idx = f'''---
title: "AI Coding Agents — Agent-Native Orchestrators & Codex Skills"
description: "{agent_count} agent-native orchestrators for Claude Code, Codex CLI, and Gemini CLI — multi-skill AI agents across engineering, product, marketing, and more."
---

<div class="domain-header" markdown>

# :material-robot: Agents

<p class="domain-count">{agent_count} agents that orchestrate skills across domains</p>

</div>

<div class="grid cards" markdown>
{agent_cards}
</div>
'''
        with open(os.path.join(agents_docs_dir, "index.md"), "w", encoding="utf-8") as f:
            f.write(idx)

    # Generate command pages (bilingual: en always, plus ru once a
    # "<name>.ru.md" sibling exists next to the source — see
    # find_command_files()/render_command_page()/_write_command_pages()).
    commands_docs_dir = os.path.join(DOCS_DIR, "commands")
    os.makedirs(commands_docs_dir, exist_ok=True)
    cmd_count = 0
    cmd_entries = []

    for cmd in find_command_files():
        _write_command_pages(cmd, commands_docs_dir)
        cmd_count += 1
        slug = slugify(cmd["name"])
        title = extract_title(cmd["path"]) or prettify(cmd["name"])
        title = re.sub(r"[*_`]", "", title)
        desc = extract_subtitle(cmd["path"]) or title
        cmd_entries.append((cmd["name"], slug, title, desc))

    # Generate commands index
    if cmd_entries:
        cmd_cards = ""
        for name, slug, _title, desc in cmd_entries:
            desc_clean = re.sub(r"[*_`\[\]]", "", desc)
            if len(desc_clean) > 120:
                desc_clean = desc_clean[:117] + "..."
            cmd_cards += f"""
-   :material-console:{{ .lg .middle }} **[`/{name}`]({slug}.md)**

    ---

    {desc_clean}
"""

        idx = f'''---
title: "Slash Commands — AI Coding Agent Commands & Codex Shortcuts"
description: "{cmd_count} slash commands for Claude Code, Codex CLI, and Gemini CLI — sprint planning, tech debt analysis, PRDs, OKRs, and more."
---

<div class="domain-header" markdown>

# :material-console: Slash Commands

<p class="domain-count">{cmd_count} commands for quick access to common operations</p>

</div>

<div class="grid cards" markdown>
{cmd_cards}
</div>
'''
        with open(os.path.join(commands_docs_dir, "index.md"), "w", encoding="utf-8") as f:
            f.write(idx)

    # Print summary
    print(f"Generated {total} skill pages across {len(skills_by_domain)} domains.")
    print(f"Generated {agent_count} agent pages.")
    print(f"Generated {cmd_count} command pages.")
    print(f"Total: {total + agent_count + cmd_count} pages.")


if __name__ == "__main__":
    parse_args()
    main()
