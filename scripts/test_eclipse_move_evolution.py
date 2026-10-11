"""Move-based evolutions through native level-up with isolated encrypted-mon fixtures."""
import re
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
from test_eclipse_friendship import fixture, candy, ids, orders
from test_shadow_runtime import monfield
from test_gym_ui import start_action
from tm_teaching_test_helpers import field
from eclipse_evolutions import project
moves={a:int(b) for a,b in re.findall(r'#define (MOVE_\w+)\s+(\d+)',(ROOT/'include/constants/moves.h').read_text())}

def moves_fixture(e,move,slot=0):
    p=e.symbols['gPlayerParty'];person=e.read(p);key=person^e.read(p+4)
    raw=bytearray().join((e.read(p+32+4*i)^key).to_bytes(4,'little') for i in range(12))
    attack=12*orders[person%24][1]
    raw[attack:attack+12]=bytes(12)
    raw[attack+slot*2:attack+slot*2+2]=moves[move].to_bytes(2,'little');raw[attack+8+slot]=10
    e.write(p+28,sum(int.from_bytes(raw[i:i+2],'little') for i in range(0,48,2))&65535,2)
    for i in range(12): e.write(p+32+4*i,int.from_bytes(raw[4*i:4*i+4],'little')^key)

def main():
    cases=[('BONSLY','SUDOWOODO','MOVE_MIMIC',50,0,0),('STEENEE','TSAREENA','MOVE_STOMP',50,0,0),
     ('CLOBBOPUS','GRAPPLOCT','MOVE_TAUNT',50,0,0),('TANGELA','TANGROWTH','MOVE_ANCIENT_POWER',50,0,0),
     ('YANMA','YANMEGA','MOVE_ANCIENT_POWER',48,0,0),('BONSLY','BONSLY','MOVE_TACKLE',50,0,0),
     ('STEENEE','STEENEE','MOVE_STOMP',50,195,0),('CLOBBOPUS','CLOBBOPUS','MOVE_TAUNT',50,0,1),
     ('TANGELA','TANGROWTH','MOVE_TACKLE',23,0,0),('YANMA','YANMEGA','MOVE_TACKLE',32,0,0),('CLOBBOPUS','GRAPPLOCT','MOVE_TAUNT',50,0,0)]
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--cases');args=parser.parse_args()
    selected=set(map(int,args.cases.split(','))) if args.cases else set(range(len(cases)))
    for n,(species,target,move,level,held,shadow) in enumerate(cases):
        if n not in selected:continue
        e=Emulator(ROOT/'pokefirered.gba')
        try:
            load_checkpoint(e,'natural-circuit-complete',True)
            fixture(e,species,255,held,shadow);moves_fixture(e,move,3 if n==10 else 0)
            e.write(e.symbols['gPlayerParty']+0x54,level,1);candy(e)
            assert monfield(e,0,0,0)&65535==ids['SPECIES_'+target],(n,species,target,monfield(e,0,0,0)&65535)
            assert e.read(e.symbols['gPlayerParty']+0x54,1)==level+1
            if n in (8,9):assert moves['MOVE_ANCIENT_POWER'] in [monfield(e,0,1,j)&65535 for j in (0,2,4,6)]
            if n==9:
                field(e);start_action(e,4)
                for _ in range(8):e.press('A',240)
                e.battery(ROOT/'test-output/move-evolution-yanmega.sav')
            print('PASS:',n,species,'->',target,'at',level+1,'required move',move,flush=True)
        finally:e.close()
    if 9 in selected:
        e=Emulator(ROOT/'pokefirered.gba')
        try:
            load_checkpoint(e,'move-evolution-yanmega',True)
            assert monfield(e,0,0,0)&65535==ids['SPECIES_YANMEGA']
            assert moves['MOVE_ANCIENT_POWER'] in [monfield(e,0,1,j)&65535 for j in (0,2,4,6)]
            print('PASS: evolved Yanmega and newly learned Ancient Power survive native Save/cold Continue')
        finally:e.close()

    body='.evolutions = EVOLUTION({EVO_LEVEL, 0, SPECIES_TSAREENA, CONDITIONS({IF_KNOWS_MOVE, MOVE_STOMP})}),'
    assert project(body,set(ids),set(),moves=set(moves))[0]==[('EVO_LEVEL_MOVE','MOVE_STOMP','SPECIES_TSAREENA')]
    assert not project(body.replace('MOVE_STOMP','MOVE_DRAGON_CHEER'),set(ids),set(),moves=set(moves))[0]
    assert not project(body.replace('{IF_KNOWS_MOVE, MOVE_STOMP}','{IF_KNOWS_MOVE, MOVE_STOMP},{IF_GENDER, MON_FEMALE}'),set(ids),set(),moves=set(moves))[0]
    print('PASS: unavailable moves and additional nested conditions remain omitted')

if __name__ == '__main__':
    main()
