"""Build the complete illustrated v3.3 strategy book without external dependencies."""
from pathlib import Path
import re,html,json,shutil,hashlib
R=Path(__file__).resolve().parents[1];D=R/'strategy-guide/dist';(D/'images').mkdir(parents=True,exist_ok=True)
def inline(s):
 s=html.escape(s)
 s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
 s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
 s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:'<a href="'+('downloads/'+m[2] if m[2].endswith('.md') else m[2])+'">'+m[1]+'</a>',s)
 return s
def md(src):
 lines=src.splitlines();out=[];i=0
 while i<len(lines):
  line=lines[i]
  if not line.strip():i+=1;continue
  if line.startswith('|'):
   rows=[]
   while i<len(lines) and lines[i].startswith('|'):
    cells=[s.strip() for s in lines[i].strip().strip('|').split('|')]
    if not all(re.fullmatch(r':?-+:?',s.replace(' ','')) for s in cells):rows.append(cells)
    i+=1
   out.append('<div class="table-wrap"><table><thead><tr>'+''.join('<th scope="col">'+inline(s)+'</th>' for s in rows[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(s)+'</td>' for s in row)+'</tr>' for row in rows[1:])+'</tbody></table></div>');continue
  if line.startswith('### '):out.append('<h3>'+inline(line[4:])+'</h3>');i+=1;continue
  if re.match(r'^\d+\. ',line):
   items=[]
   while i<len(lines):
    match=re.match(r'^\d+\. (.*)',lines[i])
    if not match:break
    text=[match[1]];i+=1
    while i<len(lines) and (lines[i].startswith(' ') or (not lines[i].strip() and i+1<len(lines) and lines[i+1].startswith(' '))):
     text.append(lines[i].strip());i+=1
    items.append(' '.join(text))
    while i<len(lines) and not lines[i].strip():i+=1
   out.append('<ol class="steps">'+''.join('<li>'+inline(s)+'</li>' for s in items)+'</ol>');continue
  if line.startswith('- '):
   items=[]
   while i<len(lines) and lines[i].startswith('- '):items.append(lines[i][2:]);i+=1
   out.append('<ul>'+''.join('<li>'+inline(s)+'</li>' for s in items)+'</ul>');continue
  p=[]
  while i<len(lines) and lines[i].strip() and not re.match(r'^(### |\||\d+\. |- )',lines[i]):p.append(lines[i].strip());i+=1
  out.append('<p>'+inline(' '.join(p))+'</p>')
 return '\n'.join(out)
s=(R/'WALKTHROUGH.md').read_text(encoding='utf-8')
s=s.replace('There is no fourth\nGym or Elite Four step in this release\'s completion route.','There is no fourth Gym in the main route. The optional European Council unlocks after Ada\'s conclusion.')
s=re.sub(r'A combined v3\.0 check.*?on v3\.0\.','These five optional rooms support native Save/Continue, both south exits and return visits. They do not change story progress.',s,flags=re.S)
# Move French marker directions into the French chapter rather than the English one.
a=s.index('### Reach the French study markers');b=s.index('## Complete the French survey');markers=s[a:b];s=s[:a]+s[b:];insert=s.index('## Complete the German delivery');s=s[:insert]+markers+'\n'+s[insert:]
parts=re.split(r'^## ',s,flags=re.M)[1:];chapters=[]
for block in parts:
 title,body=block.split('\n',1)
 if title=='Optional activities and additional completion goals':continue
 if title.startswith('Regional landmark'):
  bits=re.split(r'^### ',body,flags=re.M);chapters.append({'title':title,'body':bits[0],'group':'Optional adventures'})
  for bit in bits[1:]:t,b=bit.split('\n',1);chapters.append({'title':t,'body':b,'group':'Optional adventures'})
 else:
  group='Main story'
  if title in ['Controls and directions','Customize the world and avatar','Start a new game','Travel and team preparation']:group='Getting started'
  if title.startswith('Optional Celebi') or title.startswith('European Council'):group='Expansion adventures'
  if title=='When progress seems stuck':group='Reference desk'
  chapters.append({'title':title,'body':body,'group':group})
images={
'Complete England':[('england.png','Oxford Gym entrance after earning the first badge.')],
'Complete the French':[('france.png','Chantilly square: the quest contact stands west of the guide.')],
'Complete the German':[('germany.png','Oranienburg Gym entrance after the third badge.')],
'Meet Ada':[('celebi.png','Chantilly Forest, home of the historical journey.')],
'Help Elise':[('refuge.png','The Chantilly refuge in 1940.'),('post.png','The historical station post.')],
'Check in at Beauvais':[('beauvais.png','Beauvais reception and its welcome desk.')],
'Supply Beauvais':[('garden.png','Beauvais reception garden: Luc and Pidgey’s chapter.')],
'Complete Amiens':[('amiens.png','Amiens arrival: use the paths to find Nora and the noticeboard.')],
'Verify the Amiens':[('rouen.png','Rouen reception: the route-book search begins here.')],
'Clear the Le Havre':[('le-havre.png','Le Havre’s historical dock and crossing contacts.')],
'Recover the Southampton':[('southampton.png','Southampton arrival and the luggage search.'),('london-1940.png','Historical London: finish Rose’s welcome.'),('main-ending.png','Ada’s explicit MAIN STORY COMPLETE conclusion.')],
'Regional landmark':[('chateau.png','Inside the château visitor room.'),('palace.png','Inside the palace visitor room.')],
'Optional Gastly':[('gastly.png','Notre Dame after the optional Gastly encounter.')],
'Collect tour stamps':[('stamps.png','The three capital guides award EXP. SHARE once.')],
'Borrow Lapras':[('lapras.png','The custom Lapras rental art on a saved river ride.')],
'Optional Celebi chapter':[('archive.png','Oxford’s Radcliffe archive researcher.'),('archive-ending.png','Celebi appears at the Letters for Tomorrow conclusion.')],
'European Council':[('council.png','Council Hall: five opponents across the north row.'),('council-battle.png','A real Council battle on the released ROM.')],
'Customize':[('custom-lapras.png','Saved avatar colors carry over to travel and riding.')]
}
E=R/'artifacts/releases/v3.3-evidence'
for source,name in [('archive-ending-celebi.png','archive-ending.png'),('council-england-match-1.png','council-battle.png'),('expansion-integration-custom-lapras.png','custom-lapras.png')]:shutil.copy2(E/source,D/'images'/name)
shutil.copy2(R/'test-output/release-england-ada-ending.png',D/'images/main-ending.png')
images.update({'Start a new':[('country-menu.png','Choose England, France or Germany at the start of a new adventure.')],'Travel and team':[('england.png','Station, clinic and Gym doors use normal walking entry.')],'Complete all three landmark':[('notredame.png','Notre Dame case interior.'),('westminster.png','Westminster case interior.'),('reichstag.png','Reichstag case interior.')],'Visit the capital':[('home.png','A London neighborhood home.')],'Remaining reading':[('reading.png','London reading room with its new Council reception.')],'Use the Bicycle':[('bicycle.png','The field Bicycle on an earned saved journey.')],'London/Oxford riverboat':[('riverboat.png','The London/Oxford riverboat route.')],'Present-day Dover':[('dover.png','Dover arrival and ferry departure contacts.'),('calais.png','Calais arrival and return contacts.')],'Explore Dover':[('dover.png','Dover’s present-day port.'),('calais.png','Calais’s present-day port.')],'Explore historical Southampton':[('southampton-quay.png','Historical Southampton Town Quay.')],'Explore historical Le Havre':[('le-havre.png','Le Havre’s historical port.')],'Explore historical Amiens':[('amiens-bridge.png','Amiens river crossing.')],'Explore historical Rouen':[('rouen-bridge.png','Rouen’s riverside arrival area.')],'Explore historical London':[('london-bridge.png','Historical London’s Westminster crossing.')],'Read the historical':[('london-1940.png','The 1940 London arrival and return point.')],'Revisit the past':[('celebi.png','Return to the present-day forest to revisit historical chapters.')],'Walk the regional':[('chateau.png','Optional landmark visitor room reached through its marked entrance.')]})
for idx,c in enumerate(chapters):
 c['id']=re.sub(r'[^a-z0-9]+','-',c['title'].lower()).strip('-');c['number']=idx+1;c['html']=md(c.pop('body'));c['images']=[]
 for prefix,ims in images.items():
  if c['title'].startswith(prefix):c['images']+=ims
 c['search']=re.sub('<[^>]+>',' ',c['html'])+' '+c['title']
# Reference pages consolidate actual rewards and verified secrets.
extra=[('Secrets & things worth finding','Reference desk',"""## Rewards off the main road
| Discovery | How to get it | Reward or benefit |
| --- | --- | --- |
| Three city stamps | Speak to London, Paris and Berlin guides | One EXP. SHARE; train a supporting partner |
| Quiet Bells | Resolve Notre Dame’s case peacefully | Spell Tag, then optional level-12 Gastly encounter |
| A Place to Rest | Resolve Westminster’s case | One Rare Candy |
| Broken Signal | Resolve Reichstag’s case | Three Great Balls |
| Three case synthesis | Collect all three case rewards, read a ledger or speak to Ada | Combined account; no extra battle required |
| Beauvais, Amiens and Rouen care | Finish each local help task | Free party healing becomes available |
| Historical dockworker and luggage worker | Finish their tasks | Free care during the crossing chapters |
| Letters for Tomorrow | Collect all three archive notes and return to Ada | One PP UP and an explicit Celebi conclusion |
| European Council | Win all five matches | Permanent Champion title and one Rare Candy |

## Keep these easy-to-miss rules in mind
- Returning to Oak, Celine and Lena for their rewards is part of Gym unlocking. Winning a rival battle or delivering a parcel alone is not enough.
- The Amiens train is offered by the station dispatcher after Luc’s reunion; the Beauvais noticeboard is not that onward service.
- The Le Havre crossing and London transport do not require their Ada accounts first. You can file them after the main ending.
- Gastly can be attempted after the Quiet Bells reward. Bring spare balls; a successful capture is not a story requirement.
- The World Options BIKE preview does not mount the field Bicycle. Use the Bicycle key item to ride.
- Archive notes and Council victories stay saved when you leave. Full reward pockets do not erase completed Council victories.
- Not every façade is enterable. Gallery and visitor-room doors use A and YES at the marked approach, while station, clinic and Gym doors use walking.

These are actual implemented discoveries and shortcuts. No unreleased countries, invented legendary encounters or unsupported cheat codes are included.
"""),('Battle desk: Gym & Council teams','Reference desk',"""| Battle | Pokémon | Preparation |
| --- | --- | --- |
| Oxford rival | Pidgey 7, Eevee 8 | Finish Oliver and Alice first; heal and bring Potions |
| Ellis | Geodude 10, Onix 12 | Grass or Water attacks; report to Oak first |
| Marine | Psyduck 12, Horsea 14 | Grass or Electric attacks; collect Celine’s Miracle Seed first |
| Conrad | Voltorb 14, Pikachu 16 | Ground attacks; Marshtomp is useful; bring Paralyze Heals |
| Alfred | Pidgeotto 18, Noctowl 18, Furret 19 | Heal, avoid a purely grass-based team |
| Solene | Butterfree 19, Weepinbell 19, Skiploom 20 | Flying support; avoid exposing water/ground Pokémon |
| Otmar | Magnemite 20, Voltorb 20, Machop 21 | Ground options; switch flying partners away from Electric attacks |
| Elara | Psyduck 21, Poliwhirl 21, Horsea 22 | Grass or Electric coverage |
| Rowan | Eevee 22, Pidgeotto 22, Ivysaur 22, Pikachu 23 | Varied party; Flying against Ivysaur, Ground against Pikachu |
| Coach Ivo | Sentret 14, Mareep 15, Eevee 16 | Repeatable normal experience and prize money; heal after wins |

Damage, status and move PP work normally. Use the POKEMON command to switch; use BAG for medicine. Council nurse care restores the whole party between matches. Raising levels helps, but partners and type coverage matter too. The three badges and Ada’s ending complete the main game; the Council is a separate post-story championship.
"""),('About this edition','Reference desk',"""This guide covers the published **v3.3** game, dated October 10, 2026. Its required main path, all three starting-country access routes and optional expansions are drawn from the repository walkthrough, game scripts and release evidence. 252 release checks and the copied Austin Save/Continue check passed. Full fresh main-route playthroughs cover Bulbasaur, Chikorita and Mudkip; the other six starters do not have full-route evidence.

All walkthrough screenshots show the actual game. New location screenshots were captured with the v3.3 ROM from earned native battery saves; battle and ending frames are retained from v3.3 verification. Screenshots illustrate locations or moments and do not imply a new fresh playthrough for every illustration. Reader checklists are stored in this browser only and do not edit the game save.

The local expansion checklist is complete. USA transfer is deferred because no companion project exists yet. Additional hair geometry, mount species and countries are future scope.

This is a fan-made guide for the European Tour project, not an official Nintendo or Pokémon publication. Use normal in-game Save/Continue and keep your own save backup before changing ROM versions.
""")]
for title,group,body in extra:
 chapters.append({'title':title,'group':group,'id':re.sub(r'[^a-z0-9]+','-',title.lower()).strip('-'),'number':len(chapters)+1,'html':md(body.replace('## ','### ')),'images':[],'search':body})
(D/'guide-data.js').write_text('window.GUIDE='+json.dumps(chapters,ensure_ascii=False)+';\n',encoding='utf-8')
(D/'downloads').mkdir(exist_ok=True)
for name in ['WALKTHROUGH.md','EUROPEAN-COUNCIL.md','EXPANSION-WALKTHROUGH.md','EXPANSION-CHECKLIST.md']:shutil.copy2(R/name,D/'downloads'/name)
(D/'guide-manifest.json').write_text(json.dumps({'edition':'v3.3','rom_sha256':hashlib.sha256((R/'artifacts/Pokemon-European-Tour-Prototype.gba').read_bytes()).hexdigest(),'chapters':len(chapters),'source_documents':['WALKTHROUGH.md','EUROPEAN-COUNCIL.md','EXPANSION-WALKTHROUGH.md'],'screenshots_are_game_captures':True},indent=2))
p=R/'strategy-guide/.openai/hosting.json';j=json.loads(p.read_text());j['static']={'directory':'dist'};p.write_text(json.dumps(j,indent=2)+'\n')
print('Built',len(chapters),'complete chapters')
