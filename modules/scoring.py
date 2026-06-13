def grade(score):
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 65:
        return "C"
    if score >= 50:
        return "D"
    return "F"


def latency_score(ms):
    if ms is None:
        return 0
    if ms <= 100:
        return 100
    if ms <= 250:
        return 90
    if ms <= 500:
        return 75
    if ms <= 1000:
        return 60
    if ms <= 2500:
        return 45
    if ms <= 5000:
        return 30
    return 15


def jitter_score(ms):
    if ms is None:
        return 50
    if ms <= 30:
        return 100
    if ms <= 70:
        return 85
    if ms <= 150:
        return 65
    if ms <= 300:
        return 50
    return 30
