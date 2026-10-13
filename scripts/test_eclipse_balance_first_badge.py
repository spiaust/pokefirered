"""Earn alternate-start first badges with native training, EXP and supplies."""
import argparse,json
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
import test_eclipse_natural as natural
import test_shadow_runtime,test_continent_runtime
from test_shadow_runtime import talk,monfield
from test_continent_runtime import battle_start
from test_landmark_cases import save
from test_eclipse_natural_league import party_record
parser=argparse.ArgumentParser()
parser.add_argument('--country',choices=('england','france','germany'),required=True)
parser.add_argument('--starter',type=int,choices=range(3),required=True)
parser.add_argument('--mode',type=int,choices=(0,1,2),default=0)
parser.add_argument('--practice',type=int,choices=range(6),default=1)
args=parser.parse_args()
learn=(22,52,55,71,93,98,232,24,64,43,108)

# Keep the original callable before wrapping incidental wild encounters.
original_battle=natural.natural_battle
def battle(e):return original_battle(e,learn_moves=learn)
natural.natural_battle=battle

test_shadow_runtime.go=natural.natural_go;test_continent_runtime.go=natural.natural_go
e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,f'balance-opening-{args.country}-{args.starter}-{args.mode}-0',True)
    assert e.var(0x408c)==1 and e.var(0x4090)==args.mode
    starter=monfield(e,0,0,0)&65535;practices=0;turns_total=0
    talk(e,(2,4))
    for practice in range(45):
        if e.read(e.symbols['gPlayerParty']+84,1)>=16:break
        talk(e,(10,7));battle_start(e,((7,7),(11,11),(22,7),(24,13),(7,16),(21,18))[args.practice]);outcome,turns=battle(e)
        assert outcome==1,(practice,outcome)
        turns_total+=turns;practices+=1
        talk(e,(15,20));talk(e,(2,4))
        print('Native first-badge preparation',args.country,args.starter,practices,e.read(e.symbols['gPlayerParty']+84,1),flush=True)
    assert e.read(e.symbols['gPlayerParty']+84,1)>=16
    talk(e,(10,4));talk(e,(2,4));battle_start(e,(6,4));outcome,turns=battle(e)
    row=dict(country=args.country,starter=args.starter,initial_species=starter,mode=args.mode,nuzlocke=False,practices=practices,training_turns=turns_total,gym_outcome=outcome,gym_turns=turns,level=e.read(e.symbols['gPlayerParty']+84,1),party_count=e.read('gPlayerPartyCount',1),stage=e.var(0x408c))
    print(row,flush=True);(ROOT/f'test-output/balance-first-badge-{args.country}-{args.starter}-{args.mode}.json').write_text(json.dumps(row,indent=2)+'\n')
    assert outcome==1 and e.var(0x408c)==2
    name=f'balance-first-badge-{args.country}-{args.starter}-{args.mode}';save(e,name);record=party_record(e)
    e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,name,True)
    assert e.var(0x408c)==2 and party_record(e)==record
    print('PASS: alternate-start first badge and exact naturally trained party survive cold Continue',args.country,args.starter,flush=True)
finally:e.close()
