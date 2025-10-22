# core/cli.py
# CLI command that runs the full pipeline:
# 1) load CSV  2) compute KPIs  3) sample/sanitize feedback
# 4) call LLM for structured insights  5) write Markdown report

import typer
from rich.console import Console

from core.loader import load_feedback
from core.stats import compute_basic_stats, sample_feedback_texts
from core.guards import sanitize_samples, guard_rails_summary
from core.llm import generate_ai_insights
from core.report import write_markdown_report

app = typer.Typer(add_completion=False)
console = Console()

@app.command()
def analyze(
    csv_path: str,
    out_path: str = "report.md",
    text_col: str = "feedback",
    rating_col: str = "rating",
    date_col: str = "date",
    sample_size: int = 200,
):
    """
    Analyze customer feedback and generate a Markdown report.
    """
    console.print(f"[bold]Reading:[/bold] {csv_path}")
    df = load_feedback(csv_path)

    # Compute KPIs: total responses, average rating (if present)
    stats = compute_basic_stats(df, rating_col=rating_col)

    # Select a capped set of texts (newest first if date column exists)
    raw_texts = sample_feedback_texts(
        df, text_col=text_col, date_col=date_col, n=sample_size
    )

    # Sanitize + guard-rail the samples before sending to the LLM
    # (length caps, strip control chars, remove suspicious patterns)
    texts, warnings = sanitize_samples(raw_texts)

    # Summarize any guard-rail warnings so we can show them (transparency)
    if warnings:
        console.print("[yellow]Guard rails warnings:[/yellow]")
        for w in warnings:
            console.print(f"- {w}")

    # Produce a short human-readable guard-rail summary for the report footer
    guards_note = guard_rails_summary(warnings)

    console.print("[bold]Requesting AI insights…[/bold]")
    ai = generate_ai_insights(texts, stats)

    # Render a Markdown report
    write_markdown_report(out_path, stats, ai, guards_note=guards_note)
    console.print(f"[bold green]Done![/bold green] Report created: {out_path}")
