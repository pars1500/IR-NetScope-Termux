import time
import socket
import subprocess
import re
import requests
import dns.resolver

from modules.scoring import latency_score, jitter_score, grade


def fail(name):
    return {
        "test": name,
        "result": "FAIL",
        "latency": None,
        "score": 0,
        "grade": "F"
    }


def ping_test(target="1.1.1.1"):
    try:
        r = subprocess.run(
            ["ping", "-c", "4", target],
            capture_output=True,
            text=True,
            timeout=12
        )

        loss_match = re.search(r"(\d+)% packet loss", r.stdout)
        avg_match = re.search(r"min/avg/max/(?:mdev|stddev) = [\d.]+/([\d.]+)/", r.stdout)

        loss = int(loss_match.group(1)) if loss_match else 100
        latency = float(avg_match.group(1)) if avg_match else None

        score = latency_score(latency) - (loss * 3)
        score = max(0, min(100, score))

        return {
            "test": "Ping",
            "result": "PASS" if loss < 100 else "FAIL",
            "latency": latency,
            "score": score,
            "grade": grade(score)
        }

    except Exception:
        return fail("Ping")


def jitter_test(target="1.1.1.1"):
    try:
        r = subprocess.run(
            ["ping", "-c", "8", target],
            capture_output=True,
            text=True,
            timeout=18
        )

        times = [float(x) for x in re.findall(r"time=([\d.]+) ms", r.stdout)]

        if len(times) < 2:
            return fail("Jitter")

        diffs = [abs(times[i] - times[i - 1]) for i in range(1, len(times))]
        jitter = round(sum(diffs) / len(diffs), 2)

        score = jitter_score(jitter)

        return {
            "test": "Jitter",
            "result": "PASS",
            "latency": jitter,
            "score": score,
            "grade": grade(score)
        }

    except Exception:
        return fail("Jitter")


def dns_test(name, server):
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [server]
        resolver.timeout = 3
        resolver.lifetime = 3

        start = time.time()
        resolver.resolve("example.com", "A")
        latency = round((time.time() - start) * 1000, 2)

        score = latency_score(latency)

        return {
            "test": name,
            "result": "PASS",
            "latency": latency,
            "score": score,
            "grade": grade(score)
        }

    except Exception:
        return fail(name)


def tcp_test(name, host, port):
    try:
        start = time.time()
        s = socket.create_connection((host, port), timeout=5)
        s.close()

        latency = round((time.time() - start) * 1000, 2)
        score = latency_score(latency)

        return {
            "test": name,
            "result": "OPEN",
            "latency": latency,
            "score": score,
            "grade": grade(score)
        }

    except Exception:
        return fail(name)


def http_test(name, url):
    try:
        start = time.time()
        r = requests.get(url, timeout=8)
        latency = round((time.time() - start) * 1000, 2)

        score = latency_score(latency)

        return {
            "test": name,
            "result": "PASS" if r.status_code < 400 else "WARN",
            "latency": latency,
            "score": score,
            "grade": grade(score)
        }

    except Exception:
        return fail(name)


def traceroute_test(target="1.1.1.1"):
    try:
        r = subprocess.run(
            ["traceroute", target],
            capture_output=True,
            text=True,
            timeout=25
        )

        hops = len([
            line for line in r.stdout.splitlines()
            if re.match(r"^\s*\d+", line)
        ])

        if hops == 0:
            return fail("Traceroute")

        if hops <= 8:
            score = 100
        elif hops <= 14:
            score = 85
        elif hops <= 20:
            score = 70
        else:
            score = 50

        return {
            "test": "Traceroute",
            "result": f"{hops} Hops",
            "latency": None,
            "score": score,
            "grade": grade(score)
        }

    except Exception:
        return fail("Traceroute")


def vpn_readiness(name, score, requirement):
    if score >= 80:
        result = "READY"
    elif score >= 60:
        result = "LIMIT"
    else:
        result = "POOR"

    return {
        "test": name,
        "result": result,
        "latency": None,
        "score": score,
        "grade": grade(score)
    }


def run_assessment():
    results = []

    ping = ping_test("1.1.1.1")
    jitter = jitter_test("1.1.1.1")

    cf_dns = dns_test("Cloudflare DNS", "1.1.1.1")
    google_dns = dns_test("Google DNS", "8.8.8.8")
    quad9_dns = dns_test("Quad9 DNS", "9.9.9.9")

    cf_http = http_test("Cloudflare", "https://cloudflare.com")
    github_http = http_test("GitHub", "https://github.com")

    tcp_443 = tcp_test("TCP 443", "cloudflare.com", 443)
    tcp_80 = tcp_test("TCP 80", "cloudflare.com", 80)
    tcp_53 = tcp_test("DNS TCP 53", "1.1.1.1", 53)

    route = traceroute_test("1.1.1.1")

    results.extend([
        ping,
        jitter,
        cf_dns,
        google_dns,
        quad9_dns,
        cf_http,
        github_http,
        tcp_443,
        tcp_80,
        tcp_53,
    ])

    dns_score = round((cf_dns["score"] + google_dns["score"] + quad9_dns["score"]) / 3)
    tcp_score = round((tcp_443["score"] + tcp_80["score"]) / 2)
    base_score = round((ping["score"] + jitter["score"] + dns_score + tcp_score) / 4)

    wireguard_score = round((base_score + tcp_443["score"] + jitter["score"]) / 3)
    openvpn_score = round((base_score + tcp_443["score"] + tcp_80["score"]) / 3)
    warp_score = round((base_score + cf_dns["score"] + tcp_443["score"]) / 3)
    psiphon_score = round((base_score + tcp_443["score"] + github_http["score"]) / 3)

    v2ray_score = round((base_score + tcp_443["score"] + cf_http["score"]) / 3)
    xray_score = v2ray_score
    trojan_score = round((tcp_443["score"] + cf_http["score"]) / 2)
    shadowsocks_score = round((base_score + tcp_443["score"]) / 2)

    hysteria_score = round((base_score + jitter["score"]) / 2)
    tuic_score = round((base_score + jitter["score"]) / 2)
    singbox_score = round((wireguard_score + v2ray_score + hysteria_score) / 3)

    results.extend([
        vpn_readiness("WireGuard", wireguard_score, "UDP/Tunnel readiness"),
        vpn_readiness("OpenVPN", openvpn_score, "TCP/UDP readiness"),
        vpn_readiness("WARP", warp_score, "Cloudflare readiness"),
        vpn_readiness("Psiphon", psiphon_score, "Fallback readiness"),
        vpn_readiness("V2Ray", v2ray_score, "TLS/TCP readiness"),
        vpn_readiness("Xray", xray_score, "TLS/TCP readiness"),
        vpn_readiness("Trojan", trojan_score, "TLS 443 readiness"),
        vpn_readiness("Shadowsocks", shadowsocks_score, "Proxy readiness"),
        vpn_readiness("Hysteria", hysteria_score, "UDP stability readiness"),
        vpn_readiness("TUIC", tuic_score, "UDP/QUIC readiness"),
        vpn_readiness("Sing-box", singbox_score, "Multi-protocol readiness"),
        route
    ])

    return results
