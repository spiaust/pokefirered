"""Historical records paging, newer milestones, topics and read-only state."""
import argparse
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import open_key_item
from test_navigation import wait_task
from test_journal import journal_task,snapshot,milestone_mask

def inspect_pages(emu,mask,label=None):
    before=snapshot(emu)
    open_key_item(emu,361);wait_task(emu,'Task_EuropeMap')
    task=journal_task(emu)
    emu.press('SELECT',60);emu.press('A',60)
    assert emu.read(task+10,2)==2 and milestone_mask(emu,task)==mask
    assert emu.read(task+18,2)==0
    if label:emu.screenshot(ROOT/f'test-output/records-{label}-page1.png')
    for key in ('LEFT','RIGHT','RIGHT'):
        previous=emu.read(task+18,2);emu.press(key,60)
        assert emu.read(task+18,2)==1-previous
        assert milestone_mask(emu,task)==mask
    assert emu.read(task+18,2)==1
    if label:emu.screenshot(ROOT/f'test-output/records-{label}-page2.png')
    emu.press('A',60);assert emu.read(task+10,2)==1
    emu.press('RIGHT',60);assert emu.read(task+18,2)==1
    emu.press('A',60);assert emu.read(task+10,2)==2 and emu.read(task+18,2)==1
    emu.press('UP',60);assert emu.read(task+16,2)==1 and emu.read(task+18,2)==0
    assert emu.read(task+20,2)==0  # Historical high bits must not leak into the regional topic.
    for key in ('LEFT','RIGHT'):emu.press(key,60);assert emu.read(task+18,2)==0
    if label:emu.screenshot(ROOT/f'test-output/records-{label}-tour.png')
    emu.press('DOWN',60);assert emu.read(task+16,2)==0 and emu.read(task+18,2)==0
    assert milestone_mask(emu,task)==mask
    emu.press('RIGHT',60);emu.press('SELECT',60)
    assert emu.read(task+10,2)==0
    emu.press('SELECT',60);assert emu.read(task+18,2)==0
    emu.press('B',180);emu.press('B',180);emu.press('B',90)
    assert not emu.read('sLockFieldControls',1)
    assert snapshot(emu)==before

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--legacy',action='store_true');args=parser.parse_args()
    for case,mask in (('start-england',0),('amiens-account-complete',1023),('rouen-arrival',2047),('rouen-complete',4095),('route-book-complete',8191),('le-havre-complete',16383),('dock-check-complete',32767),('port-account-complete',65535),('southampton-complete',131071),('luggage-complete',262143),('south-account-complete',524287),('london-past-complete',1048575)):
        emu=Emulator(ROOT/'pokefirered.gba')
        try:
            load_checkpoint(emu,case,args.legacy)
            inspect_pages(emu,mask,case)
            if mask in (0,8191):emu.state(ROOT/('test-output/journal-pages-'+('empty' if mask==0 else 'complete')+'.state'))
            print(f'PASS: {case}: mask {mask}, page wrapping, lead toggle, topic reset and read-only exit',flush=True)
        finally:emu.close()
