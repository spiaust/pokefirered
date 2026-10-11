#include "global.h"
#include "event_data.h"
#include "battle_setup.h"
#include "europe_tour_journal.h"
#include "constants/flags.h"
#include "constants/vars.h"
#include "constants/opponents.h"

enum {
    TOUR_AIDE, TOUR_OLIVER, TOUR_ALICE, TOUR_RIVAL, TOUR_REPORT,
    TOUR_ELLIS, TOUR_ROCK_TM, TOUR_CELINE, TOUR_BOTH_SITES,
    TOUR_FOREST, TOUR_GARDENS, TOUR_REMY, TOUR_SURVEY_REPORT,
    TOUR_MARINE, TOUR_WATER_TM, TOUR_LENA, TOUR_KARL,
    TOUR_DELIVERY_REPORT, TOUR_CONRAD, TOUR_ELECTRIC_TM,
    TOUR_LONDON, TOUR_PARIS, TOUR_BERLIN, TOUR_REWARD, TOUR_COMPLETE,
    TOUR_NORDIC = 47, TOUR_KRAKOW = 52, TOUR_KRAKOW_WORK,
    TOUR_KRAKOW_REWARD, TOUR_CIRCUIT, TOUR_CIRCUIT_MATCHES,
    TOUR_CIRCUIT_REWARD = 69, TOUR_GUARDIANS, TOUR_CARE_THREE = 77,
    TOUR_CARE_SIX, TOUR_RESTORED, TOUR_WARSAW_MEMORY
};

const u8 gEuropeTourMilestones[7][24] = {
    _("LONDON STAMP"), _("PARIS STAMP"), _("BERLIN STAMP"),
    _("EXP. SHARE COLLECTED"), _("BOULDERBADGE"),
    _("CASCADEBADGE"), _("THUNDERBADGE")
};

const u8 gEuropeTourLeads[][4][44] = {
    {_("JOIN OAK'S FIELD STUDY"), _("Speak to OAK's aide in LONDON's square."),
     _("He stands on the west side."), _("You can take the train from any country.")},
    {_("BATTLE OLIVER"), _("Find OLIVER in ENGLISH MEADOW,"),
     _("North of LONDON; east of the main path."), _("Win his match to prepare for your rival.")},
    {_("BATTLE ALICE"), _("Find ALICE on OXFORD TRAIL,"),
     _("South of OXFORD; east of the main path."), _("Earlier trail victories count too.")},
    {_("MEET YOUR RIVAL"), _("Speak to your rival in OXFORD's square."),
     _("Your rival waits west of the town guide."), _("Win the rival match for OAK's study.")},
    {_("REPORT TO OAK'S AIDE"), _("Return to the aide in LONDON's square."),
     _("Collect his reward to battle ELLIS."), _("Keep room in ITEMS for the SOOTHE BELL.")},
    {_("CHALLENGE OXFORD GYM"), _("North of OXFORD square: walk in the door."),
     _("Challenge ELLIS and his Rock-type team."), _("The clinic can heal your party first.")},
    {_("COLLECT ROCK TOMB"), _("Speak to ELLIS in OXFORD GYM again."),
     _("Make room for the TM and, if needed,"), _("a TM CASE in KEY ITEMS. Your badge is safe.")},
    {_("JOIN THE GARDEN SURVEY"), _("Speak to CELINE in PARIS's square."),
     _("She stands on the west side."), _("Your first badge unlocks her field survey.")},
    {_("OBSERVE BOTH HABITATS"), _("Read the survey markers in FRENCH GARDENS"),
     _("and CHANTILLY FOREST, west of each path."), _("Either order; then meet REMY in CHANTILLY.")},
    {_("OBSERVE CHANTILLY FOREST"), _("Read the forest survey marker on the"),
     _("trail south of CHANTILLY; west of path."), _("The FRENCH GARDENS observation is saved.")},
    {_("OBSERVE FRENCH GARDENS"), _("Read the garden survey marker on the"),
     _("route north of PARIS; west of the path."), _("The CHANTILLY FOREST observation is saved.")},
    {_("REVIEW THE SURVEY"), _("Speak to REMY in CHANTILLY's square."),
     _("REMY waits west of the town guide."), _("He will review the notes before you report.")},
    {_("REPORT TO CELINE"), _("Return to CELINE in PARIS's square."),
     _("Collect her reward to battle MARINE."), _("Keep room in ITEMS for the MIRACLE SEED.")},
    {_("CHALLENGE CHANTILLY GYM"), _("North of town square: walk in the door."),
     _("Challenge MARINE and her Water-type team."), _("The clinic can heal your party first.")},
    {_("COLLECT WATER PULSE"), _("Speak to MARINE in CHANTILLY GYM again."),
     _("Make room for the TM and, if needed,"), _("a TM CASE in KEY ITEMS. Your badge is safe.")},
    {_("HELP REPAIR THE SIGNAL"), _("Speak to LENA in BERLIN's square."),
     _("She stands on the west side."), _("Two badges unlock her delivery request.")},
    {_("DELIVER THE REPAIR PARTS"), _("Speak to KARL in ORANIENBURG's square."),
     _("KARL waits west of the town guide."), _("Your parcel does not need a Bag slot.")},
    {_("REPORT TO LENA"), _("Return to LENA in BERLIN's square."),
     _("Collect her reward to battle CONRAD."), _("Keep room in ITEMS for the MAGNET.")},
    {_("CHALLENGE ORANIENBURG GYM"), _("North of town square: walk in the door."),
     _("Challenge CONRAD's Electric-type team."), _("The clinic can heal your party first.")},
    {_("COLLECT SHOCK WAVE"), _("Speak to CONRAD in ORANIENBURG GYM again."),
     _("Make room for the TM and, if needed,"), _("a TM CASE in KEY ITEMS. Your badge is safe.")},
    {_("COLLECT THE LONDON STAMP"), _("Speak to the town guide in LONDON."),
     _("The guide stands beside the central path."), _("City stamps can be collected in any order.")},
    {_("COLLECT THE PARIS STAMP"), _("Speak to the town guide in PARIS."),
     _("The guide stands beside the central path."), _("Your other city stamps remain recorded.")},
    {_("COLLECT THE BERLIN STAMP"), _("Speak to the town guide in BERLIN."),
     _("The guide stands beside the central path."), _("Your other city stamps remain recorded.")},
    {_("CLAIM YOUR TOUR REWARD"), _("All three city stamps are recorded."),
     _("Make room in ITEMS for one EXP. SHARE."), _("Talk to a LONDON, PARIS or BERLIN guide.")},
    {_("THREE COUNTRIES EXPLORED"), _("Your three badges and tour reward are"),
     _("recorded. Keep exploring at your own pace."), _("Use UP/DOWN to check the CELEBI journey.")},
    {_("01 / OXFORD"), _("ENGLAND"), _("Win the RIVAL match ahead."), _("Nurse left; next porter right.")},
    {_("02 / LONDON"), _("ENGLAND"), _("Win the GYM match ahead."), _("Nurse left; next porter right.")},
    {_("03 / PARIS"), _("FRANCE"), _("Win the GYM match ahead."), _("Nurse left; next porter right.")},
    {_("04 / BRUSSELS"), _("BELGIUM"), _("Win the GYM match ahead."), _("Nurse left; next porter right.")},
    {_("05 / AMSTERDAM"), _("NETHERLANDS"), _("Win the GYM match ahead."), _("Nurse left; next porter right.")},
    {_("06 / BERLIN"), _("GERMANY"), _("Win the GYM match ahead."), _("Nurse left; next porter right.")},
    {_("07 / PRAGUE"), _("CZECHIA"), _("Win the RESCUE match ahead."), _("Nurse left; next porter right.")},
    {_("08 / VIENNA"), _("AUSTRIA"), _("Win the GYM match ahead."), _("Nurse left; next porter right.")},
    {_("09 / ZURICH"), _("SWITZERLAND"), _("Win the RESCUE match ahead."), _("Nurse left; next porter right.")},
    {_("10 / ROME"), _("ITALY"), _("Win the GYM match ahead."), _("Nurse left; next porter right.")},
    {_("11 / MADRID"), _("SPAIN"), _("Win the GYM match ahead."), _("Nurse left; next porter right.")},
    {_("12 / LISBON"), _("PORTUGAL"), _("Win the RESCUE match ahead."), _("Nurse left; next porter right.")},
    {_("13 / PARIS1940"), _("FRANCE, 1940"), _("Win the RESCUE match ahead."), _("Nurse left; next porter right.")},
    {_("14 / WARSAW1943"), _("POLAND, 1943"), _("Win the RESCUE match ahead."), _("Nurse left; next porter right.")},
    {_("15 / BERLIN1944"), _("GERMANY, 1944"), _("Win the RESCUE match ahead."), _("Nurse left; next porter right.")},
    {_("16 / GENEVA"), _("SWITZERLAND"), _("Win the RESCUE match ahead."), _("Nurse left; next porter right.")},
    {_("17 / ATHENS"), _("GREECE"), _("Win the COUNCIL match ahead."), _("Nurse left; next porter right.")},
    {_("18 / ATHENS2"), _("GREECE"), _("Win the COUNCIL match ahead."), _("Nurse left; next porter right.")},
    {_("19 / ATHENS3"), _("GREECE"), _("Win the COUNCIL match ahead."), _("Nurse left; next porter right.")},
    {_("20 / ATHENS4"), _("GREECE"), _("Win the COUNCIL match ahead."), _("Nurse left; next porter right.")},
    {_("21 / CHAMPION"), _("GREECE"), _("Win the RIVAL match ahead."), _("Nurse left; next porter right.")},
    {_("EUROPEAN CHAMPION"), _("All twenty-one chapters are complete."), _("Shelters and training remain open."), _("Visit partners who still need care.")},
    {_("HUNT THE ECLIPSE REMNANTS"), _("Find ADA in modern COPENHAGEN."), _("Investigate the surviving northern relays."), _("Country porters connect the capitals.")},
    {_("COPENHAGEN / VEX"), _("Battle VEX at the Danish relay."), _("Then follow the signal to OSLO."), _("Heal and stock up before each remnant.")},
    {_("OSLO / RIME"), _("Battle RIME at the Norwegian relay."), _("The final signal leads to STOCKHOLM."), _("Your earlier relay victories stay saved.")},
    {_("STOCKHOLM / BOREAL"), _("Defeat BOREAL and silence the last relay."), _("Return to ADA in COPENHAGEN afterward."), _("The northern guardians remain available.")},
    {_("REPORT TO ADA"), _("All three remnant relays are silent."), _("Collect SHADOW BALL in COPENHAGEN."), _("Make room in the TM CASE if needed.")},
    {_("RESTORE KRAKOW SANCTUARY"), _("Use the KRAKOW porter in modern WARSAW."), _("Speak to the sanctuary caretaker."), _("Your Polish timeline choice shapes it.")},
    {_("KRAKOW / RESTORATION WORK"), _("Bring an ESCAPE ROPE and two SUPER POTIONS."), _("The last worksite needs a WATER STONE."), _("Speak to each worksite volunteer.")},
    {_("KRAKOW / CLAIM YOUR REWARD"), _("All three restoration tasks are complete."), _("Speak to the caretaker for a LUCKY EGG."), _("The refuge also offers a rescued partner.")},
    {_("ENTER THE CHAMPION CIRCUIT"), _("Find STEWART in the Champion shelter."), _("Thirteen stronger rematches await."), _("He also offers a training kit.")},
    {_("CIRCUIT 01/13 / ELLIS"), _("Next match: LONDON."), _("Normal team level: 64."), _("Heal, train and prepare your move coverage.")},
    {_("CIRCUIT 02/13 / MARINE"), _("Next match: PARIS."), _("Normal team level: 65."), _("Heal, train and prepare your move coverage.")},
    {_("CIRCUIT 03/13 / SABINE"), _("Next match: BRUSSELS."), _("Normal team level: 66."), _("Heal, train and prepare your move coverage.")},
    {_("CIRCUIT 04/13 / MAARTEN"), _("Next match: AMSTERDAM."), _("Normal team level: 67."), _("Heal, train and prepare your move coverage.")},
    {_("CIRCUIT 05/13 / GRETA"), _("Next match: BERLIN."), _("Normal team level: 68."), _("Heal, train and prepare your move coverage.")},
    {_("CIRCUIT 06/13 / IRENA"), _("Next match: VIENNA."), _("Normal team level: 69."), _("Heal, train and prepare your move coverage.")},
    {_("CIRCUIT 07/13 / FLAVIA"), _("Next match: ROME."), _("Normal team level: 70."), _("Heal, train and prepare your move coverage.")},
    {_("CIRCUIT 08/13 / INES"), _("Next match: MADRID."), _("Normal team level: 71."), _("Heal, train and prepare your move coverage.")},
    {_("CIRCUIT 09/13 / THALIA"), _("Next match: ATHENS / HALL 1."), _("Normal team level: 74."), _("Heal, train and prepare your move coverage.")},
    {_("CIRCUIT 10/13 / NIKOS"), _("Next match: ATHENS / HALL 2."), _("Normal team level: 75."), _("Heal, train and prepare your move coverage.")},
    {_("CIRCUIT 11/13 / ELENI"), _("Next match: ATHENS / HALL 3."), _("Normal team level: 76."), _("Heal, train and prepare your move coverage.")},
    {_("CIRCUIT 12/13 / LEON"), _("Next match: ATHENS / HALL 4."), _("Normal team level: 77."), _("Heal, train and prepare your move coverage.")},
    {_("CIRCUIT 13/13 / RIVAL"), _("Next match: CHAMPION SHELTER."), _("Normal team level: 80."), _("Heal, train and prepare your move coverage.")},
    {_("CLAIM THE CIRCUIT MASTER BALL"), _("Return to STEWART in the Champion shelter."), _("Your thirteen victories are recorded."), _("Keep one space in the BALLS pocket.")},
    {_("GUARDIAN / ARTICUNO"), _("A guardian awaits in modern REYKJAVIK."), _("Look for its partner near the refuge."), _("Save and bring POKE BALLS before battle.")},
    {_("GUARDIAN / ZAPDOS"), _("A guardian awaits in modern OSLO."), _("Look for its partner near the refuge."), _("Save and bring POKE BALLS before battle.")},
    {_("GUARDIAN / MOLTRES"), _("A guardian awaits in modern ROME."), _("Look for its partner near the refuge."), _("Save and bring POKE BALLS before battle.")},
    {_("GUARDIAN / SUICUNE"), _("A guardian awaits in modern HELSINKI."), _("Look for its partner near the refuge."), _("Save and bring POKE BALLS before battle.")},
    {_("GUARDIAN / LUGIA"), _("A guardian awaits in modern VALLETTA."), _("Look for its partner near the refuge."), _("Save and bring POKE BALLS before battle.")},
    {_("GUARDIAN / HO-OH"), _("A guardian awaits in modern VIENNA."), _("Look for its partner near the refuge."), _("Save and bring POKE BALLS before battle.")},
    {_("GUARDIAN / MEWTWO"), _("A guardian awaits in modern BERLIN."), _("Look for its partner near the refuge."), _("Save and bring POKE BALLS before battle.")},
    {_("REKINDLE THE RAINBOW BEACON"), _("Purify three rescued SHADOW partners."), _("Shelter keepers offer care and rest."), _("HO-OH waits in modern VIENNA afterward.")},
    {_("FREE THE LABORATORY GUARDIAN"), _("Purify all six rescued SHADOW partners."), _("Use a city PC to bring partners for care."), _("MEWTWO waits in modern BERLIN afterward.")},
    {_("EUROPE RESTORED"), _("Remnants, sanctuary and circuit complete."), _("All seven guardians have been caught."), _("Keep exploring reserves and rematches.")},
    {_("REMEMBER WARSAW"), _("Visit WARSAW in the past."), _("Complete its operation and choose a legacy."), _("Return to modern WARSAW for KRAKOW.")}

};

// Read saved postgame objectives without changing their order or rewards.
static u8 GetPostgameLead(void)
{
    u16 circuit = VarGet(VAR_ECLIPSE_CIRCUIT);
    u16 nordic = VarGet(VAR_ECLIPSE_NORDIC_HUNT);
    u16 krakow = VarGet(VAR_ECLIPSE_KRAKOW);
    u8 i;
    if (circuit >= 1 && circuit <= 13) return TOUR_CIRCUIT_MATCHES + circuit - 1;
    if (circuit == 14) return TOUR_CIRCUIT_REWARD;
    if (nordic > 0 && nordic < 5) return TOUR_NORDIC + nordic;
    if (nordic == 0 && krakow == 0) return TOUR_NORDIC;
    if (krakow < 3)
    {
        if (!(VarGet(VAR_0x40A5) & (1 << 13))) return TOUR_WARSAW_MEMORY;
        if (krakow == 0) return TOUR_KRAKOW;
        if (krakow == 2 || (FlagGet(FLAG_0x8D6) && FlagGet(FLAG_0x8D7) && FlagGet(FLAG_0x8D8))) return TOUR_KRAKOW_REWARD;
        return TOUR_KRAKOW_WORK;
    }
    if (nordic == 0) return TOUR_NORDIC;
    if (circuit == 0) return TOUR_CIRCUIT;
    for (i = 0; i < 7; i++)
    {
        if (!FlagGet(FLAG_0x8CE + i))
        {
            if (i == 5 && VarGet(VAR_SHADOW_PURIFIED) < 3) return TOUR_CARE_THREE;
            if (i == 6 && VarGet(VAR_SHADOW_PURIFIED) < 6) return TOUR_CARE_SIX;
            return TOUR_GUARDIANS + i;
        }
    }
    return TOUR_RESTORED;
}

u8 GetEuropeTourLead(void)
{
    u16 stage;
    if (VarGet(VAR_SHADOW_STARTED))
    {
        stage = VarGet(VAR_SHADOW_STAGE);
        if (stage >= 21) return GetPostgameLead();
        return 25 + stage;
    }
    if (!FlagGet(FLAG_BADGE01_GET))
    {
        stage = VarGet(VAR_EUROPE_ENGLAND_STORY);
        if (stage == 0) return TOUR_AIDE;
        if (stage == 2) return TOUR_ELLIS;
        if (HasTrainerBeenFought(TRAINER_EUROPE_RIVAL_OXFORD)) return TOUR_REPORT;
        if (!HasTrainerBeenFought(TRAINER_EUROPE_OLIVER)) return TOUR_OLIVER;
        if (!HasTrainerBeenFought(TRAINER_EUROPE_ALICE)) return TOUR_ALICE;
        return TOUR_RIVAL;
    }
    if (!VarGet(VAR_EUROPE_OXFORD_TM)) return TOUR_ROCK_TM;
    if (!FlagGet(FLAG_BADGE02_GET))
    {
        stage = VarGet(VAR_EUROPE_FRANCE_STORY);
        if (stage == 0) return TOUR_CELINE;
        if (stage == 1) return TOUR_BOTH_SITES;
        if (stage == 2) return TOUR_FOREST;
        if (stage == 3) return TOUR_GARDENS;
        if (stage == 4) return TOUR_REMY;
        if (stage == 5) return TOUR_SURVEY_REPORT;
        return TOUR_MARINE;
    }
    if (!VarGet(VAR_EUROPE_CHANTILLY_TM)) return TOUR_WATER_TM;
    if (!FlagGet(FLAG_BADGE03_GET))
    {
        stage = VarGet(VAR_EUROPE_GERMANY_STORY);
        if (stage == 0) return TOUR_LENA;
        if (stage == 1) return TOUR_KARL;
        if (stage == 2) return TOUR_DELIVERY_REPORT;
        return TOUR_CONRAD;
    }
    if (!VarGet(VAR_EUROPE_ORANIENBURG_TM)) return TOUR_ELECTRIC_TM;
    if (!VarGet(VAR_EUROPE_STAMP_LONDON)) return TOUR_LONDON;
    if (!VarGet(VAR_EUROPE_STAMP_PARIS)) return TOUR_PARIS;
    if (!VarGet(VAR_EUROPE_STAMP_BERLIN)) return TOUR_BERLIN;
    if (!VarGet(VAR_EUROPE_TOUR_REWARDED)) return TOUR_REWARD;
    return TOUR_COMPLETE;
}

u8 GetEuropeTourMilestones(void)
{
    if (VarGet(VAR_SHADOW_STARTED))
    {
        u16 stage = VarGet(VAR_SHADOW_STAGE);
        return (stage >= 2) | ((stage >= 7) << 1) | ((stage >= 11) << 2)
            | ((stage >= 12) << 3) | ((stage >= 15) << 4)
            | ((stage >= 16) << 5) | ((stage >= 21) << 6);
    }
    return (VarGet(VAR_EUROPE_STAMP_LONDON) != 0)
        | ((VarGet(VAR_EUROPE_STAMP_PARIS) != 0) << 1)
        | ((VarGet(VAR_EUROPE_STAMP_BERLIN) != 0) << 2)
        | ((VarGet(VAR_EUROPE_TOUR_REWARDED) != 0) << 3)
        | (FlagGet(FLAG_BADGE01_GET) << 4)
        | (FlagGet(FLAG_BADGE02_GET) << 5)
        | (FlagGet(FLAG_BADGE03_GET) << 6);
}

const u8 gShadowCampaignMilestones[7][24] = {
 _("FIRST BADGE"), _("RIVAL RESCUED"), _("EIGHT BADGES"),
 _("TIME PASSAGE OPEN"), _("RESISTANCE HELPED"), _("ECLIPSE DEFEATED"),
 _("EUROPEAN CHAMPION")
};
