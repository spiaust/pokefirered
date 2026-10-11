"""Validate every imported species and the complete catchable reserve partition."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
rows=json.loads((ROOT/'data/eclipse-roster.json').read_text())['species']
assert len(rows)==639
assert next(r['types'] for r in rows if r['national']==468)==['TYPE_FAIRY','TYPE_FLYING']
assert [r['national'] for r in rows]==list(range(387,1026))
assert [r['id'] for r in rows]==list(range(440,1079))
all_tokens=set()
for name in ('reserve_species','guardians'):
    tokens=re.findall(r'SPECIES_\w+',(ROOT/f'src/data/eclipse_roster/{name}.h').read_text())
    assert len(tokens)==len(set(tokens))
    assert not all_tokens.intersection(tokens)
    all_tokens.update(tokens)
named={'SPECIES_'+n for n in ('ARTICUNO','ZAPDOS','MOLTRES','SUICUNE','LUGIA','HO_OH','MEWTWO')}
assert len(all_tokens|named)==1025 and not all_tokens.intersection(named)
for r in rows:
    assert r['token'] in all_tokens
    assert r['moves'] and len(r['moves'])<=24, r['name']
    assert all(1<=lv<=100 for lv,m in r['moves'])
    assert all(0<=n<58 for n in r['machines'])
    assert 0<=r['iconPalette']<=5
    folder=ROOT/f"graphics/pokemon/eclipse_roster/{r['national']}"
    assert all((folder/n).is_file() for n in ('front.png','back.png','icon.png','normal.pal','shiny.pal'))
    for name in ('front','back','palette','shiny','icons','stats','names','learnset_pointers','machines'):
        assert '['+r['token']+']' in (ROOT/f'src/data/eclipse_roster/{name}.h').read_text()
save=(ROOT/'include/global.h').read_text()
assert '#define DEX_FLAGS_NO 52' in save
assert 'u8 eclipseSeen[80]' in save and 'u8 eclipseCaught[80]' in save and 'u8 filler_BC0[0x360]' in save
print('PASS: 1025 obtainable species partition, all 639 imported tables/assets, learnset bounds and stable save extension')
