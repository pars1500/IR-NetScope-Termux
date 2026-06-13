import time
import socket
import subprocess
import re
import requests
import dns.resolver

from modules.scoring import latency_score, jitter_score, grade


def clamp(score):
    return max(0, min(100, int(score)))


def avg(*scores):
    valid = [s for s in scores if isinstance(s, (int, float))]
    if not valid:
        return 0
    return clamp(sum(valid) / len(valid))


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

        score = latency_score(latency) - (loss * 2)
        score = clamp(score)

        return {
            "test": "ICMP Ping",
            "result": "PASS" if loss < 100 else "BLOCKED",
            "latency": latency,
            "score": score,
            "grade": grade(score)
        }

    except Exception:
        return fail("ICMP Ping")


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
            return {
                "test": "ICMP Jitter",
                "result": "UNAVAILABLE",
                "latency": None,
                "score": 50,
                "grade": "D"
            }

        diffs = [abs(times[i] - times[i - 1]) for i in range(1, len(times))]
        jitter = round(sum(diffs) / len(diffs), 2)

        score = jitter_score(jitter)

        return {
            "test": "ICMP Jitter",
            "result": "PASS",
            "latency": jitter,
            "score": score,
            "grade": grade(score)
        }

    except Exception:
        return {
            "test": "ICMP Jitter",
            "result": "UNAVAILABLE",
            "latency": None,
            "score": 50,
            "grade": "D"
        }


def dns_test(name, server):
    try:
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = [server]
        resolver.timeout = 4
        resolver.lifetime = 4

        start = time.time()
        resolver.resolve("google.com", "A")
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
        r = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "IR-NetScope-Termux"}
        )
        latency = round((time.time() - start) * 1000, 2)

        score = latency_score(latency)

        return {
            "test": name,
            "result": "PASS" if r.status_code < 500 else "WARN",
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
            return {
                "test": "Traceroute",
                "result": "BLOCKED",
                "latency": None,
                "score": 50,
                "grade": "D"
            }

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
        return {
            "test": "Traceroute",
            "result": "UNAVAILABLE",
            "latency": None,
            "score": 50,
            "grade": "D"
        }


def readiness(name, score):
    score = clamp(score)

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

    cf_http = http_test("Cloudflare HTTPS", "https://1.1.1.1")
    github_http = http_test("GitHub HTTPS", "https://github.com")
    google_http = http_test("Google HTTPS", "https://google.com")

    tcp_443 = tcp_test("TCP 443", "cloudflare.com", 443)
    tcp_80 = tcp_test("TCP 80", "cloudflare.com", 80)
    tcp_53 = tcp_test("DNS TCP 53", "1.1.1.1", 53)

    mqtt_tcp = tcp_test("MQTT TCP 1883", "test.mosquitto.org", 1883)

    route = traceroute_test("1.1.1.1")

    results.extend([
        ping,
        jitter,
        cf_dns,
        google_dns,
        quad9_dns,
        cf_http,
        github_http,
        google_http,
        tcp_443,
        tcp_80,
        tcp_53,
        mqtt_tcp,
    ])

    dns_score = avg(cf_dns["score"], google_dns["score"], quad9_dns["score"])
    http_score = avg(cf_http["score"], github_http["score"], google_http["score"])
    tcp_score = avg(tcp_443["score"], tcp_80["score"], tcp_53["score"])

    # Important:
    # ICMP ping may be blocked by mobile operators.
    # So base score depends mainly on DNS/HTTPS/TCP, not ICMP.
    base_score = avg(dns_score, http_score, tcp_score)

    tls_score = avg(tcp_443["score"], cf_http["score"], github_http["score"])
    websocket_score = avg(tcp_443["score"], github_http["score"], google_http["score"])
    polling_score = avg(tcp_443["score"], tcp_80["score"], http_score)
    tunnel_score = avg(base_score, tcp_443["score"], tls_score)
    udp_like_score = avg(base_score, jitter["score"], tcp_443["score"]) - 5
    legacy_vpn_score = avg(base_score, tcp_score) - 10
    mqtt_score = avg(mqtt_tcp["score"], tcp_443["score"], dns_score)
    grpc_score = avg(tcp_443["score"], tls_score, http_score)

    web_realtime = [
        ("WebSocket", websocket_score),
        ("WSS", tls_score),
        ("WebTransport", avg(tls_score, jitter["score"], base_score)),
        ("SSE", polling_score),
        ("Long Polling", polling_score),
        ("BOSH", polling_score - 5),
        ("WStunnel", tunnel_score),
        ("WebTunnel", tunnel_score),
        ("MQTT", mqtt_score),
        ("gRPC Streaming", grpc_score),
        ("WSMux", websocket_score - 3),
        ("WSSMux", tls_score - 3),
        ("HELIUM-WebSocket", websocket_score - 5),
    ]

    vpn_stack = [
        ("PPTP", legacy_vpn_score - 15),
        ("L2TP", legacy_vpn_score - 8),
        ("L2TP/IPsec", avg(legacy_vpn_score, udp_like_score) - 6),
        ("SSTP", tls_score),
        ("IKEv1", udp_like_score - 8),
        ("IKEv2", udp_like_score),
        ("IKEv2/IPsec", avg(udp_like_score, dns_score)),
        ("IPsec ESP/AH", udp_like_score - 10),
        ("OpenVPN UDP", udp_like_score),
        ("OpenVPN TCP", tls_score),
        ("WireGuard", avg(base_score, jitter["score"], tcp_443["score"])),
        ("SoftEther", avg(tls_score, tcp_score, http_score)),
        ("Shadowsocks", avg(base_score, tcp_443["score"])),
        ("SOCKS5", avg(tcp_score, dns_score)),
        ("V2Ray VMess", avg(tls_score, websocket_score, dns_score)),
        ("Trojan", tls_score),
        ("Outline", avg(base_score, tcp_443["score"], dns_score)),
        ("ZeroTier", udp_like_score - 5),
        ("Tinc", avg(base_score, tcp_score) - 5),
        ("OpenConnect AnyConnect", tls_score),
        ("SSTap", avg(tcp_score, dns_score)),
        ("WireGuard over TCP", avg(tls_score, base_score)),
        ("NordLynx", avg(base_score, jitter["score"], tcp_443["score"])),
        ("Lightway ExpressVPN", avg(udp_like_score, tls_score)),
        ("Hydra Hotspot Shield", avg(udp_like_score, tls_score) - 5),
        ("Catapult HideMyAss", avg(udp_like_score, tls_score) - 5),
        ("Chameleon VyprVPN", avg(tls_score, websocket_score)),
        ("Mimic Norton", avg(tls_score, websocket_score)),
    ]

    for name, score in web_realtime:
        results.append(readiness(name, score))

    for name, score in vpn_stack:
        results.append(readiness(name, score))

    results.append(route)

    return results
