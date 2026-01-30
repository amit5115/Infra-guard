import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def show_cost_impact(costs, total):
    table = Table(title="💰 Cost Impact Summary", show_lines=True)
    table.add_column("Resource", style="cyan")
    table.add_column("Before")
    table.add_column("After")
    table.add_column("Monthly Δ ($)", justify="right")

    for c in costs:
        delta = c["delta"]
        sign = "+" if delta >= 0 else "-"
        table.add_row(
            c["resource"],
            str(c["before"]),
            str(c["after"]),
            f"{sign}${abs(delta)}"
        )

    console.print(table)

    console.print(
        Panel(
            f"📊 Total Estimated Monthly Change: ${total}",
            style="bold green"
        )
    )




# ---------- BASIC UI HELPERS ----------

def header(title):
    console.print("\n" + "─" * 80)
    console.print(f"🛡️  {title}", style="bold cyan")
    console.print("─" * 80)

def success(msg):
    console.print(f"✅ {msg}", style="green")

def warning(msg):
    console.print(f"⚠️ {msg}", style="yellow")

def error(msg):
    console.print(f"❌ {msg}", style="red")

# ---------- PLAN SUMMARY ----------

def show_plan_summary(add, change, destroy):
    table = Table(title="Terraform Plan Summary", show_lines=True)
    table.add_column("Action", style="cyan")
    table.add_column("Count", style="magenta")

    table.add_row("Add", str(add))
    table.add_row("Change", str(change))
    table.add_row("Destroy", str(destroy))

    console.print(table)

# ---------- AI OUTPUT ----------

def show_ai_output(ai_text):
    try:
        data = json.loads(ai_text)
    except Exception:
        console.print(Panel(ai_text, title="AI Output", style="cyan"))
        return

    console.print(Panel(
        data.get("summary", ""),
        title="🧠 AI Summary",
        style="bold cyan"
    ))

    changes = data.get("changes", [])
    if changes:
        table = Table(title="🔧 Planned Changes", show_lines=True)
        table.add_column("Change", style="yellow")
        for c in changes:
            table.add_row(c)
        console.print(table)

    console.print(Panel(
        data.get("impact", ""),
        title="📉 Impact",
        style="magenta"
    ))

    risk = data.get("risk_level", "UNKNOWN").upper()
    color = "green" if risk == "LOW" else "yellow" if risk == "MEDIUM" else "red"

    console.print(Panel(
        risk,
        title="⚠️ Risk Level",
        style=color
    ))

    console.print(Panel(
        data.get("recommendation", ""),
        title="✅ Recommendation",
        style="bold green"
    ))

def show_cost_trend(trends):
    table = Table(title="📈 Cost Trend (Last Runs)", show_lines=True)
    table.add_column("Time", style="cyan")
    table.add_column("Monthly Cost ($)", style="magenta")

    for t in trends:
        table.add_row(t["timestamp"], str(t["monthly_cost"]))

    console.print(table)