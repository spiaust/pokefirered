"""Compose original eight-bar native M4A loops; no imported melodies."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
# Scale-degree motifs, harmonies, tempo and orchestration define each place.
SCORES=[
 ('london','Thames Lanterns',108,0,[0,2,4,5,4,2,1,2],[0,5,3,4,0,3,1,4]),
 ('paris','Garden Waltz',96,2,[4,2,1,0,2,4,6,5],[0,3,4,0,5,1,4,0]),
 ('berlin','Linden Steps',120,-2,[0,0,4,2,3,2,1,4],[0,4,5,3,0,5,1,4]),
 ('oxford','Scholars by the River',88,5,[2,4,1,2,0,1,4,3],[0,5,1,4,3,0,4,0]),
 ('chantilly','Forest Porcelain',100,7,[4,6,5,2,4,3,1,0],[0,3,5,4,0,1,3,4]),
 ('oranienburg','Havel Reflections',92,-5,[0,2,5,4,2,1,3,2],[0,5,3,0,1,3,4,0]),
 ('title','Celebi Across Europe',112,0,[0,4,6,5,4,2,3,1],[0,3,5,4,0,1,4,0]),
]
NAMES=['Cn','Cs','Dn','Ds','En','Fn','Fs','Gn','Gs','An','As','Bn']
SCALE=[0,2,4,5,7,9,11]
def note(degree,octave,transpose):
 n=12*(octave+1)+SCALE[degree%7]+12*(degree//7)+transpose
 return NAMES[n%12]+str(n//12-1)
manifest=[]
for index,(tag,title,tempo,key,motif,chords) in enumerate(SCORES):
 symbol='mus_europe_'+tag
 lines=['\t.include "MPlayDef.s"','\t.section .rodata','\t.align 2','\t.global '+symbol]
 for track in range(4):
  label=f'{symbol}_{track+1}'
  voice=[5,4,5,4][track]
  lines += [label+':',f'\t.byte KEYSH, 0',f'\t.byte VOICE, {voice}',f'\t.byte VOL, {[62,34,28,25][track]}',f'\t.byte PAN, {64+[-12,0,18,10][track]}']
  if track==0:lines += [f'\t.byte TEMPO, {tempo//2}']
  lines += [label+'_loop:']
  for bar,root in enumerate(chords):
   if track==0:
    # Four beats per bar; Paris uses a lilting dotted figure.
    degrees=[motif[bar],motif[(bar+1)%8],motif[(bar+3)%8],motif[(bar+2)%8]]
    durations=[36,12,24,24] if tag=='paris' else [24,24,24,24]
    for degree,duration in zip(degrees,durations):
     lines += [f'\t.byte N{32 if duration==36 else duration-2:02}, {note(degree,4,key)}, v088',f'\t.byte W{duration:02}']
   elif track==1:
    for degree in [root,root+4]:
     lines += [f'\t.byte N44, {note(degree,2,key)}, v072','\t.byte W48']
   elif track==2:
    for degree in [root,root+2,root+4]:lines += [f'\t.byte N90, {note(degree,3,key)}, v056']
    lines += ['\t.byte W96']
   else:
    for degree in [root,root+2,root+4,root+2,root+7,root+4,root+2,root+4]:
     lines += [f'\t.byte N10, {note(degree,4,key)}, v048','\t.byte W12']
  lines += ['\t.byte GOTO','\t.word '+label+'_loop','\t.byte FINE']
 lines += ['\t.align 2',symbol+':','\t.byte 4, 0, 0, 50','\t.word voicegroup159']
 lines += ['\t.word '+symbol+'_'+str(i) for i in range(1,5)]
 lines += ['\t.end','']
 (R/f'sound/songs/{symbol}.s').write_text('\n'.join(lines))
 manifest.append({'id':347+index,'symbol':symbol,'title':title,'tempo':tempo,'bars':8,'ticks':768,'tracks':4,'map':'Europe'+tag.title() if tag!='title' else None})
(R/'data/geography/europe-music.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Composed seven original eight-bar, four-track looping scores')
