from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from modules.scoring import grade

console = Console()


def style_result(value):
    value = str(value)

    if value in ["PASS", "OPEN", "READY"]:
        return f"[green]{value}[/green]"

    if value in ["WARN", "LIMIT"]:
        return f"[yellow]{value}[/yellow]"

    if value in ["FAIL", "POOR"]:
        return f"[red]{value}[/red]"

    return value


def style_grade(value):
    if value in ["A+", "A"]:
        return f"[bold green]{value}[/bold green]"
    if value in ["B", "C"]:
        return f"[yellow]{value}[/yellow]"
    return f"[bold red]{value}[/bold red]"


def show_report(profile, package_name, results):
    avg_score = round(sum(item["score"] for item in results) / len(results), 2)
    final_grade = grade(avg_score)

    console.print(Panel.fit(
        f"[bold]Internet:[/bold] {profile['internet']}\n"
        f"[bold]Provider:[/bold] {profile['provider']}\n"
        f"[bold]Package:[/bold] {package_name}\n"
        f"[bold]Score:[/bold] {avg_score}/100\n"
        f"[bold]Grade:[/bold] {style_grade(final_grade)}",
        title="NETWORK PROFILE",
        border_style="blue"
    ))

    table = Table(title="NetScope-Termux Report", expand=True)
    table.add_column("Test", style="cyan")
    table.add_column("Result", justify="center")
    table.add_column("Latency", justify="center")
    table.add_column("Score", justify="center")
    table.add_column("Grade", justify="center")

    for item in results:
        latency = "-" if item["latency"] is None else f"{item['latency']} ms"

        table.add_row(
            item["test"],
            style_result(item["result"]),
            latency,
            str(item["score"]),
            style_grade(item["grade"])
        )

    console.print(table)

    ready = [x["test"] for x in results if x["result"] == "READY"]
    limited = [x["test"] for x in results if x["result"] in ["LIMIT", "POOR", "FAIL"]]

    text = ""

    if ready:
        text += "Recommended Technologies:\n"
        for item in ready[:8]:
            text += f"✓ {item}\n"

    if limited:
        text += "\nLimitations:\n"
        for item in limited[:6]:
            text += f"⚠ {item}\n"

    if not text:
        text = "No critical issues detected."

    console.print(Panel.fit(
        text,
        title="NETWORK SUMMARY",
        border_style="green"
    ))

    console.print(Panel.fit(
        "A+ Excellent\n"
        "A  Very Good\n"
        "B  Good\n"
        "C  Fair\n"
        "D  Poor\n"
        "F  Critical",
        title="GRADE LEGEND",
        border_style="cyan"
    ))
