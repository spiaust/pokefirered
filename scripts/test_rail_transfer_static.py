"""Intermediate guidance changes one text block and targets valid local notices."""
from pathlib import Path
import json
from rail_compatibility import before_transfer_cues,before_resume_cues
from rail_test_helpers import route
R=Path(__file__).resolve().parents[1];raw=(R/'data/scripts/europe_train.inc').read_bytes()
assert before_transfer_cues(before_resume_cues(raw))==(R/'data/geography/rail-transfer-v105.inc').read_bytes()
s=raw.decode()
for line in ['Trip ends: {STR_VAR_1}.','Read the wall notice for local walks.','Your booking stays while you explore.']:assert line in s
print('PASS: only intermediate boarding text changes; all rail state, routing, confirmation and warp commands retained')
intermediate=set()
for origin in range(6):
 for destination in range(6):intermediate.update(route(origin,destination)[:-1])
assert intermediate=={0,1,2}
for city in ['London','Paris','Berlin']:
 m=json.loads((R/f'data/maps/Europe{city}Station/map.json').read_text());assert any(e['script']==f'Europe{city}Station_LocalBoard' for e in m['bg_events'])
print('PASS: every possible intermediate rail stop has the referenced local-walk notice')
