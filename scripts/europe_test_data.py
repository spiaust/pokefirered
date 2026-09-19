"""Stable rail order and arrival states shared by the city integration checks."""
STOPS = ("england", "france", "germany", "oxford", "chantilly", "oranienburg")
CITIES = ("London", "Paris", "Berlin", "Oxford", "Chantilly", "Oranienburg")


def arrival_state(stop):
    return f"start-{stop}" if stop in STOPS[:3] else f"{stop}-arrival"
