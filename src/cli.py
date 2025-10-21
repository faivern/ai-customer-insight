import typer
from rich.console import Console
from src.loader import load_feedback
from src.stats import compute_basic_stats, sample_feedback_texts
from src.llm import generate_ai_insights
from src.report import write_markdown_report

app = typer.Typer(add_completion=False)
console = Console()