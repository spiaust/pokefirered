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
    TOUR_LONDON, TOUR_PARIS, TOUR_BERLIN, TOUR_REWARD, TOUR_COMPLETE
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
     _("north of LONDON."), _("Win his match to prepare for your rival.")},
    {_("BATTLE ALICE"), _("Find ALICE on OXFORD TRAIL,"),
     _("south of OXFORD."), _("Earlier trail victories count too.")},
    {_("MEET YOUR RIVAL"), _("Speak to your rival in OXFORD's square."),
     _("Both required trail matches are won."), _("Win the rival match for OAK's study.")},
    {_("REPORT TO OAK'S AIDE"), _("Return to the aide in LONDON's square."),
     _("Tell him about your rival match."), _("Keep room in ITEMS for the SOOTHE BELL.")},
    {_("CHALLENGE OXFORD GYM"), _("Enter OXFORD GYM north of the square."),
     _("Challenge ELLIS and his Rock-type team."), _("The clinic can heal your party first.")},
    {_("COLLECT ROCK TOMB"), _("Speak to ELLIS in OXFORD GYM again."),
     _("Make room for the TM and, if needed,"), _("a TM CASE in KEY ITEMS. Your badge is safe.")},
    {_("JOIN THE GARDEN SURVEY"), _("Speak to CELINE in PARIS's square."),
     _("She stands on the west side."), _("Your first badge unlocks her field survey.")},
    {_("OBSERVE BOTH HABITATS"), _("Read the survey markers in FRENCH GARDENS"),
     _("and CHANTILLY FOREST, in either order."), _("Then visit REMY in CHANTILLY's square.")},
    {_("OBSERVE CHANTILLY FOREST"), _("Read the forest survey marker on the"),
     _("trail south of CHANTILLY."), _("The FRENCH GARDENS observation is saved.")},
    {_("OBSERVE FRENCH GARDENS"), _("Read the garden survey marker on the"),
     _("route north of PARIS."), _("The CHANTILLY FOREST observation is saved.")},
    {_("REVIEW THE SURVEY"), _("Speak to REMY in CHANTILLY's square."),
     _("Both habitat observations are saved."), _("He will review the notes before you report.")},
    {_("REPORT TO CELINE"), _("Return to CELINE in PARIS's square."),
     _("Give her the reviewed survey."), _("Keep room in ITEMS for the MIRACLE SEED.")},
    {_("CHALLENGE CHANTILLY GYM"), _("Enter the GYM north of CHANTILLY's square."),
     _("Challenge MARINE and her Water-type team."), _("The clinic can heal your party first.")},
    {_("COLLECT WATER PULSE"), _("Speak to MARINE in CHANTILLY GYM again."),
     _("Make room for the TM and, if needed,"), _("a TM CASE in KEY ITEMS. Your badge is safe.")},
    {_("HELP REPAIR THE SIGNAL"), _("Speak to LENA in BERLIN's square."),
     _("She stands on the west side."), _("Two badges unlock her delivery request.")},
    {_("DELIVER THE REPAIR PARTS"), _("Speak to KARL in ORANIENBURG's square."),
     _("You are carrying LENA's repair parcel."), _("It does not need a Bag slot.")},
    {_("REPORT TO LENA"), _("Return to LENA in BERLIN's square."),
     _("Tell her the parts reached KARL."), _("Keep room in ITEMS for the MAGNET.")},
    {_("CHALLENGE ORANIENBURG GYM"), _("Enter the GYM north of the town square."),
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
     _("recorded. Keep exploring at your own pace."), _("Use UP/DOWN to check the CELEBI journey.")}
};

u8 GetEuropeTourLead(void)
{
    u16 stage;
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
    return (VarGet(VAR_EUROPE_STAMP_LONDON) != 0)
        | ((VarGet(VAR_EUROPE_STAMP_PARIS) != 0) << 1)
        | ((VarGet(VAR_EUROPE_STAMP_BERLIN) != 0) << 2)
        | ((VarGet(VAR_EUROPE_TOUR_REWARDED) != 0) << 3)
        | (FlagGet(FLAG_BADGE01_GET) << 4)
        | (FlagGet(FLAG_BADGE02_GET) << 5)
        | (FlagGet(FLAG_BADGE03_GET) << 6);
}
