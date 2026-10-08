"""Follow new host directions from genuine v1.15 indoor saves."""
import json
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,talk,save
from test_time import preserved

maps=json.loads((ROOT/'data/maps/map_groups.json').read_text())['gMapGroup_Europe']
e=Emulator(ROOT/'pokefirered.gba')
try:
    for city,capital,checkpoint,host,door,name,reading in [
        ('London',0,'walkthrough-interiors-London-reading',(8,5),(29,29),'EuropeLondonEyeGallery',(2,4)),
        ('Paris',4,'walkthrough-interiors-Paris-garden',(8,5),(9,37),'EuropeEiffelVisitor',(3,4)),
        ('Berlin',8,'walkthrough-interiors-Berlin-garden',(8,4),(19,37),'EuropeGateVisitor',(3,4)),
    ]:
        load_checkpoint(e,checkpoint,True)
        history=tuple(e.var(v) for v in range(0x40C0,0x4100))
        original=preserved(e)[1:]
        go(e,host);e.press('UP');before=preserved(e);e.press('A',900)
        assert e.read('sLockFieldControls',1)
        # Each A at a finished page advances to the next full page.
        e.press('A',900);e.press('A',900)
        assert e.read('sLockFieldControls',1)
        e.screenshot(ROOT/f'test-output/eastern-host-{city}-directions.png')
        e.finish_dialogue();assert preserved(e)==before
        talk(e,host);assert preserved(e)==before
        print('PASS: '+city+' old indoor save reads expanded host dialogue and repeats without changing party/items/progress',flush=True)
        go(e,(5,7));e.walk('DOWN',1);e.frames(180)
        talk(e,door,choice='YES');assert e.location()==(43,maps.index(name),5,7)
        talk(e,reading);assert preserved(e)[1:]==original
        assert tuple(e.var(v) for v in range(0x40C0,0x4100))==history
        e.screenshot(ROOT/f'test-output/eastern-host-{city}-destination.png')
        go(e,(4,7));e.walk('DOWN',1);e.frames(180)
        assert e.location()==(43,capital,*door)
        print('PASS: '+city+' directions lead to the named landmark visitor room; reading and exit retain all completed activities',flush=True)
    save(e,'eastern-host-v118');location=e.location();before=preserved(e)
    e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'eastern-host-v118',True)
    assert e.location()==location and preserved(e)==before
    assert tuple(e.var(v) for v in range(0x40C0,0x4100))==history
    print('PASS: new v1.18 save cold Continues with exact completed state after following host directions',flush=True)
finally:e.close()
