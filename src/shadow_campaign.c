#include "global.h"
#include "pokemon.h"
#include "pokedex.h"
#include "event_data.h"
#include "field_specials.h"
#include "fieldmap.h"
#include "field_fadetransition.h"
#include "overworld.h"
#include "string_util.h"
#include "shadow_campaign.h"
#include "europe_map.h"
#include "constants/maps.h"
#include "constants/vars.h"
#include "constants/pokemon.h"
#include "constants/species.h"
static const u8 sShadowName[] = _("SHADOW");
static const u8 sHealedName[] = _("HEALED");
static const u8 sChapters[][2] = {
    {MAP_GROUP(MAP_SHADOW_OXFORD), MAP_NUM(MAP_SHADOW_OXFORD)},
    {MAP_GROUP(MAP_SHADOW_LONDON), MAP_NUM(MAP_SHADOW_LONDON)},
    {MAP_GROUP(MAP_SHADOW_PARIS), MAP_NUM(MAP_SHADOW_PARIS)},
    {MAP_GROUP(MAP_SHADOW_BRUSSELS), MAP_NUM(MAP_SHADOW_BRUSSELS)},
    {MAP_GROUP(MAP_SHADOW_AMSTERDAM), MAP_NUM(MAP_SHADOW_AMSTERDAM)},
    {MAP_GROUP(MAP_SHADOW_BERLIN), MAP_NUM(MAP_SHADOW_BERLIN)},
    {MAP_GROUP(MAP_SHADOW_PRAGUE), MAP_NUM(MAP_SHADOW_PRAGUE)},
    {MAP_GROUP(MAP_SHADOW_VIENNA), MAP_NUM(MAP_SHADOW_VIENNA)},
    {MAP_GROUP(MAP_SHADOW_ZURICH), MAP_NUM(MAP_SHADOW_ZURICH)},
    {MAP_GROUP(MAP_SHADOW_ROME), MAP_NUM(MAP_SHADOW_ROME)},
    {MAP_GROUP(MAP_SHADOW_MADRID), MAP_NUM(MAP_SHADOW_MADRID)},
    {MAP_GROUP(MAP_SHADOW_LISBON), MAP_NUM(MAP_SHADOW_LISBON)},
    {MAP_GROUP(MAP_SHADOW_PARIS1940), MAP_NUM(MAP_SHADOW_PARIS1940)},
    {MAP_GROUP(MAP_SHADOW_WARSAW1943), MAP_NUM(MAP_SHADOW_WARSAW1943)},
    {MAP_GROUP(MAP_SHADOW_BERLIN1944), MAP_NUM(MAP_SHADOW_BERLIN1944)},
    {MAP_GROUP(MAP_SHADOW_GENEVA), MAP_NUM(MAP_SHADOW_GENEVA)},
    {MAP_GROUP(MAP_SHADOW_ATHENS), MAP_NUM(MAP_SHADOW_ATHENS)},
    {MAP_GROUP(MAP_SHADOW_ATHENS2), MAP_NUM(MAP_SHADOW_ATHENS2)},
    {MAP_GROUP(MAP_SHADOW_ATHENS3), MAP_NUM(MAP_SHADOW_ATHENS3)},
    {MAP_GROUP(MAP_SHADOW_ATHENS4), MAP_NUM(MAP_SHADOW_ATHENS4)},
    {MAP_GROUP(MAP_SHADOW_CHAMPION), MAP_NUM(MAP_SHADOW_CHAMPION)},
};
void Shadow_Resume(void)
{
    u16 stage = VarGet(VAR_SHADOW_STAGE);
    if (stage >= ARRAY_COUNT(sChapters)) stage = ARRAY_COUNT(sChapters) - 1;
    SetWarpDestination(sChapters[stage][0], sChapters[stage][1], WARP_ID_NONE, 6, 7);
    DoWarp();
    ResetInitialPlayerAvatarState();
}
void Shadow_Rescue(void)
{
    u8 index = gSpecialVar_0x8004;
    u8 state = 1, friendship = 10;
    u8 location = gMapHeader.regionMapSectionId;
    u16 mask = VarGet(VAR_SHADOW_RESCUES);
    if (index >= 6 || (mask & (1 << index))) { gSpecialVar_Result = 0; return; }
    if (gPlayerPartyCount >= PARTY_SIZE) { gSpecialVar_Result = 2; return; }
    CreateMon(&gPlayerParty[gPlayerPartyCount], gSpecialVar_0x8005, gSpecialVar_0x8006, 20, FALSE, 0, OT_ID_PLAYER_ID, 0);
    SetMonData(&gPlayerParty[gPlayerPartyCount], MON_DATA_UNUSED_RIBBONS, &state);
    SetMonData(&gPlayerParty[gPlayerPartyCount], MON_DATA_FRIENDSHIP, &friendship);
    SetMonData(&gPlayerParty[gPlayerPartyCount], MON_DATA_NICKNAME, sShadowName);
    SetMonData(&gPlayerParty[gPlayerPartyCount], MON_DATA_MET_LOCATION, &location);
    CalculatePlayerPartyCount();
    GetSetPokedexFlag(SpeciesToNationalPokedexNum(gSpecialVar_0x8005), FLAG_SET_SEEN);
    GetSetPokedexFlag(SpeciesToNationalPokedexNum(gSpecialVar_0x8005), FLAG_SET_CAUGHT);
    VarSet(VAR_SHADOW_RESCUES, mask | (1 << index));
    gSpecialVar_Result = 1;
}
void Shadow_TryPurify(void)
{
    u8 i, state, friendship, ribbon = 1;
    gSpecialVar_Result = 0;
    for (i = 0; i < gPlayerPartyCount; i++)
    {
        state = GetMonData(&gPlayerParty[i], MON_DATA_UNUSED_RIBBONS, NULL);
        if (!(state & 1)) continue;
        friendship = GetMonData(&gPlayerParty[i], MON_DATA_FRIENDSHIP, NULL);
        if (friendship >= 120)
        {
            state &= ~1;
            SetMonData(&gPlayerParty[i], MON_DATA_UNUSED_RIBBONS, &state);
            SetMonData(&gPlayerParty[i], MON_DATA_NICKNAME, sHealedName);
            SetMonData(&gPlayerParty[i], MON_DATA_NATIONAL_RIBBON, &ribbon);
            VarSet(VAR_SHADOW_PURIFIED, VarGet(VAR_SHADOW_PURIFIED) + 1);
            gSpecialVar_Result = 1;
        }
        else
        {
            friendship += 10;
            SetMonData(&gPlayerParty[i], MON_DATA_FRIENDSHIP, &friendship);
            gSpecialVar_Result = 2;
        }
        return;
    }
}
bool8 Shadow_IsEnemyTrainer(u16 trainer)
{
    if (trainer >= 259 && trainer <= 375 && (trainer - 259) % 3 == 2)
    {
        switch ((trainer - 259) / 3)
        {
        case 8:
        case 11:
        case 12:
        case 17:
        case 20:
        case 38:
            return FALSE;
        default: return TRUE;
        }
    }
    switch (trainer)
    {
    case 148:
    case 164:
    case 188:
    case 196:
    case 203:
    case 210:
    case 217:
        return TRUE;
    default: return FALSE;
    }
}

bool8 Shadow_IsPast(void)
{
    return (gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_CONTINENT_LONDON) && (gSaveBlock1Ptr->location.mapNum & 1))
        || (gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_SHADOW_OXFORD)
        && gSaveBlock1Ptr->location.mapNum >= MAP_NUM(MAP_SHADOW_PARIS1940)
        && gSaveBlock1Ptr->location.mapNum <= MAP_NUM(MAP_SHADOW_BERLIN1944_ROUTE));
}

void Shadow_BeginEncounter(void)
{
    u16 area, bank, mask;
    VarSet(VAR_SHADOW_ENCOUNTER_BLOCKED, 0);
    if (!VarGet(VAR_SHADOW_NUZLOCKE)) return;
    if (gSaveBlock1Ptr->location.mapGroup != MAP_GROUP(MAP_SHADOW_OXFORD) && gSaveBlock1Ptr->location.mapGroup != MAP_GROUP(MAP_CONTINENT_LONDON) && gSaveBlock1Ptr->location.mapGroup != MAP_GROUP(MAP_EUROPE_LONDON)) return;
    area = gSaveBlock1Ptr->location.mapNum / 2;
    if (gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_CONTINENT_LONDON)) area += 21;
    if (gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_EUROPE_LONDON)) area = 60 + gSaveBlock1Ptr->location.mapNum;
    bank = VAR_0x4095 + area / 16;
    mask = 1 << (area % 16);
    VarSet(VAR_SHADOW_ENCOUNTER_BLOCKED, (VarGet(bank) & mask) != 0);
    VarSet(bank, VarGet(bank) | mask);
}

static u16 Shadow_CountryIndex(void)
{
    return gSaveBlock1Ptr->location.mapNum / 2;
}
static bool8 Shadow_CountryBit(u16 base)
{
    u16 i = Shadow_CountryIndex();
    return (VarGet(base + i / 16) & (1 << (i % 16))) != 0;
}
void Shadow_CountryStatus(void)
{
    gSpecialVar_Result = Shadow_CountryBit(VAR_SHADOW_COUNTRY_CLEARED);
}
void Shadow_CountryClear(void)
{
    u16 i = Shadow_CountryIndex(), base = VAR_SHADOW_COUNTRY_CLEARED + i / 16;
    VarSet(base, VarGet(base) | (1 << (i % 16)));
}
void Shadow_CountryMemory(void)
{
    gSpecialVar_Result = !Shadow_CountryBit(VAR_0x40A5) ? 0 : Shadow_CountryBit(VAR_0x40A2) ? 1 : 2;
}
void Shadow_CountryDecide(void)
{
    u16 i = Shadow_CountryIndex(), mask = 1 << (i % 16), bank = i / 16;
    if (Shadow_CountryBit(VAR_0x40A5)) return;
    VarSet(VAR_0x40A5 + bank, VarGet(VAR_0x40A5 + bank) | mask);
    if (gSpecialVar_0x8004 == 1) VarSet(VAR_0x40A2 + bank, VarGet(VAR_0x40A2 + bank) | mask);
}
void Shadow_CountryTravel(void)
{
    SetWarpDestination(gSaveBlock1Ptr->location.mapGroup, gSaveBlock1Ptr->location.mapNum ^ 1, WARP_ID_NONE, 18, 31);
    DoWarp();
    ResetInitialPlayerAvatarState();
}
void Shadow_ApplyTimeline(void)
{
    if (gSaveBlock1Ptr->location.mapGroup != MAP_GROUP(MAP_CONTINENT_LONDON) || Shadow_IsPast()) return;
    if (Shadow_CountryBit(VAR_0x40A5))
    {
        u8 x, y;
        for (y = 15; y < 18; y++)
            for (x = 20; x < 26; x++)
                MapGridSetMetatileIdAt(x + 7, y + 7, Shadow_CountryBit(VAR_0x40A2) ? 0x3004 : 0x3165);
        for (y = 20; y < 29; y++)
            MapGridSetMetatileIdAt(39 + 7, y + 7, 0x3165);
    }
}
static const u8 sCountryName0[] = _("LONDON");
static const u8 sCountryName1[] = _("PARIS");
static const u8 sCountryName2[] = _("BERLIN");
static const u8 sCountryName3[] = _("BRUSSELS");
static const u8 sCountryName4[] = _("AMSTERDAM");
static const u8 sCountryName5[] = _("VIENNA");
static const u8 sCountryName6[] = _("PRAGUE");
static const u8 sCountryName7[] = _("BRATISLAVA");
static const u8 sCountryName8[] = _("BERN");
static const u8 sCountryName9[] = _("ROME");
static const u8 sCountryName10[] = _("ATHENS");
static const u8 sCountryName11[] = _("MADRID");
static const u8 sCountryName12[] = _("LISBON");
static const u8 sCountryName13[] = _("WARSAW");
static const u8 sCountryName14[] = _("LUXEMBOURG");
static const u8 sCountryName15[] = _("COPENHAGEN");
static const u8 sCountryName16[] = _("OSLO");
static const u8 sCountryName17[] = _("STOCKHOLM");
static const u8 sCountryName18[] = _("HELSINKI");
static const u8 sCountryName19[] = _("REYKJAVIK");
static const u8 sCountryName20[] = _("DUBLIN");
static const u8 sCountryName21[] = _("VALLETTA");
static const u8 sCountryName22[] = _("BUDAPEST");
static const u8 sCountryName23[] = _("BUCHAREST");
static const u8 sCountryName24[] = _("SOFIA");
static const u8 sCountryName25[] = _("TIRANA");
static const u8 sCountryName26[] = _("BELGRADE");
static const u8 sCountryName27[] = _("ZAGREB");
static const u8 sCountryName28[] = _("LJUBLJANA");
static const u8 sCountryName29[] = _("SARAJEVO");
static const u8 sCountryName30[] = _("KOTOR");
static const u8 sCountryName31[] = _("SKOPJE");
static const u8 sCountryName32[] = _("MOSCOW");
static const u8 sCountryName33[] = _("KYIV");
static const u8 sCountryName34[] = _("MINSK");
static const u8 sCountryName35[] = _("VILNIUS");
static const u8 sCountryName36[] = _("RIGA");
static const u8 sCountryName37[] = _("TALLINN");
static const u8 sCountryName38[] = _("ISTANBUL");
static const u8 *const sCountryNames[] = {sCountryName0, sCountryName1, sCountryName2, sCountryName3, sCountryName4, sCountryName5, sCountryName6, sCountryName7, sCountryName8, sCountryName9, sCountryName10, sCountryName11, sCountryName12, sCountryName13, sCountryName14, sCountryName15, sCountryName16, sCountryName17, sCountryName18, sCountryName19, sCountryName20, sCountryName21, sCountryName22, sCountryName23, sCountryName24, sCountryName25, sCountryName26, sCountryName27, sCountryName28, sCountryName29, sCountryName30, sCountryName31, sCountryName32, sCountryName33, sCountryName34, sCountryName35, sCountryName36, sCountryName37, sCountryName38};
const u8 *Shadow_GetCountryMapName(u16 section)
{
 return section < ARRAY_COUNT(sCountryNames) ? sCountryNames[section] : NULL;
}

void Shadow_ApplyChallenge(void)
{
    u8 i;
    u16 zero = 0;
    if (!VarGet(VAR_SHADOW_NUZLOCKE)) return;
    for (i = 0; i < gPlayerPartyCount; i++)
        if (GetMonData(&gPlayerParty[i], MON_DATA_UNUSED_RIBBONS, NULL) & 2)
            SetMonData(&gPlayerParty[i], MON_DATA_HP, &zero);
}
void Shadow_NetworkStatus(void)
{
    u16 i, count = 0;
    for (i = 0; i < 39; i++)
        if (VarGet(VAR_0x40A5 + i / 16) & (1 << (i % 16))) count++;
    gSpecialVar_Result = count;
    ConvertIntToDecimalStringN(gStringVar1, count, STR_CONV_MODE_LEFT_ALIGN, 2);
}

void Shadow_RivalPartner(struct Pokemon *party, u8 count)
{
    u16 starter = VarGet(VAR_EUROPE_STARTER_SPECIES), species, target;
    u8 slot = count > 3 ? 3 : count - 1;
    u8 level = GetMonData(&party[slot], MON_DATA_LEVEL, NULL);
    u8 iv = VarGet(VAR_SHADOW_DIFFICULTY) == 2 ? 26 : VarGet(VAR_SHADOW_DIFFICULTY) == 1 ? 5 : 16;
    u8 i;
    switch (starter)
    {
    case SPECIES_BULBASAUR: species = SPECIES_CHARMANDER; break;
    case SPECIES_CHARMANDER: species = SPECIES_SQUIRTLE; break;
    case SPECIES_SQUIRTLE: species = SPECIES_BULBASAUR; break;
    case SPECIES_CHIKORITA: species = SPECIES_CYNDAQUIL; break;
    case SPECIES_CYNDAQUIL: species = SPECIES_TOTODILE; break;
    case SPECIES_TOTODILE: species = SPECIES_CHIKORITA; break;
    case SPECIES_TREECKO: species = SPECIES_TORCHIC; break;
    case SPECIES_TORCHIC: species = SPECIES_MUDKIP; break;
    case SPECIES_MUDKIP: species = SPECIES_TREECKO; break;
    default: species = SPECIES_EEVEE; break;
    }
    CreateMon(&party[slot], species, level, iv, FALSE, 0, OT_ID_RANDOM_NO_SHINY, 0);
    for (i = 0; i < 2; i++)
    {
        target = GetEvolutionTargetSpecies(&party[slot], EVO_MODE_NORMAL, 0);
        if (!target) break;
        SetMonData(&party[slot], MON_DATA_SPECIES, &target);
        CalculateMonStats(&party[slot]);
        GiveMonInitialMoveset(&party[slot]);
    }
}

void Shadow_ShowCredits(void)
{
    OpenEuropeCredits(CB2_ReturnToFieldContinueScript);
}
