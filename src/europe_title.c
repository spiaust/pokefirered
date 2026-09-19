#include "global.h"
#include "gflib.h"
#include "task.h"
#include "menu.h"
#include "m4a.h"
#include "load_save.h"
#include "new_game.h"
#include "save.h"
#include "main_menu.h"
#include "clear_save_data_screen.h"
#include "constants/songs.h"

// Rendered with native GBA tiles and fonts: no large bitmap or new art tools.
static const struct BgTemplate sEuropeTitleBg[] = {
    {.bg = 0, .charBaseIndex = 0, .mapBaseIndex = 31, .priority = 0}
};
static const struct WindowTemplate sEuropeTitleWindows[] = {
    {.bg = 0, .width = 30, .height = 20, .paletteNum = 0, .baseBlock = 1},
    DUMMY_WIN_TEMPLATE
};
static const u16 sEuropeTitlePalette[] = {
    RGB(2, 5, 12), RGB(2, 5, 12), RGB(29, 30, 27), RGB(31, 24, 8),
    RGB(9, 20, 22), RGB(4, 10, 18), RGB(18, 25, 26), RGB(0, 0, 0)
};
static const u8 sEuropeTitleColors[] = {1, 2, 1};
static const u8 sEuropeTitleGold[] = {1, 3, 1};
static const u8 sPokemon[] = _("POKéMON");
static const u8 sEuropeanTour[] = _("EUROPEAN TOUR");
static const u8 sTagline[] = _("Three countries. Your adventure.");
static const u8 sLondon[] = _("LONDON");
static const u8 sParis[] = _("PARIS");
static const u8 sBerlin[] = _("BERLIN");
static const u8 sPressStart[] = _("PRESS START");

static void EuropeTitleVBlank(void)
{
    TransferPlttBuffer();
}

static void EuropeTitleText(const u8 *text, u16 center, u16 y, const u8 *colors)
{
    u16 width = GetStringWidth(FONT_NORMAL, text, 0);
    AddTextPrinterParameterized3(0, FONT_NORMAL, center - width / 2, y, colors, 0, text);
}

static void EuropeTitleDraw(void)
{
    u16 x;
    FillWindowPixelBuffer(0, PIXEL_FILL(1));
    FillWindowPixelRect(0, PIXEL_FILL(3), 16, 8, 208, 1);
    EuropeTitleText(sPokemon, 120, 15, sEuropeTitleGold);
    EuropeTitleText(sEuropeanTour, 120, 34, sEuropeTitleColors);
    EuropeTitleText(sTagline, 120, 53, sEuropeTitleColors);
    // Stylized clock tower, Paris tower, and Brandenburg Gate.
    FillWindowPixelRect(0, PIXEL_FILL(4), 18, 91, 41, 9);
    FillWindowPixelRect(0, PIXEL_FILL(2), 32, 78, 12, 22);
    FillWindowPixelRect(0, PIXEL_FILL(3), 35, 71, 6, 7);
    FillWindowPixelRect(0, PIXEL_FILL(1), 36, 81, 4, 4);
    for (x = 0; x < 20; x++)
        FillWindowPixelRect(0, PIXEL_FILL(4), 120 - x / 2, 79 + x, 1 + x, 1);
    FillWindowPixelRect(0, PIXEL_FILL(3), 119, 72, 3, 14);
    FillWindowPixelRect(0, PIXEL_FILL(1), 117, 92, 7, 7);
    FillWindowPixelRect(0, PIXEL_FILL(2), 181, 82, 39, 5);
    FillWindowPixelRect(0, PIXEL_FILL(3), 193, 76, 15, 5);
    for (x = 183; x < 221; x += 7)
        FillWindowPixelRect(0, PIXEL_FILL(4), x, 88, 3, 12);
    FillWindowPixelRect(0, PIXEL_FILL(3), 38, 107, 164, 2);
    for (x = 38; x <= 202; x += 82)
    {
        FillWindowPixelRect(0, PIXEL_FILL(3), x - 3, 104, 7, 7);
        FillWindowPixelRect(0, PIXEL_FILL(1), x - 1, 106, 3, 3);
    }
    EuropeTitleText(sLondon, 38, 114, sEuropeTitleColors);
    EuropeTitleText(sParis, 120, 114, sEuropeTitleColors);
    EuropeTitleText(sBerlin, 202, 114, sEuropeTitleColors);
    EuropeTitleText(sPressStart, 120, 139, sEuropeTitleGold);
    PutWindowTilemap(0);
    CopyWindowToVram(0, COPYWIN_FULL);
}

static void Task_EuropeTitle(u8 taskId)
{
    s16 *data = gTasks[taskId].data;
    if (gPaletteFade.active)
        return;
    if (data[0] == 0)
    {
        if (JOY_HELD(B_BUTTON | SELECT_BUTTON | DPAD_UP) == (B_BUTTON | SELECT_BUTTON | DPAD_UP))
            data[1] = 1;
        else if (!JOY_NEW(A_BUTTON | START_BUTTON))
            return;
        PlaySE(SE_SELECT);
        FadeOutBGM(4);
        BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
        data[0] = 1;
    }
    else
    {
        bool8 clearSave = data[1];
        SetVBlankCallback(NULL);
        FreeAllWindowBuffers();
        DestroyTask(taskId);
        SeedRngAndSetTrainerId();
        SetSaveBlocksPointers();
        ResetMenuAndMonGlobals();
        Save_ResetSaveCounters();
        LoadGameSave(SAVE_NORMAL);
        if (gSaveFileStatus == SAVE_STATUS_EMPTY || gSaveFileStatus == SAVE_STATUS_INVALID)
            Sav2_ClearSetDefault();
        SetPokemonCryStereo(gSaveBlock2Ptr->optionsSound);
        InitHeap(gHeap, HEAP_SIZE);
        SetMainCallback2(clearSave ? CB2_SaveClearScreen_Init : CB2_InitMainMenu);
    }
}

static void CB2_EuropeTitle(void)
{
    RunTasks();
    UpdatePaletteFade();
}

void CB2_InitTitleScreen(void)
{
    SetVBlankCallback(NULL);
    SetGpuReg(REG_OFFSET_DISPCNT, 0);
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    SetGpuReg(REG_OFFSET_BLDALPHA, 0);
    SetGpuReg(REG_OFFSET_BLDY, 0);
    StartTimer1();
    InitHeap(gHeap, HEAP_SIZE);
    ResetTasks();
    ResetSpriteData();
    FreeAllSpritePalettes();
    ResetPaletteFade();
    DmaClearLarge16(3, (void *)VRAM, VRAM_SIZE, 0x1000);
    ResetBgsAndClearDma3BusyFlags(FALSE);
    InitBgsFromTemplates(0, sEuropeTitleBg, ARRAY_COUNT(sEuropeTitleBg));
    ChangeBgX(0, 0, 0);
    ChangeBgY(0, 0, 0);
    InitWindows(sEuropeTitleWindows);
    DeactivateAllTextPrinters();
    LoadPalette(sEuropeTitlePalette, 0, sizeof(sEuropeTitlePalette));
    EuropeTitleDraw();
    ShowBg(0);
    BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
    CreateTask(Task_EuropeTitle, 0);
    SetVBlankCallback(EuropeTitleVBlank);
    SetMainCallback2(CB2_EuropeTitle);
    m4aSongNumStart(MUS_TITLE);
}
