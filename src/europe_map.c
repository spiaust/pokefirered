#include "global.h"
#include "gflib.h"
#include "menu.h"
#include "task.h"
#include "overworld.h"
#include "scanline_effect.h"
#include "europe_map.h"
#include "europe_tour_journal.h"
#include "event_data.h"
#include "constants/flags.h"
#include "constants/vars.h"
#include "constants/songs.h"
#include "constants/maps.h"

static EWRAM_DATA MainCallback sEuropeMapReturn = NULL;
static EWRAM_DATA u8 sEuropeMapSelection = 0;
static EWRAM_DATA u8 sEuropeMapCurrent = 0;
static EWRAM_DATA bool8 sEuropeMapPast = FALSE;
static const struct BgTemplate sMapBg[] = {
    {.bg = 0, .charBaseIndex = 0, .mapBaseIndex = 31, .priority = 0}
};
static const struct WindowTemplate sMapWindows[] = {
    {.bg = 0, .width = 30, .height = 20, .paletteNum = 0, .baseBlock = 1},
    DUMMY_WIN_TEMPLATE
};
static const u16 sMapPalette[] = {
    RGB(2, 5, 12), RGB(2, 5, 12), RGB(29, 30, 27), RGB(31, 24, 8),
    RGB(8, 17, 15), RGB(13, 23, 17), RGB(6, 11, 18), RGB(24, 13, 12)
};
static const u8 sWhite[] = {1, 2, 1};
static const u8 sGold[] = {1, 3, 1};
static const u8 sNorthLabel[] = _("N");
static const u8 sHeading[] = _("EUROPEAN TRAVEL MAP");
static const u8 sPastHeading[] = _("PRESENT-DAY TRAVEL MAP");
static const u8 sPastLocation[] = _("YOU: FRANCE, 1940");
static const u8 sBeauvaisLocation[] = _("YOU: BEAUVAIS, 1940");
static const u8 sLondonPastLocation[] = _("YOU: LONDON, 1940");
static const u8 sSouthamptonLocation[] = _("YOU: SOUTHAMPTON, 1940");
static const u8 sLeHavreLocation[] = _("YOU: LE HAVRE, 1940");
static const u8 sRouenLocation[] = _("YOU: ROUEN, 1940");
static const u8 sAmiensLocation[] = _("YOU: AMIENS, 1940");
static const u8 sPastHint[] = _("Return via CELEBI near your arrival.");
static const u8 sControls[] = _("D-PAD: STOP  SELECT: STORY  B: BACK");
static const u8 sLondon[] = _("LONDON");
static const u8 sParis[] = _("PARIS");
static const u8 sBerlin[] = _("BERLIN");
static const u8 sOxford[] = _("OXFORD");
static const u8 sChantilly[] = _("CHANTILLY");
static const u8 sOranienburg[] = _("ORANIENBURG");
static const u8 sInEngland[] = _("YOU: ENGLAND");
static const u8 sInFrance[] = _("YOU: FRANCE");
static const u8 sInGermany[] = _("YOU: GERMANY");
static const u8 *const sLocations[] = {sInEngland, sInFrance, sInGermany, sInEngland, sInFrance, sInGermany, sInEngland, sInFrance};
static const u8 sLondonInfo[] = _("ENGLAND / ENGLISH MEADOW");
static const u8 sParisInfo[] = _("FRANCE / FRENCH GARDENS");
static const u8 sBerlinInfo[] = _("GERMANY / GERMAN WOODLAND");
static const u8 sOxfordInfo[] = _("ENGLAND / OXFORD TRAIL");
static const u8 sChantillyInfo[] = _("FRANCE / CHANTILLY FOREST");
static const u8 sOranienburgInfo[] = _("GERMANY / HAVEL TRAIL");
static const u8 sDoverInfo[] = _("DOVER PORT / COACH TO LONDON");
static const u8 sCalaisInfo[] = _("CALAIS PORT / COACH TO PARIS");
static const u8 sCoastHint[] = _("Dover-Calais ferry; coaches to cities.");
static const u8 sDover[] = _("DOVER");
static const u8 sCalais[] = _("CALAIS");
static const u8 *const sDetails[] = {sLondonInfo, sParisInfo, sBerlinInfo, sOxfordInfo, sChantillyInfo, sOranienburgInfo, sDoverInfo, sCalaisInfo};
static const u8 sRailHint[] = _("Change trains at intermediate stops.");
static const u8 sHelpHint[] = _("A: TRAVEL INFO");
#include "data/europe_geography.h"
static EWRAM_DATA bool8 sWorldOptions = FALSE;
static const u8 *const sCityNames[] = {sLondon, sParis, sBerlin, sOxford, sChantilly, sOranienburg, sDover, sCalais};

enum { JOURNAL_MAP, JOURNAL_LEAD, JOURNAL_RECORDS };
enum {
    LEAD_BADGE, LEAD_ADA, LEAD_FOREST, LEAD_VISION, LEAD_PAST,
    LEAD_ELISE, LEAD_KEEPER, LEAD_BLANKET, LEAD_GUIDE, LEAD_NOTICE,
    LEAD_DISPATCHER, LEAD_NEWS, LEAD_TRAIN, LEAD_CHECK_IN,
    LEAD_MESSAGE, LEAD_DELIVER_MESSAGE, LEAD_REPLY, LEAD_ACCOUNT,
    LEAD_SUPPLIES, LEAD_COLLECT_PARCEL, LEAD_DELIVER_PARCEL,
    LEAD_GARDEN, LEAD_FIND_PIDGEY, LEAD_RETURN_PIDGEY, LEAD_AMIENS,
    LEAD_NORA, LEAD_AMIENS_NOTICE, LEAD_AMIENS_REPORT, LEAD_REUNION,
    LEAD_REPORTS, LEAD_PORTER, LEAD_MIRA, LEAD_VERIFY, LEAD_REUNITE, LEAD_REST, LEAD_AMIENS_ARCHIVED,
    LEAD_AMIENS_BULLETIN, LEAD_AMIENS_CHECK, LEAD_AMIENS_DELIVER, LEAD_AMIENS_WAIT, LEAD_ROUEN_LEON, LEAD_ROUEN_READY, LEAD_ROUEN_BOOK, LEAD_ROUEN_BOOK_RETURN, LEAD_ROUEN_BOOK_DONE, LEAD_LE_HAVRE_CAPTAIN, LEAD_LE_HAVRE_READY, LEAD_DOCK_NOTICE, LEAD_DOCK_CAPTAIN, LEAD_DOCK_DONE, LEAD_PORT_ARCHIVED, LEAD_SOUTHAMPTON_HOST, LEAD_SOUTHAMPTON_DONE, LEAD_LUGGAGE_FIND, LEAD_LUGGAGE_RETURN, LEAD_LUGGAGE_DONE, LEAD_SOUTH_ACCOUNT, LEAD_LONDON_ROSE, LEAD_LONDON_WELCOME
};
static const u8 sJournalHeading[] = _("CELEBI JOURNEY / CURRENT LEAD");
#define JOURNAL_RECORDS_PER_PAGE 10
static const u8 sRecordsHeadings[][40] = {
    _("CELEBI JOURNEY / RECORDS 1/2"), _("CELEBI JOURNEY / RECORDS 2/2")
};
static const u8 sRecordPageControls[] = _("A: LEAD  LEFT/RIGHT: PAGE");
static const u8 sJournalControls[] = _("UP/DOWN: TOPIC  SELECT: MAP  B: BACK");
static const u8 sTourHeading[] = _("EUROPE TOUR / CURRENT LEAD");
static const u8 sTourRecordsHeading[] = _("EUROPE TOUR / STAMPS AND BADGES");
static const u8 sTourHint[] = _("City guides offer optional tour stamps.");
static const u8 sShowRecords[] = _("A: VIEW MILESTONES");
static const u8 sShowLead[] = _("A: VIEW CURRENT LEAD");
static const u8 sJournalPastHint[] = _("CELEBI waits near your past arrival.");
static const u8 sJournalPresentHint[] = _("Past visits: CELEBI in CHANTILLY FOREST.");
static const u8 sDone[] = _("DONE");
static const u8 sNotDone[] = _("--");
static const u8 sMilestones[][24] = {
    _("CELEBI'S VISION"), _("REFUGE BLANKET"), _("DEPARTURE NEWS"),
    _("BEAUVAIS CHECK-IN"), _("ELISE'S ACCOUNT"), _("RECEPTION CARE"),
    _("LUC AND PIDGEY"), _("AMIENS ARRIVAL"), _("MIRA AND MEOWTH"), _("AMIENS ACCOUNT"),
    _("AMIENS BULLETIN"), _("ROUEN ARRIVAL"), _("ROUEN ROUTE BOOK"), _("LE HAVRE ARRIVAL"), _("DOCK INSTRUCTIONS"), _("PORT ACCOUNT"), _("SOUTHAMPTON ARRIVAL"), _("TRAVELER LUGGAGE"), _("SOUTHAMPTON ACCOUNT"), _("LONDON RECEPTION")
};
// Each entry is a title followed by three short lines of actionable guidance.
static const u8 sJournalLeads[][4][44] = {
    {_("PREPARE FOR THE JOURNEY"), _("Earn the THUNDERBADGE in ORANIENBURG."),
     _("Then meet ADA in OXFORD's square."), _("She studies a strange visitor in France.")},
    {_("MEET THE RESEARCHER"), _("Speak to ADA in OXFORD's square."),
     _("She is east of the town guide."), _("Ask about the CHANTILLY sighting.")},
    {_("INVESTIGATE THE SIGHTING"), _("Walk south from CHANTILLY into the forest."),
     _("Look beside the middle path, just south"), _("of the survey sign. Listen to CELEBI.")},
    {_("REPORT THE VISION"), _("Return to ADA in present-day OXFORD."),
     _("Tell her what you saw in the forest."), _("Keep room in ITEMS for her reward.")},
    {_("FOLLOW CELEBI"), _("Return to CELEBI in CHANTILLY FOREST."),
     _("Accept its invitation to visit 1940."), _("You can ask it to bring you home anytime.")},
    {_("MEET ELISE AND EEVEE"), _("In the 1940 refuge, speak to ELISE."),
     _("She is beside the keeper at the north end."), _("Find out what EEVEE needs.")},
    {_("ASK FOR A BLANKET"), _("Speak to the keeper beside ELISE"),
     _("in the 1940 CHANTILLY refuge."), _("Ask for something to keep EEVEE warm.")},
    {_("BRING EEVEE THE BLANKET"), _("Return to ELISE beside the refuge keeper."),
     _("You are carrying the blanket for EEVEE."), _("Speak to her to hand it over.")},
    {_("VISIT THE STATION POST"), _("Speak to the refuge's southeast guide."),
     _("The keeper needs reliable departure news."), _("The guide will take you to the post.")},
    {_("READ THE STATION NOTICE"), _("At the 1940 station post, read the board"),
     _("northeast of the dispatcher."), _("Then ask him to confirm the instructions.")},
    {_("CONFIRM THE INSTRUCTIONS"), _("Speak to the station dispatcher."),
     _("He stands beside the return guide."), _("Check the notice before sharing its news.")},
    {_("TAKE NEWS TO THE REFUGE"), _("Ask the post's guide to return you."),
     _("Tell the refuge keeper the confirmed news."), _("Keep the families and POKEMON together.")},
    {_("TRAVEL TO BEAUVAIS"), _("Visit the station post with the guide."),
     _("Read the board to board the train."), _("ELISE and EEVEE have a place at reception.")},
    {_("CHECK IN AT RECEPTION"), _("Speak to the host at the back of the"),
     _("BEAUVAIS reception room."), _("Help ELISE and EEVEE settle in together.")},
    {_("ASK ABOUT A MESSAGE HOME"), _("Speak to ELISE at BEAUVAIS reception."),
     _("After seeing EEVEE, ask how you can help."), _("The refuge keeper is waiting for news.")},
    {_("DELIVER ELISE'S MESSAGE"), _("Take reception's south return service."),
     _("Ask the post's guide to visit the refuge."), _("Tell the keeper ELISE and EEVEE are safe.")},
    {_("BRING BACK THE REPLY"), _("Take the train to BEAUVAIS again."),
     _("Speak to ELISE at reception."), _("She is waiting for the keeper's reply.")},
    {_("RECORD THE FIRST ACCOUNT"), _("Return through CELEBI to the present."),
     _("Tell ADA in OXFORD about ELISE's journey."), _("Keep room in POKE BALLS for her reward.")},
    {_("HELP AT RECEPTION"), _("Return to BEAUVAIS in 1940."),
     _("Speak to the host at the back of reception."), _("Ask about supplies for a care corner.")},
    {_("COLLECT THE CARE PARCEL"), _("Take reception's south return service."),
     _("Speak to the CHANTILLY post dispatcher."), _("He has the parcel for the BEAUVAIS host.")},
    {_("DELIVER THE CARE PARCEL"), _("Read the post's board to ride to BEAUVAIS."),
     _("Hand the parcel to the reception host."), _("You do not need space in your Bag.")},
    {_("VISIT THE GARDEN"), _("Ask ELISE to visit the BEAUVAIS garden."),
     _("Speak to LUC on its west side."), _("He is looking for his PIDGEY.")},
    {_("FIND LUC'S PIDGEY"), _("Look beside the garden's northeast trees."),
     _("Approach PIDGEY and whistle LUC's tune."), _("You can ask LUC to remind you.")},
    {_("REUNITE LUC AND PIDGEY"), _("Bring PIDGEY to LUC on the garden's west"),
     _("side. It is traveling with you safely."), _("Speak to LUC to reunite them.")},
    {_("TAKE THE ONWARD TRAIN"), _("Speak to the CHANTILLY post dispatcher."),
     _("He can send you onward to AMIENS."), _("The board still offers BEAUVAIS trains.")},
    {_("MEET NORA IN AMIENS"), _("Speak to NORA by the west courtyard path."),
     _("She welcomes people and POKEMON together."), _("The guide and CELEBI wait to the south.")},
    {_("READ THE AMIENS NOTICE"), _("Read the board by the northeast trees"),
     _("in the AMIENS reception courtyard."), _("Then return to NORA on the west path.")},
    {_("CONFIRM THE MEETING POINT"), _("Speak to NORA in the AMIENS courtyard."),
     _("You copied the meeting instructions."), _("Check them with her before moving on.")},
    {_("HELP WITH A REUNION"), _("Ask NORA about MIRA's missing MEOWTH."),
     _("She is on the AMIENS courtyard west path."), _("She needs help comparing two reports.")},
    {_("COLLECT BOTH REPORTS"), _("Speak to MIRA on the north path and"),
     _("the porter on the east side of AMIENS."), _("You can visit them in either order.")},
    {_("SPEAK TO THE PORTER"), _("You recorded MIRA's description."),
     _("Find the porter on the courtyard's east"), _("side, then bring both reports to NORA.")},
    {_("SPEAK TO MIRA"), _("You recorded the porter's description."),
     _("Find MIRA on the courtyard's north path,"), _("then bring both reports to NORA.")},
    {_("CHECK WITH NORA"), _("Both descriptions are recorded."),
     _("Speak to NORA on the west path."), _("She will check the match before moving.")},
    {_("REUNITE MIRA AND MEOWTH"), _("NORA has checked both descriptions."),
     _("Give MIRA the news on the north path."), _("The porter will bring MEOWTH over.")},
    {_("TELL ADA ABOUT AMIENS"), _("Return with CELEBI, then visit ADA in"),
     _("OXFORD to record MIRA and MEOWTH's story."), _("NORA still offers free care in AMIENS.")},
    {_("CHECK THE AMIENS DEPARTURE NEWS"), _("Return through CELEBI and take the AMIENS"),
     _("train. Speak to the porter on the east"), _("side about the latest travel bulletin.")},
    {_("READ THE NEW BULLETIN"), _("Read the northeast notice in AMIENS."),
     _("The porter needs its exact instructions."), _("Bring your notes back to him.")},
    {_("VERIFY THE BULLETIN"), _("You copied the departure instructions."),
     _("Check them with the porter on the east"), _("side before passing them to NORA.")},
    {_("BRING THE NEWS TO NORA"), _("The porter confirmed the waiting plan."),
     _("Tell NORA beside the west path."), _("She will keep the traveling groups ready.")},
    {_("BOARD THE ROUEN TRAIN"), _("Speak to the porter on the east side of"),
     _("AMIENS. The onward service is now ready."), _("NORA and the return guide remain there.")},
    {_("MEET LEON IN ROUEN"), _("Speak to LEON on the west courtyard path."),
     _("He will explain the reception stop."), _("The guide returns you directly to AMIENS.")},
    {_("HELP LEON IN ROUEN"), _("Speak to LEON on the west courtyard path."),
     _("He needs help finding a missing route book."), _("The riverside crossing leads east.")},
    {_("FIND THE ROUTE BOOK"), _("Follow the east path to the crossing."),
     _("Cross to the far bank, then head north."), _("Look for a wrapped book beside the water.")},
    {_("RETURN THE ROUTE BOOK"), _("You have the wrapped route book."),
     _("Bring it to LEON on the west path."), _("The book is carried with your quest notes.")},
    {_("TRAVEL TO LE HAVRE"), _("Speak to the clerk southeast of LEON,"),
     _("near ROUEN's path to the riverside."), _("LEON still offers free party care.")},
    {_("MEET THE LE HAVRE CAPTAIN"), _("Speak to the captain below your arrival."),
     _("He explains the port reception."), _("CELEBI waits beside you on the pier.")},
    {_("HELP THE LE HAVRE DOCKWORKER"), _("Speak to the worker on the upper quay,"),
     _("to the right of the closed entrance."), _("He needs the posted instructions checked.")},
    {_("READ THE DOCK NOTICE"), _("Read the notice on the closed entrance"),
     _("above the LE HAVRE pier."), _("Then check its details with the captain.")},
    {_("CONFIRM WITH THE CAPTAIN"), _("You copied the dock instructions."),
     _("Speak to the captain below your arrival."), _("The return service remains available.")},
    {_("THE FERRY IS READY"), _("The clerk can take you to SOUTHAMPTON."),
     _("You may also visit ADA in OXFORD"), _("to file your notes. This is optional.")},
    {_("SAIL FROM LE HAVRE"), _("Speak to the ferry clerk on the quay,"),
     _("left of the closed entrance."), _("He offers transport to SOUTHAMPTON.")},
    {_("REPORT TO THE RECEPTION HOST"), _("Speak to the host below your arrival"),
     _("at SOUTHAMPTON reception."), _("He can also arrange your return.")},
    {_("HELP THE RECEPTION WORKER"), _("Speak to the worker on the upper quay"),
     _("at SOUTHAMPTON, right of the entrance."), _("A traveler has misplaced a bag.")},
    {_("FIND THE TRAVELER'S BAG"), _("Look on the left side of the upper quay"),
     _("for the bag with a green label."), _("Bring it to the reception worker.")},
    {_("RETURN THE LABELED BAG"), _("Take the bag to the reception worker"),
     _("on the right side of the upper quay."), _("The traveler is waiting for it.")},
    {_("THE LONDON GROUP IS READY"), _("The clerk can take you to LONDON."),
     _("You may also visit ADA in OXFORD"), _("to file your notes. This is optional.")},
    {_("TRAVEL TO LONDON RECEPTION"), _("Speak to the clerk below the care worker"),
     _("on SOUTHAMPTON's upper quay."), _("He offers onward transport to LONDON.")},
    {_("MEET ROSE AT RECEPTION"), _("Speak to ROSE on the courtyard's left"),
     _("to record your arrival in LONDON."), _("The guide and CELEBI offer returns.")},
    {_("LONDON ARRIVAL RECORDED"), _("ROSE welcomes you to the courtyard."),
     _("The guide returns you to SOUTHAMPTON."), _("CELEBI can take you to the present.")}
};

static u8 GetJournalLead(void)
{
    u16 stage = VarGet(VAR_EUROPE_CELEBI_STORY);
    if (stage == 0)
        return FlagGet(FLAG_BADGE03_GET) ? LEAD_ADA : LEAD_BADGE;
    if (stage == 1) return LEAD_FOREST;
    if (stage == 2) return LEAD_VISION;
    stage = VarGet(VAR_EUROPE_PAST_STORY);
    if (stage == 0) return LEAD_PAST;
    if (stage == 1) return LEAD_ELISE;
    if (stage == 2) return LEAD_KEEPER;
    if (stage == 3) return LEAD_BLANKET;
    stage = VarGet(VAR_EUROPE_DEPARTURE_STORY);
    if (stage == 0) return LEAD_GUIDE;
    if (stage == 1) return LEAD_NOTICE;
    if (stage == 2) return LEAD_DISPATCHER;
    if (stage == 3) return LEAD_NEWS;
    stage = VarGet(VAR_EUROPE_EVAC_STORY);
    if (stage == 0) return LEAD_TRAIN;
    if (stage == 1) return LEAD_CHECK_IN;
    stage = VarGet(VAR_EUROPE_MESSAGE_STORY);
    if (stage == 0) return LEAD_MESSAGE;
    if (stage == 1) return LEAD_DELIVER_MESSAGE;
    if (stage == 2) return LEAD_REPLY;
    if (stage == 3) return LEAD_ACCOUNT;
    stage = VarGet(VAR_EUROPE_RELIEF_STORY);
    if (stage == 0) return LEAD_SUPPLIES;
    if (stage == 1) return LEAD_COLLECT_PARCEL;
    if (stage == 2) return LEAD_DELIVER_PARCEL;
    stage = VarGet(VAR_EUROPE_GARDEN_STORY);
    if (stage == 0) return LEAD_GARDEN;
    if (stage == 1) return LEAD_FIND_PIDGEY;
    if (stage == 2) return LEAD_RETURN_PIDGEY;
    stage = VarGet(VAR_EUROPE_AMIENS_STORY);
    if (stage == 0) return LEAD_AMIENS;
    if (stage == 1) return LEAD_NORA;
    if (stage == 2) return LEAD_AMIENS_NOTICE;
    if (stage == 3) return LEAD_AMIENS_REPORT;
    stage = VarGet(VAR_EUROPE_REUNION_STORY);
    if (stage <= 5) return LEAD_REUNION + stage;
    if (!VarGet(VAR_EUROPE_AMIENS_ACCOUNT)) return LEAD_REST;
    stage = VarGet(VAR_EUROPE_AMIENS_NEWS);
    if (stage < 4) return LEAD_AMIENS_ARCHIVED + stage;
    stage = VarGet(VAR_EUROPE_ROUEN_STORY);
    if (stage < 2) return LEAD_AMIENS_WAIT + stage;
    stage = VarGet(VAR_EUROPE_ROUEN_BOOK);
    if (stage < 3) return LEAD_ROUEN_READY + stage;
    stage = VarGet(VAR_EUROPE_LE_HAVRE_STORY);
    if (stage < 2) return LEAD_ROUEN_BOOK_DONE + stage;
    stage = VarGet(VAR_EUROPE_DOCK_CHECK);
    if (stage < 3) return LEAD_LE_HAVRE_READY + stage;
    if (VarGet(VAR_EUROPE_PORT_ACCOUNT) != 1 && !VarGet(VAR_EUROPE_SOUTHAMPTON)) return LEAD_DOCK_DONE;
    stage = VarGet(VAR_EUROPE_SOUTHAMPTON);
    if (stage < 2) return LEAD_PORT_ARCHIVED + stage;
    stage = VarGet(VAR_EUROPE_LUGGAGE);
    if (stage < 3) return LEAD_SOUTHAMPTON_DONE + stage;
    if (VarGet(VAR_EUROPE_SOUTH_ACCOUNT) != 1 && !VarGet(VAR_EUROPE_LONDON_PAST)) return LEAD_LUGGAGE_DONE;
    stage = VarGet(VAR_EUROPE_LONDON_PAST);
    return LEAD_SOUTH_ACCOUNT + (stage > 2 ? 2 : stage);
}

static u32 GetJournalMilestones(void)
{
    return (VarGet(VAR_EUROPE_CELEBI_STORY) >= 3)
        | ((VarGet(VAR_EUROPE_PAST_STORY) >= 4) << 1)
        | ((VarGet(VAR_EUROPE_DEPARTURE_STORY) >= 4) << 2)
        | ((VarGet(VAR_EUROPE_EVAC_STORY) >= 2) << 3)
        | ((VarGet(VAR_EUROPE_MESSAGE_STORY) >= 4) << 4)
        | ((VarGet(VAR_EUROPE_RELIEF_STORY) >= 3) << 5)
        | ((VarGet(VAR_EUROPE_GARDEN_STORY) >= 3) << 6)
        | ((VarGet(VAR_EUROPE_AMIENS_STORY) >= 4) << 7)
        | ((VarGet(VAR_EUROPE_REUNION_STORY) >= 6) << 8)
        | ((VarGet(VAR_EUROPE_AMIENS_ACCOUNT) == 1) << 9)
        | ((VarGet(VAR_EUROPE_AMIENS_NEWS) >= 4) << 10)
        | ((VarGet(VAR_EUROPE_ROUEN_STORY) >= 2) << 11)
        | ((VarGet(VAR_EUROPE_ROUEN_BOOK) >= 3) << 12)
        | ((VarGet(VAR_EUROPE_LE_HAVRE_STORY) >= 2) << 13)
        | ((VarGet(VAR_EUROPE_DOCK_CHECK) >= 3) << 14)
        | ((VarGet(VAR_EUROPE_PORT_ACCOUNT) == 1) << 15)
        | ((VarGet(VAR_EUROPE_SOUTHAMPTON) >= 2) << 16)
        | ((VarGet(VAR_EUROPE_LUGGAGE) >= 3) << 17)
        | ((VarGet(VAR_EUROPE_SOUTH_ACCOUNT) == 1) << 18)
        | ((VarGet(VAR_EUROPE_LONDON_PAST) >= 2) << 19);
}

static void MapText(const u8 *text, u8 x, u8 y, const u8 *colors)
{
    AddTextPrinterParameterized3(0, FONT_SMALL, x, y, colors, 0, text);
}

static void MapRect(u8 color, u8 x, u8 y, u8 w, u8 h)
{
    FillWindowPixelRect(0, PIXEL_FILL(color), x, y, w, h);
}

static void DrawEuropeJournal(u8 taskId)
{
    u8 i;
    u8 lead = gTasks[taskId].data[2];
    u32 milestones = (u16)gTasks[taskId].data[3] | ((u32)(u16)gTasks[taskId].data[6] << 16);
    bool8 records = gTasks[taskId].data[1] == JOURNAL_RECORDS;
    bool8 tour = gTasks[taskId].data[4];
    u8 start = tour ? 0 : gTasks[taskId].data[5] * JOURNAL_RECORDS_PER_PAGE;
    u8 end = tour ? ARRAY_COUNT(gEuropeTourMilestones) : min(start + JOURNAL_RECORDS_PER_PAGE, ARRAY_COUNT(sMilestones));
    const u8 (*leads)[4][44] = tour ? gEuropeTourLeads : sJournalLeads;
    const u8 (*labels)[24] = tour ? gEuropeTourMilestones : sMilestones;
    FillWindowPixelBuffer(0, PIXEL_FILL(1));
    MapText(tour ? (records ? sTourRecordsHeading : sTourHeading) : (records ? sRecordsHeadings[gTasks[taskId].data[5]] : sJournalHeading), 7, 2, sGold);
    MapRect(4, 7, 19, 226, 1);
    if (records)
    {
        for (i = start; i < end; i++)
        {
            bool8 done = (milestones & (1 << i)) != 0;
            MapText(labels[i], 7, 24 + (i - start) * (tour ? 14 : 11), done ? sGold : sWhite);
            MapText(done ? sDone : sNotDone, 201, 24 + (i - start) * (tour ? 14 : 11), done ? sGold : sWhite);
        }
    }
    else
    {
        MapText(leads[lead][0], 7, 29, sGold);
        for (i = 1; i < 4; i++)
            MapText(leads[lead][i], 7, 36 + i * 16, sWhite);
        MapText(tour ? sTourHint : (sEuropeMapPast ? sJournalPastHint : sJournalPresentHint), 7, 110, sWhite);
    }
    MapText(records ? (tour ? sShowLead : sRecordPageControls) : sShowRecords, 7, records && !tour ? 134 : 128, sGold);
    MapText(sJournalControls, 7, 145, sGold);
    PutWindowTilemap(0);
    CopyWindowToVram(0, COPYWIN_FULL);
}

static const u8 *GetEuropeMapLocation(void)
{
    u8 map = gSaveBlock1Ptr->location.mapNum;
    if (!sEuropeMapPast)
        return sLocations[sEuropeMapCurrent];
    if (map == MAP_NUM(MAP_EUROPE_LONDON_PAST))
        return sLondonPastLocation;
    if (map == MAP_NUM(MAP_EUROPE_SOUTHAMPTON_PAST))
        return sSouthamptonLocation;
    if (map == MAP_NUM(MAP_EUROPE_LE_HAVRE_PAST))
        return sLeHavreLocation;
    if (map == MAP_NUM(MAP_EUROPE_ROUEN_PAST))
        return sRouenLocation;
    if (map == MAP_NUM(MAP_EUROPE_AMIENS_PAST))
        return sAmiensLocation;
    if (map == MAP_NUM(MAP_EUROPE_BEAUVAIS_PAST) || map == MAP_NUM(MAP_EUROPE_BEAUVAIS_GARDEN))
        return sBeauvaisLocation;
    return sPastLocation;
}

static void DrawEuropeMap(bool8 info)
{
    u8 i;
    u8 x, y;
    u16 span;
    FillWindowPixelBuffer(0, PIXEL_FILL(1));
    MapText(sEuropeMapPast ? sPastHeading : sHeading, 7, 2, sGold);
    // Projected Natural Earth land and WGS84 city centres. Labels never move the dots.
    MapRect(5, 83, 18, 1, 87);
    for (span = 0; span < ARRAY_COUNT(sLandSpans); span++)
    {
        MapRect(VarGet(VAR_EUROPE_MAP_DETAIL) ? 5 : 4, sLandSpans[span][0], sLandSpans[span][1], sLandSpans[span][2], 1);
        if (VarGet(VAR_EUROPE_MAP_DETAIL) && sLandSpans[span][2] > 2)
            MapRect(4, sLandSpans[span][0] + 1, sLandSpans[span][1], sLandSpans[span][2] - 2, 1);
    }
    for (i = 0; i < ARRAY_COUNT(sCityX); i++)
    {
        MapText(sCityNames[i], 7, 18 + i * 11, i == sEuropeMapSelection ? sGold : sWhite);
        MapRect(2, sCityX[i], sCityY[i], 1, 1);
    }
    x = sCityX[sEuropeMapSelection];
    y = sCityY[sEuropeMapSelection];
    MapRect(3, x - 2, y - 2, 5, 1);
    MapRect(3, x - 2, y + 2, 5, 1);
    MapRect(3, x - 2, y - 1, 1, 3);
    MapRect(3, x + 2, y - 1, 1, 3);
    MapText(sNorthLabel, 225, 18, sWhite);
    MapText(GetEuropeMapLocation(), 7, 111, sWhite);
    MapText(sHelpHint, 163, 111, sGold);
    MapText(sEuropeMapPast ? sPastHint : (info ? (sEuropeMapSelection >= 6 ? sCoastHint : sRailHint) : sDetails[sEuropeMapSelection]), 7, 127, sWhite);
    MapText(sControls, 7, 145, sGold);
    PutWindowTilemap(0);
    CopyWindowToVram(0, COPYWIN_FULL);
}

static void MapVBlank(void)
{
    TransferPlttBuffer();
}

static const u8 sWorldOptionText0[] = _("WORLD OPTIONS");
static const u8 sWorldOptionText1[] = _("MAP DETAIL: SHADED");
static const u8 sWorldOptionText2[] = _("MAP DETAIL: SIMPLE");
static const u8 sWorldOptionText3[] = _("MAP COLORS: HIGH CONTRAST");
static const u8 sWorldOptionText4[] = _("MAP COLORS: NATURAL");
static const u8 sWorldOptionText5[] = _("Cosmetic choices. Your trainer ID stays.");
static const u8 sWorldOptionText6[] = _("Saved with your normal game save.");
static const u8 sWorldOptionText7[] = _("UP/DOWN: ROW  LEFT/RIGHT: CHANGE");
static const u8 sWorldOptionText8[] = _("A: CHANGE  B/START: BACK");

static void DrawWorldOptions(u8 row)
{
    static const u8 sOriginal[] = _("AVATAR: ORIGINAL");
    static const u8 sRed[] = _("AVATAR: RED");
    static const u8 sLeaf[] = _("AVATAR: LEAF");
    u16 style = VarGet(VAR_EUROPE_AVATAR_STYLE);
    FillWindowPixelBuffer(0, PIXEL_FILL(1));
    MapText(sWorldOptionText0, 7, 4, sGold);
    MapRect(4, 7, 20, 226, 1);
    MapText(VarGet(VAR_EUROPE_MAP_DETAIL) ? sWorldOptionText1 : sWorldOptionText2, 12, 32, row == 0 ? sGold : sWhite);
    MapText(style == 1 ? sRed : style == 2 ? sLeaf : sOriginal, 12, 55, row == 1 ? sGold : sWhite);
    MapText(VarGet(VAR_EUROPE_MAP_CONTRAST) ? sWorldOptionText3 : sWorldOptionText4, 12, 78, row == 2 ? sGold : sWhite);
    MapText(sWorldOptionText5, 7, 106, sWhite);
    MapText(sWorldOptionText6, 7, 119, sWhite);
    MapText(sWorldOptionText7, 7, 135, sGold);
    MapText(sWorldOptionText8, 7, 147, sGold);
    PutWindowTilemap(0);
    CopyWindowToVram(0, COPYWIN_FULL);
}

static void Task_EuropeMap(u8 taskId)
{
    if (gPaletteFade.active)
        return;
    if (gTasks[taskId].data[0])
    {
        SetVBlankCallback(NULL);
        FreeAllWindowBuffers();
        DestroyTask(taskId);
        SetMainCallback2(sEuropeMapReturn);
    }
    else if (JOY_NEW(B_BUTTON | START_BUTTON))
    {
        PlaySE(SE_SELECT);
        BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
        gTasks[taskId].data[0] = 1;
    }
    else if (sWorldOptions)
    {
        u8 row = gTasks[taskId].data[1];
        if (JOY_NEW(DPAD_UP | DPAD_DOWN))
        {
            row = (row + (JOY_NEW(DPAD_UP) ? 2 : 1)) % 3;
            gTasks[taskId].data[1] = row;
            PlaySE(SE_SELECT);
            DrawWorldOptions(row);
        }
        else if (JOY_NEW(A_BUTTON | DPAD_LEFT | DPAD_RIGHT))
        {
            u16 var = row == 0 ? VAR_EUROPE_MAP_DETAIL : row == 1 ? VAR_EUROPE_AVATAR_STYLE : VAR_EUROPE_MAP_CONTRAST;
            u8 count = row == 1 ? 3 : 2;
            VarSet(var, (VarGet(var) + (JOY_NEW(DPAD_LEFT) ? count - 1 : 1)) % count);
            PlaySE(SE_SELECT);
            DrawWorldOptions(row);
        }
    }
    else if (JOY_NEW(SELECT_BUTTON))
    {
        PlaySE(SE_SELECT);
        if (gTasks[taskId].data[1] != JOURNAL_MAP)
        {
            gTasks[taskId].data[1] = JOURNAL_MAP;
            DrawEuropeMap(FALSE);
        }
        else
        {
            gTasks[taskId].data[1] = JOURNAL_LEAD;
            gTasks[taskId].data[4] = 0;
            gTasks[taskId].data[5] = 0;
            gTasks[taskId].data[2] = GetJournalLead();
            gTasks[taskId].data[3] = GetJournalMilestones();
            gTasks[taskId].data[6] = GetJournalMilestones() >> 16;
            DrawEuropeJournal(taskId);
        }
    }
    else if (gTasks[taskId].data[1] != JOURNAL_MAP)
    {
        if (JOY_NEW(DPAD_UP | DPAD_DOWN))
        {
            bool8 tour = !gTasks[taskId].data[4];
            PlaySE(SE_SELECT);
            gTasks[taskId].data[4] = tour;
            gTasks[taskId].data[5] = 0;
            gTasks[taskId].data[2] = tour ? GetEuropeTourLead() : GetJournalLead();
            gTasks[taskId].data[3] = tour ? GetEuropeTourMilestones() : GetJournalMilestones();
            gTasks[taskId].data[6] = tour ? 0 : GetJournalMilestones() >> 16;
            DrawEuropeJournal(taskId);
        }
        else if (gTasks[taskId].data[1] == JOURNAL_RECORDS && !gTasks[taskId].data[4]
            && JOY_NEW(DPAD_LEFT | DPAD_RIGHT))
        {
            PlaySE(SE_SELECT);
            gTasks[taskId].data[5] ^= 1;
            DrawEuropeJournal(taskId);
        }
        else if (JOY_NEW(A_BUTTON))
        {
            PlaySE(SE_SELECT);
            gTasks[taskId].data[1] = gTasks[taskId].data[1] == JOURNAL_LEAD ? JOURNAL_RECORDS : JOURNAL_LEAD;
            DrawEuropeJournal(taskId);
        }
    }
    else if (JOY_NEW(DPAD_LEFT | DPAD_UP | DPAD_RIGHT | DPAD_DOWN))
    {
        if (JOY_NEW(DPAD_LEFT | DPAD_UP))
            sEuropeMapSelection = (sEuropeMapSelection + ARRAY_COUNT(sCityX) - 1) % ARRAY_COUNT(sCityX);
        else
            sEuropeMapSelection = (sEuropeMapSelection + 1) % ARRAY_COUNT(sCityX);
        PlaySE(SE_SELECT);
        DrawEuropeMap(FALSE);
    }
    else if (JOY_NEW(A_BUTTON))
    {
        PlaySE(SE_SELECT);
        DrawEuropeMap(TRUE);
    }
}

static void CB2_EuropeMap(void)
{
    RunTasks();
    UpdatePaletteFade();
}

static void CB2_InitEuropeMap(void)
{
    SetVBlankCallback(NULL);
    SetHBlankCallback(NULL);
    ScanlineEffect_Stop();
    SetGpuReg(REG_OFFSET_DISPCNT, 0);
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    SetGpuReg(REG_OFFSET_BLDALPHA, 0);
    SetGpuReg(REG_OFFSET_BLDY, 0);
    ResetTasks();
    ResetSpriteData();
    FreeAllSpritePalettes();
    ResetPaletteFade();
    DmaClearLarge16(3, (void *)VRAM, VRAM_SIZE, 0x1000);
    ResetBgsAndClearDma3BusyFlags(FALSE);
    InitBgsFromTemplates(0, sMapBg, ARRAY_COUNT(sMapBg));
    ChangeBgX(0, 0, 0);
    ChangeBgY(0, 0, 0);
    InitWindows(sMapWindows);
    DeactivateAllTextPrinters();
    LoadPalette(sMapPalette, 0, sizeof(sMapPalette));
    if (VarGet(VAR_EUROPE_MAP_CONTRAST) && !sWorldOptions)
    {
        const u16 land = RGB(18, 23, 19);
        const u16 coast = RGB(27, 30, 25);
        LoadPalette(&land, 4, 2);
        LoadPalette(&coast, 5, 2);
    }
    if (sWorldOptions) DrawWorldOptions(0);
    else DrawEuropeMap(FALSE);
    ShowBg(0);
    BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
    CreateTask(Task_EuropeMap, 0);
    SetVBlankCallback(MapVBlank);
    SetMainCallback2(CB2_EuropeMap);
}

void OpenEuropeMap(MainCallback callback)
{
    sWorldOptions = FALSE;
    sEuropeMapReturn = callback;
    sEuropeMapPast = gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_EUROPE_CHANTILLY_PAST)
        && (gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_EUROPE_CHANTILLY_PAST)
            || gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_EUROPE_CHANTILLY_PAST_POST)
            || gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_EUROPE_BEAUVAIS_PAST)
            || gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_EUROPE_BEAUVAIS_GARDEN)
            || gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_EUROPE_AMIENS_PAST)
            || gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_EUROPE_ROUEN_PAST)
            || gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_EUROPE_LE_HAVRE_PAST)
            || gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_EUROPE_SOUTHAMPTON_PAST)
            || gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_EUROPE_LONDON_PAST));
    // Use map identities, so adding another town cannot mislabel its country.
    switch (gSaveBlock1Ptr->location.mapNum)
    {
    case MAP_NUM(MAP_EUROPE_LONDON_PAST):
    case MAP_NUM(MAP_EUROPE_SOUTHAMPTON_PAST):
        sEuropeMapCurrent = 0;
        break;
    case MAP_NUM(MAP_EUROPE_PARIS):
    case MAP_NUM(MAP_EUROPE_NOTREDAME):
    case MAP_NUM(MAP_EUROPE_PARIS_COUNTRYSIDE):
    case MAP_NUM(MAP_EUROPE_PARIS_STATION):
    case MAP_NUM(MAP_EUROPE_PARIS_CENTER):
        sEuropeMapCurrent = 1;
        break;
    case MAP_NUM(MAP_EUROPE_BERLIN):
    case MAP_NUM(MAP_EUROPE_REICHSTAG):
    case MAP_NUM(MAP_EUROPE_BERLIN_COUNTRYSIDE):
    case MAP_NUM(MAP_EUROPE_BERLIN_STATION):
    case MAP_NUM(MAP_EUROPE_BERLIN_CENTER):
        sEuropeMapCurrent = 2;
        break;
    case MAP_NUM(MAP_EUROPE_OXFORD):
    case MAP_NUM(MAP_EUROPE_OXFORD_TRAIL):
    case MAP_NUM(MAP_EUROPE_OXFORD_STATION):
    case MAP_NUM(MAP_EUROPE_OXFORD_CENTER):
    case MAP_NUM(MAP_EUROPE_OXFORD_GYM):
        sEuropeMapCurrent = 3;
        break;
    case MAP_NUM(MAP_EUROPE_CHANTILLY):
    case MAP_NUM(MAP_EUROPE_CHANTILLY_TRAIL):
    case MAP_NUM(MAP_EUROPE_CHANTILLY_STATION):
    case MAP_NUM(MAP_EUROPE_CHANTILLY_CENTER):
    case MAP_NUM(MAP_EUROPE_CHANTILLY_GYM):
    case MAP_NUM(MAP_EUROPE_CHANTILLY_PAST):
    case MAP_NUM(MAP_EUROPE_CHANTILLY_PAST_POST):
    case MAP_NUM(MAP_EUROPE_BEAUVAIS_PAST):
    case MAP_NUM(MAP_EUROPE_BEAUVAIS_GARDEN):
    case MAP_NUM(MAP_EUROPE_AMIENS_PAST):
    case MAP_NUM(MAP_EUROPE_ROUEN_PAST):
    case MAP_NUM(MAP_EUROPE_LE_HAVRE_PAST):
        sEuropeMapCurrent = 4;
        break;
    case MAP_NUM(MAP_EUROPE_ORANIENBURG):
    case MAP_NUM(MAP_EUROPE_ORANIENBURG_TRAIL):
    case MAP_NUM(MAP_EUROPE_ORANIENBURG_STATION):
    case MAP_NUM(MAP_EUROPE_ORANIENBURG_CENTER):
    case MAP_NUM(MAP_EUROPE_ORANIENBURG_GYM):
        sEuropeMapCurrent = 5;
        break;
    case MAP_NUM(MAP_EUROPE_DOVER_PORT):
        sEuropeMapCurrent = 6;
        break;
    case MAP_NUM(MAP_EUROPE_CALAIS_PORT):
        sEuropeMapCurrent = 7;
        break;
    default:
        sEuropeMapCurrent = 0;
        break;
    }
    sEuropeMapSelection = sEuropeMapCurrent;
    // Defer resetting tasks until the caller has finished its cleanup.
    SetMainCallback2(CB2_InitEuropeMap);
}

void OpenEuropeWorldOptions(MainCallback callback)
{
    sWorldOptions = TRUE;
    sEuropeMapReturn = callback;
    SetMainCallback2(CB2_InitEuropeMap);
}
