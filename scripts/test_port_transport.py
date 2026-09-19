"""Cold batteries exercise coastal cancellations, badges and real rail detours."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_coast import decline_checks,accept,crossing,finish_coastal_booking,coach,leave_port
from rail_test_helpers import BOOKING

for city,index in [('dover',27),('calais',28)]:
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'coast-'+city,True)
  assert e.location()==(43,index,8,5)
  path=ROOT/'test-output/port-transport-current.state';e.state(path)
  addr=e.read('gSaveBlock1Ptr')+0xEE0+0x822//8
  e.write(addr,e.read(addr,1)&~(1<<(0x822%8)),1)
  e.press('DOWN');e.press('A',180);e.finish_dialogue()
  assert e.location()==(43,index,8,5) and not e.task_active('Task_YesNoMenu_HandleInput')
  e.state(path,True);decline_checks(e,True);accept(e,55-index);crossing(e)
  leave_port(e);e.walk('DOWN',4);e.walk('LEFT',7);coach(e)
  decline_checks(e);accept(e,index)
  print(f'PASS: {city} cold battery, ferry badge gate, No/B, free round trip and coach entry',flush=True)
 finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'coast-booking',True)
 assert e.var(BOOKING)==3
 finish_coastal_booking(e)
 assert e.location()[:2]==(43,10) and e.var(BOOKING)==0
 print('PASS: old coastal booking resumes through the Paris clerk to Berlin',flush=True)
finally:e.close()
