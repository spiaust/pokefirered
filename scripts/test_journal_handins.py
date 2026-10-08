"""Genuine old-ROM report-back saves and new cold Continue journal reads."""
import sys
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import save
from test_tour_journal import inspect,snapshot
CASES=[('story-rival-won',4),('france-report',12),('germany-delivered',17)]
for case,lead in CASES:
 e=Emulator(ROOT/('artifacts/releases/Pokemon-European-Tour-v1.12.gba' if '--prepare' in sys.argv else 'pokefirered.gba'))
 try:
  if '--prepare' in sys.argv:
   load_checkpoint(e,case,True);save(e,'journal-handin-'+case+'-v112')
   print('Prepared genuine v1.12 report-back battery: '+case,flush=True)
   continue
  load_checkpoint(e,'journal-handin-'+case+'-v112',True)
  inspect(e,lead,'handin-'+case);inspect(e,lead)
  save(e,'journal-handin-'+case);saved=snapshot(e)
  print('PASS: '+case+' old v1.12 battery, correct report-back lead and repeated read-only journal topics',flush=True)
 finally:e.close()
 if '--prepare' not in sys.argv:
  e=Emulator(ROOT/'pokefirered.gba')
  try:
   load_checkpoint(e,'journal-handin-'+case,True);assert snapshot(e)==saved
   inspect(e,lead,'handin-'+case+'-continued')
   print('PASS: '+case+' cold Continue retains exact state and correct report-back lead',flush=True)
  finally:e.close()
