"""Visit three capital neighborhood homes on the completed walkthrough save."""
import json
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go, talk, save
from test_time import preserved
from test_tour import travel

maps = json.loads((ROOT/'data/maps/map_groups.json').read_text())['gMapGroup_Europe']


def history(e):
    return tuple(e.var(v) for v in range(0x40C0, 0x4100))


e = Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e, 'current-bicycle-complete', True)
    original = preserved(e)[1:], history(e)
    for city, destination, name, approach, record, facing in [
        ('London', 0, 'EuropeLondonHome', (45,33), (6,3), 'DOWN'),
        ('Paris', 1, 'EuropeParisHome', (45,39), (9,2), 'UP'),
        ('Berlin', 2, 'EuropeBerlinHome', (43,32), (6,3), 'DOWN'),
    ]:
        go(e, (16,14)); travel(e, destination)
        for choice in ['NO','B']:
            go(e, approach); before = preserved(e)
            talk(e, approach, choice=choice)
            assert e.location() == (43,destination*4,*approach) and preserved(e) == before
        talk(e, approach, choice='YES')
        inside = maps.index(name)
        assert e.location() == (43,inside,5,7)
        for point, direction in [((8,5),'UP'), ((3,4),'UP'), (record,facing)]:
            go(e,point); before=preserved(e)
            e.press(direction); e.press('A',180)
            assert e.read('sLockFieldControls',1)
            e.finish_dialogue(); assert preserved(e)==before
        e.screenshot(ROOT/f'test-output/current-rooms-{city}.png')
        assert (preserved(e)[1:],history(e)) == original
        print('PASS: '+city+' home No/B, entry, host, notebook and local display preserve completed activities and party',flush=True)
        go(e,(9,7)); checkpoint='current-rooms-'+city
        save(e,checkpoint); saved=preserved(e),history(e)
        e.close(); e=Emulator(ROOT/'pokefirered.gba')
        load_checkpoint(e,checkpoint,True)
        assert e.location()==(43,inside,9,7) and (preserved(e),history(e))==saved
        print('PASS: '+city+' interior cold Continue retains exact location, party, items and quest history',flush=True)
        go(e,(4,7)); e.walk('DOWN',1); e.frames(180)
        assert e.location()==(43,destination*4,*approach)
        talk(e,approach,choice='YES'); go(e,(5,7)); e.walk('DOWN',1); e.frames(180)
        assert e.location()==(43,destination*4,*approach)
        assert (preserved(e)[1:],history(e))==original
        print('PASS: '+city+' both front exit tiles and re-entry return to the correct capital with all completion state retained',flush=True)
    go(e,(16,14)); travel(e,3); go(e,(18,14))
    save(e,'current-rooms-complete')
    before=preserved(e); e.press('DOWN'); e.press('A',900)
    e.screenshot(ROOT/'test-output/current-rooms-ada.png'); e.finish_dialogue()
    assert preserved(e)==before and (preserved(e)[1:],history(e))==original
    print('PASS: normal return to Oxford retains party, all completed activities and Ada conclusion',flush=True)
finally:
    e.close()
