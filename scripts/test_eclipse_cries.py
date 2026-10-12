"""Check all compiled cry assets and native normal/reverse playback.
Only disposable emulator checkpoints and an explicit field-script fixture are used.
"""
import hashlib, json, struct, wave
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
ROWS = json.loads((ROOT/'data/eclipse-cries.json').read_text())['species']

def compiled(e):
    rom = (ROOT/'pokefirered.gba').read_bytes()
    assert len(ROWS) == 639
    end = 0x08000000 + len(rom)
    for i, row in enumerate(ROWS):
        path = ROOT / row['source_path']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256']
        with wave.open(str(path), 'rb') as wav:
            assert wav.getnframes() == row['frames'] and wav.getframerate() == row['rate']
        sample = e.symbols[f'Cry_Eclipse_{row["national"]}']
        assert e.symbols['gEclipseCryTable'] < sample < end
        for table, kind in [('gEclipseCryTable', 0x20), ('gEclipseCryTable_Reverse', 0x30)]:
            address = e.symbols[table] + 12*i
            assert e.read(address,1) == kind and e.read(address+4) == sample
            assert e.read(address+8) == 0x00ff00ff
        offset = sample - 0x08000000
        sample_type, flags, frequency, loop, size = struct.unpack_from('<HHIII', rom, offset)
        assert sample_type == 1 and flags == 0
        assert size == row['frames'], (row['token'], size, row['frames'])
        assert frequency == row['rate']*1024 and loop == 0, (row['token'], frequency, row['rate'], loop)
        assert sample + 16 + (size+1)//2 <= end
    print('PASS: all 639 pinned WAV hashes, compiled normal/reverse tones and PCM lengths/rates',flush=True)

def script_cry(e, species, mode, expected):
    # Invoke actual playmoncry/waitmoncry bytecode through the normal field interpreter.
    # gStringVar4 is unused by these commands and is restored when the fixture ends.
    scratch = e.symbols['gStringVar4']
    saved = [e.read(scratch+i,1) for i in range(7)]
    code = bytes([0xa1]) + struct.pack('<HH', species, mode) + bytes([0xc5, 0x02])
    for i, byte in enumerate(code): e.write(scratch+i,byte,1)
    ctx = e.symbols['sGlobalScriptContext']
    assert not e.read('sLockFieldControls',1)
    e.write(ctx,0,1);e.write(ctx+1,1,1);e.write(ctx+4,0)
    e.write(ctx+8,scratch);e.write('sGlobalScriptContextStatus',0,1)
    e.frames(1)
    elapsed = 1
    player = e.read('gMPlay_PokemonCry')
    assert player and e.read(player+48) == expected, (species,mode,hex(e.read(player+48)),hex(expected))
    # Observe the actual mixer channel referencing and traversing this ROM wave.
    sample = e.read(expected+4)
    channel = None
    for _ in range(12):
        e.frames(1)
        elapsed += 1
        for i in range(12):
            p = e.symbols['gSoundInfo'] + 80 + 64*i
            if e.read(p+36) == sample and e.read(p,1): channel = p
        if channel is not None: break
    assert channel is not None, ('no active PCM channel',species,mode)
    pointer = e.read(channel+40)
    e.frames(3)
    elapsed += 3
    assert e.read(channel+40) != pointer, ('sample not progressing',species,mode)
    for _ in range(360):
        if not e.read('sLockFieldControls',1): break
        e.frames(1)
        elapsed += 1
    if mode == 0:
        minimum = e.read(sample+12)*60 // (e.read(sample+4) >> 10)
        assert elapsed >= minimum-8, ("normal cry truncated",species,elapsed,minimum)
    assert not e.read('sLockFieldControls',1), ('waitmoncry stuck',species,mode)
    for i,byte in enumerate(saved): e.write(scratch+i,byte,1)

def main():
    e = Emulator(ROOT/'pokefirered.gba')
    try:
        compiled(e)
        load_checkpoint(e,'natural-circuit-complete',True)
        # Both boundaries, each generation, multiword/form aliases and longest sample.
        selected = sorted({0,26,35,107,262,334,420,439,479,540,632,638,
                           max(range(639),key=lambda i:ROWS[i]['frames'])})
        for i in selected:
            row=ROWS[i]
            for mode,table in [(0,'gEclipseCryTable'),(9,'gEclipseCryTable_Reverse')]:
                script_cry(e,row['id'],mode,e.symbols[table]+12*i)
            print('PASS: native normal/reversed PCM playback and wait completion',row['token'],flush=True)
        # Original cry-table and alternate-Unown fallback behavior must remain intact.
        for species,index in [(1,0),(25,24),(411,387),(439,200)]:
            for mode,table in [(0,'gCryTable'),(9,'gCryTable_Reverse')]:
                script_cry(e,species,mode,e.symbols[table]+12*index)
        print('PASS: original Bulbasaur/Pikachu/Chimecho and alternate Unown legacy mappings',flush=True)
        from test_eclipse_friendship import fixture
        from test_gym_ui import start_action
        from test_navigation import wait_task
        from tm_teaching_test_helpers import field
        fixture(e,'PECHARUNT',255,0,0)
        start_action(e,1)
        wait_task(e,'Task_HandleChooseMonInput')
        e.press('A',60)
        wait_task(e,'Task_HandleSelectionMenuInput')
        e.press('A',240)
        assert e.read(e.read('gMPlay_PokemonCry')+48) == e.symbols['gEclipseCryTable']+638*12
        assert e.read(e.symbols['gMain']+4)&~1 == e.symbols['CB2_RunPokemonSummaryScreen']&~1
        e.screenshot(ROOT/'test-output/cry-pecharunt-summary.png')
        field(e)
        print('PASS: Gen IX cry through native party/summary UI and return to field',flush=True)

    finally:e.close()
if __name__ == '__main__': main()
