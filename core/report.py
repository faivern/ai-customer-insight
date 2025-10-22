from datetime import datetime
from typing import Dict, List

HEADER = """# Customer Insight Report

Generated: {timestamp}

"""

def _render_list(title: str, items: List[str]) -> str:
    if not items:
        return f"## {title}\n\n- (none)\n\n"
    lines = "\n".join(f"- {x}" for x in items)
    return f"## {title}\n\n{lines}\n\n"

def write_markdown_report(out_path: str, stats: Dict, ai: Dict, guards_note: str = ""):
    """
    Creates a readable, shareable Markdown report with:
      - Overview (KPIs)
      - AI insights (TL;DR, themes, improvements, quick wins, long-term)
      - Guard-rail notes (transparency)
    """
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    md = HEADER.format(timestamp=ts)

    md += "## Overview\n\n"
    md += f"- **Total responses:** {stats['total_responses']}\n"
    if stats["avg_rating"] is not None:
        md += f"- **Average rating:** {stats['avg_rating']} / 5\n"
    else:
        md += "- **Average rating:** (missing in dataset)\n"
    md += "\n---\n\n"

    md += "## TL;DR\n\n"
    md += ai.get("tldr", "(no summary)") + "\n\n"

    md += _render_list("Top Themes", ai.get("themes", []))
    md += _render_list("Recommended Improvements (Prioritized)", ai.get("improvements", []))
    md += _render_list("Quick Wins", ai.get("quick_wins", []))
    md += _render_list("Long-Term Actions", ai.get("long_term", []))

    if guards_note:
        md += "---\n\n"
        md += f"**Safety & Guard Rails:** {guards_note}\n"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)