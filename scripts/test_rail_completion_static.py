"""Walking completion changes dialogue only."""
from pathlib import Path
from rail_compatibility import before_completion_cues
R=Path(__file__).resolve().parents[1];raw=(R/'data/scripts/europe_train.inc').read_bytes()
assert before_completion_cues(raw)==(R/'data/geography/rail-completion-v107.inc').read_bytes()
for line in ['Destination: {STR_VAR_1}','Your booking is cleared.','Talk to me to choose another trip.']:assert line in raw.decode()
print('PASS: only walking-completion dialogue changes; all arrival, booking, routing and warp commands retained')
