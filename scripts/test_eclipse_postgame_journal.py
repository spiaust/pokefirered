"""Native read-only postgame journal with explicit progress fixtures.
Covers every lead, active circuit priority, care gates and stable campaign leads.
No battle wins or reward claims are asserted from these fixtures.
"""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_continent_runtime import var
from test_gym_ui import open_key_item
from test_navigation import wait_task
from test_journal import journal_task
from test_time import preserved
import json,re

def setflag(e,n,on):
 p=e.read('gSaveBlock1Ptr')+0xee0+n//8
 old=e.read(p,1);bit=1<<(n%8);e.write(p,old|bit if on else old&~bit,1)
def record(e):
 p=e.read('gSaveBlock1Ptr')
 return e.location(),preserved(e),tuple(e.var(v) for v in range(0x408c,0x40d2)),bytes(e.read(p+0xee0+i,1) for i in range(0x8ce//8,0x8e0//8+1))
def inspect(e,lead,label):
 before=record(e);open_key_item(e,361);wait_task(e,'Task_EuropeMap')
 e.press('SELECT',60);t=journal_task(e)
 assert e.read(t+16,2)==1
 e.press('DOWN',60);assert e.read(t+16,2)==0
 e.press('UP',60);assert e.read(t+16,2)==1
 assert e.read(t+12,2)==lead,(label,e.read(t+12,2),lead)
 if lead>=47:assert e.read(t+14,2)==127
 if label:e.screenshot(ROOT/f'test-output/postgame-journal-{label}.png')
 e.press('A',60);assert e.read(t+10,2)==2
 e.press('SELECT',60);e.press('START',180);wait_task(e,'Task_BagMenu_HandleInput')
 e.press('B',180);e.press('B',90)
 assert record(e)==before,(label,'journal changed saved state')

def main():
 # Validate the stored native font against every new line before runtime QA.
 rows=json.loads((ROOT/'data/eclipse-postgame-journal.json').read_text())['rows']
 font=(ROOT/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontSmallLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
 chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(ROOT/'charmap.txt').read_text(encoding='utf-8'),re.M)}
 for row in rows:
  for s in row:assert len(s)<44 and sum(widths[chars[c]] for c in s)<=226,s
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'natural-league-20-complete',True)
  base=ROOT/'test-output/postgame-journal-base.state';e.state(base)
  cases=[]
  for n in range(5):cases.append((n,0,0,0,0,0,False,47+n,'nordic-'+str(n)))
  cases.append((0,1,0,0,0,0,True,53,'active-krakow'))
  cases.extend([(5,0,0,0,0,0,False,80,'warsaw-memory'),(5,0,0,0,0,0,True,52,'krakow-start'),(5,1,0,0,0,0,True,53,'krakow-work'),(5,2,0,0,0,0,True,54,'krakow-reward'),(5,1,0,0,0,7,True,54,'krakow-work-ready'),(5,3,0,0,0,0,True,55,'circuit-start')])
  # An active circuit remains visible even when other optional quests are unfinished.
  for n in range(1,15):cases.append((0,0,n,0,0,0,False,55+n if n<14 else 69,'circuit-'+str(n)))
  for n in range(7):cases.append((5,3,15,(1<<n)-1,6,0,True,70+n,'guardian-'+str(n)))
  cases.extend([(5,3,15,31,2,0,True,77,'care-three'),(5,3,15,63,5,0,True,78,'care-six'),(5,3,15,127,6,0,True,79,'all-complete')])
  for nordic,krakow,circuit,caught,purified,tasks,memory,lead,label in cases:
   e.state(base,True)
   for v,x in [(0x40bd,nordic),(0x40be,krakow),(0x40bf,circuit),(0x408f,purified),(0x40a5,8192 if memory else 0)]:var(e,v,x)
   for n in range(7):setflag(e,0x8ce+n,bool(caught&(1<<n)))
   for n in range(3):setflag(e,0x8d6+n,bool(tasks&(1<<n)))
   inspect(e,lead,label)
   print('PASS: native read-only lead',label,flush=True)
  for stage in [0,12,20]:
   e.state(base,True);var(e,0x408c,stage);inspect(e,25+stage,'campaign-'+str(stage))
  load_checkpoint(e,'natural-circuit-complete',True)
  from test_eclipse_legendaries import flag
  from test_oxford_gym import count_pocket
  assert e.var(0x40bf)==15 and flag(e,0x8dd) and count_pocket(e,1,0x430,13)==1
  inspect(e,47+e.var(0x40bd),'earned-circuit-complete')
  print('PASS: naturally earned final circuit and unique Master Ball load on the final journal ROM',flush=True)
  print('PASS: all 34 postgame leads, pending rewards, active-circuit priority, care gates, font widths and unchanged campaign leads',flush=True)
 finally:e.close()
if __name__=='__main__':main()
