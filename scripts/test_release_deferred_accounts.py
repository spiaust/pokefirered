"""Read the conclusion and archive deferred accounts from the fresh-route save."""
import sys
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint, researcher, report
from test_landmark_cases import save

PREFIX = 'release-'+sys.argv[sys.argv.index('--country')+1]+'-' if '--country' in sys.argv else 'walkthrough-'

e = Emulator(ROOT / 'pokefirered.gba')
try:
    load_checkpoint(e, PREFIX+'complete', True)
    assert e.var(0x40D5) == 2
    for _ in range(3):
        if e.var(0x40D9) == e.var(0x40D6) == 1: break
        researcher(e)
        for _ in range(160):
            if not e.read('sLockFieldControls',1):break
            e.press('A',90)
        assert not e.read('sLockFieldControls',1)
    assert e.var(0x40D9) == e.var(0x40D6) == 1
    researcher(e); e.frames(900)
    assert e.read('sLockFieldControls', 1)
    e.screenshot(ROOT / f'test-output/{PREFIX}ada-conclusion.png')
    for _ in range(160):
        if not e.read('sLockFieldControls',1):break
        e.press('A',90)
    assert not e.read('sLockFieldControls',1)
    save(e, PREFIX+'all-accounts')
    print('PASS: fresh-route ending files both deferred accounts and shows Ada conclusion again without resetting progress', flush=True)
finally:
    e.close()
