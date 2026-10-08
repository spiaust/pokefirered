"""Exercise animated title, record native soundtrack, and visit every town."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_tour import travel
from test_time import preserved
from key_item_test_helpers import reload
import ctypes,json,wave,array,math

bridge=ROOT/'.local-tools/emulator_audio_bridge.so'
e=Emulator(ROOT/'pokefirered.gba',bridge=bridge)
scores=json.loads((ROOT/'data/geography/europe-music.json').read_text())
def music(score):
 assert e.read('gMPlayInfo_BGM')==e.symbols[score['symbol']],(score,e.read('gMPlayInfo_BGM'))
 assert e.read(e.symbols[score['symbol']],1)==4
 assert e.read(e.symbols['gMPlayInfo_BGM']+4)&15==15
def record(score):
 music(score);clock=e.read(e.symbols['gMPlayInfo_BGM']+12)
 pcm=ROOT/f'test-output/{score["symbol"]}.pcm'
 samples=e.lib.emulator_record_pcm(str(pcm).encode(),3000);assert samples>1500000
 music(score);assert e.read(e.symbols['gMPlayInfo_BGM']+12)>clock+1536
 data=pcm.read_bytes();values=array.array('h',data)
 rms=math.sqrt(sum(v*v for v in values)/len(values));peak=max(abs(v) for v in values)
 assert rms>30 and peak<32767,(score['symbol'],rms,peak)
 with wave.open(str(pcm.with_suffix('.wav')),'wb') as w:
  w.setnchannels(2);w.setsampwidth(2);w.setframerate(32768);w.writeframes(data)
 pcm.unlink()
 print('PASS: '+score['title']+' native stereo audio is non-silent, unclipped and plays past two loop boundaries',flush=True)

try:
 e.frames(600)
 for _ in range(20):
  if e.read(e.symbols['gMain']+4)&~1==e.symbols['CB2_EuropeTitleRun']&~1:break
  e.press('START',60)
 assert e.read(e.symbols['gMain']+4)&~1==e.symbols['CB2_EuropeTitleRun']&~1
 e.frames(60);music(scores[-1]);mon=e.read('sEuropeTitleMon',1);assert mon<64
 frames=[];towns=set();positions=set()
 for i in range(90):
  frame=e.read('sEuropeTitleFrame',2);towns.add((frame//240)%6)
  positions.add((e.read(e.symbols['gSprites']+68*mon+36,2),e.read(e.symbols['gSprites']+68*mon+38,2)))
  p=ROOT/f'test-output/europe-title-frame-{i:03}.png';e.screenshot(p);frames.append(p)
  e.frames(16)
 assert towns==set(range(6)) and len(positions)>8,(towns,len(positions))
 (ROOT/'test-output/europe-title-frames.json').write_text(json.dumps([p.name for p in frames]))
 print('PASS: native title animates Celebi, lights and all six town scenes through a full 24-second cycle',flush=True)
 record(scores[-1]);e.press('START',180)
 e.screenshot(ROOT/'test-output/europe-title-new-game.png')
 assert e.read(e.symbols['gMain']+4)&~1!=e.symbols['CB2_EuropeTitleRun']&~1
 assert e.read(e.symbols['gMain']+4)&~1==e.symbols['CB2_NewGameScene']&~1
 print('PASS: START from a fresh battery enters the normal New Game controls introduction',flush=True)
 e.battery(ROOT/'test-output/map-select-complete.sav',True);e.frames(600)
 for _ in range(20):
  if e.read(e.symbols['gMain']+4)&~1==e.symbols['CB2_EuropeTitleRun']&~1:break
  e.press('START',60)
 assert e.read(e.symbols['gMain']+4)&~1==e.symbols['CB2_EuropeTitleRun']&~1
 e.frames(60);e.press('START',180)
 assert e.read(e.symbols['gMain']+4)&~1==e.symbols['CB2_MainMenu']&~1
 e.screenshot(ROOT/'test-output/europe-title-main-menu.png')
 for _ in range(3):
  e.press('B',180)
  assert e.read(e.symbols['gMain']+4)&~1==e.symbols['CB2_EuropeTitleRun']&~1
  music(scores[-1]);e.press('A',180)
  assert e.read(e.symbols['gMain']+4)&~1==e.symbols['CB2_MainMenu']&~1
 print('PASS: main-menu B returns to the animated splash and A reopens the menu through three cycles',flush=True)
 load_checkpoint(e,'map-select-complete',True)
 history=tuple(e.var(v) for v in range(0x40C0,0x4100));original=preserved(e)[1:]
 for dest,score in enumerate(scores[:6]):
  if e.location()[1]!=dest*4:go(e,(16,14));travel(e,dest)
  e.frames(300);assert e.location()[:2]==(43,dest*4)
  record(score)
  assert preserved(e)[1:]==original and tuple(e.var(v) for v in range(0x40C0,0x4100))==history
  e.screenshot(ROOT/f'test-output/europe-music-{score["symbol"][11:]}.png')
 print('PASS: normal trains reach all six custom town themes while completed story/items/money/badges remain exact',flush=True)
 # Keep the audio-enabled bridge for a cold reload, using normal Save/Continue.
 from test_landmark_cases import save
 save(e,'europe-presentation-v125');before=preserved(e);location=e.location();e.close()
 e=Emulator(ROOT/'pokefirered.gba',bridge=bridge);load_checkpoint(e,'europe-presentation-v125',True);e.frames(300)
 assert e.location()==location and preserved(e)==before;music(scores[5])
 print('PASS: new cold Continue restores exact saved state and the correct Oranienburg custom theme',flush=True)
finally:e.close()
