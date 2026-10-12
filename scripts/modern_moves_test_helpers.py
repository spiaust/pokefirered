"""Native battle input with explicit move/stat/HP/RNG fixtures, never player saves."""
from emulator import ROOT
from test_celebi import load_checkpoint
from test_continent_runtime import world,var,battle_start
from test_shadow_runtime import go,ensure_visible
from test_eclipse_natural import first_symbol
from test_eclipse_move_evolution import moves,ids

def single(e):
    load_checkpoint(e,'natural-league-20-complete',True);world(e,0);ensure_visible(e);go(e,(40,25))
    var(e,0x40a0,ids['SPECIES_PIKACHU']);battle_start(e,(40,25))
    action=first_symbol('HandleInputChooseAction')
    for _ in range(100):
        if e.read('gBattlerControllerFuncs')&~1==action:break
        e.press('A',30)
    assert e.read('gBattlerControllerFuncs')&~1==action
    return e.symbols['gBattleMons']

def attack(e,move,seed=1,ownhp=100,enemyhp=1000,ability=0,attacker_ability=0,expected_hits=1,enemy_species=None,confused=False,enemy_type=0,attacker_types=(0,0),attacker_accuracy=6,enemy_evasion=6,attacker_item=None,focus_energy=False,crit_seed=None,enemy_types=None,attacker_attack_stage=6,enemy_defense_stage=6,maxhp=1000):
    b=e.symbols['gBattleMons'];enemy=b+88
    e.write('gRngValue',seed)
    target_types=enemy_types or (enemy_type,enemy_type)
    for q,hp in [(b,ownhp),(enemy,enemyhp)]:
        e.write(q+40,hp,2);e.write(q+44,maxhp,2);e.write(q+76,0);e.write(q+80,0)
        e.write(q+2,100,2);e.write(q+4,100,2)
        e.write(q+8,100,2);e.write(q+10,100,2)
        e.write(q+6,100 if q==b else 40,2)
        e.write(q+32,ability if q==enemy else attacker_ability,1)
        e.write(q+33,target_types[0] if q==enemy else attacker_types[0],1);e.write(q+34,target_types[1] if q==enemy else attacker_types[1],1)
        for j in range(8):e.write(q+24+j,6,1)
    e.write(b+25,attacker_attack_stage,1);e.write(enemy+26,enemy_defense_stage,1)
    e.write(b+30,attacker_accuracy,1);e.write(enemy+31,enemy_evasion,1)
    if attacker_item is not None:e.write(b+46,attacker_item,2)
    if focus_energy:e.write(b+80,1<<20)
    if confused:e.write(b+80,3)
    if enemy_species is not None:e.write(enemy,enemy_species,2)
    for slot in range(4):e.write(enemy+12+slot*2,moves['MOVE_SPLASH'],2);e.write(enemy+36+slot,40,1)
    pp=e.read(e.symbols['gBattleMoves']+12*moves[move]+4,1)
    e.write(b+12,moves[move],2);e.write(b+36,pp,1)
    if move=='MOVE_STRUGGLE':
        # Force the real out-of-PP path, rather than selecting Struggle as a learned move.
        for slot in range(4):e.write(b+12+2*slot,moves['MOVE_TACKLE'],2);e.write(b+36+slot,0,1)
        pp=0
    expected_pp=pp if move=='MOVE_STRUGGLE' else pp-1
    action=first_symbol('HandleInputChooseAction')
    e.press('UP',2);e.press('LEFT',2);e.press('A',90);e.press('UP',2);e.press('LEFT',2);e.frames(2,'A')
    hp=enemyhp;hits=[];started=False;flinched=False;crits=[];crit_rolls=[]
    flinch=e.symbols['BattleScript_MoveUsedFlinched']
    for n in range(9000):
        current=e.read(enemy+40,2)
        if current<hp:hits.append(hp-current)
        hp=current
        script=e.read('gBattlescriptCurrInstr')
        flinched |= bool(e.read(enemy+80)&8) or flinch<=script<flinch+11
        started |= (move!='MOVE_STRUGGLE' and e.read(b+36,1)==expected_pp) or (move=='MOVE_STRUGGLE' and bool(hits)) or (confused and e.read(b+40,2)<ownhp)
        if started and ((enemyhp==1 and (e.read(b+40,2)!=ownhp or (hp==0 and move not in ('MOVE_ABSORB','MOVE_MEGA_DRAIN','MOVE_GIGA_DRAIN','MOVE_DRAINING_KISS','MOVE_DRAIN_PUNCH','MOVE_TAKE_DOWN','MOVE_DOUBLE_EDGE','MOVE_SUBMISSION','MOVE_HEAD_CHARGE','MOVE_STRUGGLE')))) or e.read('gBattlerControllerFuncs')&~1==action):break
        crit_step=e.read('gBattlerAttacker',1)==0 and e.read(script,1)==4 and e.read('gBattleControllerExecFlags')==0
        if crit_step and crit_seed is not None:e.write('gRngValue',crit_seed)
        e.frames(1,'A' if n%60==0 else 0)
        if crit_step and e.read('gBattlescriptCurrInstr')==script+1:
            crits.append(e.read('gCritMultiplier',1));crit_rolls.append(e.read('gRngValue')>>16)
    else:raise AssertionError(('Native move did not finish',move))
    self_hit=confused and not hits and e.read(b+40,2)<ownhp and e.read(b+36,1)==pp
    assert started and (self_hit or ((expected_hits is None or len(hits)==expected_hits) and e.read(b+36,1)==expected_pp)),(move,hits)
    return dict(crits=crits,crit_rolls=crit_rolls,hits=len(hits),damage=sum(hits),ownhp=e.read(b+40,2),spdef=e.read(enemy+29,1),flinched=flinched,power=e.read('gBattleMovePower',2))
