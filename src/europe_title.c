#include "global.h"
#include "gflib.h"
#include "new_menu_helpers.h"
#include "menu.h"
#include "task.h"
#include "main.h"
#include "m4a.h"
#include "scanline_effect.h"
#include "trainer_pokemon_sprites.h"
#include "trig.h"
#include "help_system.h"
#include "load_save.h"
#include "save.h"
#include "new_game.h"
#include "main_menu.h"
#include "clear_save_data_screen.h"
#include "berry_fix_program.h"
#include "constants/songs.h"
#include "constants/species.h"

static EWRAM_DATA u16 sEuropeTitleFrame = 0;
static EWRAM_DATA u8 sEuropeTitleMon = MAX_SPRITES;
static EWRAM_DATA u8 sEuropeTitleExit = 0;
static const struct BgTemplate sTitleBg[] = {
    {.bg = 0, .charBaseIndex = 0, .mapBaseIndex = 31, .priority = 1}
};
static const struct WindowTemplate sTitleWindows[] = {
    {.bg = 0, .width = 30, .height = 20, .paletteNum = 0, .baseBlock = 1},
    DUMMY_WIN_TEMPLATE
};
static const u16 sTitlePalette[] = {
    RGB(2, 4, 10), RGB(2, 4, 10), RGB(29, 30, 27), RGB(31, 25, 12),
    RGB(7, 12, 20), RGB(11, 19, 24), RGB(5, 8, 15), RGB(12, 24, 18),
    RGB(20, 29, 23), RGB(6, 13, 22), RGB(16, 18, 23), RGB(24, 20, 15)
};
static const u8 sWhite[] = {1, 2, 1};
static const u8 sGold[] = {1, 3, 1};
static const u8 sGreen[] = {1, 8, 1};
static const u8 sTitle[] = _("POKEMON");
static const u8 sSubtitle[] = _("EUROPEAN TOUR");
static const u8 sTagline[] = _("A journey through places and time");
static const u8 sStart[] = _("PRESS START");
static const u8 sLondon[] = _("LONDON / THAMES LANTERNS");
static const u8 sParis[] = _("PARIS / GARDEN WALTZ");
static const u8 sBerlin[] = _("BERLIN / LINDEN STEPS");
static const u8 sOxford[] = _("OXFORD / RIVER SCHOLARS");
static const u8 sChantilly[] = _("CHANTILLY / FOREST PORCELAIN");
static const u8 sOranienburg[] = _("ORANIENBURG / HAVEL REFLECTIONS");
static const u8 *const sTownCaptions[] = {sLondon, sParis, sBerlin, sOxford, sChantilly, sOranienburg};

static void Rect(u8 color, u16 x, u16 y, u16 w, u16 h)
{
    FillWindowPixelRect(0, PIXEL_FILL(color), x, y, w, h);
}

static void Text(const u8 *str, u8 y, const u8 *colors)
{
    u16 width = GetStringWidth(FONT_NORMAL, str, 0);
    AddTextPrinterParameterized4(0, FONT_NORMAL, (240 - width) / 2, y, 0, 0, colors, TEXT_SKIP_DRAW, str);
}

// Small native pixel silhouettes, drawn directly into a 4bpp GBA window.
static void DrawTown(u8 town)
{
    u16 x, y, i;
    Rect(1, 0, 91, 240, 69);
    Rect(9, 0, 124, 240, 15);
    Rect(5, 0, 128, 240, 1);
    Rect(4, 0, 139, 240, 2);
    for (i = 0; i < 12; i++)
    {
        x = i * 21;
        y = 112 + (i % 3) * 3;
        Rect(6, x, y, 16, 124 - y);
        Rect(3, x + 4, y + 4, 2, 2);
        Rect(3, x + 10, y + 4, 2, 2);
    }
    if (town == 0) // Clock tower and Westminster bridge.
    {
        Rect(10, 48, 96, 12, 28); Rect(11, 51, 88, 6, 8);
        Rect(3, 52, 99, 4, 4); Rect(10, 30, 112, 55, 12);
        Rect(10, 106, 120, 79, 4);
        for (i = 0; i < 4; i++) Rect(10, 112 + i * 20, 124, 4, 12);
    }
    else if (town == 1) // Eiffel tower with open arch.
    {
        for (i = 0; i < 36; i++)
        {
            x = 173 - i / 3;
            Rect(10, x, 88 + i, 2, 1);
            Rect(10, 346 - x, 88 + i, 2, 1);
        }
        Rect(3, 172, 84, 3, 4); Rect(10, 163, 106, 22, 2); Rect(10, 160, 115, 28, 2);
    }
    else if (town == 2) // Brandenburg gate.
    {
        Rect(10, 132, 101, 61, 7); Rect(11, 142, 97, 41, 4);
        for (i = 0; i < 6; i++) Rect(10, 138 + i * 9, 108, 4, 16);
        Rect(10, 158, 91, 10, 6);
    }
    else if (town == 3) // Oxford college towers.
    {
        Rect(10, 139, 107, 53, 17);
        for (i = 0; i < 3; i++)
        {
            Rect(10, 136 + i * 24, 97, 11, 27);
            Rect(11, 139 + i * 24, 92, 5, 5);
            Rect(3, 140 + i * 24, 102, 3, 5);
        }
    }
    else if (town == 4) // Chantilly chateau above the water.
    {
        Rect(11, 127, 110, 71, 14);
        for (i = 0; i < 4; i++)
        {
            Rect(10, 127 + i * 21, 99, 8, 25);
            Rect(5, 129 + i * 21, 93, 4, 6);
        }
        Rect(3, 153, 114, 17, 10);
    }
    else // Oranienburg palace and the Havel.
    {
        Rect(11, 124, 108, 83, 16); Rect(10, 151, 100, 29, 8);
        Rect(5, 156, 94, 19, 6);
        for (i = 0; i < 8; i++) Rect(3, 128 + i * 10, 113, 3, 5);
    }
    Text(sTownCaptions[town], 140, sGold);
}

static void DrawLights(void)
{
    u8 i;
    for (i = 0; i < 14; i++)
    {
        u16 x = 9 + (i * 37) % 222;
        u16 y = 49 + (i * 13) % 38;
        Rect(((sEuropeTitleFrame / 16 + i) % 4 == 0) ? 8 : 4, x, y, 2, 2);
    }
    Rect(1, 71, 75, 102, 16);
    if ((sEuropeTitleFrame / 32) % 3 != 2) Text(sStart, 75, sWhite);
    CopyWindowToVram(0, COPYWIN_GFX);
}

static void TitleVBlank(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void FinishTitle(void)
{
    SetVBlankCallback(NULL);
    if (sEuropeTitleMon < MAX_SPRITES) FreeAndDestroyMonPicSprite(sEuropeTitleMon);
    sEuropeTitleMon = MAX_SPRITES;
    FreeAllWindowBuffers();
    if (sEuropeTitleExit == 2)
        SetMainCallback2(CB2_SaveClearScreen_Init);
    else if (sEuropeTitleExit == 3)
        SetMainCallback2(CB2_InitBerryFixProgram);
    else
    {
        SeedRngAndSetTrainerId();
        SetSaveBlocksPointers();
        ResetMenuAndMonGlobals();
        Save_ResetSaveCounters();
        LoadGameSave(SAVE_NORMAL);
        if (gSaveFileStatus == SAVE_STATUS_EMPTY || gSaveFileStatus == SAVE_STATUS_INVALID)
            Sav2_ClearSetDefault();
        SetPokemonCryStereo(gSaveBlock2Ptr->optionsSound);
        InitHeap(gHeap, HEAP_SIZE);
        SetMainCallback2(CB2_InitMainMenu);
    }
}

static void CB2_EuropeTitleRun(void)
{
    if (sEuropeTitleExit)
    {
        if (!gPaletteFade.active) { FinishTitle(); return; }
    }
    else
    {
        sEuropeTitleFrame++;
        if (sEuropeTitleFrame % 240 == 0) DrawTown((sEuropeTitleFrame / 240) % 6);
        if (sEuropeTitleFrame % 16 == 0) DrawLights();
        if (sEuropeTitleMon < MAX_SPRITES)
        {
            gSprites[sEuropeTitleMon].x2 = Sin(sEuropeTitleFrame & 255, 6);
            gSprites[sEuropeTitleMon].y2 = Cos((sEuropeTitleFrame * 2) & 255, 4);
        }
        if (!gPaletteFade.active)
        {
            if (JOY_HELD(B_BUTTON | SELECT_BUTTON | DPAD_UP) == (B_BUTTON | SELECT_BUTTON | DPAD_UP))
                sEuropeTitleExit = 2;
            else if (JOY_HELD(B_BUTTON | SELECT_BUTTON) == (B_BUTTON | SELECT_BUTTON))
                sEuropeTitleExit = 3;
            else if (JOY_NEW(A_BUTTON | START_BUTTON))
                sEuropeTitleExit = 1;
            if (sEuropeTitleExit)
            {
                if (sEuropeTitleExit == 1) PlayCry_Normal(SPECIES_CELEBI, 0);
                FadeOutBGM(4);
                BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
            }
        }
    }
    RunTasks();
    AnimateSprites();
    BuildOamBuffer();
    UpdatePaletteFade();
}

void CB2_InitTitleScreen(void)
{
    SetVBlankCallback(NULL);
    StartTimer1();
    InitHeap(gHeap, HEAP_SIZE);
    ResetTasks();
    ResetSpriteData();
    FreeAllSpritePalettes();
    ResetPaletteFade();
    ScanlineEffect_Stop();
    HelpSystem_Disable();
    SetGpuReg(REG_OFFSET_DISPCNT, 0);
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    SetGpuReg(REG_OFFSET_BLDALPHA, 0);
    SetGpuReg(REG_OFFSET_BLDY, 0);
    DmaFill16(3, 0, (void *)VRAM, VRAM_SIZE);
    DmaFill32(3, 0, (void *)OAM, OAM_SIZE);
    ResetBgsAndClearDma3BusyFlags(FALSE);
    InitBgsFromTemplates(0, sTitleBg, ARRAY_COUNT(sTitleBg));
    ChangeBgX(0, 0, 0); ChangeBgY(0, 0, 0);
    InitWindows(sTitleWindows);
    DeactivateAllTextPrinters();
    LoadPalette(sTitlePalette, 0, sizeof(sTitlePalette));
    FillWindowPixelBuffer(0, PIXEL_FILL(1));
    Text(sTitle, 2, sGold);
    Text(sSubtitle, 17, sWhite);
    Text(sTagline, 34, sGreen);
    sEuropeTitleFrame = 0; sEuropeTitleExit = 0;
    DrawTown(0); DrawLights();
    PutWindowTilemap(0); CopyWindowToVram(0, COPYWIN_FULL);
    sEuropeTitleMon = CreateMonPicSprite_HandleDeoxys(SPECIES_CELEBI, 0, 0x8000, TRUE, 37, 73, 0, 0xFFFF);
    if (sEuropeTitleMon < MAX_SPRITES) gSprites[sEuropeTitleMon].oam.priority = 0;
    ShowBg(0);
    SetGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_OBJ_ON | DISPCNT_OBJ_1D_MAP);
    BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
    m4aSongNumStart(MUS_EUROPE_TITLE);
    SetVBlankCallback(TitleVBlank);
    SetMainCallback2(CB2_EuropeTitleRun);
}
