"""Conservative projection of pinned RHH evolution rules into FireRed methods.
Nested conditions are never silently discarded. Unsupported rules are audited.
"""
import re

# Gender forms share the roster's single base-species model.
GENDER_FORM_ALIASES = {
    "SPECIES_MEOWSTIC_F": "SPECIES_MEOWSTIC",
    "SPECIES_OINKOLOGNE_F": "SPECIES_OINKOLOGNE",
}

HELD_TRADE_ITEMS = {'ITEM_ELECTIRIZER','ITEM_MAGMARIZER','ITEM_PROTECTOR','ITEM_DUBIOUS_DISC','ITEM_REAPER_CLOTH','ITEM_SACHET','ITEM_WHIPPED_DREAM'}

def project(body, species, items, aliases=None, moves=None):
    accepted, omitted = [], []
    match = re.search(r"\.evolutions\s*=\s*EVOLUTION\(", body)
    if not match:
        return accepted, omitted
    start = match.end()
    depth = 1
    end = start
    while end < len(body) and depth:
        depth += (body[end] == '(') - (body[end] == ')')
        end += 1
    text = body[start:end-1]
    depth = 0
    for i, c in enumerate(text):
        if c == '{':
            if not depth: begin = i
            depth += 1
        elif c == '}':
            depth -= 1
            if depth: continue
            raw = text[begin:i+1]
            m = re.match(r"\{(EVO_\w+),\s*([^,}]+),\s*(SPECIES_\w+)(.*)\}", raw, re.S)
            if not m: continue
            method, param, target, tail = m.groups()
            target = (aliases or {}).get(target, target)
            param = param.strip()
            conditions = re.findall(r"\{(IF_\w+),\s*([^}]+)\}", tail)
            supported = not tail.strip()
            if method == 'EVO_LEVEL' and conditions:
                rules = dict((k, v.strip()) for k,v in conditions)
                if len(rules) != len(conditions):
                    omitted.append(raw); continue
                if len(rules) == 1 and rules.get('IF_GENDER') in ('MON_MALE', 'MON_FEMALE') and param.isdigit():
                    method = 'EVO_LEVEL_MALE' if rules['IF_GENDER'] == 'MON_MALE' else 'EVO_LEVEL_FEMALE'; supported = True
                if param == '0' and len(rules) == 1 and rules.get('IF_KNOWS_MOVE') in (moves or set()):
                    method = 'EVO_LEVEL_MOVE'; param = rules['IF_KNOWS_MOVE']; supported = True
                if param == '0' and len(rules) == 2 and rules.get('IF_HOLD_ITEM') in items:
                    if rules.get('IF_NOT_TIME') == 'TIME_NIGHT': method = 'EVO_LEVEL_ITEM_DAY'; param = rules['IF_HOLD_ITEM']; supported = True
                    elif rules.get('IF_TIME') == 'TIME_NIGHT': method = 'EVO_LEVEL_ITEM_NIGHT'; param = rules['IF_HOLD_ITEM']; supported = True
                if param == '0' and rules.get('IF_MIN_FRIENDSHIP') == 'FRIENDSHIP_EVO_THRESHOLD':
                    if len(rules) == 1: method = 'EVO_FRIENDSHIP'; supported = True
                    elif len(rules) == 2 and rules.get('IF_NOT_TIME') == 'TIME_NIGHT': method = 'EVO_FRIENDSHIP_DAY'; supported = True
                    elif len(rules) == 2 and rules.get('IF_TIME') == 'TIME_NIGHT': method = 'EVO_FRIENDSHIP_NIGHT'; supported = True
                    elif len(rules) == 2 and rules.get('IF_KNOWS_MOVE_TYPE') == 'TYPE_FAIRY': method = 'EVO_FRIENDSHIP_MOVE_TYPE'; param = 'TYPE_FAIRY'; supported = True
            if method == 'EVO_TRADE' and param == '0' and len(conditions) == 1 and conditions[0][0] == 'IF_HOLD_ITEM':
                item = conditions[0][1].strip()
                if item in items: method = 'EVO_TRADE_ITEM'; param = item; supported = True
            if method == 'EVO_ITEM' and len(conditions) == 1 and conditions[0][0] == 'IF_GENDER':
                gender = conditions[0][1].strip()
                if gender in ('MON_MALE','MON_FEMALE'):
                    method = 'EVO_ITEM_MALE' if gender == 'MON_MALE' else 'EVO_ITEM_FEMALE'; supported = True
            if method not in ('EVO_LEVEL','EVO_LEVEL_MALE','EVO_LEVEL_FEMALE','EVO_LEVEL_MOVE','EVO_FRIENDSHIP','EVO_FRIENDSHIP_DAY','EVO_FRIENDSHIP_NIGHT','EVO_FRIENDSHIP_MOVE_TYPE','EVO_TRADE','EVO_TRADE_ITEM','EVO_ITEM','EVO_ITEM_MALE','EVO_ITEM_FEMALE','EVO_LEVEL_ITEM_DAY','EVO_LEVEL_ITEM_NIGHT'): supported = False
            if method in ('EVO_ITEM','EVO_ITEM_MALE','EVO_ITEM_FEMALE') and param in HELD_TRADE_ITEMS: supported = False
            if method == 'EVO_LEVEL_MOVE' and param not in (moves or set()): supported = False
            if target not in species or (method in ('EVO_ITEM','EVO_TRADE_ITEM','EVO_ITEM_MALE','EVO_ITEM_FEMALE','EVO_LEVEL_ITEM_DAY','EVO_LEVEL_ITEM_NIGHT') and param not in items): supported = False
            if supported: accepted.append((method,param,target))
            else: omitted.append(raw)
    return accepted, omitted

if __name__ == '__main__':
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    roster = json.loads((root/'data/eclipse-roster.json').read_text(encoding='utf-8'))
    source = json.loads((root/'data/eclipse-roster-source.json').read_text(encoding='utf-8'))
    species = set(re.findall(r'#define (SPECIES_\w+)\s+', (root/'include/constants/species.h').read_text()))
    items = set(re.findall(r'#define (ITEM_\w+)\s+', (root/'include/constants/items.h').read_text()))
    moves = set(re.findall(r'#define (MOVE_\w+)\s+', (root/'include/constants/moves.h').read_text()))
    aliases = {r['source_token']: r['token'] for r in roster['species']}
    aliases.update(GENDER_FORM_ALIASES)
    lines, audit = [], []
    for row in roster['species']:
        accepted, omitted = project(source[str(row['national'])]['body'], species, items, aliases, moves)
        if accepted: lines.append('['+row['token']+'] = {'+', '.join('{'+', '.join(e)+'}' for e in accepted[:8])+'},')
        audit.append(dict(species=row['token'], supported=accepted, omitted=omitted))
    (root/'src/data/eclipse_roster/evolutions.h').write_bytes(('// Generated by scripts/eclipse_evolutions.py; do not edit.\n'+'\n'.join(lines)+'\n').encode('utf-8'))
    (root/'data/eclipse-evolution-projection.json').write_bytes((json.dumps(audit,indent=2)+'\n').encode('utf-8'))
    print('Projected',sum(len(x['supported']) for x in audit),'rules;',sum(len(x['omitted']) for x in audit),'explicitly omitted')
