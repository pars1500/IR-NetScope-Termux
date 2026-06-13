IR-NetScope-Termux

"Python" (https://img.shields.io/badge/Python-3.13-blue)
"Platform" (https://img.shields.io/badge/Platform-Termux-green)
"License" (https://img.shields.io/badge/License-MIT-orange)
"Status" (https://img.shields.io/badge/Status-Active-success)
"Network" (https://img.shields.io/badge/Network-Diagnostics-red)

Professional Network Assessment Tool for Android Termux

Screenshot

"NetScope-Termux" (screenshots/report.jpg)

"Network" (https://img.shields.io/badge/Network-Diagnostics-red)

Professional Network Assessment Tool for Android Termux

---

Features

- Internet Health Assessment
- Ping Analysis
- Jitter Analysis
- DNS Benchmark
- Cloudflare Connectivity Check
- TCP Connectivity Check
- Traceroute Analysis
- VPN Technology Readiness Assessment
- Network Quality Scoring
- Grade System (A+ to F)
- Mobile-Friendly Terminal Interface

---

Tested Technologies

- WireGuard
- OpenVPN
- WARP
- Psiphon
- V2Ray
- Xray
- Trojan
- Shadowsocks
- Hysteria
- TUIC
- Sing-box

---

Installation

Copy and run:

```bash

pkg update -y && pkg upgrade -y && \
pkg install git python traceroute inetutils -y && \
git clone https://github.com/pars1500/IR-NetScope-Termux.git && \
cd IR-NetScope-Termux && \
pip install -r requirements.txt


```

---

Run

```bash

cd IR-NetScope-Termux && python main.py

```

---

Update

```bash

cd IR-NetScope-Termux && git pull


```

---

Remove

```bash

rm -rf ~/IR-NetScope-Termux


```

---

Workflow

Step 1 - Select Internet Type

Fixed Internet
Mobile Internet

Step 2 - Select Internet Provider

MCI / Hamrah Aval
Irancell
Rightel
Shatel
Asiatech
Pars Online
Pishgaman
Mokhaberat
HiWEB
Mobinnet
Other

Step 3 - Run Professional Network Assessment

Step 4 - Review Results

---

Assessment Categories

Core Network
├── Ping
├── Jitter
└── Traceroute

DNS Services
├── Cloudflare DNS
├── Google DNS
└── Quad9 DNS

Cloudflare Ecosystem
├── Cloudflare Connectivity
└── Cloudflare Reachability

VPN Technology Readiness
├── WireGuard
├── OpenVPN
├── WARP
├── Psiphon
├── V2Ray
├── Xray
├── Trojan
├── Shadowsocks
├── Hysteria
├── TUIC
└── Sing-box

---

Example Report

NETWORK PROFILE

Internet : Mobile Internet
Provider : Irancell
Package  : Professional Network Assessment

Score    : 89/100
Grade    : B

+----------------+--------+---------+-------+-------+
| Test           | Result | Latency | Score | Grade |
+----------------+--------+---------+-------+-------+
| Ping           | PASS   | 82 ms   | 90    | A     |
| Jitter         | PASS   | 14 ms   | 95    | A     |
| Cloudflare DNS | PASS   | 43 ms   | 90    | A     |
| WireGuard      | READY  | -       | 91    | A     |
| OpenVPN        | READY  | -       | 90    | A     |
| WARP           | READY  | -       | 88    | B     |
| V2Ray          | READY  | -       | 90    | A     |
| Traceroute     | 11Hop  | -       | 80    | B     |
+----------------+--------+---------+-------+-------+

---

Grade System

A+  Excellent
A   Very Good
B   Good
C   Fair
D   Poor
F   Critical

---

Network Quality Interpretation

95 - 100   A+   Excellent
90 - 94    A    Very Good
80 - 89    B    Good
70 - 79    C    Fair
60 - 69    D    Poor
0  - 59    F    Critical

---

Project Goals

- Provide a simple network assessment tool for Android Termux users.
- Measure network stability and connectivity quality.
- Evaluate readiness for modern VPN technologies.
- Generate clear and actionable results.

---

Author

pars1500

License

MIT License
