"""Detour guidance changes one resume line and preserves rail behavior."""
from pathlib import Path
from rail_compatibility import before_detour_cues
R=Path(__file__).resolve().parents[1];raw=(R/'data/scripts/europe_train.inc').read_bytes()
assert before_detour_cues(raw)==(R/'data/geography/rail-detour-v108.inc').read_bytes()
assert b'Route starts from this station.' in raw
print('PASS: only resume route-origin dialogue changes; all booking, cancellation, routing and warp commands retained')
