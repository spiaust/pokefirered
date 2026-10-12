"""All compiled imported learnsets must match metadata and preserve prior lessons."""
import json,subprocess
from emulator import Emulator,ROOT
from test_eclipse_move_evolution import moves
meta=json.loads((ROOT/'data/eclipse-roster.json').read_text())['species']
baseline=json.loads(subprocess.check_output(['git','show','bac223d7d:data/eclipse-roster.json'],cwd=ROOT).decode())['species']
old={r['national']:r['moves'] for r in baseline}
e=Emulator(ROOT/'pokefirered.gba')
try:
    total=changed=0
    for row in meta:
        assert all(pair in row['moves'] for pair in old[row['national']])
        total+=len(row['moves'])-len(old[row['national']]);changed+=row['moves']!=old[row['national']]
        pointer=e.read(e.symbols['gLevelUpLearnsets']+4*row['id']);actual=[]
        for i in range(25):
            value=e.read(pointer+2*i,2)
            if value==65535:break
            actual.append([value>>9,value&511])
        else:raise AssertionError('No learnset terminator: '+row['name'])
        assert actual==[[level,moves[move]] for level,move in row['moves']],row['name']
        assert len(actual)<=24
    assert total>=88 and changed>=80,(total,changed)
    print('PASS: all 639 compiled learnsets match metadata; previous lessons retained;',total,'new lessons across',changed,'species')
finally:e.close()
