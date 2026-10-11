"""Prevent nested source requirements from becoming unconditional evolutions."""
import re
import json
from emulator import ROOT
from eclipse_evolutions import project
species={'SPECIES_LUCARIO','SPECIES_CHANSEY'};items={'ITEM_OVAL_STONE'}
def rule(conditions): return '.evolutions = EVOLUTION({EVO_LEVEL, 0, SPECIES_LUCARIO, CONDITIONS('+conditions+')}),'
assert project(rule('{IF_MIN_FRIENDSHIP, FRIENDSHIP_EVO_THRESHOLD},{IF_NOT_TIME, TIME_NIGHT}'),species,items)[0]==[('EVO_FRIENDSHIP_DAY','0','SPECIES_LUCARIO')]
for condition in ('{IF_GENDER, MON_FEMALE}','{IF_HOLD_ITEM, ITEM_OVAL_STONE}','{IF_KNOWS_MOVE, MOVE_ANCIENT_POWER}'):
    accepted,omitted=project(rule('{IF_MIN_FRIENDSHIP, FRIENDSHIP_EVO_THRESHOLD},'+condition),species,items)
    assert not accepted and len(omitted)==1
accepted,omitted=project('.evolutions = EVOLUTION({EVO_LEVEL, 20, SPECIES_LUCARIO},{EVO_ITEM, ITEM_OVAL_STONE, SPECIES_CHANSEY, CONDITIONS({IF_NOT_TIME, TIME_NIGHT})}),',species,items)
assert accepted==[('EVO_LEVEL','20','SPECIES_LUCARIO')] and len(omitted)==1
rows=json.loads((ROOT/'data/eclipse-evolution-projection.json').read_text())
assert len(rows)==639
rules={r['species']:r['supported'] for r in rows}
for token in ('BUDEW','BUNEARY','CHINGLING','MUNCHLAX','RIOLU','WOOBAT','SWADLOON','TYPE_NULL','SNOM'):
    assert rules['SPECIES_'+token][0][0].startswith('EVO_FRIENDSHIP')
for token in ('CHERUBI','SHELLOS','SCATTERBUG','SPEWPA','FLABEBE','PUMPKABOO','FINIZEN'):
    assert rules['SPECIES_'+token],token
print('PASS: nested unsupported conditions rejected; nine friendship routes and seven base-form aliases preserved')

from eclipse_evolutions import GENDER_FORM_ALIASES
body='.evolutions = EVOLUTION({EVO_LEVEL, 21, SPECIES_VESPIQUEN, CONDITIONS({IF_GENDER, MON_FEMALE})}),'
assert project(body,{'SPECIES_VESPIQUEN'},set())[0]==[('EVO_LEVEL_FEMALE','21','SPECIES_VESPIQUEN')]
for extra in ('{IF_GENDER, MON_MALE}','{IF_TIME, TIME_NIGHT}'):
    assert not project(body.replace('{IF_GENDER, MON_FEMALE}','{IF_GENDER, MON_FEMALE},'+extra),{'SPECIES_VESPIQUEN'},set())[0]
assert not project(body.replace('MON_FEMALE','MON_GENDERLESS'),{'SPECIES_VESPIQUEN'},set())[0]
assert project(body.replace('21','25').replace('SPECIES_VESPIQUEN','SPECIES_MEOWSTIC_F'),{'SPECIES_MEOWSTIC'},set(),GENDER_FORM_ALIASES)[0]==[('EVO_LEVEL_FEMALE','25','SPECIES_MEOWSTIC')]
for token in ('BURMY','ESPURR','LECHONK'):assert len(rules['SPECIES_'+token])==2
print('PASS: gender rules, both-gender base projections, and contradictory/extra condition rejection')

body='.evolutions = EVOLUTION({EVO_ITEM, ITEM_DAWN_STONE, SPECIES_GALLADE, CONDITIONS({IF_GENDER, MON_MALE})}),'
assert project(body,{'SPECIES_GALLADE'},{'ITEM_DAWN_STONE'})[0]==[('EVO_ITEM_MALE','ITEM_DAWN_STONE','SPECIES_GALLADE')]
assert not project(body,{'SPECIES_GALLADE'},set())[0]
assert not project(body.replace('{IF_GENDER, MON_MALE}','{IF_GENDER, MON_MALE},{IF_TIME, TIME_NIGHT}'),{'SPECIES_GALLADE'},{'ITEM_DAWN_STONE'})[0]
for token in ('MINCCINO','LAMPENT','FLOETTE','DOUBLADE','CRABRAWLER','CETODDLE'):assert rules['SPECIES_'+token][0][0]=='EVO_ITEM'
print('PASS: six imported stone routes and conditional Dawn Stone item availability')

body='.evolutions = EVOLUTION({EVO_LEVEL, 0, SPECIES_SYLVEON, CONDITIONS({IF_MIN_FRIENDSHIP, FRIENDSHIP_EVO_THRESHOLD},{IF_KNOWS_MOVE_TYPE, TYPE_FAIRY})}),'
assert project(body,{'SPECIES_SYLVEON'},set())[0]==[('EVO_FRIENDSHIP_MOVE_TYPE','TYPE_FAIRY','SPECIES_SYLVEON')]
for bad in (body.replace('TYPE_FAIRY','TYPE_UNKNOWN'),body.replace('{IF_KNOWS_MOVE_TYPE, TYPE_FAIRY}','{IF_KNOWS_MOVE_TYPE, TYPE_FAIRY},{IF_TIME, TIME_NIGHT}'),body.replace('FRIENDSHIP_EVO_THRESHOLD','1')):
    assert not project(bad,{'SPECIES_SYLVEON'},set())[0]
print('PASS: friendship plus Fairy move type; unknown types and extra conditions rejected')

# Original animation indices must remain stable when new moves are appended.
anims=(ROOT/'data/battle_anim_scripts.s').read_text().split('gBattleAnims_Moves::',1)[1].split('gBattleAnims_StatusConditions::',1)[0]
pointers=re.findall(r'\.4byte (Move_\w+)',anims)
assert len(pointers)==362 and pointers[68]=='Move_COUNTER' and pointers[360]=='Move_CHARM' and pointers[361]=='Move_COUNT'
print('PASS: original move animation indices and appended move/sentinel remain aligned')

body='.evolutions = EVOLUTION({EVO_LEVEL, 0, SPECIES_CHANSEY, CONDITIONS({IF_NOT_TIME, TIME_NIGHT},{IF_HOLD_ITEM, ITEM_OVAL_STONE})}),'
assert project(body,{'SPECIES_CHANSEY'},{'ITEM_OVAL_STONE'})[0]==[('EVO_LEVEL_ITEM_DAY','ITEM_OVAL_STONE','SPECIES_CHANSEY')]
assert project(body.replace('IF_NOT_TIME','IF_TIME'),{'SPECIES_CHANSEY'},{'ITEM_OVAL_STONE'})[0]==[('EVO_LEVEL_ITEM_NIGHT','ITEM_OVAL_STONE','SPECIES_CHANSEY')]
for bad in (body.replace('TIME_NIGHT','TIME_EVENING'),body.replace('{IF_HOLD_ITEM, ITEM_OVAL_STONE}','{IF_HOLD_ITEM, ITEM_OVAL_STONE},{IF_GENDER, MON_FEMALE}'),body.replace('EVO_LEVEL, 0','EVO_LEVEL, 10')):
    assert not project(bad,{'SPECIES_CHANSEY'},{'ITEM_OVAL_STONE'})[0]
assert not project(body,{'SPECIES_CHANSEY'},set())[0]
assert next(r for r in rows if r['species']=='SPECIES_HAPPINY')['supported']==[['EVO_LEVEL_ITEM_DAY','ITEM_OVAL_STONE','SPECIES_CHANSEY']]
print('PASS: held-item time conditions, item availability and additional-condition rejection')
