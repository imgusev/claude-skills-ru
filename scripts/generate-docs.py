#!/usr/bin/env python3
"""Generate MkDocs documentation pages from SKILL.md files, agents, and commands.

Bilingual (en/ru) for skill and domain-index pages: every page is always
emitted in English from SKILL.md; it is additionally emitted in Russian
(suffix .ru.md) if a SKILL.ru.md sibling already exists next to the source
(created by scripts/translate.py). Agents and commands stay English-only —
out of scope for this iteration (see ARCHITECTURE.md §2.3).
"""

import argparse
import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(REPO_ROOT, "docs")

# Placeholder for this fork's GitHub identity — replace before publishing
# (see README.md / README.ru.md "before you publish" section, ARCH-1).
GITHUB_BASE = "https://github.com/<GH_USER>/<REPO>/tree/main"

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
        m = re.search(r'description:\s*"([^"]+)"', fm)
        if m:
            return m.group(1).strip()
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

    # Generate agent pages
    agents_dir = os.path.join(REPO_ROOT, "agents")
    agents_docs_dir = os.path.join(DOCS_DIR, "agents")
    os.makedirs(agents_docs_dir, exist_ok=True)
    agent_count = 0
    agent_entries = []

    # Agent domain mapping for display
    AGENT_DOMAINS = {
        "business-growth": ("Business & Growth", ":material-trending-up:"),
        "c-level": ("C-Level Advisory", ":material-account-tie:"),
        "engineering-team": ("Engineering - Core", ":material-code-braces:"),
        "engineering": ("Engineering - POWERFUL", ":material-rocket-launch:"),
        "finance": ("Finance", ":material-calculator-variant:"),
        "marketing": ("Marketing", ":material-bullhorn-outline:"),
        "product": ("Product", ":material-lightbulb-outline:"),
        "project-management": ("Project Management", ":material-clipboard-check-outline:"),
        "ra-qm-team": ("Regulatory & Quality", ":material-shield-check-outline:"),
        "markdown-html": ("Markdown to HTML", ":material-language-html5:"),
    }

    if os.path.isdir(agents_dir):
        for domain_folder in sorted(os.listdir(agents_dir)):
            domain_path = os.path.join(agents_dir, domain_folder)
            if not os.path.isdir(domain_path):
                continue
            domain_info = AGENT_DOMAINS.get(domain_folder, (prettify(domain_folder), ":material-account:"))
            domain_label, domain_icon = domain_info
            for agent_file in sorted(os.listdir(domain_path)):
                if not agent_file.endswith(".md"):
                    continue
                agent_name = agent_file.replace(".md", "")
                agent_path = os.path.join(domain_path, agent_file)
                rel = os.path.relpath(agent_path, REPO_ROOT).replace(os.sep, "/")
                title = extract_title(agent_path) or prettify(agent_name)
                title = re.sub(r"[*_`]", "", title)
                # If H1 is a raw slug (cs-foo-bar), prettify it
                if re.match(r"^cs-[a-z-]+$", title):
                    title = prettify(title.removeprefix("cs-"))

                with open(agent_path, encoding="utf-8") as f:
                    content = f.read()

                content_clean = strip_content(content)
                content_clean = rewrite_relative_links(content_clean, rel)

                agent_seo_title = f"{title} — AI Coding Agent & Codex Skill"
                agent_fm_desc = extract_description_from_frontmatter(agent_path)
                if agent_fm_desc:
                    agent_clean = agent_fm_desc.strip("'\"").replace('"', "'")
                    if len(agent_clean) > 150:
                        agent_clean = agent_clean[:150].rsplit(" ", 1)[0].rstrip(".,;:—-")
                    agent_desc = f"{agent_clean}. Agent-native orchestrator for Claude Code, Codex, Gemini CLI."
                else:
                    agent_desc = f"{title} — agent-native AI orchestrator for {domain_label}. Works with Claude Code, Codex CLI, Gemini CLI, and OpenClaw."

                page = f'''---
title: "{agent_seo_title}"
description: "{agent_desc}"
---

# {title}

<div class="page-meta" markdown>
<span class="meta-badge">:material-robot: {UI_STRINGS["agent_badge"]["en"]}</span>
<span class="meta-badge">{domain_icon} {domain_label}</span>
<span class="meta-badge">:material-github: <a href="{GITHUB_BASE}/{rel}">{UI_STRINGS["source"]["en"]}</a></span>
</div>

{content_clean}'''
                slug = slugify(agent_name)
                out_path = os.path.join(agents_docs_dir, f"{slug}.md")
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(page)
                agent_count += 1
                agent_entries.append((title, slug, domain_label, domain_icon))

    # Pass 2: walk plugin-internal agents/ folders.
    # Plugins like c-level-agents, executive-mentor, agenthub, llm-wiki,
    # self-improving-agent bundle agents alongside their skills at
    # <domain>/<plugin>/agents/*.md. These weren't previously discovered;
    # nav entries in mkdocs.yml that point to them would 404.
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
    seen_slugs = {entry[1] for entry in agent_entries}
    for skill_domain in DOMAINS:
        skill_domain_path = os.path.join(REPO_ROOT, skill_domain)
        if not os.path.isdir(skill_domain_path):
            continue
        # Pass 2a: <domain>/agents/<agent>.md (v2.8.0 pattern — business-operations, commercial)
        domain_agents = os.path.join(skill_domain_path, "agents")
        candidate_dirs = []
        if os.path.isdir(domain_agents):
            candidate_dirs.append(domain_agents)
        # Pass 2b: <domain>/<plugin>/agents/<agent>.md (legacy pattern — c-level-agents, agenthub, etc.)
        for plugin_name in sorted(os.listdir(skill_domain_path)):
            plugin_agents_dir = os.path.join(skill_domain_path, plugin_name, "agents")
            if os.path.isdir(plugin_agents_dir):
                candidate_dirs.append(plugin_agents_dir)
        for plugin_agents_dir in candidate_dirs:
            agent_domain_key = SKILL_TO_AGENT_DOMAIN.get(skill_domain, skill_domain)
            domain_info = AGENT_DOMAINS.get(agent_domain_key, (prettify(agent_domain_key), ":material-account:"))
            domain_label, domain_icon = domain_info
            for agent_file in sorted(os.listdir(plugin_agents_dir)):
                if not agent_file.endswith(".md"):
                    continue
                agent_name = agent_file.replace(".md", "")
                slug = slugify(agent_name)
                if slug in seen_slugs:
                    continue
                agent_path = os.path.join(plugin_agents_dir, agent_file)
                rel = os.path.relpath(agent_path, REPO_ROOT).replace(os.sep, "/")
                title = extract_title(agent_path) or prettify(agent_name)
                title = re.sub(r"[*_`]", "", title)
                if re.match(r"^cs-[a-z-]+$", title):
                    title = prettify(title.removeprefix("cs-"))

                with open(agent_path, encoding="utf-8") as f:
                    content = f.read()

                content_clean = strip_content(content)
                content_clean = rewrite_relative_links(content_clean, rel)

                agent_seo_title = f"{title} — AI Coding Agent & Codex Skill"
                agent_fm_desc = extract_description_from_frontmatter(agent_path)
                if agent_fm_desc:
                    agent_clean = agent_fm_desc.strip("'\"").replace('"', "'")
                    if len(agent_clean) > 150:
                        agent_clean = agent_clean[:150].rsplit(" ", 1)[0].rstrip(".,;:—-")
                    agent_desc = f"{agent_clean}. Agent-native orchestrator for Claude Code, Codex, Gemini CLI."
                else:
                    agent_desc = f"{title} — agent-native AI orchestrator for {domain_label}. Works with Claude Code, Codex CLI, Gemini CLI, and OpenClaw."

                page = f'''---
title: "{agent_seo_title}"
description: "{agent_desc}"
---

# {title}

<div class="page-meta" markdown>
<span class="meta-badge">:material-robot: {UI_STRINGS["agent_badge"]["en"]}</span>
<span class="meta-badge">{domain_icon} {domain_label}</span>
<span class="meta-badge">:material-github: <a href="{GITHUB_BASE}/{rel}">{UI_STRINGS["source"]["en"]}</a></span>
</div>

{content_clean}'''
                out_path = os.path.join(agents_docs_dir, f"{slug}.md")
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(page)
                agent_count += 1
                agent_entries.append((title, slug, domain_label, domain_icon))
                seen_slugs.add(slug)

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

    # Generate command pages
    commands_dir = os.path.join(REPO_ROOT, "commands")
    commands_docs_dir = os.path.join(DOCS_DIR, "commands")
    os.makedirs(commands_docs_dir, exist_ok=True)
    cmd_count = 0
    cmd_entries = []

    if os.path.isdir(commands_dir):
        for cmd_file in sorted(os.listdir(commands_dir)):
            if not cmd_file.endswith(".md") or cmd_file == "CLAUDE.md":
                continue
            cmd_name = cmd_file.replace(".md", "")
            cmd_path = os.path.join(commands_dir, cmd_file)
            rel = os.path.relpath(cmd_path, REPO_ROOT).replace(os.sep, "/")
            title = extract_title(cmd_path) or prettify(cmd_name)
            title = re.sub(r"[*_`]", "", title)

            with open(cmd_path, encoding="utf-8") as f:
                content = f.read()

            content_clean = strip_content(content)
            content_clean = rewrite_relative_links(content_clean, rel)

            cmd_fm_desc = extract_description_from_frontmatter(cmd_path)
            if cmd_fm_desc:
                cmd_clean = cmd_fm_desc.strip("'\"").replace('"', "'")
                if len(cmd_clean) > 150:
                    cmd_clean = cmd_clean[:150].rsplit(" ", 1)[0].rstrip(".,;:—-")
                cmd_desc = f"{cmd_clean}. Slash command for Claude Code, Codex CLI, Gemini CLI."
            else:
                cmd_desc = f"/{cmd_name} — slash command for Claude Code, Codex CLI, and Gemini CLI. Run directly in your AI coding agent."

            page = f'''---
title: "/{cmd_name} — Slash Command for AI Coding Agents"
description: "{cmd_desc}"
---

# /{cmd_name}

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: {UI_STRINGS["slash_command_badge"]["en"]}</span>
<span class="meta-badge">:material-github: <a href="{GITHUB_BASE}/{rel}">{UI_STRINGS["source"]["en"]}</a></span>
</div>

{content_clean}'''
            slug = slugify(cmd_name)
            out_path = os.path.join(commands_docs_dir, f"{slug}.md")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(page)
            cmd_count += 1
            desc = extract_subtitle(cmd_path) or title
            cmd_entries.append((cmd_name, slug, title, desc))

    # Pass 2: domain-level and skill-internal commands/ folders.
    # Patterns:
    #   <domain>/commands/<cmd>.md         — v2.8.0 (business-operations, commercial)
    #   <domain>/<skill>/commands/<cmd>.md — v2.7.0 (productivity, research, marketing top-level)
    seen_cmd_slugs = {entry[1] for entry in cmd_entries}
    extra_cmd_dirs = []
    for skill_domain in DOMAINS:
        skill_domain_path = os.path.join(REPO_ROOT, skill_domain)
        if not os.path.isdir(skill_domain_path):
            continue
        # v2.8.0 pattern: <domain>/commands/
        domain_cmds = os.path.join(skill_domain_path, "commands")
        if os.path.isdir(domain_cmds):
            extra_cmd_dirs.append(domain_cmds)
        # v2.7.0 pattern: <domain>/<skill>/commands/
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
            if slug in seen_cmd_slugs:
                continue
            cmd_path = os.path.join(cmd_dir, cmd_file)
            rel = os.path.relpath(cmd_path, REPO_ROOT).replace(os.sep, "/")
            title = extract_title(cmd_path) or prettify(cmd_name)
            title = re.sub(r"[*_`]", "", title)

            with open(cmd_path, encoding="utf-8") as f:
                content = f.read()

            content_clean = strip_content(content)
            content_clean = rewrite_relative_links(content_clean, rel)

            cmd_fm_desc = extract_description_from_frontmatter(cmd_path)
            if cmd_fm_desc:
                cmd_clean = cmd_fm_desc.strip("'\"").replace('"', "'")
                if len(cmd_clean) > 150:
                    cmd_clean = cmd_clean[:150].rsplit(" ", 1)[0].rstrip(".,;:—-")
                cmd_desc = f"{cmd_clean}. Slash command for Claude Code, Codex CLI, Gemini CLI."
            else:
                cmd_desc = f"/{cmd_name} — slash command for Claude Code, Codex CLI, and Gemini CLI. Run directly in your AI coding agent."

            page = f'''---
title: "/{cmd_name} — Slash Command for AI Coding Agents"
description: "{cmd_desc}"
---

# /{cmd_name}

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: {UI_STRINGS["slash_command_badge"]["en"]}</span>
<span class="meta-badge">:material-github: <a href="{GITHUB_BASE}/{rel}">{UI_STRINGS["source"]["en"]}</a></span>
</div>

{content_clean}'''
            out_path = os.path.join(commands_docs_dir, f"{slug}.md")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(page)
            cmd_count += 1
            seen_cmd_slugs.add(slug)
            desc = extract_subtitle(cmd_path) or title
            cmd_entries.append((cmd_name, slug, title, desc))

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
