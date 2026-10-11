"""Native gender-dependent evolution with isolated species, personality and level fixtures."""
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
from test_eclipse_friendship import fixture, candy, ids, orders
from test_shadow_runtime import monfield
from test_gym_ui import start_action
from tm_teaching_test_helpers import field
from eclipse_evolutions import project, GENDER_FORM_ALIASES

def gender_fixture(e,female):
    p=e.symbols['gPlayerParty'];old=e.read(p);ot=e.read(p+4)
    data=[(e.read(p+32+4*i)^(old^ot)).to_bytes(4,'little') for i in range(12)]
    raw=b''.join(data);blocks=[raw[12*s:12*s+12] for s in orders[old%24]]
    new=(old&~255)|(0 if female else 255)
    physical=[None]*4
    for block,slot in zip(blocks,orders[new%24]):physical[slot]=block
    raw=b''.join(physical);e.write(p,new)
    for i in range(12):e.write(p+32+4*i,int.from_bytes(raw[4*i:4*i+4],'little')^(new^ot))

def main():
    cases=[('COMBEE','VESPIQUEN',True,20,0,0),('COMBEE','COMBEE',False,20,0,0),
     ('COMBEE','COMBEE',True,19,0,0),('SALANDIT','SALAZZLE',True,32,0,0),
     ('SALANDIT','SALANDIT',False,32,0,0),('BURMY','WORMADAM',True,19,0,0),
     ('BURMY','MOTHIM',False,19,0,0),('COMBEE','COMBEE',True,50,195,0),
     ('SALANDIT','SALANDIT',True,50,0,1),('ESPURR','MEOWSTIC',True,24,0,0),
     ('ESPURR','MEOWSTIC',False,24,0,0),('LECHONK','OINKOLOGNE',True,17,0,0),
     ('LECHONK','OINKOLOGNE',False,17,0,0)]
    for n,(species,target,female,level,held,shadow) in enumerate(cases):
        e=Emulator(ROOT/'pokefirered.gba')
        try:
            load_checkpoint(e,'natural-circuit-complete',True)
            fixture(e,species,255,held,shadow);gender_fixture(e,female)
            e.write(e.symbols['gPlayerParty']+0x54,level,1);candy(e)
            assert monfield(e,0,0,0)&65535==ids['SPECIES_'+target],(n,species,target,monfield(e,0,0,0)&65535)
            assert e.read(e.symbols['gPlayerParty']+0x54,1)==level+1
            assert e.read('gPlayerParty')&255==(0 if female else 255)
            if n==12:
                field(e);start_action(e,4)
                for _ in range(8):e.press('A',240)
                e.battery(ROOT/'test-output/gender-evolution-oinkologne.sav')
            print('PASS:',n,species,'female' if female else 'male','->',target,'level',level+1,flush=True)
        finally:e.close()
    e=Emulator(ROOT/'pokefirered.gba')
    try:
        load_checkpoint(e,'gender-evolution-oinkologne',True)
        assert monfield(e,0,0,0)&65535==ids['SPECIES_OINKOLOGNE']
        assert e.read('gPlayerParty')&255==255
        extra=ids['SPECIES_OINKOLOGNE']-440;save=e.read('gSaveBlock2Ptr');mask=1<<(extra%8)
        assert e.read(save+0xb20+extra//8,1)&mask
        assert e.read(save+0xb70+extra//8,1)&mask
        print('PASS: evolved Gen IX species, personality and seen/caught flags survive Save/cold Continue')
    finally:e.close()
    body='.evolutions = EVOLUTION({EVO_LEVEL, 21, SPECIES_VESPIQUEN, CONDITIONS({IF_GENDER, MON_FEMALE})}),'
    assert project(body,set(ids),set())[0]==[('EVO_LEVEL_FEMALE','21','SPECIES_VESPIQUEN')]
    assert not project(body.replace('MON_FEMALE','MON_GENDERLESS'),set(ids),set())[0]
    assert not project(body.replace('{IF_GENDER, MON_FEMALE}','{IF_GENDER, MON_FEMALE},{IF_TIME, TIME_NIGHT}'),set(ids),set())[0]
    assert not project(body.replace('{IF_GENDER, MON_FEMALE}','{IF_GENDER, MON_FEMALE},{IF_GENDER, MON_MALE}'),set(ids),set())[0]
    print('PASS: unknown gender and unsupported additional conditions remain omitted')

if __name__ == '__main__':
    main()
