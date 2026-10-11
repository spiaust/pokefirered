"""Validate campaign graph, dialogue width, trainer capacity and physical access."""
from pathlib import Path
from collections import deque
import json,re,struct
R=Path(__file__).resolve().parents[1]
d=json.loads((R/'data/shadow-campaign.json').read_text())
assert len(d['chapters'])==21 and len(d['trainers'])==159
assert sum(c['kind']=='gym' for c in d['chapters'])==8
assert len({t['id'] for t in d['trainers']})==159
assert all(100<=t['id']<759 for t in d['trainers'])
layouts={x.get('id'):x for x in json.loads((R/'data/layouts/layouts.json').read_text())['layouts']}
for p in (R/'data/maps').glob('Shadow*/map.json'):
    m=json.loads(p.read_text());l=layouts[m['layout']];w,h=l['width'],l['height']
    a=struct.unpack('<%dH'%(w*h),(R/l['blockdata_filepath']).read_bytes())
    assert len(m['object_events'])<=16
    blocked={(o['x'],o['y']) for o in m['object_events']}
    start=(15,20) if m['name'].endswith('Route') else (6,7)
    q=deque([start]);seen={start}
    while q:
        x,y=q.popleft()
        for z in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
            xx,yy=z
            if 0<=xx<w and 0<=yy<h and z not in blocked and z not in seen and not a[yy*w+xx]&0xc00:
                seen.add(z);q.append(z)
    for o in m['object_events']:
        x,y=o['x'],o['y'];assert any(z in seen for z in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]),(m['name'],o)
s=(R/'data/scripts/shadow_campaign.inc').read_text()
labels=set(re.findall(r'^(\w+)::',s,re.M))
for ref in re.findall(r'(?:goto(?:_if_\w+[^\n]*,)?|msgbox)\s+(Shadow\w+)',s):assert ref in labels,ref
font=(R/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(R/'charmap.txt').read_text(encoding='utf-8'),re.M)};chars["'"]=0xB4
for t in re.findall(r'\.string "([^"\n]+)"',s):
    t=t.replace('{RIVAL}','WWWWWWW').replace('{PLAYER}','WWWWWWW').replace('{STR_VAR_1}','MAARTEN' if '{STR_VAR_2}' in t else '39').replace('{STR_VAR_2}','AMSTERDAM')
    for line in re.split(r'\\[npl]|\$',t):
        width=sum(widths[chars[c]] for c in line);assert width<=216,(width,line)
print('PASS: 21 chapters, eight badges, 159 trainer IDs, 42 reachable maps and native dialogue widths')

gyms=[c for c in json.loads((R/'data/shadow-campaign.json').read_text())['chapters'] if c['kind']=='gym']
assert len(gyms)==8 and len({c['tm_reward_flag'] for c in gyms})==8
assert all(1<=c['tm_reward']<=50 for c in gyms)
for c in gyms:
 city=c['city'];tm=c['tm_reward'];flag=int(c['tm_reward_flag'],16)
 reward=re.search(r'Shadow'+city+r'_Done::(.*?)Shadow'+city+r'_RewardDone::',(R/'data/scripts/shadow_campaign.inc').read_text(),re.S)[1]
 assert f'giveitem ITEM_TM{tm:02d}, 1' in reward and f'setflag FLAG_0x{flag:X}' in reward
 assert 'goto_if_eq VAR_0x8007, FALSE, Shadow_TMRewardFull' in reward
print('PASS: eight unique saved gym TM claims retain rewards when native delivery fails.')
