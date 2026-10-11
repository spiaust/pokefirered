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
static const u16 sTitlePalette[] = INCBIN_U16("graphics/eclipse_title/artwork.gbapal");
static const u8 sTitleArtwork[] = INCBIN_U8("graphics/eclipse_title/artwork.4bpp");
static const u8 sWhite[] = {0, 2, 1};
static const u8 sGreen[] = {0, 8, 1};
static const u8 sTagline[] = _("Eight badges. One broken timeline.");
static const u8 sStart[] = _("PRESS START");

static void Text(const u8 *str, u8 y, const u8 *colors)
{
    u16 width = GetStringWidth(FONT_SMALL, str, 0);
    AddTextPrinterParameterized4(0, FONT_SMALL, (240 - width) / 2, y, 0, 0, colors, TEXT_SKIP_DRAW, str);
}

static void DrawLights(void)
{
    // Restore the artwork before blinking; no opaque boxes over the river.
    CopyToWindowPixelBuffer(0, sTitleArtwork, sizeof(sTitleArtwork), 0);
    Text(sTagline, 128, sGreen);
    if ((sEuropeTitleFrame / 32) % 3 != 2) Text(sStart, 144, sWhite);
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
    sEuropeTitleFrame = 0; sEuropeTitleExit = 0;
    DrawLights();
    PutWindowTilemap(0); CopyWindowToVram(0, COPYWIN_FULL);
    sEuropeTitleMon = CreateMonPicSprite_HandleDeoxys(SPECIES_CELEBI, 0, 0x8000, TRUE, 43, 101, 0, 0xFFFF);
    if (sEuropeTitleMon < MAX_SPRITES) gSprites[sEuropeTitleMon].oam.priority = 0;
    ShowBg(0);
    SetGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_OBJ_ON | DISPCNT_OBJ_1D_MAP);
    BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
    m4aSongNumStart(MUS_EUROPE_TITLE);
    SetVBlankCallback(TitleVBlank);
    SetMainCallback2(CB2_EuropeTitleRun);
}
