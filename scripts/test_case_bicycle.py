"""Bicycle visits to all completed landmark cases, using normal controls."""
import json
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,talk,save
from test_gym_ui import open_key_item
from test_time import preserved
from test_tour import travel

maps=json.loads((ROOT/'data/maps/map_groups.json').read_text())['gMapGroup_Europe']


def history(e):
    return tuple(e.var(v) for v in range(0x40C0,0x4100))


e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'visitor-bike-complete',True)
    original=preserved(e)[1:],history(e)
    assert all(e.var(v)==6 for v in range(0x40C0,0x40C3))
    for city,destination,name,door in [
        ('London',0,'EuropeWestminster',(14,35)),
        ('Paris',1,'EuropeNotreDame',(28,35)),
        ('Berlin',2,'EuropeReichstag',(21,33)),
    ]:
        go(e,(16,14));travel(e,destination)
        go(e,door);open_key_item(e,360);e.frames(120)
        assert e.read('gPlayerAvatar',1)&2
        for choice in ['NO','B']:
            before=preserved(e);talk(e,door,choice=choice)
            assert e.location()==(43,destination*4,*door) and e.read('gPlayerAvatar',1)&2
            assert preserved(e)==before and history(e)==original[1]
        talk(e,door,choice='YES')
        assert e.location()==(43,maps.index(name),10,15)
        assert not e.read('gPlayerAvatar',1)&2
        for point,direction in [((8,15),'UP'),((12,14),'DOWN')]:
            go(e,point);before=preserved(e);talk(e,point,d=direction)
            assert preserved(e)==before and history(e)==original[1]
        assert preserved(e)[1:]==original[0]
        print('PASS: '+city+' case Bicycle No/B, automatic indoor dismount and completed curator/ledger repeat preserve rewards and synthesis state',flush=True)
        go(e,(10,15));checkpoint='case-bike-'+city
        save(e,checkpoint);saved=preserved(e)
        e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,checkpoint,True)
        assert e.location()==(43,maps.index(name),10,15) and preserved(e)==saved
        assert not e.read('gPlayerAvatar',1)&2 and history(e)==original[1]
        e.screenshot(ROOT/f'test-output/{checkpoint}-inside.png')
        e.walk('DOWN',1);e.frames(180)
        assert e.location()==(43,destination*4,*door)
        if e.read('gPlayerAvatar',1)&2:open_key_item(e,360);e.frames(120)
        assert not e.read('gPlayerAvatar',1)&2 and not e.read('sLockFieldControls',1)
        assert (preserved(e)[1:],history(e))==original
        print('PASS: '+city+' case indoor cold Continue and south exit retain exact save state and controllable outdoor walking',flush=True)
    go(e,(16,14));travel(e,3);go(e,(18,14))
    save(e,'case-bike-complete');saved=preserved(e)
    e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'case-bike-complete',True)
    assert e.location()==(43,12,18,14) and preserved(e)==saved
    before=preserved(e);e.press('DOWN');e.press('A',900)
    e.screenshot(ROOT/'test-output/case-bike-ada.png');e.finish_dialogue()
    assert preserved(e)==before and (preserved(e)[1:],history(e))==original
    print('PASS: final cold Continue and Ada conclusion retain all three completed cases, captured party and main ending after Bicycle visits',flush=True)
finally:e.close()
