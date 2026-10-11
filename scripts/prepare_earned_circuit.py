"""Buy final-rematch supplies using the earned ten-match checkpoint.
Optional owned Ice Beam/Lucky Egg preparation uses native menus only.
Never opens personal saves or writes party stats, money, items or progress.
"""
import sys
sys.path.insert(0,'scripts')
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
import test_eclipse_natural as natural
import test_shadow_runtime,test_continent_runtime
from test_shadow_runtime import talk
from natural_supplies_test_helpers import buy
from natural_preparation_test_helpers import teach,give
from test_oxford_gym import count_pocket
from test_landmark_cases import save
test_shadow_runtime.go=natural.natural_go;test_continent_runtime.go=natural.natural_go
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'natural-circuit-10-complete',True)
 buy(e,((19,12,3000),(23,10,600)))
 if count_pocket(e,301,0x464,58):teach(e,150,301,58,0)
 if count_pocket(e,197,0x310,42):give(e,150,197)
 talk(e,(2,4));save(e,'natural-circuit-final-prepared')
 print('PASS: native purchased supplies and saved final preparation',flush=True)
finally:e.close()
