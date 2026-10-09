"""Native TM Case selection and safe return to the field."""
from collections import Counter
from test_time import preserved
from test_gym_ui import open_key_item
from test_navigation import wait_task

def state(e):
 p=preserved(e)
 return p[:3]+(Counter(x for x in p[3] if x[0]),)+p[4:]

def select(e,tm):
 open_key_item(e,364);e.frames(180)
 base=e.read('gSaveBlock1Ptr')+0x464
 target=next(i for i in range(58) if e.read(base+4*i,2)==tm)
 for _ in range(60):e.press('UP',10)
 for _ in range(target):e.press('DOWN',60)
 e.press('A',180);e.press('A',180)
 wait_task(e,'Task_HandleChooseMonInput');e.frames(60)

def field(e):
 for _ in range(8):e.press('B',180)
 assert not e.read('sLockFieldControls',1)
 assert not e.task_active('Task_HandleChooseMonInput')
