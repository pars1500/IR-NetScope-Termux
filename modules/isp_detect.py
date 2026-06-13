import requests


def normalize_provider(text):
    if not text:
        return "Unknown"

    t = text.lower()

    known = {
        "mci": "MCI / Hamrah Aval",
        "hamrah": "MCI / Hamrah Aval",
        "mobile communication company": "MCI / Hamrah Aval",
        "irancell": "Irancell",
        "mtn": "Irancell",
        "rightel": "Rightel",
        "shatel": "Shatel",
        "asiatech": "Asiatech",
        "pars online": "Pars Online",
        "pishgaman": "Pishgaman",
        "mokhaberat": "Mokhaberat",
        "telecommunication company": "Mokhaberat",
        "hiweb": "HiWEB",
        "hi web": "HiWEB",
        "mobinnet": "Mobinnet",
    }

    for key, value in known.items():
        if key in t:
            return value

    return text


def detect_isp():
    services = [
        "https://ipapi.co/json/",
        "https://ipinfo.io/json",
        "https://ifconfig.co/json"
    ]

    for url in services:
        try:
            r = requests.get(url, timeout=8)
            data = r.json()

            ip = data.get("ip") or data.get("query") or "-"
            raw_provider = (
                data.get("org")
                or data.get("asn_org")
                or data.get("isp")
                or data.get("organization")
                or "Unknown"
            )

            provider = normalize_provider(raw_provider)

            asn = data.get("asn", "-")
            if asn == "-" and str(raw_provider).startswith("AS"):
                asn = str(raw_provider).split()[0]

            country = data.get("country_name") or data.get("country") or "-"
            city = data.get("city") or "-"

            if ip != "-" and provider != "Unknown":
                return {
                    "ip": ip,
                    "provider": provider,
                    "raw_provider": raw_provider,
                    "asn": asn,
                    "country": country,
                    "city": city,
                    "source": url
                }

        except Exception:
            continue

    return {
        "ip": "-",
        "provider": "Unknown",
        "raw_provider": "Unknown",
        "asn": "-",
        "country": "-",
        "city": "-",
        "source": "none"
    }
