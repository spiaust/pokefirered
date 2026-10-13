"""Native New Game starter/difficulty balance matrix; no battle/stat/EXP edits."""
import json,argparse
from emulator import Emulator,ROOT
from test_shadow_runtime import talk,monfield
from test_continent_runtime import battle_start,menu_row
from test_gym_ui import open_key_item
from test_navigation import wait_task
from test_eclipse_natural import natural_battle
from test_landmark_cases import save
from test_celebi import load_checkpoint
parser=argparse.ArgumentParser();parser.add_argument('--mode',type=int,choices=(0,1,2),default=0);parser.add_argument('--nuzlocke',action='store_true');args=parser.parse_args()
results=[]
for country,city in [('england','London'),('france','Paris'),('germany','Berlin')]:
 for starter in range(3):
  e=Emulator(ROOT/'pokefirered.gba')
  try:
   e.state(ROOT/f'test-output/start-{country}-{starter}.state',True)
   before=(monfield(e,0,0,0)&65535,e.read(e.symbols['gPlayerParty']+84,1))
   objects=json.loads((ROOT/f'data/maps/Europe{city}/map.json').read_text())['object_events']
   door=next(o for o in objects if o['script']=='Shadow_Entrance')
   talk(e,(door['x'],door['y']+1))
   open_key_item(e,363);wait_task(e,'Task_EuropeMap');menu_row(e,8)
   for _ in range(args.mode):e.press('A',60)
   assert e.var(0x4090)==args.mode
   if args.nuzlocke:menu_row(e,9);e.press('A',60)
   assert e.var(0x4091)==int(args.nuzlocke)
   for _ in range(3):e.press('B',180)
   battle_start(e,(6,4))
   enemy=(monfield(e,0,0,0,'gEnemyParty')&65535,e.read(e.symbols['gEnemyParty']+84,1))
   outcome,turns=natural_battle(e)
   row=dict(country=country,starter=starter,species=before[0],start_level=before[1],mode=args.mode,nuzlocke=args.nuzlocke,enemy_species=enemy[0],enemy_level=enemy[1],outcome=outcome,turns=turns,stage=e.var(0x408c),end_level=e.read(e.symbols['gPlayerParty']+84,1),hp=e.read(e.symbols['gPlayerParty']+86,2))
   print(row,flush=True);results.append(row)
   if outcome==1:
    name=f'balance-opening-{country}-{starter}-{args.mode}-{int(args.nuzlocke)}';save(e,name)
    e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,name,True)
    assert e.var(0x408c)==1 and e.var(0x4090)==args.mode and e.var(0x4091)==int(args.nuzlocke)
    assert monfield(e,0,0,0)&65535==before[0]
   else:e.screenshot(ROOT/f'test-output/balance-opening-loss-{country}-{starter}-{args.mode}.png')
  finally:e.close()
p=ROOT/f'test-output/balance-openings-{args.mode}-{int(args.nuzlocke)}.json';p.write_text(json.dumps(results,indent=2)+'\n')
assert all(r['outcome']==1 and r['stage']==1 for r in results),results
print('PASS: all nine starter openings and cold saves',args.mode,args.nuzlocke,flush=True)
