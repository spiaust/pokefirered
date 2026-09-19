"""Run the existing integration checks in dependency order."""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
checks = [
    ["test_maps.py"], ["test_title.py"], ["test_country.py"], ["test_evolution.py"],
    ["test_oxford.py"],
    ["test_chantilly.py"],
    ["test_oranienburg.py"],
    ["test_rail_journeys.py"],
    ["test_navigation.py"], ["test_cities.py"],
    ["test_trainers.py"], ["test_challenges.py"], ["test_challenge_rewards.py"], ["test_england_story.py"], ["test_oxford_gym.py"], ["test_gym_ui.py"], ["test_france_story.py"], ["test_chantilly_gym.py"], ["test_water_gym_ui.py"], ["test_germany_story.py"], ["test_oranienburg_gym.py"], ["test_electric_gym_ui.py"], ["test_ferry.py"], ["test_ride.py"], ["test_coast.py"], ["test_celebi.py"], ["test_time.py"], ["test_departure.py"], ["test_evac.py"], ["test_message.py"], ["test_shops.py"],
    ["test_relief.py"], ["test_garden.py"], ["test_journal.py"], ["test_tour_journal.py"], ["test_amiens.py"], ["test_reunion.py"], ["test_amiens_care.py"], ["test_amiens_account.py"], ["test_amiens_news.py"], ["test_rouen.py"], ["test_rouen_riverside.py"], ["test_rouen_book.py"], ["test_rouen_care.py"], ["test_le_havre.py"], ["test_dock_check.py"], ["test_dock_care.py"], ["test_port_account.py"], ["test_port_return.py"], ["test_southampton.py"], ["test_luggage.py"], ["test_southampton_care.py"], ["test_south_return.py"], ["test_south_account.py"], ["test_london_past.py"], ["test_journal_pages.py"], ["test_trail_journey.py"],
    ["test_world.py", "england"], ["test_world.py", "france"],
    ["test_world.py", "germany"], ["test_trains.py"], ["test_tour.py"],
    ["test_save.py"], ["test_bicycle.py"], ["test_capture.py"],
]
for script, *args in checks:
    print(f"Running {script} {' '.join(args)}", flush=True)
    subprocess.run([sys.executable, str(root / "scripts" / script), *args],
                   # Cold saves now cover 221 checkpoints; allow roughly five seconds each.
                   cwd=root, check=True, timeout=1160 if script == "test_save.py" else 300)
print("All prototype integration checks passed.", flush=True)
