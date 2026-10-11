"""Native ordered circuit with explicit victory fixtures, not a balance proof."""
import json,re
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_shadow_runtime import talk,go,monfield,setstage,groups
from test_continent_runtime import var,battle_start
from test_landmark_cases import save
from test_eclipse_nordic import win
from test_eclipse_legendaries import flag
from test_oxford_gym import count_pocket
D=json.loads((ROOT/'data/eclipse-postgame.json').read_text())['champion_circuit']
SPECIES={a:int(b) for a,b in re.findall(r'#define (SPECIES_\w+)\s+(\d+)',(ROOT/'include/constants/species.h').read_text())}
MOVES={a:int(b) for a,b in re.findall(r'#define (MOVE_\w+)\s+(\d+)',(ROOT/'include/constants/moves.h').read_text())}
ITEMS={a:int(b) for a,b in re.findall(r'#define (ITEM_\w+)\s+(\d+)',(ROOT/'include/constants/items.h').read_text())}
COUNTERS={'BULBASAUR':('CHARIZARD','fire'),'CHARMANDER':('BLASTOISE','water'),'SQUIRTLE':('VENUSAUR','grass'),'CHIKORITA':('TYPHLOSION','fire'),'CYNDAQUIL':('FERALIGATR','water'),'TOTODILE':('MEGANIUM','grass'),'TREECKO':('BLAZIKEN','fire'),'TORCHIC':('SWAMPERT','water'),'MUDKIP':('SCEPTILE','grass')}
ACE_MOVES={'fire':'FLAMETHROWER EARTHQUAKE BRICK_BREAK SUNNY_DAY','water':'SURF ICE_BEAM EARTHQUAKE PROTECT','grass':'GIGA_DRAIN SUNNY_DAY SOLAR_BEAM TOXIC'}


def shelter(e,name):
 target=groups['gMapGroup_Shadow'].index(name)
 while e.location()[1]!=target:
  assert e.location()[0]==44 and not e.location()[1]&1
  old=e.location()[1];talk(e,(2,7) if old>target else (10,4));assert e.location()[1]!=old
 assert e.location()[:2]==(44,target)


def check_team(e,row,delta):
 starter=next(k for k in COUNTERS if SPECIES['SPECIES_'+k]==e.var(0x40f6))
 for j,mon in enumerate(row['party']):
  species=mon['species'];moves=mon['moves'];item=mon['item']
  if row['id']==391 and j==5:
   species,kind=COUNTERS[starter];moves=ACE_MOVES[kind].split();item='LUM_BERRY'
  assert e.read(e.symbols['gEnemyParty']+100*j+84,1)==row['level']+delta
  assert monfield(e,j,0,0,'gEnemyParty')&0xffff==SPECIES['SPECIES_'+species]
  assert monfield(e,j,0,2,'gEnemyParty')&0xffff==ITEMS['ITEM_'+item]
  assert [monfield(e,j,1,k,'gEnemyParty')&0xffff for k in (0,2,4,6)]==[MOVES['MOVE_'+m] for m in moves]
  assert not monfield(e,j,3,8,'gEnemyParty')&(1<<27)


def main():
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'eclipse-finished',True);assert e.location()[:2]==(44,40);e.write('sWildEncountersDisabled',1,1)
  setstage(e,20);talk(e,(5,6));assert e.var(0x40bf)==0
  setstage(e,21);talk(e,(5,6),'NO');assert e.var(0x40bf)==0
  talk(e,(6,4));assert e.var(0x40bf)==0 and not e.in_battle()
  talk(e,(5,6),'YES');assert e.var(0x40bf)==1
  talk(e,(6,4));assert e.var(0x40bf)==1 and not e.in_battle()
  for i,row in enumerate(D['trainers']):
   shelter(e,row['map'])
   if i<8 and not flag(e,0x8c6+i):talk(e,(6,4),'NO');assert flag(e,0x8c6+i)
   talk(e,(6,4),'NO');assert e.var(0x40bf)==i+1 and not e.in_battle()
   before=ROOT/f"test-output/circuit-pre-{row['id']}.state";e.state(before)
   for mode,delta in ((1,-4),(2,5),(0,0)):
    e.state(before,True);var(e,0x4090,mode);battle_start(e,(6,4));check_team(e,row,delta)
    if mode==0:win(e)
   assert e.var(0x40bf)==i+2 and e.var(0x408c)==21
   if i in (0,8,12):e.screenshot(ROOT/f"test-output/eclipse-circuit-{row['name'].lower()}.png")
   talk(e,(6,4));assert not e.in_battle() and e.var(0x40bf)==i+2
   if i==4:
    save(e,'eclipse-circuit-partial');e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'eclipse-circuit-partial',True);e.write('sWildEncountersDisabled',1,1)
    assert e.var(0x40bf)==6 and e.var(0x408c)==21
   print('PASS:',row['name'],'all three difficulty teams; native ordered victory',i+1,'of 13.',flush=True)
  ready=ROOT/'test-output/circuit-reward-ready.state';e.state(ready)
  pocket=e.read('gSaveBlock1Ptr')+0x430;slot=next(i for i in range(13) if e.read(pocket+4*i,2) in (0,1));key=e.read(e.read('gSaveBlock2Ptr')+0xf20,2)
  e.write(pocket+4*slot,1,2);e.write(pocket+4*slot+2,999^key,2)
  talk(e,(5,6));assert not flag(e,0x8dd) and e.var(0x40bf)==14
  e.state(ready,True);before=count_pocket(e,1,0x430,13);talk(e,(5,6))
  assert flag(e,0x8dd) and e.var(0x40bf)==15 and count_pocket(e,1,0x430,13)==before+1
  talk(e,(5,6),'NO');assert e.var(0x40bf)==15 and count_pocket(e,1,0x430,13)==before+1
  save(e,'eclipse-circuit-complete');e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'eclipse-circuit-complete',True)
  assert e.var(0x40bf)==15 and flag(e,0x8dd) and count_pocket(e,1,0x430,13)==before+1
  battle_start(e,(6,4));win(e);assert e.var(0x40bf)==15
  talk(e,(5,6),'YES');assert e.var(0x40bf)==1 and flag(e,0x8dd)
  # A completed second lap is a progress fixture: reward must never duplicate.
  var(e,0x40bf,14);talk(e,(5,6));assert e.var(0x40bf)==15 and count_pocket(e,1,0x430,13)==before+1
  print('PASS: start/order/decline, missing badge TM claims, partial/cold saves, full-ball-pocket retry, unique reward, free rematch and another-lap guard.',flush=True)
 finally:e.close()

if __name__=='__main__':main()
