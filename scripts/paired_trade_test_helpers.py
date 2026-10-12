"""Shared isolated party fixtures and native exchange UI helpers."""
from emulator import ROOT
from test_eclipse_friendship import fixture,ids,orders
from test_shadow_runtime import monfield,go
from test_navigation import wait_task
from tm_teaching_test_helpers import field

def buddy(e,species,slot=1,egg=False,fainted=False,held=0):
    lead=e.symbols['gPlayerParty'];p=lead+100*slot
    for i in range(25):e.write(p+4*i,e.read(lead+4*i))
    person=e.read(p);key=person^e.read(p+4);raw=bytearray().join((e.read(p+32+4*i)^key).to_bytes(4,'little') for i in range(12))
    growth=12*orders[person%24][0];misc=12*orders[person%24][3]
    raw[growth:growth+2]=ids['SPECIES_'+species].to_bytes(2,'little')
    raw[growth+2:growth+4]=held.to_bytes(2,'little')
    ivs=int.from_bytes(raw[misc+4:misc+8],'little');raw[misc+4:misc+8]=((ivs&~(1<<30))|(int(egg)<<30)).to_bytes(4,'little')
    e.write(p+19,(e.read(p+19,1)&~4)|(int(egg)<<2),1)
    e.write(p+28,sum(int.from_bytes(raw[i:i+2],'little') for i in range(0,48,2))&65535,2)
    for i in range(12):e.write(p+32+4*i,int.from_bytes(raw[4*i:4*i+4],'little')^key)
    if fainted:e.write(p+0x56,0,2)

def pair(e,species,partner=None,slot=1,egg=False,fainted=False,ownheld=0,buddyheld=0,shadow=0):
    fixture(e,species,255,ownheld,shadow)
    for i in range(25,150):e.write(e.symbols['gPlayerParty']+4*i,0)
    if partner:
        for i in range(1,slot):buddy(e,'SQUIRTLE',i)
        buddy(e,partner,slot,egg,fainted,buddyheld)
        e.write('gPlayerPartyCount',slot+1,1)

def advance_offer(e):
    for _ in range(60):
        if e.task_active('Task_YesNoMenu_HandleInput'):return
        e.press('A',90)
    raise AssertionError('Exchange offer did not appear')

def offer(e,second=False):
    go(e,(14,31));e.press('UP');e.press('A',90);advance_offer(e)
    if second:e.press('B',180);advance_offer(e)

def choose(e,slot=0,cancel=False):
    e.press('A',180);wait_task(e,'Task_HandleChooseMonInput')
    if cancel:e.press('B',180);finish(e);return
    for _ in range(12):
        if e.read(e.symbols['gPartyMenu']+9,1)==slot:break
        e.press('DOWN',60)
    assert e.read(e.symbols['gPartyMenu']+9,1)==slot
    e.press('A',180)

def finish(e):
    for _ in range(180):
        if not e.read('sLockFieldControls',1):break
        e.press('A',90)
    else:
        e.screenshot(ROOT/'test-output/paired-exchange-stuck.png')
        raise AssertionError('Exchange did not return field control')
    field(e)
