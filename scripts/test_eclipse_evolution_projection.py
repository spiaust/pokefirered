"""Prevent nested source requirements from becoming unconditional evolutions."""
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
