"""Author landmark case scripts and readable, persistent field notes."""
from pathlib import Path
import textwrap
R=Path(__file__).resolve().parents[1]
CASES=[
 ('NotreDame','PARIS','Paris',28,35,'0x40C0','ITEM_SPELL_TAG',1,
  'The Quiet Bells',
  'GASTLY have gathered in the undercroft. Visitors think they are angry. Help me learn what is frightening them. Will you investigate?',
  'The caretaker notes that the GASTLY appeared after a noisy repair began. They hide when the tools start.',
  'An old route ledger describes quiet shelters for traveling people and POKEMON. A green visitor appears in its margins.',
  'The GASTLY need shelter, not chasing. Ask the caretaker to pause the noisy work?',
  'The tools fall silent. GASTLY drift into the quiet side aisle. Their restless calls become a gentle murmur.',
  'You listened before acting. Keep this SPELL TAG. The old ledger mentions CHANTILLY; ADA in OXFORD studies such routes.'),
 ('Westminster','LONDON','London',14,35,'0x40C1','ITEM_RARE_CANDY',1,
  'A Place to Rest',
  'A flock of HOOTHOOT is circling the river instead of resting. This visitor room holds old route records. Will you find out what they need?',
  'The riverside keeper reports that repairs closed a sheltered passage. The flock returns there every evening.',
  'A reception ledger records travelers arriving from SOUTHAMPTON with their POKEMON. Keeping companions together helped them settle.',
  'Ask the keeper to reopen the safe shelter route before evening?',
  'The keeper opens the sheltered passage. The flock settles beneath the eaves. A familiar route feels safe again.',
  'Thank you. Take a RARE CANDY for your team. The ledger links this place with SOUTHAMPTON and France. Share that clue with ADA.'),
 ('Reichstag','BERLIN','Berlin',21,33,'0x40C2','ITEM_GREAT_BALL',3,
  'The Broken Signal',
  'A temporary relay is drawing MAGNEMITE away from their usual route. Our visitor archive may help. Will you investigate?',
  'The technician recorded a repeating pulse from the temporary relay. Nearby MAGNEMITE turn toward it whenever it sounds.',
  'The archive describes how routes change when stations close. Safe paths depend on reliable signals and people sharing accurate news.',
  'Ask the technician to disconnect the faulty relay and restore the proper signal?',
  'The false pulse stops. MAGNEMITE return to the riverside route. The technician marks the safe path for future visitors.',
  'These GREAT BALLS are for your travels. LENA and KARL maintain trail beacons too. ADA is comparing changes along old routes.')]
out=['@ Independent cases: 0 unstarted, 1 accepted, 2/3 one clue, 4 both, 5 resolved, 6 rewarded.']
def text(label,message):
 lines=textwrap.wrap(message,34,break_long_words=False);out.append(label+'::')
 for i,line in enumerate(lines):out.append('\t.string "'+line+('$' if i==len(lines)-1 else '\\p' if i%2 else '\\n')+'"')
for tag,region,city,x,y,var,reward,count,title,offer,a,b,resolve,result,thanks in CASES:
 p='EuropeCase_'+tag
 out.append(f'''{p}_Enter::
 lockall
 msgbox {p}_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeCase_End
 closemessage
 warp MAP_EUROPE_{tag.upper()}, 10, 15
 waitstate
 releaseall
 end
{p}_Exit::
 lockall
 warp MAP_EUROPE_{region}, {x}, {y}
 waitstate
 releaseall
 end
{p}_Curator::
 lock
 faceplayer
 goto_if_eq {var}, 6, {p}_Complete
 goto_if_eq {var}, 5, {p}_Reward
 goto_if_ne {var}, 0, {p}_Progress
 msgbox {p}_OfferText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeCase_End
 setvar {var}, 1
{p}_Progress::
 msgbox {p}_ProgressText
 goto EuropeCase_End
{p}_Reward::
 checkitemspace {reward}, {count}
 goto_if_eq VAR_RESULT, FALSE, EuropeCase_Full
 msgbox {p}_ThanksText
 giveitem {reward}, {count}
 setvar {var}, 6
{p}_Complete::
 msgbox {p}_CompleteText
 call EuropeCase_Synthesis
 goto EuropeCase_End
{p}_Resolve::
 lockall
 goto_if_ge {var}, 5, {p}_After
 goto_if_ne {var}, 4, {p}_NeedClues
 msgbox {p}_ResolveText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeCase_End
 setvar {var}, 5
 msgbox {p}_ResultText
 goto EuropeCase_End
{p}_NeedClues::
 msgbox EuropeCase_NeedCluesText
 goto EuropeCase_End
{p}_After::''')
 if tag=='NotreDame':out.append(''' msgbox EuropeCase_GastlyText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeCase_End
 setwildbattle SPECIES_GASTLY, 12
 dowildbattle
 releaseall
 end''')
 else:out.append(f' msgbox {p}_ResultText\n goto EuropeCase_End')
 for clue,other,state,msg in [('A',3,2,a),('B',2,3,b)]:
  out.append(f'''{p}_Clue{clue}::
 lockall
 goto_if_eq {var}, 0, {p}_NeedClues
 msgbox {p}_Clue{clue}Text
 goto_if_ge {var}, 4, EuropeCase_End
 goto_if_eq {var}, {other}, {p}_Both
 setvar {var}, {state}
 goto EuropeCase_End''')
  text(p+'_Clue'+clue+'Text',msg)
 out.append(f'{p}_Both::\n setvar {var}, 4\n msgbox EuropeCase_BothText\n goto EuropeCase_End')
 for suffix,msg in [('EntryText',f'{title}. Enter the landmark visitor area?'),('OfferText',offer),('ProgressText','Read the two records in the side aisles. Then speak to the attendant at the north end. Return here when the case is resolved.'),('ResolveText',resolve),('ResultText',result),('ThanksText',thanks),('CompleteText',title+' is resolved. Your field notes are safe. You can still explore this area and read its records.')]:text(p+'_'+suffix,msg)
out.append('''EuropeCase_Full::
 msgbox EuropeCase_FullText
EuropeCase_End::
 releaseall
 end
EuropeCase_Synthesis::
 compare 0x40C0, 6
 goto_if_ne EuropeCase_Return
 compare 0x40C1, 6
 goto_if_ne EuropeCase_Return
 compare 0x40C2, 6
 goto_if_ne EuropeCase_Return
 msgbox EuropeCase_SynthesisText
EuropeCase_Return::
 return
EuropeCase_Ledger::
 lockall
 msgbox EuropeCase_LedgerText''')
for tag,region,city,x,y,var,*_ in CASES:
 out.append(f' compare {var}, 6\n call_if_eq EuropeCase_{tag}_Recorded\n compare {var}, 6\n call_if_ne EuropeCase_{tag}_Open')
out.append(' call EuropeCase_Synthesis\n goto EuropeCase_End')
for tag,region,*_ in CASES:
 for suffix,msg in [('Recorded',region+': case resolved and reward collected.'),('Open',region+': this case is still open. Speak to the landmark curator for directions.')]:
  out.append(f'EuropeCase_{tag}_{suffix}::\n msgbox EuropeCase_{tag}_{suffix}Text\n return');text(f'EuropeCase_{tag}_{suffix}Text',msg)
for label,msg in [('Full','Your case is resolved. Make room in the BAG for your reward, then speak to me again.'),('NeedClues','Speak to the curator near the entrance, then read both records before deciding what to do.'),('Both','Both clues are recorded. Speak to the attendant at the north end.'),('Gastly','A GASTLY approaches calmly. Meet it in an optional wild battle? You may catch it or leave.'),('Synthesis','All three cases point to the same lesson: disturbed routes separate POKEMON from safe places. The old ledger names CHANTILLY and SOUTHAMPTON. Bring this pattern to ADA in OXFORD after earning the three regional badges.'),('Ledger','LANDMARK FIELD NOTES. These cases are optional investigations alongside your regional studies. Each curator keeps your progress.')]:text('EuropeCase_'+label+'Text',msg)
(R/'data/scripts/europe_landmarks.inc').write_text('\n'.join(out)+'\n')
