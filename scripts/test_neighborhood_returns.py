"""Read neighborhood return signs and follow the routes on completed saves."""
import json
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,talk,save
from test_time import preserved

maps=json.loads((ROOT/'data/maps/map_groups.json').read_text())['gMapGroup_Europe']
e=Emulator(ROOT/'pokefirered.gba')
try:
    for city,capital,checkpoint,sign,pages,door,name,reading in [
        ('London',0,'walkthrough-interiors-London-reading',(55,36),3,(29,29),'EuropeLondonEyeGallery',(2,4)),
        ('Paris',4,'walkthrough-interiors-Paris-garden',(55,42),2,(9,37),'EuropeEiffelVisitor',(3,4)),
        ('Berlin',8,'walkthrough-interiors-Berlin-garden',(56,35),5,(19,37),'EuropeGateVisitor',(3,4)),
    ]:
        load_checkpoint(e,checkpoint,True)
        history=tuple(e.var(v) for v in range(0x40C0,0x4100));original=preserved(e)[1:]
        go(e,(5,7));e.walk('DOWN',1);e.frames(180)
        go(e,sign);e.press('UP');before=preserved(e);e.press('A',900)
        for _ in range(pages-1):
            assert e.read('sLockFieldControls',1)
            e.press('A',900)
        assert e.read('sLockFieldControls',1)
        e.screenshot(ROOT/f'test-output/neighborhood-return-{city}.png')
        e.finish_dialogue();assert preserved(e)==before
        talk(e,sign);assert preserved(e)==before
        print('PASS: '+city+' sign displays landmark return page and repeats with exact saved state retained',flush=True)
        talk(e,door,choice='YES');assert e.location()==(43,maps.index(name),5,7)
        talk(e,reading);go(e,(4,7));e.walk('DOWN',1);e.frames(180)
        assert e.location()==(43,capital,*door) and preserved(e)[1:]==original
        assert tuple(e.var(v) for v in range(0x40C0,0x4100))==history
        print('PASS: '+city+' sign route reaches the named visitor room and returns with all completed activities retained',flush=True)
    save(e,'neighborhood-return-v119');location=e.location();before=preserved(e)
    e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'neighborhood-return-v119',True)
    assert e.location()==location and preserved(e)==before
    assert tuple(e.var(v) for v in range(0x40C0,0x4100))==history
    print('PASS: new v1.19 cold Continue retains exact completed state after neighborhood return routes',flush=True)
finally:e.close()
