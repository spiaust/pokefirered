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
assert len(pointers)==366 and pointers[68]=='Move_COUNTER' and pointers[360]=='Move_CHARM' and pointers[361]=='Move_DOUBLE_SLAP' and pointers[362]=='Move_PSYBEAM' and pointers[363]=='Move_DRAGON_BREATH' and pointers[364]=='Move_HELPING_HAND' and pointers[365]=='Move_COUNT'
print('PASS: original move animation indices and appended move/sentinel remain aligned')

body='.evolutions = EVOLUTION({EVO_LEVEL, 0, SPECIES_CHANSEY, CONDITIONS({IF_NOT_TIME, TIME_NIGHT},{IF_HOLD_ITEM, ITEM_OVAL_STONE})}),'
assert project(body,{'SPECIES_CHANSEY'},{'ITEM_OVAL_STONE'})[0]==[('EVO_LEVEL_ITEM_DAY','ITEM_OVAL_STONE','SPECIES_CHANSEY')]
assert project(body.replace('IF_NOT_TIME','IF_TIME'),{'SPECIES_CHANSEY'},{'ITEM_OVAL_STONE'})[0]==[('EVO_LEVEL_ITEM_NIGHT','ITEM_OVAL_STONE','SPECIES_CHANSEY')]
for bad in (body.replace('TIME_NIGHT','TIME_EVENING'),body.replace('{IF_HOLD_ITEM, ITEM_OVAL_STONE}','{IF_HOLD_ITEM, ITEM_OVAL_STONE},{IF_GENDER, MON_FEMALE}'),body.replace('EVO_LEVEL, 0','EVO_LEVEL, 10')):
    assert not project(bad,{'SPECIES_CHANSEY'},{'ITEM_OVAL_STONE'})[0]
assert not project(body,{'SPECIES_CHANSEY'},set())[0]
assert next(r for r in rows if r['species']=='SPECIES_HAPPINY')['supported']==[['EVO_LEVEL_ITEM_DAY','ITEM_OVAL_STONE','SPECIES_CHANSEY']]
print('PASS: held-item time conditions, item availability and additional-condition rejection')

body='.evolutions = EVOLUTION({EVO_TRADE, 0, SPECIES_AROMATISSE, CONDITIONS({IF_HOLD_ITEM, ITEM_SACHET})}),'
assert project(body,{'SPECIES_AROMATISSE'},{'ITEM_SACHET'})[0]==[('EVO_TRADE_ITEM','ITEM_SACHET','SPECIES_AROMATISSE')]
for bad in (body.replace('IF_HOLD_ITEM','IF_TRADE_PARTNER'),body.replace('{IF_HOLD_ITEM, ITEM_SACHET}','{IF_HOLD_ITEM, ITEM_SACHET},{IF_TIME, TIME_NIGHT}'),body.replace('EVO_TRADE, 0','EVO_TRADE, 1')):
    assert not project(bad,{'SPECIES_AROMATISSE'},{'ITEM_SACHET'})[0]
assert not project(body,{'SPECIES_AROMATISSE'},set())[0]
assert not project('.evolutions = EVOLUTION({EVO_ITEM, ITEM_SACHET, SPECIES_AROMATISSE}),',{'SPECIES_AROMATISSE'},{'ITEM_SACHET'})[0]
for token,item,target in [('SPRITZEE','SACHET','AROMATISSE'),('SWIRLIX','WHIPPED_DREAM','SLURPUFF')]:
    r=next(r for r in rows if r['species']=='SPECIES_'+token)
    assert r['supported']==[['EVO_TRADE_ITEM','ITEM_'+item,'SPECIES_'+target]] and len(r['omitted'])==1
print('PASS: known held-item trade conditions, unavailable/extra/paired rules and direct-use alternatives')

assert not project('.evolutions = EVOLUTION({EVO_ITEM, ITEM_SACHET, SPECIES_AROMATISSE, CONDITIONS({IF_GENDER, MON_FEMALE})}),',{'SPECIES_AROMATISSE'},{'ITEM_SACHET'})[0]

body='.evolutions = EVOLUTION({EVO_LEVEL, 0, SPECIES_MANTINE, CONDITIONS({IF_SPECIES_IN_PARTY, SPECIES_REMORAID})}),'
assert project(body,{'SPECIES_MANTINE','SPECIES_REMORAID'},set())[0]==[('EVO_LEVEL_PARTY_SPECIES','SPECIES_REMORAID','SPECIES_MANTINE')]
assert not project(body,{'SPECIES_MANTINE'},set())[0]
assert not project(body.replace('EVO_LEVEL, 0','EVO_LEVEL, 20'),{'SPECIES_MANTINE','SPECIES_REMORAID'},set())[0]
body='.evolutions = EVOLUTION({EVO_LEVEL, 32, SPECIES_PANGORO, CONDITIONS({IF_TYPE_IN_PARTY, TYPE_DARK})}),'
assert project(body,{'SPECIES_PANGORO'},set())[0]==[('EVO_LEVEL_PARTY_TYPE','(32 << 8) | TYPE_DARK','SPECIES_PANGORO')]
assert not project(body.replace('TYPE_DARK','TYPE_UNKNOWN'),{'SPECIES_PANGORO'},set())[0]
assert not project(body.replace('{IF_TYPE_IN_PARTY, TYPE_DARK}','{IF_TYPE_IN_PARTY, TYPE_DARK},{IF_TIME, TIME_NIGHT}'),{'SPECIES_PANGORO'},set())[0]
body='.evolutions = EVOLUTION({EVO_LEVEL, 53, SPECIES_LUNALA, CONDITIONS({IF_TIME, TIME_NIGHT})}),'
assert project(body,{'SPECIES_LUNALA'},set())[0]==[('EVO_LEVEL_NIGHT','53','SPECIES_LUNALA')]
for bad in (body.replace('TIME_NIGHT','TIME_DUSK'),body.replace('EVO_LEVEL, 53','EVO_LEVEL, 101'),body.replace('{IF_TIME, TIME_NIGHT}','{IF_TIME, TIME_NIGHT},{IF_GENDER, MON_MALE}')):
    assert not project(bad,{'SPECIES_LUNALA'},set())[0]
print('PASS: bounded levels, party species/type requirements and time conditions remain conservative')

body='.evolutions = EVOLUTION({EVO_LEVEL, 50, SPECIES_GOODRA, CONDITIONS({IF_WEATHER, WEATHER_RAIN})}),'
assert project(body,{'SPECIES_GOODRA'},set())[0]==[('EVO_LEVEL_RAIN','50','SPECIES_GOODRA')]
assert project(body.replace('WEATHER_RAIN','WEATHER_FOG'),{'SPECIES_GOODRA'},set())[0]==[('EVO_LEVEL_FOG','50','SPECIES_GOODRA')]
for bad in (body.replace('WEATHER_RAIN','WEATHER_SNOW'),body.replace('EVO_LEVEL, 50','EVO_LEVEL, 101'),body.replace('{IF_WEATHER, WEATHER_RAIN}','{IF_WEATHER, WEATHER_RAIN},{IF_TIME, TIME_NIGHT}')):
    assert not project(bad,{'SPECIES_GOODRA'},set())[0]
assert len(next(r for r in rows if r['species']=='SPECIES_SLIGGOO')['supported'])==2
print('PASS: minimum-level rain/fog conditions preserve unknown-weather and extra-condition rejection')
