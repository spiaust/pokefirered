"""Native party-dependent evolutions, encrypted buddy/egg fixtures and cold-save QA."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_eclipse_friendship import fixture,candy,ids,orders
from test_eclipse_move_evolution import moves_fixture
from test_shadow_runtime import monfield
from test_gym_ui import start_action
from tm_teaching_test_helpers import field

def buddy(e,species,slot=1,egg=False,fainted=False):
    lead=e.symbols['gPlayerParty'];p=lead+100*slot
    for i in range(25):e.write(p+4*i,e.read(lead+4*i))
    person=e.read(p);key=person^e.read(p+4);raw=bytearray().join((e.read(p+32+4*i)^key).to_bytes(4,'little') for i in range(12))
    growth=12*orders[person%24][0];misc=12*orders[person%24][3]
    raw[growth:growth+2]=ids['SPECIES_'+species].to_bytes(2,'little')
    ivs=int.from_bytes(raw[misc+4:misc+8],'little');raw[misc+4:misc+8]=((ivs&~(1<<30))|(int(egg)<<30)).to_bytes(4,'little')
    e.write(p+19,(e.read(p+19,1)&~4)|(int(egg)<<2),1)
    e.write(p+28,sum(int.from_bytes(raw[i:i+2],'little') for i in range(0,48,2))&65535,2)
    for i in range(12):e.write(p+32+4*i,int.from_bytes(raw[4*i:4*i+4],'little')^key)
    if fainted:e.write(p+0x56,0,2)

cases=[('MANTYKE','MANTINE',50,'REMORAID',1,False,False,False,0,0),
 ('MANTYKE','MANTYKE',50,None,1,False,False,False,0,0),('MANTYKE','MANTYKE',50,'SQUIRTLE',1,False,False,False,0,0),
 ('MANTYKE','MANTYKE',50,'REMORAID',1,True,False,False,0,0),('MANTYKE','MANTINE',50,'REMORAID',1,False,True,False,0,0),
 ('MANTYKE','MANTYKE',50,'REMORAID',1,False,False,True,0,0),('MANTYKE','MANTINE',50,'REMORAID',5,False,False,False,0,0),
 ('PANCHAM','PANGORO',31,'HOUNDOOM',1,False,False,False,0,0),('PANCHAM','PANCHAM',30,'HOUNDOOM',1,False,False,False,0,0),
 ('PANCHAM','PANCHAM',50,None,1,False,False,False,0,0),('PANCHAM','PANCHAM',50,'SQUIRTLE',1,False,False,False,0,0),
 ('PANCHAM','PANCHAM',50,'HOUNDOOM',1,True,False,False,0,0),('PANCHAM','PANGORO',31,'HOUNDOOM',1,False,True,False,0,0),
 ('PANCHAM','PANCHAM',50,'HOUNDOOM',1,False,False,True,0,0),('PANCHAM','PANGORO',31,'GRENINJA',5,False,False,False,0,0),
 ('PANCHAM','PANCHAM',50,'HOUNDOOM',1,False,False,False,195,0),('PANCHAM','PANCHAM',50,'HOUNDOOM',1,False,False,False,0,1)]
for n,(species,target,level,partner,slot,egg,fainted,boxed,held,shadow) in enumerate(cases):
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'natural-circuit-complete',True);fixture(e,species,255,held,shadow);moves_fixture(e,'MOVE_TACKLE')
        e.write(e.symbols['gPlayerParty']+0x54,level,1)
        for i in range(25,150):e.write(e.symbols['gPlayerParty']+4*i,0)
        if partner:
            for i in range(1,slot):buddy(e,'SQUIRTLE',i)
            buddy(e,partner,slot,egg,fainted)
            if boxed:
                storage=e.read('gPokemonStoragePtr')+4;p=e.symbols['gPlayerParty']+100*slot
                for i in range(20):e.write(storage+4*i,e.read(p+4*i))
                for i in range(25):e.write(p+4*i,0)
            else:e.write('gPlayerPartyCount',slot+1,1)
        candy(e)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_'+target],(n,target)
        print('PASS:',n,species,'->',target,'partner',partner,'slot',slot,'egg',egg,'fainted',fainted,'boxed',boxed,flush=True)
        if n==14:
            field(e);start_action(e,4)
            for _ in range(8):e.press('A',240)
            e.battery(ROOT/'test-output/party-pangoro.sav')
    finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'party-pangoro',True)
    assert monfield(e,0,0,0)&65535==ids['SPECIES_PANGORO'] and monfield(e,5,0,0)&65535==ids['SPECIES_GRENINJA']
    extra=ids['SPECIES_PANGORO']-440;mask=1<<(extra%8);sb=e.read('gSaveBlock2Ptr')
    assert e.read(sb+0xb20+extra//8,1)&mask and e.read(sb+0xb70+extra//8,1)&mask
    print('PASS: Pangoro, sixth-slot Greninja and seen/caught flags survive native Save/cold Continue',flush=True)
finally:e.close()
