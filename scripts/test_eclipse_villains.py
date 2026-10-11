"""Native villain field/battle rendering QA. Uses earned checkpoint with explicit
chapter, trainer-defeat and remnant-order fixtures to isolate artwork; no balancing claims.
"""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_shadow_runtime import go,talk,setstage
from test_continent_runtime import world,var
from test_country import wait_menu
import json,hashlib
BASE=ROOT/'graphics/eclipse_villains'
NAMES=['grunt','veil','boreal','patrol','vex','rime','warden','director']
def bytes_at(e,p,n):return bytes(e.read(p+i,1) for i in range(n))
def lz(e,p):
 assert e.read(p,1)==0x10
 size=e.read(p+1,1)|(e.read(p+2,1)<<8)|(e.read(p+3,1)<<16);p+=4;out=bytearray()
 while len(out)<size:
  flags=e.read(p,1);p+=1
  for shift in range(7,-1,-1):
   if len(out)>=size:break
   if flags&(1<<shift):
    a,b=e.read(p,1),e.read(p+1,1);p+=2
    count=(a>>4)+3;offset=((a&15)<<8|b)+1
    for _ in range(count):out.append(out[-offset])
   else:out.append(e.read(p,1));p+=1
 return bytes(out[:size])
def sprite_data(e,sid):
 p=e.symbols['gSprites']+68*sid
 return p,e.read(p+4,2)&1023,e.read(p+5,1)>>4

def field_check(e,name,visible=True):
 gfx=201+NAMES.index(name)
 slots=[i for i in range(16) if e.read(e.symbols['gObjectEvents']+36*i,1)&1 and e.read(e.symbols['gObjectEvents']+36*i+5,1)==gfx]
 assert slots,(name,e.location(),'missing field actor')
 p=e.symbols['gObjectEvents']+36*slots[0];sid=e.read(p+4,1);sp,tile,pal=sprite_data(e,sid)
 assert 12<=pal<16,(name,'palette collision',pal)
 assert bytes_at(e,0x6010000+32*tile,256)==bytes_at(e,e.symbols['gObjectEventPic_Eclipse'+name.title()],256),(name,'walking sprite tiles')
 raw=bytes_at(e,e.symbols['gObjectEventPal_EclipseVillains'],32)
 actual=bytes_at(e,e.symbols['gPlttBufferUnfaded']+512+32*pal,32)
 if e.location()[0]==44 and e.location()[1] in [24,26,28]:
  assert actual!=raw,(name,'historical tint missing')
 else:assert actual==raw,(name,'field palette colors changed')
 flags=e.read(e.symbols['gSprites']+68*sid+0x3e,2)
 assert flags&1
 if visible:assert not flags&4,(name,'field actor invisible')
 checks=json.loads((BASE/'overworld/frame_checksums.json').read_text())[name]
 sheet=e.symbols['gObjectEventPic_Eclipse'+name.title()]
 for frame in range(9):assert hashlib.sha256(bytes_at(e,sheet+256*frame,256)).hexdigest()==checks[frame],(name,frame,'native frame packing differs from PNG pixels')
 e.screenshot(ROOT/f'test-output/villain-{name}-field.png')
 return pal

def enter_battle(e,target,trainer,name):
 go(e,target);e.press('UP');e.press('A',180);wait_menu(e,'Task_YesNoMenu_HandleInput');e.press('A',30)
 pic=148+NAMES.index(name)
 for _ in range(160):
  if e.in_battle():
   sid=e.read(e.symbols['gBattlerSpriteIds']+1,1)
   if sid<64:
    sp,tile,pal=sprite_data(e,sid)
    if e.read(sp+6,2)==pic and e.read(sp+0x3e,2)&1:break
  if e.in_battle():e.frames(8)
  else:e.press('A',30)
 else:
  e.screenshot(ROOT/f'test-output/villain-{name}-stalled.png')
  raise AssertionError((name,'trainer portrait did not load',e.location(),e.in_battle(),e.var(0x408c),e.read('gTrainerBattleOpponent_A',2),[(i,e.read(e.symbols['gSprites']+68*i+6,2)) for i in range(64) if e.read(e.symbols['gSprites']+68*i+0x3e,2)&1]))
 assert e.read('gTrainerBattleOpponent_A',2)==trainer
 # Let the trainer finish sliding into view without advancing the battle text.
 e.frames(180);sp,tile,pal=sprite_data(e,sid)
 raw=lz(e,e.symbols['gTrainerFrontPic_Eclipse'+name.title()])
 assert len(raw)==2048 and bytes_at(e,0x6010000+32*tile,2048)==raw,(name,'battle portrait VRAM')
 colors=lz(e,e.symbols['gTrainerPalette_Eclipse'+name.title()])
 assert bytes_at(e,e.symbols['gPlttBufferUnfaded']+512+32*pal,32)==colors,(name,'battle palette')
 e.screenshot(ROOT/f'test-output/villain-{name}-battle.png')
 print('PASS:',name,'native field palette and tiles, battle portrait and palette',flush=True)

def main():
 countries=json.loads((ROOT/'data/continent-campaign.json').read_text())['countries']
 groups=json.loads((ROOT/'data/maps/map_groups.json').read_text())['gMapGroup_Continent']
 cases=[('grunt',6,148),('veil',8,164),('patrol',12,196),('warden',13,203),('director',14,210),('vex',21,376),('rime',21,377),('boreal',21,378)]
 for name,stage,trainer in cases:
  e=Emulator(ROOT/'pokefirered.gba')
  try:
   load_checkpoint(e,'natural-league-20-complete',True)
   var(e,0x40d1,1);e.write('sWildEncountersDisabled',1,1)
   if name in ['vex','rime','boreal']:
    city={'vex':'Copenhagen','rime':'Oslo','boreal':'Stockholm'}[name]
    var(e,0x40bd,{'vex':1,'rime':2,'boreal':3}[name]);world(e,groups.index('Continent'+city)//2)
    o=next(o for o in json.loads((ROOT/f'data/maps/Continent{city}/map.json').read_text())['object_events'] if o['script']=='EclipseNordic_'+name.title())
    target=(o['x'],o['y']+1);go(e,target)
   else:
    setstage(e,stage);talk(e,(6,7));talk(e,(10,16),'YES')
    assert e.location()[:2]==(44,2*stage),e.location();target=(6,4);go(e,target)
   flag=0x500+trainer;p=e.read('gSaveBlock1Ptr')+0xee0+flag//8
   e.write(p,e.read(p,1)&~(1<<(flag%8)),1)
   field_check(e,name);enter_battle(e,target,trainer,name)
  finally:e.close()

if __name__=='__main__':main()
