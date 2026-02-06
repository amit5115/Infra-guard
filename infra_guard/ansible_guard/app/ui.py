from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def header(title):

    console.print(f"\n🛡️  {title}", style="bold cyan")

def success(msg):

    console.print(f"✅ {msg}", style="green")

def warning(msg):

    console.print(f"⚠️ {msg}", style="yellow")

def error(msg):

    console.print(f"❌ {msg}", style="bold red")

def show_risks(risks):

    table = Table(

        title="🚨 Risky Ansible Tasks Detected",

        show_lines=True

    )

    table.add_column("Task", style="cyan")

    table.add_column("Reason", style="yellow")

    table.add_column("Risk Level", style="red")

    for r in risks:

        table.add_row(

            str(r.get("task", "unknown")),

            str(r.get("reason", "unspecified")),

            str(r.get("risk", "MEDIUM")),

        )

    console.print(table)



console = Console()


def show_ai_analysis(ai):
    # -------------------------
    # SAFE EXTRACTION
    # -------------------------
    summary = ai.get("summary", "No summary available")
    risk_level = ai.get("risk_level", "UNKNOWN")
    recommendation = ai.get("recommendation", "Review manually")
    impact = ai.get("impact", [])

    # -------------------------
    # AI SUMMARY
    # -------------------------
    console.print(
        Panel(
            summary,
            title="🧠 AI Summary",
            style="cyan"
        )
    )

    # -------------------------
    # RISK LEVEL
    # -------------------------
    table = Table(title="⚠️ Risk Level", show_header=True, header_style="bold red")
    table.add_column("Overall Risk", style="red")
    table.add_row(str(risk_level))
    console.print(table)

    # -------------------------
    # IMPACT (SAFE)
    # -------------------------
    if isinstance(impact, list) and impact:
        impact_text = "\n".join(f"- {i}" for i in impact)
    else:
        impact_text = "- No detailed impact available"

    console.print(
        Panel(
            impact_text,
            title="📉 Impact",
            style="yellow"
        )
    )

    # -------------------------
    # RECOMMENDATION
    # -------------------------
    console.print(
        Panel(
            recommendation,
            title="✅ Recommendation",
            style="green"
        )
    )