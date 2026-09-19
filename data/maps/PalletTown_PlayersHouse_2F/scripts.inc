PalletTown_PlayersHouse_2F_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Europe_CountrySelection_OnFrame
	map_script MAP_SCRIPT_ON_TRANSITION, PalletTown_PlayersHouse_2F_OnTransition
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, PalletTown_PlayersHouse_2F_OnWarp
	.byte 0

Europe_CountrySelection_OnFrame::
	map_script_2 VAR_EUROPE_HOME_COUNTRY, 0, Europe_ChooseCountry
	.2byte 0

Europe_ChooseCountry::
	lockall
	msgbox Europe_Text_ChooseCountry, MSGBOX_DEFAULT
	multichoice 17, 2, MULTICHOICE_EUROPE_COUNTRY, TRUE
	copyvar VAR_EUROPE_HOME_COUNTRY, VAR_RESULT
	addvar VAR_EUROPE_HOME_COUNTRY, 1
	goto_if_eq VAR_EUROPE_HOME_COUNTRY, 1, Europe_StartEngland
	goto_if_eq VAR_EUROPE_HOME_COUNTRY, 2, Europe_StartFrance
	goto Europe_StartGermany

Europe_StartEngland::
	msgbox Europe_Text_EnglandStarters
	multichoice 5, 2, MULTICHOICE_EUROPE_STARTER_ENGLAND, FALSE
	goto_if_eq VAR_RESULT, 127, Europe_ChooseCountryAgain
	goto_if_eq VAR_RESULT, 0, Europe_PreviewBulbasaur
	goto_if_eq VAR_RESULT, 1, Europe_PreviewCyndaquil
	setvar VAR_0x8004, SPECIES_TOTODILE
	goto Europe_PreviewStarter

Europe_StartFrance::
	msgbox Europe_Text_FranceStarters
	multichoice 5, 2, MULTICHOICE_EUROPE_STARTER_FRANCE, FALSE
	goto_if_eq VAR_RESULT, 127, Europe_ChooseCountryAgain
	goto_if_eq VAR_RESULT, 0, Europe_PreviewChikorita
	goto_if_eq VAR_RESULT, 1, Europe_PreviewTorchic
	setvar VAR_0x8004, SPECIES_SQUIRTLE
	goto Europe_PreviewStarter

Europe_StartGermany::
	msgbox Europe_Text_GermanyStarters
	multichoice 5, 2, MULTICHOICE_EUROPE_STARTER_GERMANY, FALSE
	goto_if_eq VAR_RESULT, 127, Europe_ChooseCountryAgain
	goto_if_eq VAR_RESULT, 0, Europe_PreviewTreecko
	goto_if_eq VAR_RESULT, 1, Europe_PreviewCharmander
	setvar VAR_0x8004, SPECIES_MUDKIP
	goto Europe_PreviewStarter

Europe_ChooseCountryAgain::
	setvar VAR_EUROPE_HOME_COUNTRY, 0
	goto Europe_ChooseCountry

Europe_PreviewBulbasaur::
	setvar VAR_0x8004, SPECIES_BULBASAUR
	goto Europe_PreviewStarter

Europe_PreviewCyndaquil::
	setvar VAR_0x8004, SPECIES_CYNDAQUIL
	goto Europe_PreviewStarter

Europe_PreviewChikorita::
	setvar VAR_0x8004, SPECIES_CHIKORITA
	goto Europe_PreviewStarter

Europe_PreviewTorchic::
	setvar VAR_0x8004, SPECIES_TORCHIC
	goto Europe_PreviewStarter

Europe_PreviewTreecko::
	setvar VAR_0x8004, SPECIES_TREECKO
	goto Europe_PreviewStarter

Europe_PreviewCharmander::
	setvar VAR_0x8004, SPECIES_CHARMANDER
	goto Europe_PreviewStarter

Europe_PreviewStarter::
	bufferspeciesname STR_VAR_1, VAR_0x8004
	showmonpic VAR_0x8004, 10, 3
	msgbox Europe_Text_ConfirmStarter, MSGBOX_YESNO
	hidemonpic
	goto_if_eq VAR_RESULT, NO, Europe_ReturnToStarters
	copyvar VAR_EUROPE_STARTER_SPECIES, VAR_0x8004
	givemon VAR_EUROPE_STARTER_SPECIES, 8, ITEM_NONE
	bufferspeciesname STR_VAR_1, VAR_EUROPE_STARTER_SPECIES
	call Europe_PackTravelBag
	goto_if_eq VAR_EUROPE_HOME_COUNTRY, 1, Europe_ArriveLondon
	goto_if_eq VAR_EUROPE_HOME_COUNTRY, 2, Europe_ArriveParis
	warp MAP_EUROPE_BERLIN, 15, 14
	waitstate
	releaseall
	end

Europe_ArriveLondon::
	warp MAP_EUROPE_LONDON, 15, 14
	waitstate
	releaseall
	end

Europe_ArriveParis::
	warp MAP_EUROPE_PARIS, 15, 14
	waitstate
	releaseall
	end

Europe_ReturnToStarters::
	goto_if_eq VAR_EUROPE_HOME_COUNTRY, 1, Europe_StartEngland
	goto_if_eq VAR_EUROPE_HOME_COUNTRY, 2, Europe_StartFrance
	goto Europe_StartGermany

Europe_Text_EnglandStarters::
	.string "ENGLAND: Choose your first partner!\n"
	.string "Press B to choose another country.$"

Europe_Text_FranceStarters::
	.string "FRANCE: Choose your first partner!\n"
	.string "Press B to choose another country.$"

Europe_Text_GermanyStarters::
	.string "GERMANY: Choose your first partner!\n"
	.string "Press B to choose another country.$"

Europe_Text_ConfirmStarter::
	.string "Will you choose {STR_VAR_1}\n"
	.string "as your first traveling partner?$"

Europe_PackTravelBag::
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_SYS_POKEDEX_GET
	special EnableNationalPokedex
	setflag FLAG_SYS_B_DASH
	additem ITEM_POKE_BALL, 10
	additem ITEM_POTION, 5
	additem ITEM_BICYCLE, 1
	additem ITEM_TOWN_MAP, 1
	msgbox Europe_Text_Starter, MSGBOX_DEFAULT
	closemessage
	return

Europe_Text_Starter::
	.string "{STR_VAR_1} will be your first partner!\p"
	.string "Your BAG has POKE BALLS, POTIONS,\n"
	.string "a BICYCLE, and a TOWN MAP.\p"
	.string "Welcome to the European Tour!$"

Europe_Text_ChooseCountry::
	.string "Where will your European\n"
	.string "adventure begin?$"

PalletTown_PlayersHouse_2F_OnTransition::
	call_if_eq VAR_MAP_SCENE_PALLET_TOWN_PLAYERS_HOUSE_2F, 0, PalletTown_PlayersHouse_2F_EventScript_SetRespawn
	end

PalletTown_PlayersHouse_2F_EventScript_SetRespawn::
	setrespawn HEAL_LOCATION_PALLET_TOWN
	return

PalletTown_PlayersHouse_2F_OnWarp::
	map_script_2 VAR_MAP_SCENE_PALLET_TOWN_PLAYERS_HOUSE_2F, 0, PalletTown_PlayersHouse_2F_FirstWarpIn
	.2byte 0

PalletTown_PlayersHouse_2F_FirstWarpIn::
	turnobject LOCALID_PLAYER, DIR_NORTH
	setvar VAR_MAP_SCENE_PALLET_TOWN_PLAYERS_HOUSE_2F, 1
	end

PalletTown_PlayersHouse_2F_EventScript_NES::
	msgbox PalletTown_PlayersHouse_2F_Text_PlayedWithNES, MSGBOX_SIGN
	end

PalletTown_PlayersHouse_2F_EventScript_Sign::
	msgbox PalletTown_PlayersHouse_2F_Text_PressLRForHelp, MSGBOX_SIGN
	end

PalletTown_PlayersHouse_2F_EventScript_PC::
	goto_if_questlog EventScript_ReleaseEnd
	lockall
	setvar VAR_0x8004, HELPCONTEXT_BEDROOM_PC
	special Script_SetHelpContext
	setvar VAR_0x8004, 1
	special AnimatePcTurnOn
	playse SE_PC_ON
	msgbox Text_PlayerBootedUpPC
	special BedroomPC
	waitstate
	special SetHelpContextForMap
	releaseall
	end

EventScript_PalletTown_PlayersHouse_2F_ShutDownPC::
	setvar VAR_0x8004, 1
	playse SE_PC_OFF
	special AnimatePcTurnOff
	special SetHelpContextForMap
	releaseall
	end
