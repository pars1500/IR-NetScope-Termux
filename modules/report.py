import os
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from modules.scoring import grade

console = Console()


def style_result(value):
    value = str(value)

    if value in ["PASS", "OPEN", "READY"]:
        return f"[green]{value}[/green]"

    if value in ["WARN", "LIMIT", "BLOCKED", "UNAVAILABLE"]:
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


def clean_text(value):
    return str(value).replace("[", "").replace("]", "")


def build_log_text(profile, package_name, results, avg_score, final_grade):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = []
    lines.append("IR-NetScope-Termux Network Assessment Log")
    lines.append("=" * 50)
    lines.append(f"Date/Time     : {now}")
    lines.append(f"Package       : {package_name}")
    lines.append(f"Score         : {avg_score}/100")
    lines.append(f"Grade         : {final_grade}")
    lines.append("")
    lines.append("NETWORK PROFILE")
    lines.append("-" * 50)
    lines.append(f"Public IP     : {profile.get('ip', '-')}")
    lines.append(f"Detected ISP  : {profile.get('provider', '-')}")
    lines.append(f"Raw Provider  : {profile.get('raw_provider', '-')}")
    lines.append(f"ASN           : {profile.get('asn', '-')}")
    lines.append(f"Location      : {profile.get('city', '-')} / {profile.get('country', '-')}")
    lines.append(f"Source        : {profile.get('source', '-')}")
    lines.append("")
    lines.append("TEST RESULTS")
    lines.append("-" * 50)
    lines.append(f"{'Test':30} {'Result':12} {'Latency':14} {'Score':8} {'Grade'}")
    lines.append("-" * 80)

    for item in results:
        latency = "-" if item["latency"] is None else f"{item['latency']} ms"
        lines.append(
            f"{item['test'][:30]:30} "
            f"{str(item['result'])[:12]:12} "
            f"{latency[:14]:14} "
            f"{str(item['score'])[:8]:8} "
            f"{item['grade']}"
        )

    lines.append("")
    lines.append("GRADE LEGEND")
    lines.append("-" * 50)
    lines.append("A+ Excellent")
    lines.append("A  Very Good")
    lines.append("B  Good")
    lines.append("C  Fair")
    lines.append("D  Poor")
    lines.append("F  Critical")
    lines.append("")
    lines.append("NOTE")
    lines.append("-" * 50)
    lines.append("VPN and protocol results are readiness assessments.")
    lines.append("They estimate network compatibility and do not run official VPN clients.")

    return "\n".join(lines)


def ask_save_log(profile, package_name, results, avg_score, final_grade):
    answer = input("\nDo you want to save a log file? (y/n): ").strip().lower()

    if answer not in ["y", "yes"]:
        console.print("[yellow]Log file was not saved.[/yellow]")
        return

    folder = "/sdcard/Download/IR-NetScope-Logs"

    try:
        os.makedirs(folder, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"IR-NetScope_Log_{timestamp}.txt"
        path = os.path.join(folder, filename)

        text = build_log_text(profile, package_name, results, avg_score, final_grade)

        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

        console.print(Panel.fit(
            f"[green]Log file saved successfully.[/green]\n\n{path}",
            title="LOG SAVED",
            border_style="green"
        ))

    except Exception as e:
        console.print(Panel.fit(
            f"[red]Failed to save log file.[/red]\n\n{e}\n\n"
            "Tip: Run this command first:\n"
            "termux-setup-storage",
            title="LOG ERROR",
            border_style="red"
        ))


def show_report(profile, package_name, results):
    avg_score = round(sum(item["score"] for item in results) / len(results), 2)
    final_grade = grade(avg_score)

    console.print(Panel.fit(
        f"[bold]Public IP:[/bold] {profile.get('ip', '-')}\n"
        f"[bold]Detected ISP:[/bold] {profile.get('provider', '-')}\n"
        f"[bold]ASN:[/bold] {profile.get('asn', '-')}\n"
        f"[bold]Location:[/bold] {profile.get('city', '-')} / {profile.get('country', '-')}\n"
        f"[bold]Package:[/bold] {package_name}\n"
        f"[bold]Score:[/bold] {avg_score}/100\n"
        f"[bold]Grade:[/bold] {style_grade(final_grade)}",
        title="NETWORK PROFILE",
        border_style="blue"
    ))

    table = Table(title="IR-NetScope-Termux Report", expand=True)
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
    limited = [x["test"] for x in results if x["result"] in ["LIMIT", "POOR", "FAIL", "BLOCKED"]]

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

    ask_save_log(profile, package_name, results, avg_score, final_grade)
