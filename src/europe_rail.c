#include "global.h"
#include "event_data.h"
#include "string_util.h"
#include "constants/vars.h"

// Local branches join a London--Paris--Berlin main line.
// Rows are origins, columns are final destinations; values are next stops.
static const u8 sNextStop[6][6] = {
    {0, 1, 1, 3, 1, 1},
    {0, 1, 2, 0, 4, 2},
    {1, 1, 2, 1, 1, 5},
    {0, 0, 0, 3, 0, 0},
    {1, 1, 1, 1, 4, 1},
    {2, 2, 2, 2, 2, 5}
};
static const u8 sLondon[] = _("LONDON");
static const u8 sParis[] = _("PARIS");
static const u8 sBerlin[] = _("BERLIN");
static const u8 sOxford[] = _("OXFORD");
static const u8 sChantilly[] = _("CHANTILLY");
static const u8 sOranienburg[] = _("ORANIENBURG");
static const u8 *const sStops[] = {sLondon, sParis, sBerlin, sOxford, sChantilly, sOranienburg};

void EuropeRail_LoadJourney(void)
{
    u16 booking = VarGet(VAR_EUROPE_RAIL_DESTINATION);
    gSpecialVar_Result = FALSE;
    if (booking >= 1 && booking <= ARRAY_COUNT(sStops))
    {
        gSpecialVar_0x8005 = booking - 1;
        gSpecialVar_Result = TRUE;
    }
    else
    {
        // Unused/invalid data from an older save cannot become a route index.
        VarSet(VAR_EUROPE_RAIL_DESTINATION, 0);
    }
}

void EuropeRail_PrepareJourney(void)
{
    u16 origin = gSpecialVar_0x8004;
    u16 destination = gSpecialVar_0x8005;
    u8 cursor;
    u8 legs = 0;
    gSpecialVar_Result = 0xFFFF;
    if (origin >= ARRAY_COUNT(sStops) || destination >= ARRAY_COUNT(sStops))
        return;
    cursor = origin;
    while (cursor != destination && legs < ARRAY_COUNT(sStops))
    {
        cursor = sNextStop[cursor][destination];
        legs++;
    }
    if (cursor != destination)
        return;
    gSpecialVar_Result = sNextStop[origin][destination];
    StringCopy(gStringVar1, sStops[destination]);
    StringCopy(gStringVar2, sStops[gSpecialVar_Result]);
    ConvertIntToDecimalStringN(gStringVar3, legs, STR_CONV_MODE_LEFT_ALIGN, 1);
}
