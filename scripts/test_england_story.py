"""Play England's field study, Oxford rival, reward recovery and repeat talks."""
from emulator import Emulator, ROOT
from test_country import wait_menu, party_species
from test_tour import travel, item_count
from test_challenge_rewards import reach_guide, set_win
from test_challenges import fight_with_supplies
from test_trainers import money, defeated, fight

STORY = 0x40FB
BELL = 184

def speak(emu):
    assert emu.location()[2:] == (10, 14), emu.location()
    emu.press('DOWN')
    emu.press('A', 180)

def finished_talk(emu):
    speak(emu)
    emu.finish_dialogue()
    assert not emu.in_battle()
    assert not emu.task_active('Task_YesNoMenu_HandleInput')

def heal_oxford(emu):
    # From the guide approach to the clinic, then to the rival.
    emu.walk('LEFT', 10)
    emu.walk('UP', 5)
    emu.frames(180)
    emu.walk('UP', 4)
    emu.walk('RIGHT', 1)
    emu.press('UP')
    emu.press('A', 180)
    emu.finish_dialogue()
    emu.walk('DOWN', 5)
    emu.frames(180)
    emu.walk('RIGHT', 4)
    emu.walk('DOWN', 4)
    assert emu.location() == (43, 12, 10, 14), emu.location()

if __name__ == '__main__':
    emu = Emulator(ROOT / 'pokefirered.gba')
    try:
        for home, country in enumerate(('england', 'france', 'germany'), 1):
            emu.state(ROOT / f'test-output/start-{country}.state', True)
            emu.walk('RIGHT', 1)
            if home != 1:
                travel(emu, 0)
            emu.walk('LEFT', 6)
            speak(emu)
            wait_menu(emu, 'Task_YesNoMenu_HandleInput')
            prompt = ROOT / f'test-output/story-{country}-offer.state'
            emu.state(prompt)
            for decline in ('B', 'NO'):
                emu.state(prompt, True)
                if decline == 'NO':
                    emu.press('DOWN')
                    emu.press('A', 180)
                else:
                    emu.press('B', 180)
                emu.finish_dialogue()
                assert emu.var(STORY) == 0
            emu.state(prompt, True)
            emu.press('A', 180)
            emu.finish_dialogue()
            assert emu.var(STORY) == 1 and emu.var(0x40F0) == home
            finished_talk(emu)
            assert emu.var(STORY) == 1 and item_count(emu, BELL) == 0
            if home == 1:
                emu.state(ROOT / 'test-output/story-active.state')
            print(f'PASS: {country} home: mission No/B, acceptance, repeated directions; home retained', flush=True)

        emu.state(ROOT / 'test-output/story-active.state', True)
        emu.walk('RIGHT', 6)
        travel(emu, 3)
        emu.walk('LEFT', 6)
        finished_talk(emu)
        assert not defeated(emu, 6)
        # Isolate prerequisite branches without fabricating the winning playthrough.
        set_win(emu, 743, True)
        finished_talk(emu)
        assert not defeated(emu, 6)
        assert emu.var(STORY) == 1
        print('PASS: rival requires both Oliver and Alice; neither missing match starts battle', flush=True)

        # Begin with two real trail victories; earlier wins must count.
        emu.state(ROOT / 'test-output/challenge-england-won.state', True)
        reach_guide(emu)
        emu.walk('LEFT', 6)
        finished_talk(emu)
        assert emu.var(STORY) == 0 and not defeated(emu, 6)
        emu.walk('RIGHT', 6)
        travel(emu, 0)
        emu.walk('LEFT', 6)
        speak(emu)
        wait_menu(emu, 'Task_YesNoMenu_HandleInput')
        emu.press('A', 180)
        emu.finish_dialogue()
        emu.walk('RIGHT', 6)
        travel(emu, 3)
        heal_oxford(emu)
        speak(emu)
        wait_menu(emu, 'Task_YesNoMenu_HandleInput')
        prompt = ROOT / 'test-output/story-rival-prompt.state'
        emu.state(prompt)
        prize_before = money(emu)
        for decline in ('B', 'NO'):
            emu.state(prompt, True)
            if decline == 'NO':
                emu.press('DOWN')
                emu.press('A', 180)
            else:
                emu.press('B', 180)
            emu.finish_dialogue()
            assert not defeated(emu, 6) and not emu.in_battle()
            assert money(emu) == prize_before and emu.var(STORY) == 1
        emu.state(prompt, True)
        emu.press('A', 180)
        for _ in range(30):
            if emu.in_battle(): break
            emu.press('A', 90)
        assert emu.in_battle()
        emu.frames(300)
        assert emu.read('gTrainerBattleOpponent_A', 2) == 749
        assert tuple(party_species(emu, 'gEnemyParty', i) for i in range(2)) == (16, 133)
        battle = ROOT / 'test-output/story-rival-battle.state'
        emu.state(battle)
        emu.screenshot(ROOT / 'test-output/story-rival-battle.png')
        fight_with_supplies(emu)
        assert defeated(emu, 6) and money(emu) > prize_before
        prize_after = money(emu)
        finished_talk(emu)
        assert money(emu) == prize_after and emu.var(STORY) == 1
        emu.state(ROOT / 'test-output/story-rival-won.state')
        print('PASS: previous trail wins unlock rival; No/B, real victory, prize and no repeat payout', flush=True)

        emu.walk('RIGHT', 6)
        travel(emu, 0)
        emu.walk('LEFT', 6)
        ready = ROOT / 'test-output/story-report-ready.state'
        emu.state(ready)
        finished_talk(emu)
        assert emu.var(STORY) == 2 and item_count(emu, BELL) == 1
        finished_talk(emu)
        assert emu.var(STORY) == 2 and item_count(emu, BELL) == 1
        emu.state(ROOT / 'test-output/story-complete.state')
        emu.walk('RIGHT', 6)
        travel(emu, 3)
        emu.walk('LEFT', 6)
        finished_talk(emu)
        assert emu.var(STORY) == 2 and money(emu) == prize_after
        print('PASS: return report grants one Soothe Bell; aide and rival repeats preserve completion', flush=True)

        emu.state(ready, True)
        bag = emu.read('gSaveBlock1Ptr') + 0x310
        key = emu.read(emu.read('gSaveBlock2Ptr') + 0xF20, 2)
        for i in range(42):
            emu.write(bag + i * 4, 13, 2)
            emu.write(bag + i * 4 + 2, 99 ^ key, 2)
        finished_talk(emu)
        assert emu.var(STORY) == 1 and item_count(emu, BELL) == 0
        emu.state(ROOT / 'test-output/story-pending.state')
        emu.write(bag, 0, 2)
        emu.write(bag + 2, key, 2)
        finished_talk(emu)
        assert emu.var(STORY) == 2 and item_count(emu, BELL) == 1
        finished_talk(emu)
        assert item_count(emu, BELL) == 1
        print('PASS: full Bag preserves report and pending Soothe Bell; retry grants it once', flush=True)

        emu.state(battle, True)
        party = emu.symbols['gPlayerParty']
        mon = emu.symbols['gBattleMons']
        emu.write(party + 0x56, 1, 2)
        emu.write(mon + 0x28, 1, 2)
        emu.write(mon + 0x06, 1, 2)
        emu.write(mon + 0x02, 1, 2)
        fight(emu)
        assert emu.location()[:2] == (43, 15), emu.location()
        assert not defeated(emu, 6) and emu.var(STORY) == 1
        assert emu.read(party + 0x56, 2) > 1
        emu.walk('DOWN', 5)
        emu.frames(180)
        emu.walk('RIGHT', 4)
        emu.walk('DOWN', 4)
        speak(emu)
        wait_menu(emu, 'Task_YesNoMenu_HandleInput')
        emu.press('B', 180)
        emu.finish_dialogue()
        assert not defeated(emu, 6) and emu.var(STORY) == 1
        print('PASS: rival loss heals in Oxford without victory or story completion; retry remains available', flush=True)
    finally:
        emu.close()
