# scripts/common.py

def priority_score(priority):

    return {
        "HIGH": 1000,
        "NORMAL": 100,
        "LOW": 10
    }.get(priority, 0)
