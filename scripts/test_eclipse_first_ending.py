"""Original Champion victory still launches credits after rematch routing.
Explicit stage/defeated-flag and victory fixtures isolate the first-ending callback.
"""
from test_eclipse_circuit import *
from test_navigation import wait_task


def main():
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'eclipse-finished',True);setstage(e,20)
  n=0x500+252;p=e.read('gSaveBlock1Ptr')+0xee0+n//8;e.write(p,e.read(p,1)&~(1<<(n%8)),1)
  battle_start(e,(6,4));win(e,finish=False)
  for _ in range(50):
   if e.task_active('Task_EuropeMap'):break
   e.press('A',90)
  wait_task(e,'Task_EuropeMap');assert e.var(0x408c)==21 and e.var(0x40bf)==0
  for i in range(3):
   e.screenshot(ROOT/f'test-output/eclipse-first-ending-{i}.png')
   if i<2:e.press('A',90)
  e.press('B',240);e.finish_dialogue();assert flag(e,0x82c) and e.location()[:2]==(44,40)
  print('PASS: original Champion victory advances the main ending, launches all three credits pages and returns to the shelter without starting the circuit.',flush=True)
 finally:e.close()

if __name__=='__main__':main()
