"""Follow town/service/route transitions and cold Continue with normal controls."""
import json,re
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_tour import travel
from test_time import preserved
from key_item_test_helpers import reload

groups=json.loads((ROOT/'data/maps/map_groups.json').read_text())['gMapGroup_Europe']
constants={m[1]:int(m[2],0) for m in re.finditer(r'^#define (MUS_\w+)\s+(0x[0-9A-Fa-f]+|\d+)\b',(ROOT/'include/constants/songs.h').read_text(),re.M)}
songs=re.findall(r'^\s*song (\w+),',(ROOT/'sound/song_table.inc').read_text(),re.M)
def music(e):
 name=groups[e.location()[1]]
 constant=json.loads((ROOT/f'data/maps/{name}/map.json').read_text())['music']
 symbol=songs[constants[constant]]
 e.frames(180)
 assert e.read('gMPlayInfo_BGM')==e.symbols[symbol],(name,symbol,hex(e.read('gMPlayInfo_BGM')))
 assert e.read(e.symbols['gMPlayInfo_BGM']+4)&0xffff
 clock=e.read(e.symbols['gMPlayInfo_BGM']+12);e.frames(90)
 assert e.read(e.symbols['gMPlayInfo_BGM']+12)>clock
 return constant

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'europe-presentation-v125',True)
 original=preserved(e)[1:];history=tuple(e.var(v) for v in range(0x40C0,0x4100))
 for dest,city in enumerate(['London','Paris','Berlin','Oxford','Chantilly','Oranienburg']):
  if e.location()[1]!=dest*4:go(e,(16,14));travel(e,dest)
  assert music(e)=='MUS_EUROPE_'+city.upper()
  # Station entrance, indoor Save/Continue, and outdoor theme restoration.
  go(e,(23,10));e.walk('UP',1);e.frames(180)
  assert e.location()[:2]==(43,dest*4+2);assert music(e)=='MUS_PALLET'
  e=reload(e,'music-transition-'+city+'-station');assert music(e)=='MUS_PALLET'
  go(e,(4,7));e.walk('DOWN',2);e.frames(180)
  assert e.location()[:2]==(43,dest*4) and music(e)=='MUS_EUROPE_'+city.upper()
  assert preserved(e)[1:]==original
  print('PASS: '+city+' station music, indoor cold Continue and restored custom town theme retain saved progress',flush=True)
  # Nurse care, its fanfare, and Continue must not leave service music stuck.
  go(e,(6,10));e.walk('UP',1);e.frames(180)
  assert e.location()[:2]==(43,dest*4+3) and music(e)=='MUS_POKE_CENTER'
  e=reload(e,'music-transition-'+city+'-clinic');assert music(e)=='MUS_POKE_CENTER'
  e.walk('UP',4);e.walk('RIGHT',1);e.press('UP');e.press('A',180);e.finish_dialogue()
  assert music(e)=='MUS_POKE_CENTER'
  e.walk('DOWN',5);e.frames(180)
  assert e.location()[:2]==(43,dest*4) and music(e)=='MUS_EUROPE_'+city.upper()
  assert preserved(e)[1:]==original
  print('PASS: '+city+' clinic music, indoor cold Continue, nurse fanfare and restored town theme retain money/items/progress',flush=True)
  # The capitals connect north; the branch towns connect south.
  if dest<3:
   go(e,(15,14));e.walk('UP',15);e.frames(180)
  else:
   go(e,(15,23));e.walk('DOWN',1);e.frames(180)
  assert e.location()[:2]==(43,dest*4+1),e.location()
  route=music(e)
  e=reload(e,'music-transition-'+city+'-route');assert music(e)==route
  if dest<3:e.walk('DOWN',1)
  else:e.walk('UP',1)
  e.frames(180)
  assert e.location()[:2]==(43,dest*4) and music(e)=='MUS_EUROPE_'+city.upper()
  assert preserved(e)[1:]==original and tuple(e.var(v) for v in range(0x40C0,0x4100))==history
  print('PASS: '+city+' countryside boundary, route cold Continue and restored town theme retain completed activities',flush=True)
 e=reload(e,'music-transitions-v125');assert music(e)=='MUS_EUROPE_ORANIENBURG'
 assert preserved(e)[1:]==original and tuple(e.var(v) for v in range(0x40C0,0x4100))==history
 print('PASS: final cold Continue retains all completed activities after eighteen service/route music round trips',flush=True)
finally:e.close()
