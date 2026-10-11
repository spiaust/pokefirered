"""Cold-load champion save, replay three credits pages and verify one-time network reward."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_shadow_runtime import go,talk
from test_continent_runtime import var
from test_navigation import wait_task
def item_count(e,item):
 bag=e.read('gSaveBlock1Ptr')+0x430;key=e.read(e.read('gSaveBlock2Ptr')+0xf20,2)
 return sum(e.read(bag+4*i+2,2)^key for i in range(13) if e.read(bag+4*i,2)==item)

def main():
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'eclipse-finished',True);assert e.var(0x408C)==21
  talk(e,(10,7));talk(e,(15,20))
  go(e,(6,4));e.press('UP');e.press('A',180)
  for _ in range(50):
   if e.task_active('Task_EuropeMap'):break
   e.press('A',90)
  wait_task(e,'Task_EuropeMap');e.frames(90)
  for i in range(3):
   e.screenshot(ROOT/f'test-output/eclipse-credits-{i}.png')
   if i<2:e.press('A',90)
  e.press('B',240);e.finish_dialogue();assert e.location()[:2]==(44,40)
  for bank in range(3):var(e,0x40A5+bank,0xffff if bank<2 else 0x7f)
  go(e,(7,8));e.press('RIGHT');before=item_count(e,1);e.press('A',180);e.finish_dialogue()
  assert e.var(0x40B3)==1 and item_count(e,1)==before+1
  e.press('A',180);e.finish_dialogue();assert item_count(e,1)==before+1
  e.screenshot(ROOT/'test-output/eclipse-network-finale.png')
  print('PASS: three native credits pages return to field; all-country epilogue awards one Master Ball without duplicates.',flush=True)
 finally:e.close()
if __name__=='__main__':main()
