"""Old indoor branch-station batteries, notice reads, local walks and Continue."""
import sys
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,save
from test_time import preserved

CASES=[('Oxford',12,(18,14)),('Chantilly',16,(10,14)),('Oranienburg',20,(10,14))]

def read(e,city,label):
    go(e,(9,2));before=preserved(e);e.press('UP');e.press('A',900)
    for page in range(2):
        assert e.read('sLockFieldControls',1) and e.location()[2:]==(9,2)
        e.screenshot(ROOT/f'test-output/branch-board-{city}-{label}-{page}.png')
        if page==0:e.press('A',900)
    e.finish_dialogue()
    assert preserved(e)==before and not e.read('sLockFieldControls',1)

if '--prepare' in sys.argv:
    for city,index,contact in CASES:
        e=Emulator(ROOT/'artifacts/releases/Pokemon-European-Tour-v1.09.gba')
        try:
            load_checkpoint(e,'rail-foot-'+city.lower()+'-v107',True)
            go(e,(9,2));save(e,'branch-board-'+city+'-v109')
            print('Prepared genuine v1.09 indoor station battery: '+city,flush=True)
        finally:e.close()
else:
    for city,index,contact in CASES:
        e=Emulator(ROOT/'pokefirered.gba')
        try:
            load_checkpoint(e,'branch-board-'+city+'-v109',True)
            assert e.location()==(43,index+2,9,2);before=preserved(e)[1:]
            read(e,city,'old-save');read(e,city,'repeat')
            go(e,(4,7));e.walk('DOWN',2);e.frames(180)
            assert e.location()==(43,index,23,10)
            go(e,(15,10));go(e,contact)
            e.screenshot(ROOT/f'test-output/branch-board-{city}-contact.png')
            go(e,(23,10));e.walk('UP',1);e.frames(180);e.walk('UP',1)
            read(e,city,'reentered');assert preserved(e)[1:]==before
            save(e,'branch-board-'+city);saved=preserved(e)
            print('PASS: '+city+' genuine old indoor save reads both notice pages repeatedly, reaches Gym/contact approaches and re-enters without progress changes',flush=True)
        finally:e.close()
        e=Emulator(ROOT/'pokefirered.gba')
        try:
            load_checkpoint(e,'branch-board-'+city,True)
            assert e.location()==(43,index+2,9,2) and preserved(e)==saved
            read(e,city,'continued');go(e,(4,7));e.walk('DOWN',2);e.frames(180)
            assert e.location()==(43,index,23,10)
            print('PASS: '+city+' new indoor save cold Continues with exact state, reads notice and exits normally',flush=True)
        finally:e.close()
