"""Resume guidance preserves every command and all other dialogue."""
from pathlib import Path
from rail_compatibility import before_resume_cues
R=Path(__file__).resolve().parents[1];raw=(R/'data/scripts/europe_train.inc').read_bytes()
assert before_resume_cues(raw)==(R/'data/geography/rail-resume-v106.inc').read_bytes()
for line in ['Your booking stays while you explore.','Board the next train?','NO opens the cancellation choice.']:assert line in raw.decode()
print('PASS: only saved-trip resume text changes; all routing, cancellation and warp commands retained')
