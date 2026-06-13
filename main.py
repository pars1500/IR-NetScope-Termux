from rich.console import Console
from rich.panel import Panel

from modules.network_tests import run_assessment
from modules.report import show_report
from modules.isp_detect import detect_isp

console = Console()


def main():
    console.print(Panel.fit(
        "[bold cyan]IR-NetScope-Termux[/bold cyan]\n"
        "One Click Professional Network Assessment",
        border_style="green"
    ))

    console.print("\n[bold cyan]Detecting ISP and Network Profile...[/bold cyan]\n")

    isp_info = detect_isp()

    console.print(Panel.fit(
        f"[bold]Public IP:[/bold] {isp_info['ip']}\n"
        f"[bold]Detected ISP:[/bold] {isp_info['provider']}\n"
        f"[bold]Raw Provider:[/bold] {isp_info['raw_provider']}\n"
        f"[bold]ASN:[/bold] {isp_info['asn']}\n"
        f"[bold]Location:[/bold] {isp_info['city']} / {isp_info['country']}\n"
        f"[bold]Source:[/bold] {isp_info['source']}",
        title="AUTO DETECTION",
        border_style="blue"
    ))

    console.print("\n[bold cyan]Starting professional assessment automatically...[/bold cyan]\n")

    profile = {
        "internet": "Auto Detected",
        "provider": isp_info["provider"],
        "raw_provider": isp_info["raw_provider"],
        "ip": isp_info["ip"],
        "asn": isp_info["asn"],
        "country": isp_info["country"],
        "city": isp_info["city"],
        "source": isp_info["source"]
    }

    results = run_assessment()
    show_report(profile, "Professional Network Assessment", results)


if __name__ == "__main__":
    main()
