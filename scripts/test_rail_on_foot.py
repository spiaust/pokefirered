"""Old-ROM walking arrivals, completion, rebooking and cold Continue."""
import sys
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint,STORY
from test_landmark_cases import go,save
from test_time import preserved
from test_country import wait_menu
from rail_test_helpers import BOOKING,choose_destination,board,speak_from_arrival
from test_oxford import walk_to_oxford
from test_chantilly import walk_to_chantilly
from test_oranienburg import walk_to_oranienburg
VARS=(STORY,0x40ef,0x40f0,*range(0x40f2,0x4100))
CASES=[('oxford','start-france',1,0,3,walk_to_oxford),('chantilly','start-england',0,1,4,walk_to_chantilly),('oranienburg','start-france',1,2,5,walk_to_oranienburg)]
def without_booking(value):
 value=list(value);variables=list(value[2]);variables[VARS.index(BOOKING)]=0;value[2]=tuple(variables);return tuple(value)

if '--prepare' in sys.argv:
 for tag,checkpoint,origin,capital,destination,walk in CASES:
  e=Emulator(ROOT/'artifacts/releases/Pokemon-European-Tour-v1.07.gba')
  try:
   load_checkpoint(e,checkpoint,True);before=without_booking(preserved(e))[1:]
   go(e,(23,10));e.walk('UP',1);e.frames(180);e.walk('UP',1);speak_from_arrival(e)
   choose_destination(e,destination);board(e,capital,destination)
   e.walk('DOWN',2);e.frames(180);go(e,(15,14));walk(e)
   assert e.var(BOOKING)==destination+1 and without_booking(preserved(e))[1:]==before
   go(e,(23,10));e.walk('UP',1);e.frames(180);e.walk('UP',1);go(e,(7,7))
   assert e.location()==(43,destination*4+2,7,7)
   save(e,'rail-foot-'+tag+'-v107')
   print('Prepared genuine v1.07 booked walking arrival: '+tag,flush=True)
  finally:e.close()
else:
 for tag,checkpoint,origin,capital,destination,walk in CASES:
  e=Emulator(ROOT/'pokefirered.gba')
  try:
   load_checkpoint(e,'rail-foot-'+tag+'-v107',True)
   assert e.location()==(43,destination*4+2,7,7) and e.var(BOOKING)==destination+1
   before=preserved(e);e.press('UP');e.press('A',900)
   assert e.read('sLockFieldControls',1) and e.var(BOOKING)==0
   assert e.read('gStringVar3',1)==0xa1
   expected=bytes([0xbb+ord(c)-65 for c in tag.upper()]+[255])
   assert bytes(e.read(e.symbols['gStringVar1']+i,1) for i in range(len(expected)))==expected
   e.screenshot(ROOT/f'test-output/rail-foot-{tag}-0.png');e.press('A',900)
   e.screenshot(ROOT/f'test-output/rail-foot-{tag}-1.png');e.finish_dialogue()
   assert not e.read('sLockFieldControls',1) and e.location()==(43,destination*4+2,7,7)
   assert without_booking(preserved(e))==without_booking(before)
   # A second interaction must offer a fresh trip, not repeat completion.
   e.press('A',180);wait_menu(e,'Task_MultichoiceMenu_HandleInput');e.press('B',180);e.finish_dialogue()
   assert e.var(BOOKING)==0 and without_booking(preserved(e))==without_booking(before)
   save(e,'rail-foot-'+tag+'-complete');saved=preserved(e)
   print('PASS: '+tag+' old walking-arrival save names destination, clears only booking, releases controls and offers a fresh trip',flush=True)
  finally:e.close()
  e=Emulator(ROOT/'pokefirered.gba')
  try:
   load_checkpoint(e,'rail-foot-'+tag+'-complete',True)
   assert preserved(e)==saved and e.var(BOOKING)==0
   e.press('UP');e.press('A',180);choose_destination(e,capital);board(e,capital,capital)
   assert e.var(BOOKING)==0 and without_booking(preserved(e))[1:]==without_booking(saved)[1:]
   e.screenshot(ROOT/f'test-output/rail-foot-{tag}-return.png')
   print('PASS: '+tag+' completed save cold Continues without stale booking and boards a new return train',flush=True)
  finally:e.close()
