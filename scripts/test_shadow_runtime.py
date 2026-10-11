"""Native entry/access/rescue tests, with explicit late-game state fixtures.

Stage writes isolate rescue scenarios; they do not assert a natural playthrough.
"""
from pathlib import Path
from collections import deque
import json,struct,re
from emulator import Emulator,ROOT
from test_country import wait_menu
from test_landmark_cases import go as base_go,save
from test_celebi import load_checkpoint
layouts={x.get('id'):x for x in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text())
def go(e,target):
    g,idx,x,y=e.location()
    if g==43:return base_go(e,target)
    n=groups['gMapGroup_Shadow' if g==44 else 'gMapGroup_Continent'][idx];m=json.loads((ROOT/f'data/maps/{n}/map.json').read_text());l=layouts[m['layout']];w,h=l['width'],l['height'];a=struct.unpack('<%dH'%(w*h),(ROOT/l['blockdata_filepath']).read_bytes());blocked={(o['x'],o['y']) for o in m['object_events']}
    q=deque([(x,y)]);prev={(x,y):None}
    while q and target not in prev:
        x,y=q.popleft()
        for z,d in [((x+1,y),'RIGHT'),((x-1,y),'LEFT'),((x,y+1),'DOWN'),((x,y-1),'UP')]:
            xx,yy=z
            if 0<=xx<w and 0<=yy<h and z not in blocked and z not in prev and not a[yy*w+xx]&0xc00 and (a[yy*w+xx]&1023)!=0x12b:prev[z]=((x,y),d);q.append(z)
    assert target in prev,(n,target)
    path=[];z=target
    while prev[z]:z,d=prev[z];path.append(d)
    for d in path[::-1]:e.walk(d,1)
    assert e.location()[2:]==target,(n,target,e.location())
def ensure_visible(e):
    # Rate-based spawn may initially be absent; walking lets the native field system retry.
    e.write('sWildEncountersDisabled',1,1)
    g,idx,_,_=e.location();n=groups['gMapGroup_Shadow' if g==44 else 'gMapGroup_Continent'][idx]
    m=json.loads((ROOT/f'data/maps/{n}/map.json').read_text());local=next(i+1 for i,o in enumerate(m['object_events']) if o['graphics_id']=='OBJ_EVENT_GFX_VAR_0')
    target=(17,15) if g==44 else (40,25);go(e,target)
    for _ in range(48):
        for i in range(16):
            p=e.symbols['gObjectEvents']+36*i
            if e.read(p,1)&1 and e.read(p+8,1)==local and e.read(p+9,1)==idx and e.read(p+10,1)==g:return target
        e.walk('LEFT',1);e.walk('RIGHT',1)
    raise AssertionError('native rate-based wild spawn never appeared')

def talk(e,target,choice=None):
    go(e,target);e.press('UP');e.press('A',180)
    if choice is not None:
        wait_menu(e,'Task_YesNoMenu_HandleInput')
        e.press('B' if choice=='NO' else 'A',180)
    e.finish_dialogue();e.frames(240)
def setstage(e,n):e.write(e.read('gSaveBlock1Ptr')+0x1000+2*(0x408C-0x4000),n,2)
def monfield(e,index,block,offset,party="gPlayerParty"):
    # Decrypt the box data to inspect persistence without changing it.
    source=(ROOT/'src/pokemon.c').read_text();order={int(a):int(b) for a,b in re.findall(r'SUBSTRUCT_CASE\(\s*(\d+),\s*(\d+),',source)}
    # SUBSTRUCT_CASE expands four slots; parse the full permutation table instead.
    rows={int(a):tuple(map(int,b)) for a,*b in re.findall(r'SUBSTRUCT_CASE\(\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)',source)}
    p=e.symbols[party]+100*index;person=e.read(p);key=person^e.read(p+4);slot=rows[person%24][block];word=e.read(p+32+12*slot+(offset//4)*4)^key
    return word>>(8*(offset%4))
def main():
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        for country,idx in [('england',0),('france',4),('germany',8)]:
            e.state(ROOT/f'test-output/start-{country}.state',True)
            m=json.loads((ROOT/f'data/maps/Europe{["London","Paris","Berlin"][idx//4]}/map.json').read_text());o=next(o for o in m['object_events'] if o['script']=='Shadow_Entrance')
            talk(e,(o['x'],o['y']+1))
            assert e.var(0x408D)==1 and e.var(0x408C)==0 and e.location()[:2]==(44,0),(country,e.location())
            print('PASS:',country,'native entrance, gifts and current-chapter warp',flush=True)
        e.screenshot(ROOT/'test-output/eclipse-shelter.png')
        talk(e,(6,4),'NO');assert e.var(0x408C)==0 and not e.in_battle()
        talk(e,(10,4));assert e.location()[:2]==(44,0) and e.var(0x408C)==0
        p=e.symbols['gPlayerParty'];e.write(p+0x56,1,2);talk(e,(2,4));assert e.read(p+0x56,2)==e.read(p+0x58,2)
        talk(e,(10,7));assert e.location()[:2]==(44,1)
        e.screenshot(ROOT/'test-output/eclipse-overworld.png')
        ensure_visible(e);talk(e,(17,15),'NO');assert not e.in_battle() and e.var(0x408C)==0
        talk(e,(15,20));assert e.location()[:2]==(44,0)
        print('PASS: decline, locked next chapter, nurse, route travel and visible encounter decline',flush=True)
        talk(e,(6,7));assert e.location()[:2]==(43,0)
        setstage(e,3);talk(e,(10,16));assert e.location()[:2]==(44,6)
        # Previous porter takes us to the completed Paris rescue chapter.
        talk(e,(2,7));assert e.location()[:2]==(44,4)
        talk(e,(8,4));assert e.read('gPlayerPartyCount',1)==2 and e.var(0x408E)==1
        shadow=monfield(e,1,3,8);assert shadow&(1<<27),(hex(shadow),'shadow bit')
        talk(e,(8,4));assert e.read('gPlayerPartyCount',1)==2
        talk(e,(4,4));assert e.var(0x408F)==0
        for _ in range(12):talk(e,(4,4))
        assert e.var(0x408F)==1 and not(monfield(e,1,3,8)&(1<<27))
        talk(e,(4,4));assert e.var(0x408F)==1
        print('PASS: one-time rescue, persistent shadow bit, repeated care, purification and no duplicate count',flush=True)
        save(e,'eclipse-purified');before=(e.location(),e.var(0x408C),e.var(0x408E),e.var(0x408F));e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'eclipse-purified',True)
        assert (e.location(),e.var(0x408C),e.var(0x408E),e.var(0x408F))==before
        assert e.read('gPlayerPartyCount',1)==2 and not(monfield(e,1,3,8)&(1<<27))
        print('PASS: native Save and cold Continue preserves chapter, rescued party and purification',flush=True)
    finally:e.close()

if __name__ == '__main__': main()
