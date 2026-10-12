"""Project supported regular ability slots without changing other species data.
Pinned families are fetched into the roster cache when missing; hidden slots stay omitted.
"""
import json,re,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CLASSIC={name:'ABILITY_TECHNICIAN' for name in ('MEOWTH','PERSIAN','SCYTHER','SCIZOR','SMEARGLE','HITMONTOP')}
CLASSIC.update({name:'ABILITY_SKILL_LINK' for name in ('SHELLDER','CLOYSTER')})
CLASSIC['HITMONCHAN']='ABILITY_IRON_FIST'
CLASSIC['EEVEE']='ABILITY_ADAPTABILITY'
CLASSIC['HITMONLEE']='ABILITY_RECKLESS'
CLASSIC.update({name:'ABILITY_SUPER_LUCK' for name in ('MURKROW','ABSOL')})
CLASSIC.update({name:'ABILITY_TINTED_LENS' for name in ('VENONAT','VENOMOTH','ILLUMISE')})
CLASSIC['CAMERUPT']='ABILITY_SOLID_ROCK'
CLASSIC['MR_MIME']='ABILITY_FILTER'
CLASSIC.update({name:'ABILITY_SNIPER' for name in ('HORSEA','SEADRA','KINGDRA','REMORAID','OCTILLERY')})
def family_source(gen):
    path=f'src/data/pokemon/species_info/gen_{gen}_families.h'
    cached=ROOT/'.local-tools/roster'/path
    if not cached.exists():
        url='https://raw.githubusercontent.com/rh-hideout/pokeemerald-expansion/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/'+path
        content=urllib.request.urlopen(url,timeout=60).read()
        cached.parent.mkdir(parents=True,exist_ok=True);cached.write_bytes(content)
    return cached.read_text(encoding='utf-8')

def refresh():
    supported=set(re.findall(r'#define (ABILITY_\w+)\s+\d+', (ROOT/'include/constants/abilities.h').read_text(encoding='utf-8')))
    p=ROOT/'data/eclipse-roster.json';meta=json.loads(p.read_text(encoding='utf-8'))
    stats_path=ROOT/'src/data/eclipse_roster/stats.h';stats=stats_path.read_text(encoding='utf-8');changed=[]
    for row in meta['species']:
        values=[a if a in supported else 'ABILITY_NONE' for a in row['source_abilities'][:2]]
        values=(values+['ABILITY_NONE']*2)[:2]
        if row['abilities']!=values:changed.append(row['token'])
        row['abilities']=values
        pattern=r'(\['+row['token']+r'\].*?\.abilities\s*=\s*)\{[^}]*\}'
        stats,count=re.subn(pattern,lambda m:m[1]+'{'+', '.join(values)+'}',stats)
        assert count==1,row['token']
    families=''.join(family_source(gen) for gen in (1,2,3))
    classic_path=ROOT/'src/data/pokemon/species_info.h';classic=classic_path.read_text(encoding='utf-8')
    for name,expected in CLASSIC.items():
        body=re.search(r'\[SPECIES_'+name+r'\]\s*=\s*\{(.*?)(?=\n\s*\[SPECIES_|\Z)',families,re.S)[1]
        match=re.search(r'\.abilities\s*=\s*\{([^}]*)\}',body)
        if match:
            ability_text=match[1] # Modern branch appears first in pinned source.
        else:
            macro=re.search(r'\.abilities\s*=\s*(\w+)',body)[1]
            candidates=re.findall(r'#define\s+'+macro+r'\s+\{([^}]*)\}',families)
            ability_text=next(v for v in candidates if expected in v)
        values=re.findall(r'ABILITY_\w+',ability_text)[:2]
        assert expected in values and all(v in supported for v in values),name
        pattern=r'(\[SPECIES_'+name+r'\]\s*=\s*\{.*?\.abilities\s*=\s*)\{[^}]*\}'
        classic,count=re.subn(pattern,lambda m:m[1]+'{'+', '.join(values)+'}',classic,flags=re.S)
        assert count==1,name
    p.write_bytes((json.dumps(meta,ensure_ascii=False,indent=2)+'\n').encode())
    stats_path.write_bytes(stats.encode());classic_path.write_bytes(classic.encode())
    print('Restored',len(changed),'imported ability slots:',', '.join(changed),';',len(CLASSIC),'classic regular slots verified')
if __name__=='__main__':refresh()
