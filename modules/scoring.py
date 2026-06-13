def grade(score):
    if score >= 95:
        return "A+"
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def latency_score(ms):
    if ms is None:
        return 0
    if ms <= 80:
        return 100
    if ms <= 150:
        return 90
    if ms <= 300:
        return 75
    if ms <= 600:
        return 55
    return 25


def jitter_score(ms):
    if ms is None:
        return 0
    if ms <= 20:
        return 100
    if ms <= 50:
        return 85
    if ms <= 100:
        return 70
    if ms <= 200:
        return 50
    return 20
