"""Extend native sprite coverage so visible encounters retain every encounter-table species."""
from pathlib import Path
from PIL import Image
import json,re
R=Path(__file__).resolve().parents[1]
W=json.loads((R/'src/data/wild_encounters.json').read_text());species={m['species'][8:] for x in W['wild_encounter_groups'][0]['encounters'] if x['map'].startswith(('MAP_SHADOW_','MAP_CONTINENT_')) for m in x.get('land_mons',{}).get('mons',[])}|{'HOUNDOUR','DRATINI'}
p=R/'include/constants/event_objects.h';defs=p.read_text();existing=set(re.findall(r'#define OBJ_EVENT_GFX_(\w+)\s+\d+',defs));todo=sorted(species-existing);nextid=int(re.search(r'NUM_OBJ_EVENT_GFX\s+(\d+)',defs)[1]);assert nextid+len(todo)<240
if not todo:
 print('Native sprites already cover all encounter species.');raise SystemExit(0)
colors={k:[tuple(map(int,t.split())) for t in (R/f'graphics/object_events/palettes/npc_{k.lower()}.pal').read_text().splitlines()[3:]] for k in ('BLUE','PINK','GREEN','WHITE')};slots={'BLUE':1,'PINK':2,'GREEN':3,'WHITE':4}
gfx='';pictures='';infos='';decls='';pointers='';cases=''
for j,sp in enumerate(todo):
 n=nextid+j;tag=sp.title().replace('_','');filename=sp.lower().replace('_','_');src=R/f'graphics/pokemon/{filename}/icon.png'
 assert src.exists(),src
 native=Image.open(src).crop((0,0,32,32));mask=Image.new('L',native.size);mask.putdata([0 if v==0 else 255 for v in native.getdata()]);mask=mask.resize((16,16),Image.Resampling.NEAREST);im=native.convert('RGB').resize((16,16),Image.Resampling.NEAREST)
 def nearest(palette,pixel):return min(range(1,16),key=lambda k:sum((palette[k][c]-pixel[c])**2 for c in range(3)))
 palette=min(colors,key=lambda k:sum(sum((colors[k][nearest(colors[k],im.getpixel((x,y)))][c]-im.getpixel((x,y))[c])**2 for c in range(3)) for y in range(16) for x in range(16) if mask.getpixel((x,y))))
 sheet=Image.new('P',(16,48));sheet.putpalette(sum((list(c) for c in colors[palette]),[])+[0]*720)
 for y in range(16):
  for x in range(16):
   idx=nearest(colors[palette],im.getpixel((x,y))) if mask.getpixel((x,y)) else 0
   for f in range(3):sheet.putpixel((x,y+f*16),idx)
 sheet.save(R/f'graphics/object_events/pics/pokemon/{filename}.png')
 defs=defs.replace('#define NUM_OBJ_EVENT_GFX',f'#define OBJ_EVENT_GFX_{sp} {n}\n#define NUM_OBJ_EVENT_GFX',1)
 gfx+=f'\nconst u16 gObjectEventPic_{tag}[] = INCBIN_U16("graphics/object_events/pics/pokemon/{filename}.4bpp");\n'
 pictures+=f'\nstatic const struct SpriteFrameImage sPicTable_{tag}[] = {{\n'+''.join(f' overworld_frame(gObjectEventPic_{tag}, 2, 2, {f}),\n' for f in [0,1,2,0,0,1,1,2,2])+'};\n'
 infos+=f'\nconst struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_{tag} = {{.tileTag = TAG_NONE, .paletteTag = OBJ_EVENT_PAL_TAG_NPC_{palette}, .reflectionPaletteTag = OBJ_EVENT_PAL_TAG_NONE, .size = 128, .width = 16, .height = 16, .paletteSlot = PALSLOT_NPC_{slots[palette]}, .shadowSize = SHADOW_SIZE_M, .inanimate = FALSE, .disableReflectionPaletteLoad = FALSE, .tracks = TRACKS_FOOT, .oam = &gObjectEventBaseOam_16x16, .subspriteTables = gObjectEventSpriteOamTables_16x16, .anims = sAnimTable_Standard, .images = sPicTable_{tag}, .affineAnims = gDummySpriteAffineAnimTable}};\n'
 decls+=f'const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_{tag};\n';pointers+=f' [OBJ_EVENT_GFX_{sp}] = &gObjectEventGraphicsInfo_{tag},\n';cases+=f'    case SPECIES_{sp}: return OBJ_EVENT_GFX_{sp};\n'
defs=re.sub(r'NUM_OBJ_EVENT_GFX\s+\d+',f'NUM_OBJ_EVENT_GFX     {nextid+len(todo)}',defs);p.write_text(defs)
for name,extra in [('object_event_graphics.h',gfx),('object_event_pic_tables.h',pictures),('object_event_graphics_info.h',infos)]:p=R/f'src/data/object_events/{name}';p.write_text(p.read_text()+extra)
p=R/'src/data/object_events/object_event_graphics_info_pointers.h';s=p.read_text();pos=s.rfind('};');s=s[:pos]+pointers+s[pos:];p.write_text(decls+s)
p=R/'src/wild_encounter.c';s=p.read_text().replace('    default: return 0xFFFF;',cases+'    default: return 0xFFFF;');p.write_text(s)
for name,sp in [('ShadowParis','PIKACHU'),('ShadowPrague','HOUNDOUR'),('ShadowZurich','EEVEE'),('ShadowParis1940','MAREEP'),('ShadowWarsaw1943','LAPRAS'),('ShadowBerlin1944','DRATINI')]:
 p=R/f'data/maps/{name}/map.json';m=json.loads(p.read_text());next(o for o in m['object_events'] if o['x']==8 and o['y']==3)['graphics_id']='OBJ_EVENT_GFX_'+sp;p.write_text(json.dumps(m,indent=2)+'\n')
print(len(todo),'native sprite adaptations added; all',len(species),'encounter and rescue species have appropriate sprites.')
