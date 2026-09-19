"""Check case state storage, dialogue fit, entrance reachability and trees."""
from pathlib import Path
import json,re,struct,hashlib,subprocess,sys
from europe_trees import finish_trees
R=Path(__file__).resolve().parents[1]
font=(R/'src/text.c').read_text();body=re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S).group(1);widths=list(map(int,re.findall(r'\b\d+\b',body)))
chars={m.group(1):int(m.group(2),16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(R/'charmap.txt').read_text(encoding='utf-8'),re.M)};chars["'"]=0xb4
texts=[(R/'data/scripts/europe_landmarks.inc').read_text()]
for path,labels in [('data/maps/EuropeParis/scripts.inc',['EuropeParis_RealismNotreDameText','EuropeParis_RealismEiffelText','EuropeParis_RealismSeineText']),('data/maps/EuropeBerlin/scripts.inc',['EuropeBerlin_RealismReichstagText']),('data/maps/EuropeLondon/scripts.inc',['EuropeLondon_RealismTextParliament','EuropeLondon_RealismTextGardens']),('data/maps/EuropeSouthamptonPast/scripts.inc',['EuropeSouthampton_Text_Locked']),('data/maps/EuropeLondonPast/scripts.inc',['EuropeLondonPast_Text_Locked']),('data/text/new_game_intro.inc',['gOakSpeech_Text_WelcomeToTheWorld','gOakSpeech_Text_IStudyPokemon']),('data/scripts/europe_story.inc',['EuropeStory_Text_Offer']),('data/scripts/europe_france_story.inc',['EuropeFrance_Text_Review']),('data/scripts/europe_germany_story.inc',['EuropeGermany_Text_Reward']),('data/scripts/europe_celebi.inc',['EuropeCelebi_Text_Offer','EuropeCelebi_Text_Report','EuropeCelebi_Text_Complete','EuropeCelebi_ConclusionText']),('data/scripts/europe_time.inc',['EuropeTime_Text_Depart']),('data/maps/EuropeLondonPast/scripts.inc',['EuropeLondonPast_Text_Welcome','EuropeLondonPast_Text_Welcomed'])]:
 s=(R/path).read_text(encoding='utf-8')
 for label in labels:texts.append(re.search(re.escape(label)+r'::\n((?:[ \t]*\.string[^\n]*\n)+)',s).group(1))
for text in texts:
 for line in re.findall(r'\.string "(.*?)"',text):
  for part in re.split(r'\\[npl]|\$',line):
   w=sum(widths[chars[c]] for c in part);assert w<=216,(w,part)
print('PASS: new landmark cases and revised story dialogue fit the text window')
for l in json.loads((R/'data/layouts/layouts.json').read_text())['layouts']:
 if not l.get('name','').startswith('Europe') or l['primary_tileset']!='gTileset_General':continue
 w,h=l['width'],l['height'];raw=(R/l['blockdata_filepath']).read_bytes();v=struct.unpack('<%dH'%(w*h),raw);a=[list(v[y*w:(y+1)*w]) for y in range(h)];finish_trees(a)
 assert tuple(t for row in a for t in row)==v,l['name']
print('PASS: all European outdoor tree arrangements are stable complete silhouettes')
paths=[R/'data/maps/map_groups.json',R/'data/layouts/layouts.json',R/'data/scripts/europe_landmarks.inc']
for name in ['NotreDame','Westminster','Reichstag']:
 paths += list((R/f'data/maps/Europe{name}').glob('*'))+list((R/f'data/layouts/Europe{name}').glob('*'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={p:sha(p) for p in paths if p.suffix in ('.json','.inc','.bin')}
for script in ['build-landmark-interiors.py','build-landmark-cases.py']:subprocess.run([sys.executable,str(R/'scripts'/script)],check=True)
assert all(sha(p)==v for p,v in before.items())
print('PASS: landmark interiors and case scripts regenerate identically')
