from rich.console import Console
from rich.panel import Panel

from modules.network_tests import run_assessment
from modules.report import show_report

console = Console()

INTERNET_TYPES = {
    "1": "Fixed Internet",
    "2": "Mobile Internet"
}

PROVIDERS = {
    "1": "MCI / Hamrah Aval",
    "2": "Irancell",
    "3": "Rightel",
    "4": "Shatel",
    "5": "Asiatech",
    "6": "Pars Online",
    "7": "Pishgaman",
    "8": "Mokhaberat",
    "9": "HiWEB",
    "10": "Mobinnet",
    "11": "Other"
}


def select(title, options):
    while True:
        console.print(Panel.fit(title, border_style="cyan"))

        for key, value in options.items():
            console.print(f"[green]{key}[/green]) {value}")

        choice = input("\nSelect number: ").strip()

        if choice in options:
            return options[choice]

        console.print("[red]Invalid choice. Try again.[/red]")


def main():
    console.print(Panel.fit(
        "[bold cyan]NetScope-Termux[/bold cyan]\n"
        "One Click Professional Network Assessment",
        border_style="green"
    ))

    internet = select("Step 1 - Select Internet Type", INTERNET_TYPES)
    provider = select("Step 2 - Select Internet Provider", PROVIDERS)

    console.print(Panel.fit(
        "[green]1[/green]) Professional Network Assessment\n"
        "[red]0[/red]) Exit",
        title="Step 3 - Select Test",
        border_style="green"
    ))

    choice = input("\nSelect number: ").strip()

    if choice == "0":
        console.print("[red]Exit.[/red]")
        return

    console.print("\n[bold cyan]Running professional assessment...[/bold cyan]\n")

    profile = {
        "internet": internet,
        "provider": provider
    }

    results = run_assessment()
    show_report(profile, "Professional Network Assessment", results)


if __name__ == "__main__":
    main()
