"""Import pinned RHH Gen IV-IX data/assets into the native FireRed tables.
Downloads pinned RHH inputs into .local-tools/roster; generated JSON records
all projections to the existing move/ability engine. No existing species IDs
or save offsets are changed. Source credit accompanies imported assets.
"""
from pathlib import Path
import json,re,urllib.request,time
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from eclipse_evolutions import project, GENDER_FORM_ALIASES
ROOT=Path(__file__).resolve().parents[1]; CACHE=ROOT/'.local-tools/roster'
SHA='7b4344c7ee867c98c8fb9d6026791df4f8eaecf7'
ENTRIES=json.loads((ROOT/'data/eclipse-roster-source.json').read_text())
def source(path):
 f=CACHE/path
 if not f.exists():
  f.parent.mkdir(parents=True,exist_ok=True)
  f.write_bytes(urllib.request.urlopen(f'https://raw.githubusercontent.com/rh-hideout/pokeemerald-expansion/{SHA}/{path}',timeout=60).read())
 return f.read_text(encoding='utf-8')
GRAPHICS=source('src/data/graphics/pokemon.h')
GFX={}
for sym,path in re.findall(r'\b(gMon\w+)\[\]\s*=\s*INCGFX_\w+\("([^"]+)"',GRAPHICS):GFX.setdefault(sym,path)
MOVES=set(re.findall(r'#define (MOVE_\w+)\s+\d+', (ROOT/'include/constants/moves.h').read_text()))
ABILITIES=set(re.findall(r'#define (ABILITY_\w+)\s+\d+', (ROOT/'include/constants/abilities.h').read_text()))
MACHINES=re.findall(r'\bMOVE_\w+', (ROOT/'src/data/party_menu.h').read_text().split('sTMHMMoves')[1].split('};')[0])
GAMES=[json.loads(source(f'tools/learnset_helpers/porymoves_files/{x}.json')) for x in ('sv','swsh','bdsp','usum')]
LEVEL=source('src/data/pokemon/level_up_learnsets/gen_9.h')
LEARN={name:re.findall(r'LEVEL_UP_MOVE\(\s*(\d+),\s*(MOVE_\w+)\)',body) for name,body in re.findall(r'\b(s\w+LevelUpLearnset)\[\]\s*=\s*\{(.*?)\};',LEVEL,re.S)}
def field(body,key,default='0'):
 m=re.search(r'\.'+key+r'\s*=\s*([^,\n]+)',body);return m[1].strip() if m else default
def number(body,key,default=0):
 v=field(body,key,str(default))
 if '?' in v:v=v.split('?')[1].split(':')[0].strip()
 try:return int(v)
 except ValueError:return default
def text(body,key,default=''):
 m=re.search(r'\.'+key+r'\s*=\s*_\("([^"]+)"\)',body);return m[1] if m else default
def array(body,key,pattern):
 m=re.search(r'\.'+key+r'\s*=\s*(.*?)(?=,\s*\.|\n|$)',body)
 return re.findall(pattern,m[1]) if m else []

rows=[]
for nat in range(387,1026):
 r=ENTRIES[str(nat)];b=re.sub(r'\([^()]*\?\s*(TYPE_\w+)\s*:\s*TYPE_\w+\)',r'\1',r['body']);token=r['national'].replace('NATIONAL_DEX_','SPECIES_')
 source=r['token'][8:];name=text(b,'speciesName',source.title())
 learn=LEARN.get(field(b,'levelUpLearnset'),[])
 adapted=[(max(1,int(l)),m) for l,m in learn if m in MOVES]
 adapted=sorted(set(adapted),key=lambda x:x[0])
 if not adapted:raise ValueError(('No supported level moves',nat,name))
 teach=set()
 for game in GAMES:
  g=game.get(source,game.get(token[8:],{}));teach.update(g.get('TMMoves',[]))
 abilities=array(b,'abilities',r'ABILITY_\w+')[:2]
 native_abilities=[a if a in ABILITIES else 'ABILITY_NONE' for a in abilities]
 native_abilities=(native_abilities+['ABILITY_NONE']*2)[:2]
 gfx={}
 for k in ('frontPic','backPic','palette','shinyPalette','iconSprite'):
  sym=field(b,k);assert sym in GFX,(name,k,sym);gfx[k]=GFX[sym]
 fp=re.search(r'FOOTPRINT\((\w+)\)',b)
 if fp and 'gMonFootprint_'+fp[1] in GFX:gfx['footprint']=GFX['gMonFootprint_'+fp[1]]
 row={'national':nat,'id':nat+53,'token':token,'source_token':r['token'],'name':name,'generation':4 if nat<=493 else 5 if nat<=649 else 6 if nat<=721 else 7 if nat<=809 else 8 if nat<=905 else 9,
 'stats':{k:number(b,k,50) for k in ('baseHP','baseAttack','baseDefense','baseSpeed','baseSpAttack','baseSpDefense')},'types':array(b,'types',r'TYPE_\w+'),
 'catchRate':number(b,'catchRate',45),'expYield':min(255,number(b,'expYield',100)),'genderRatio':field(b,'genderRatio','MON_GENDERLESS'),'eggCycles':number(b,'eggCycles',20),
 'growthRate':field(b,'growthRate','GROWTH_MEDIUM_FAST'),'eggGroups':array(b,'eggGroups',r'EGG_GROUP_\w+'),'abilities':native_abilities,'source_abilities':abilities,'bodyColor':field(b,'bodyColor','BODY_COLOR_GRAY'),
 'evYield':{k:number(b,'evYield_'+k) for k in ('HP','Attack','Defense','Speed','SpAttack','SpDefense')},'category':text(b,'categoryName','UNKNOWN'),'height':number(b,'height',10),'weight':number(b,'weight',100),
 'moves':adapted,'omitted_moves':[(int(l),m) for l,m in learn if m not in MOVES],'machines':[i for i,m in enumerate(MACHINES) if m in teach],
 'frontOffset':number(b,'frontPicYOffset',8),'backOffset':number(b,'backPicYOffset',8),'iconPalette':number(b,'iconPalIndex'), 'assets':gfx,
 'evolutions':re.findall(r'\{(EVO_\w+),\s*([^,}]+),\s*(SPECIES_\w+)\}',b)}
 assert len(row['types']) in (1,2) and row['iconPalette']<6,(name,row['types'],row['iconPalette'])
 rows.append(row)
print('Prepared',len(rows),'species; machine moves',len(MACHINES),flush=True)
paths=sorted({p for r in rows for p in r['assets'].values()} | {'CREDITS.md'} | {f'graphics/pokemon/icon_palettes/pal{i}.pal' for i in range(6)})
def fetch(path):
 f=CACHE/path;f.parent.mkdir(parents=True,exist_ok=True)
 if not f.exists():
  for attempt in range(4):
   try:f.write_bytes(urllib.request.urlopen(f'https://raw.githubusercontent.com/rh-hideout/pokeemerald-expansion/{SHA}/{path}',timeout=60).read());break
   except Exception:
    if attempt==3:raise
    time.sleep(1+attempt)
 return path
with ThreadPoolExecutor(max_workers=12) as pool:
 for i,_ in enumerate(pool.map(fetch,paths)):
  if i%300==0:print('Cached assets',i,'/',len(paths),flush=True)
OUT=ROOT/'src/data/eclipse_roster';OUT.mkdir(exist_ok=True)
for i in range(6):
 dst=ROOT/f'graphics/pokemon/icon_palettes/eclipse_palette_{i}.pal'
 dst.write_bytes((CACHE/f'graphics/pokemon/icon_palettes/pal{i}.pal').read_bytes())
def write(path,s):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(s.encode('utf-8'))
def inc(name,s):write('src/data/eclipse_roster/'+name+'.h',s+'\n')
credit=(CACHE/'CREDITS.md').read_bytes();(ROOT/'data/RHH-ROSTER-CREDITS.md').write_bytes(credit)
write('data/eclipse-roster.json',json.dumps({'source':'https://github.com/rh-hideout/pokeemerald-expansion','commit':SHA,'projection':'Gen III move/ability subset; original species unchanged','species':rows},indent=2)+'\n')
gfx=[];decl=[];front=[];back=[];pal=[];shiny=[];icons=[];iconp=[];foot=[];stats=[];names=[];levels=[];ptrs=[];tms=[];dex=[];evo=[];evo_audit=[];coordsf=[];coordsb=[];elevation=[]
source_to_token={r['source_token']:r['token'] for r in rows};source_to_token.update(GENDER_FORM_ALIASES);existing_species=set(re.findall(r'#define (SPECIES_\w+)\s+\d+', (ROOT/'include/constants/species.h').read_text()))
dextexts=[]
for r in rows:
 n=r['national'];token=r['token'];folder=f'graphics/pokemon/eclipse_roster/{n}';dst=ROOT/folder;dst.mkdir(parents=True,exist_ok=True)
 for k,out,size in (('frontPic','front',(64,64)),('backPic','back',(64,64)),('iconSprite','icon',(32,64)),('footprint','footprint',(16,16))):
  if k not in r['assets']:continue
  im=Image.open(CACHE/r['assets'][k]);assert im.mode=='P',(n,k,im.mode)
  assert im.width>=size[0] and im.height>=size[1],(n,k,im.size)
  im.crop((0,0,*size)).save(dst/(out+'.png'))
 for k,out in (('palette','normal'),('shinyPalette','shiny')):(dst/(out+'.pal')).write_bytes((CACHE/r['assets'][k]).read_bytes())
 for name,suffix,ctype in (('Front','front.4bpp.lz','u32'),('Back','back.4bpp.lz','u32'),('Pal','normal.gbapal.lz','u32'),('Shiny','shiny.gbapal.lz','u32'),('Icon','icon.4bpp','u8')):
  sym=f'gEclipse{name}{n}';gfx.append(f'const {ctype} {sym}[] = INCBIN_{ctype.upper()}("{folder}/{suffix}");');decl.append(f'extern const {ctype} {sym}[];')
 front.append(f'[{token}] = {{gEclipseFront{n}, 0x800, {token}}},');back.append(f'[{token}] = {{gEclipseBack{n}, 0x800, {token}}},')
 pal.append(f'[{token}] = {{gEclipsePal{n}, {token}}},');shiny.append(f'[{token}] = {{gEclipseShiny{n}, {token}}},');icons.append(f'[{token}] = gEclipseIcon{n},');iconp.append(f'[{token}] = {r["iconPalette"]},')
 if 'footprint' in r['assets']:
  gfx.append(f'const u8 gEclipseFoot{n}[] = INCBIN_U8("{folder}/footprint.1bpp");');decl.append(f'extern const u8 gEclipseFoot{n}[];');foot.append(f'[{token}] = gEclipseFoot{n},')
 else:foot.append(f'[{token}] = gMonFootprint_Bulbasaur,')
 body=[f'.{k} = {v}' for k,v in r['stats'].items()]+[f'.types = {{{r["types"][0]}, {r["types"][-1]}}}',f'.catchRate = {r["catchRate"]}',f'.expYield = {r["expYield"]}']
 body += [f'.evYield_{k} = {v}' for k,v in r['evYield'].items()]
 eggs=r['eggGroups'] or ['EGG_GROUP_UNDISCOVERED'];eggs=[x.replace('EGG_GROUP_NO_EGGS_DISCOVERED','EGG_GROUP_UNDISCOVERED') for x in eggs]
 body += [f'.genderRatio = {r["genderRatio"]}',f'.eggCycles = {r["eggCycles"]}', '.friendship = 70', f'.growthRate = {r["growthRate"]}', f'.eggGroups = {{{eggs[0]}, {eggs[-1]}}}',f'.abilities = {{{", ".join(r["abilities"])}}}', f'.bodyColor = {r["bodyColor"]}', '.noFlip = FALSE']
 stats.append(f'[{token}] = {{'+', '.join(body)+'},');native_name=r['name'].upper().replace(':','').replace('-',' ');native_name=native_name[:10];names.append(f'[{token}] = _("{native_name}"),')
 levels.append(f'static const u16 sEclipseLearn{n}[] = {{'+', '.join(f'LEVEL_UP_MOVE({l}, {m})' for l,m in r['moves'])+', LEVEL_UP_END};');ptrs.append(f'[{token}] = sEclipseLearn{n},')
 mask=sum(1<<i for i in r['machines']);tms.append(f'[{token}] = {{0x{mask&0xffffffff:08x}, 0x{mask>>32:08x}}},')
 category=r['category'].upper()[:11];desc=f'GENERATION {r["generation"]} - {category}.\\nFind partners across Europe.\\nSELECT shows its learnable moves.'
 dex.append(f'[NATIONAL_DEX_{token[8:]}] = {{.categoryName = _("{category}"), .height = {r["height"]}, .weight = {r["weight"]}, .description = sEclipseDex{n}, .unusedDescription = sEclipseDex{n}, .pokemonScale = 256, .trainerScale = 256}},')
 dextexts.append(f'static const u8 sEclipseDex{n}[] = _("{desc}");')
 supported, omitted = project(ENTRIES[str(n)]['body'], existing_species | set(source_to_token.values()), set(re.findall(r'#define (ITEM_\w+)\s+', (ROOT/'include/constants/items.h').read_text())), source_to_token, MOVES)
 evo_audit.append(dict(species=token, supported=supported, omitted=omitted))
 evos=['{'+', '.join(rule)+'}' for rule in supported]
 if evos:evo.append(f'[{token}] = {{'+', '.join(evos[:5])+'},')
 coordsf.append(f'[{token}] = {{MON_COORDS_SIZE(64, 64), {r["frontOffset"]}}},');coordsb.append(f'[{token}] = {{MON_COORDS_SIZE(64, 64), {r["backOffset"]}}},');elevation.append(f'[{token}] = 0,')
for name,data in [('assets',gfx),('declarations',decl),('front',front),('back',back),('palette',pal),('shiny',shiny),('icons',icons),('icon_palette',iconp),('footprints',foot),('stats',stats),('names',names),('learnsets',levels),('learnset_pointers',ptrs),('machines',tms),('dex',dex),('dex_text',dextexts),('evolutions',evo),('front_coords',coordsf),('back_coords',coordsb),('elevation',elevation)]:inc(name,'\n'.join(data))
(ROOT/'data/eclipse-evolution-projection.json').write_text(json.dumps(evo_audit,indent=2)+'\n',encoding='utf-8')
# Each country has a reproducible 16-17 member reserve; guardians keep their own gates.
guardians=[r['token'] for r in rows if re.search(r'\.is(?:RestrictedLegendary|SubLegendary|Mythical)\s*=\s*TRUE', ENTRIES[str(r['national'])]['body'])]
old_legends = {'ARTICUNO','ZAPDOS','MOLTRES','MEWTWO','MEW','RAIKOU','ENTEI','SUICUNE','LUGIA','HO_OH','CELEBI','REGIROCK','REGICE','REGISTEEL','LATIAS','LATIOS','KYOGRE','GROUDON','RAYQUAZA','JIRACHI','DEOXYS'}
named_guardians = {'ARTICUNO','ZAPDOS','MOLTRES','SUICUNE','LUGIA','HO_OH','MEWTWO'}
old_species = [(token,int(n)) for token,n in re.findall(r'#define (SPECIES_\w+)\s+(\d+)\s*$', (ROOT/'include/constants/species.h').read_text(), re.M) if 1 <= int(n) <= 251 or 277 <= int(n) <= 411]
old_reserve = [token for token,n in old_species if token[8:] not in old_legends]
old_guardians = [token for token,n in old_species if token[8:] in old_legends - named_guardians]
inc('reserve_species',',\n'.join(old_reserve + [r['token'] for r in rows if r['token'] not in guardians]))
inc('guardians',',\n'.join(old_guardians + guardians))
print('Generated 639 species; reserves include original partners and preserve named guardian gates.',flush=True)
