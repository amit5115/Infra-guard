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
    # 🧠 AI Summary
    console.print(
        Panel(
            ai["summary"],
            title="🧠 AI Summary",
            style="cyan"
        )
    )

    # 🚨 Risk Level
    table = Table(title="🚨 Risk Level", show_header=True, header_style="bold red")
    table.add_column("Overall Risk", style="red")
    table.add_row(ai["risk_level"])
    console.print(table)

    # 📉 Impact
    impact = "\n".join(f"- {i}" for i in ai["impact"])
    console.print(
        Panel(
            impact,
            title="📉 Impact",
            style="yellow"
        )
    )

    # ✅ Recommendation
    console.print(
        Panel(
            ai["recommendation"],
            title="✅ Recommendation",
            style="green"
        )
    )
