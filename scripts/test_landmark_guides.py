"""Follow landmark-guide directions to stations and free clinics."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,talk,save
from test_time import preserved

e=Emulator(ROOT/'pokefirered.gba')
try:
    for city,capital,checkpoint,guide in [
        ('London',0,'walkthrough-interiors-London-Eye',(6,4)),
        ('Paris',4,'walkthrough-interiors-Paris-Eiffel',(8,4)),
        ('Berlin',8,'walkthrough-interiors-Berlin-Gate',(8,4)),
    ]:
        load_checkpoint(e,checkpoint,True)
        history=tuple(e.var(v) for v in range(0x40C0,0x4100));original=preserved(e)[1:]
        go(e,guide);e.press('UP');before=preserved(e);e.press('A',900)
        for page in range(3):
            assert e.read('sLockFieldControls',1)
            e.press('A',900)
            if page>=1:
                e.screenshot(ROOT/f'test-output/landmark-guide-{city}-{page}.png')
        assert e.read('sLockFieldControls',1)
        e.finish_dialogue();assert preserved(e)==before
        talk(e,guide);assert preserved(e)==before
        print('PASS: '+city+' old indoor save shows both new guide pages; repeats retain exact party/items/progress',flush=True)
        go(e,(5,7));e.walk('DOWN',1);e.frames(180)
        go(e,(16,14));go(e,(23,10));e.walk('UP',1);e.frames(180)
        assert e.location()[:2]==(43,capital+2)
        go(e,(4,7));e.walk('DOWN',2);e.frames(180)
        go(e,(6,10));e.walk('UP',1);e.frames(180)
        assert e.location()[:2]==(43,capital+3)
        e.walk('UP',4);e.walk('RIGHT',1);e.press('UP');e.press('A',180);e.finish_dialogue()
        for i in range(e.read('gPlayerPartyCount',1)):
            p=e.symbols['gPlayerParty']+100*i
            assert e.read(p+86,2)==e.read(p+88,2)
        e.walk('DOWN',5);e.frames(180)
        assert e.location()==(43,capital,6,10) and preserved(e)[1:]==original
        assert tuple(e.var(v) for v in range(0x40C0,0x4100))==history
        print('PASS: '+city+' south exit and northward paths reach station and free clinic; healing preserves money/items/completion',flush=True)
    save(e,'landmark-guide-v120');location=e.location();before=preserved(e)
    e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'landmark-guide-v120',True)
    assert e.location()==location and preserved(e)==before
    assert tuple(e.var(v) for v in range(0x40C0,0x4100))==history
    print('PASS: new v1.20 cold Continue retains exact state after landmark-to-service routes',flush=True)
finally:e.close()
