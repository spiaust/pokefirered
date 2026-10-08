"""Soundtrack IDs, original score loops, and town bindings preserve gameplay data."""
from pathlib import Path
import json,re,hashlib,subprocess,sys
r=Path(__file__).resolve().parents[1];base=r/'data/geography/v124-presentation'
scores=json.loads((r/'data/geography/europe-music.json').read_text())
table=re.findall(r'^\s*song (\w+),', (r/'sound/song_table.inc').read_text(),re.M)
old_table=re.findall(r'^\s*song (\w+),',(base/'sound/song_table.inc').read_text(),re.M)
assert table[:347]==old_table and len(table)==354
for s in scores:
 assert table[s['id']]==s['symbol']
 assert re.search(r'#define MUS_EUROPE_'+s['symbol'][11:].upper()+r'\s+'+str(s['id'])+r'\b',(r/'include/constants/songs.h').read_text())
 if s['map']:
  p=Path('data/maps')/s['map']/'map.json';now=json.loads((r/p).read_text());old=json.loads((base/p).read_text())
  assert now.pop('music')=='MUS_EUROPE_'+s['symbol'][11:].upper();old.pop('music');assert now==old
print('PASS: seven appended music IDs retain all 347 existing songs; six town maps change music only')
hashes={s['symbol']:hashlib.sha256((r/'sound/songs'/(s['symbol']+'.s')).read_bytes()).hexdigest() for s in scores}
subprocess.run([sys.executable,str(r/'scripts/build-europe-music.py')],check=True,stdout=subprocess.DEVNULL)
assert len(set(hashes.values()))==7
for s in scores:
 p=r/'sound/songs'/(s['symbol']+'.s');assert hashlib.sha256(p.read_bytes()).hexdigest()==hashes[s['symbol']]
 text=p.read_text();assert text.count('.byte GOTO')==4 and text.count('.byte FINE')==4
 for body in re.findall(r'_loop:\n(.*?)\t.byte GOTO',text,re.S):
  assert sum(map(int,re.findall(r'\.byte W(\d+)',body)))==768
print('PASS: seven distinct original scores regenerate exactly; all 28 tracks loop at the same eight-bar boundary')
title=(r/'src/europe_title.c').read_text()
font=(r/'src/text.c').read_text()
widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)}
for text in re.findall(r'_\("([^"]+)"\)',title):assert sum(widths[chars[c]] for c in text)<=232,text
for caption in ['LONDON','PARIS','BERLIN','OXFORD','CHANTILLY','ORANIENBURG']:assert caption in title
assert 'SPECIES_CELEBI' in title and 'Sin(' in title and 'Cos(' in title
assert 'CB2_InitMainMenu' in title and 'LoadGameSave(SAVE_NORMAL)' in title and 'CB2_SaveClearScreen_Init' in title
print('PASS: title text fits; animated title includes Celebi, six towns, normal main-menu/save loading and special entry points')
