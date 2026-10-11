"""Read emulator RTC through cartridge GPIO in America/Chicago."""
from datetime import datetime,timezone
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint

e=Emulator(ROOT/'pokefirered.gba')
try:
    load_checkpoint(e,'natural-league-20-complete',True)
    for hour,minute,expected in [(13,0,480),(4,0,1380),(23,30,1110)]:
        e.rtc(int(datetime(2026,10,11,hour,minute,tzinfo=timezone.utc).timestamp()))
        e.frames(120)
        assert e.read('sEclipseLocalMinute',2)==expected,(hour,minute,e.read('sEclipseLocalMinute',2))
    print('PASS: Chicago local RTC reads morning, previous-day night and dusk through native cartridge GPIO')
finally:e.close()
