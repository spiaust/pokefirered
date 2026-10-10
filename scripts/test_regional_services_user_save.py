"""Read a copied player battery; never save over the original."""
import hashlib,json,re,shutil
from emulator import Emulator,ROOT
from test_time import preserved
from test_country import party_species
from test_gym_ui import start_action
from test_navigation import wait_task
from key_item_test_helpers import reload

original=ROOT/'artifacts/Pokemon-European-Tour-Prototype.sav'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
original_hash=sha(original)
assert sha(ROOT/'artifacts/Pokemon-European-Tour-Prototype.gba')==sha(ROOT/'artifacts/releases/Pokemon-European-Tour-v1.97.gba')
copy=ROOT/'test-output/v198-user-save-input.sav';shutil.copy2(original,copy)
e=Emulator(ROOT/'pokefirered.gba')
try:
 e.battery(copy,True);e.frames(600);e.press('START',480);e.press('START',180)
 e.screenshot(ROOT/'test-output/v198-user-save-continue.png')
 e.press('A',300);e.frames(300);e.press('B',90);e.finish_dialogue()
 count=e.read('gPlayerPartyCount',1);assert 1<=count<=6,count
 sb=e.read('gSaveBlock2Ptr');chars={int(m[2],16):m[1] for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(ROOT/'charmap.txt').read_text(),re.M)}
 name=''
 for i in range(8):
  v=e.read(sb+i,1)
  if v==255:break
  name+=chars.get(v,'?')
 species=[party_species(e,index=i) for i in range(count)]
 assert all(0<s<440 for s in species),species
 location=e.location();assert location[0]<44 and location[2]<100 and location[3]<100,location
 before=preserved(e);e.screenshot(ROOT/'test-output/v198-user-save-field.png')
 start_action(e,1);e.frames(240);e.screenshot(ROOT/'test-output/v198-user-save-party.png');e.press('B',180);e.press('B',90);assert preserved(e)==before
 start_action(e,2);wait_task(e,'Task_BagMenu_HandleInput');e.screenshot(ROOT/'test-output/v198-user-save-bag.png');e.press('B',180);e.press('B',90);assert preserved(e)==before
 e=reload(e,'v198-user-save-roundtrip');assert preserved(e)==before and e.location()==location
 assert sha(original)==original_hash
 result={'rom_sha256':sha(ROOT/'pokefirered.gba'),'player_name':name,'location':location,'party_species':species,'party_levels':[e.read(e.symbols['gPlayerParty']+100*i+84,1) for i in range(count)],'money':before[1],'original_save_sha256':original_hash,'original_save_unchanged':True,'native_continue':True,'party_and_bag_menus':True,'native_save_and_cold_continue':True}
 (ROOT/'test-output/v198-user-save.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result),flush=True)
finally:
 e.close()
 assert sha(original)==original_hash
