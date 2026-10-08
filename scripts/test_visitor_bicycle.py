"""Bicycle entrance declines, indoor Continue and exits across visitor rooms."""
import json
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,talk,save
from test_gym_ui import open_key_item
from test_time import preserved
from test_tour import travel

maps=json.loads((ROOT/'data/maps/map_groups.json').read_text())['gMapGroup_Europe']
rows=[
    ('London',0,'EuropeLondonHome',(45,33)),
    ('London',0,'EuropeLondonReadingRoom',(55,33)),
    ('London',0,'EuropeLondonEyeGallery',(29,29)),
    ('Paris',4,'EuropeParisHome',(45,39)),
    ('Paris',4,'EuropeParisGardenRoom',(55,39)),
    ('Paris',4,'EuropeEiffelVisitor',(9,37)),
    ('Berlin',8,'EuropeBerlinHome',(43,32)),
    ('Berlin',8,'EuropeBerlinLibrary',(51,32)),
    ('Berlin',8,'EuropeBerlinGardenRoom',(58,32)),
    ('Berlin',8,'EuropeGateVisitor',(19,37)),
]
e=Emulator(ROOT/'pokefirered.gba')
try:
    previous=None
    for city,capital,name,door in rows:
        if city!=previous:
            load_checkpoint(e,'walkthrough-rooms-'+city,True)
            go(e,(5,7));e.walk('DOWN',1);e.frames(180)
            original=preserved(e)[1:]
            history=tuple(e.var(v) for v in range(0x40C0,0x4100))
        go(e,door);open_key_item(e,360);e.frames(120)
        assert e.read('gPlayerAvatar',1)&2
        for choice in ['NO','B']:
            before=preserved(e);talk(e,door,choice=choice)
            assert e.location()==(43,capital,*door) and e.read('gPlayerAvatar',1)&2
            assert preserved(e)==before
        talk(e,door,choice='YES')
        assert e.location()==(43,maps.index(name),5,7)
        assert not e.read('gPlayerAvatar',1)&2,(name,'Bicycle retained inside')
        checkpoint='visitor-bike-'+name
        save(e,checkpoint);before=preserved(e)
        e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,checkpoint,True)
        assert e.location()==(43,maps.index(name),5,7) and preserved(e)==before
        assert not e.read('gPlayerAvatar',1)&2
        e.screenshot(ROOT/f'test-output/{checkpoint}-inside.png')
        e.walk('DOWN',1);e.frames(180)
        assert e.location()==(43,capital,*door)
        # If native outdoor return restores cycling, put it away before walking.
        if e.read('gPlayerAvatar',1)&2:open_key_item(e,360);e.frames(120)
        assert not e.read('gPlayerAvatar',1)&2
        assert preserved(e)[1:]==original
        assert tuple(e.var(v) for v in range(0x40C0,0x4100))==history
        assert not e.read('sLockFieldControls',1)
        print('PASS: '+name+' Bicycle No/B, automatic indoor dismount, exact cold Continue and outdoor exit preserve completed activities',flush=True)
        previous=city
    go(e,(16,14));travel(e,3);go(e,(18,14))
    before=preserved(e);e.press('DOWN');e.press('A',900);e.finish_dialogue()
    assert preserved(e)==before
    assert tuple(e.var(v) for v in range(0x40C0,0x4100))==history
    save(e,'visitor-bike-complete')
    print('PASS: after all ten Bicycle visitor-room trips, normal return to Oxford retains Ada conclusion and completion',flush=True)
finally:e.close()
