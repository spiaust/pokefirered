"""Clerk cues change text only, preserving all booking and travel commands."""
from pathlib import Path
import re
from rail_compatibility import before_clerk_cues,before_transfer_cues
R=Path(__file__).resolve().parents[1];raw=(R/'data/scripts/europe_train.inc').read_bytes()
assert before_clerk_cues(raw)==(R/'data/geography/rail-clerk-v104.inc').read_bytes()
s=before_transfer_cues(raw).decode()
for line in ['Choose a stop to preview your trip.','B or EXIT closes the stop list.','No booking is made until you board.','Talk to me to choose another stop.']:assert line in s
print('PASS: documented rail text updates retain all booking, cancellation, transfer and warp commands')
for label in ['Preview','Resume','Cancel','Canceled','Completed','Board','FinalBoard']:
 pattern=re.escape('Europe_Train_Text_'+label)+r'::'+chr(10)+r'(?:[ \t]*\.string[^\n]*\n)+'
 old=(R/'data/geography/rail-clerk-v104.inc').read_text();assert re.search(pattern,s).group(0)==re.search(pattern,old).group(0)
print('PASS: route preview, saved-journey confirmation and prior boarding commands remain compatible')
