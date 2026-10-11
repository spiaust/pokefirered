Shadow_End::
 release
 end
Shadow_Entrance::
 lock
 faceplayer
 goto_if_eq VAR_SHADOW_STARTED, 1, Shadow_EntranceReady
 msgbox Shadow_WelcomeText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 setvar VAR_SHADOW_STARTED, 1
 setvar VAR_SHADOW_STAGE, 0
 giveitem ITEM_EXP_SHARE, 1
 giveitem ITEM_POKE_BALL, 10
Shadow_EntranceReady::
 checkitem ITEM_FAME_CHECKER, 1
 goto_if_eq VAR_RESULT, TRUE, Shadow_EntranceMap
 giveitem ITEM_FAME_CHECKER, 1
Shadow_EntranceMap::
 checkitem ITEM_TOWN_MAP, 1
 goto_if_eq VAR_RESULT, TRUE, Shadow_EntranceOffer
 giveitem ITEM_TOWN_MAP, 1
Shadow_EntranceOffer::
 msgbox Shadow_ResumeText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 special Shadow_Resume
 waitstate
 release
 end
Shadow_Nurse::
 lock
 faceplayer
 special HealPlayerParty
 msgbox Shadow_HealText
 goto Shadow_End
Shadow_Locked::
 msgbox Shadow_LockedText
 goto Shadow_End
Shadow_Rescued::
 msgbox Shadow_RescuedText
 goto Shadow_End
Shadow_Full::
 msgbox Shadow_FullText
 goto Shadow_End
Shadow_Purify::
 lock
 faceplayer
 special Shadow_TryPurify
 goto_if_eq VAR_RESULT, 1, Shadow_Purified
 goto_if_eq VAR_RESULT, 2, Shadow_Care
 msgbox Shadow_NoShadowText
 goto Shadow_End
Shadow_Purified::
 msgbox Shadow_PurifiedText
 goto Shadow_End
Shadow_Care::
 msgbox Shadow_CareText
 goto Shadow_End
Shadow_Shop::
 lock
 faceplayer
 pokemart Shadow_ShopItems
 release
 end
 .align 2
Shadow_ShopItems::
 .2byte ITEM_POKE_BALL, ITEM_GREAT_BALL, ITEM_ULTRA_BALL, ITEM_POTION, ITEM_SUPER_POTION, ITEM_HYPER_POTION, ITEM_REVIVE, ITEM_ANTIDOTE, ITEM_PARALYZE_HEAL, ITEM_AWAKENING, ITEM_BURN_HEAL, ITEM_ICE_HEAL, ITEM_FULL_HEAL, ITEM_MAX_POTION, ITEM_FULL_RESTORE, ITEM_FIRE_STONE, ITEM_WATER_STONE, ITEM_THUNDER_STONE, ITEM_LEAF_STONE, ITEM_MOON_STONE, ITEM_SUN_STONE, ITEM_NONE
Shadow_WelcomeText::
	.string "ADA: Join the ECLIPSE campaign?\nEight badges, a rival and a\pmystery across Europe await.\nThis journey has its own saved\pprogress. You can return to\nthese shelters after a defeat.$"
Shadow_ResumeText::
	.string "Continue your ECLIPSE journey? I\nwill take you to the current\pchapter. Nurse left; mission\nstraight ahead; next porter\pright. Route guide lower right.\nRescue partner and keeper beside\pthe mission.$"
Shadow_HealText::
	.string "Your partners are fully rested.\nCome back whenever you need\pcare.$"
Shadow_LockedText::
	.string "Complete the current chapter\nfirst. Talk to the mission\ptrainer straight ahead. ADA at\nyour starting city can return\pyou to your current objective.$"
Shadow_PracticeText::
	.string "Would you like a practice\nbattle? We can battle again to\phelp your team grow.$"
Shadow_PracticeIntroText::
	.string "Let us compare our partners!$"
Shadow_PracticeDefeatText::
	.string "Your partners worked together\nwell.$"
Shadow_PracticeAfterText::
	.string "Heal at the shelter, then come\nback for another match whenever\pyou like.$"
Shadow_RescuedText::
	.string "The rescued SHADOW partner\njoined your party! Its heart is\pclosed. It deals and takes extra\ndamage, and cannot evolve until\ppurified. Bring it to the\nkeeper; patient care and\ptraveling restore trust.$"
Shadow_FullText::
	.string "Your party is full. Leave a\nplace for this partner at a city\pPC, then return. This rescue\nwill wait for you.$"
Shadow_AlreadyText::
	.string "This partner has already been\nrescued. Thank you for giving it\pa home.$"
Shadow_PartnerText::
	.string "This partner is safe with the\nshelter. Other shelters hold\prescued SHADOW POKEMON after\ntheir missions. Talk to the\pkeeper to help reopen a closed\nheart.$"
Shadow_PurifiedText::
	.string "A shadow partner has opened its\nheart! The shadow effect is gone\pand it can evolve normally. Its\nname now reads HEALED. You have\pgiven it a new beginning.$"
Shadow_CareText::
	.string "The shadow partner is not ready\nyet. We spent a quiet care\psession together. Return after\nmore walks or another rest.\pThere is no penalty for taking\nyour time.$"
Shadow_NoShadowText::
	.string "There are no shadow partners in\nyour party. You may bring one\pfrom your PC for care.\nPurification is always free.$"
Shadow_HomeText::
	.string "CELEBI: Return to modern Lisbon?\nThe historical chapter will keep\pyour progress. ADA can bring you\nback to your unfinished mission.$"

	.include "data/maps/ShadowOxford/scripts.inc"
	.include "data/maps/ShadowOxfordRoute/scripts.inc"
ShadowOxford_Mission::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 0, Shadow_Locked
	goto_if_gt VAR_SHADOW_STAGE, 0, ShadowOxford_Done
	msgbox ShadowOxford_Before, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	trainerbattle_single 100, ShadowOxford_Intro, ShadowOxford_Defeat, ShadowOxford_Victory
	goto Shadow_End
ShadowOxford_Victory::
	setvar VAR_SHADOW_STAGE, 1
ShadowOxford_Done::
	msgbox ShadowOxford_After
	goto Shadow_End
ShadowOxford_Before::
	.string "ADA: Welcome to the European\nLeague. Your rival believes\pstrength means never needing\nhelp. Show them what a partner\pcan do. The station porter will\nopen the next journey after your\pmatch. Shall we battle?$"
ShadowOxford_After::
	.string "{RIVAL}: You won. A League\ncourier vanished near Paris. I\pam going after the badges, but I\nwill keep an eye out. First,\pearn your badge here.$"
ShadowOxford_Intro::
	.string "Your partners are ready. Let us\nbegin.$"
ShadowOxford_Defeat::
	.string "The battle is decided.$"
ShadowOxford_Next::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 1, Shadow_Locked
	msgbox ShadowOxford_NextText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_LONDON, 6, 7
	waitstate
	release
	end
ShadowOxford_NextText::
	.string "Travel to LONDON? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowOxford_Previous::
	lock
	faceplayer
	msgbox ShadowOxford_PreviousText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_OXFORD, 6, 7
	waitstate
	release
	end
ShadowOxford_PreviousText::
	.string "Travel to OXFORD? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowOxford_Route::
	lock
	faceplayer
	warp MAP_SHADOW_OXFORD_ROUTE, 15, 20
	waitstate
	release
	end
ShadowOxford_Trainer0::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 101
	trainerbattle_single 101, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowOxford_Trainer1::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 102
	trainerbattle_single 102, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowOxford_Trainer2::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 103
	trainerbattle_single 103, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowOxford_Trainer3::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 104
	trainerbattle_single 104, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowOxford_Trainer4::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 105
	trainerbattle_single 105, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowOxford_Trainer5::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 106
	trainerbattle_single 106, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowOxford_Rival::
	lock
	faceplayer
	msgbox ShadowOxford_RivalText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 107
	trainerbattle_single 107, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	goto Shadow_End
ShadowOxford_RivalText::
	.string "{RIVAL}: I can win this alone.\nLet me prove it.$"
ShadowOxford_RouteExit::
	lock
	faceplayer
	warp MAP_SHADOW_OXFORD, 6, 7
	waitstate
	release
	end
ShadowOxford_Keeper::
	lock
	faceplayer
	msgbox Shadow_PartnerText
	goto Shadow_End
	.include "data/maps/ShadowLondon/scripts.inc"
	.include "data/maps/ShadowLondonRoute/scripts.inc"
ShadowLondon_Mission::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 1, Shadow_Locked
	goto_if_gt VAR_SHADOW_STAGE, 1, ShadowLondon_Done
	msgbox ShadowLondon_Before, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	trainerbattle_single 108, ShadowLondon_Intro, ShadowLondon_Defeat, ShadowLondon_Victory
	goto Shadow_End
ShadowLondon_Victory::
	setvar VAR_SHADOW_STAGE, 2
	setflag FLAG_BADGE01_GET
ShadowLondon_Done::
 goto_if_set FLAG_0x8C6, ShadowLondon_RewardDone
 msgbox Shadow_TMRewardText
 giveitem ITEM_TM39, 1
 goto_if_eq VAR_0x8007, FALSE, Shadow_TMRewardFull
 setflag FLAG_0x8C6
ShadowLondon_RewardDone::
	msgbox ShadowLondon_After
	goto Shadow_End
ShadowLondon_Before::
	.string "ELLIS: Eight countries host our\nLeague challenge. Rock is your\pfirst test. Team ECLIPSE calls\nfrightened POKEMON powerful. We\pcall that cruelty. Shall we\nbattle?$"
ShadowLondon_After::
	.string "ELLIS: The BOULDERBADGE is\nyours. Take the ferry to France.\pFind ADA's missing courier\nbefore ECLIPSE does.$"
ShadowLondon_Intro::
	.string "Your partners are ready. Let us\nbegin.$"
ShadowLondon_Defeat::
	.string "The battle is decided.$"
ShadowLondon_Next::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 2, Shadow_Locked
	msgbox ShadowLondon_NextText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_PARIS, 6, 7
	waitstate
	release
	end
ShadowLondon_NextText::
	.string "Travel to PARIS? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowLondon_Previous::
	lock
	faceplayer
	msgbox ShadowLondon_PreviousText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_OXFORD, 6, 7
	waitstate
	release
	end
ShadowLondon_PreviousText::
	.string "Travel to OXFORD? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowLondon_Route::
	lock
	faceplayer
	warp MAP_SHADOW_LONDON_ROUTE, 15, 20
	waitstate
	release
	end
ShadowLondon_Trainer0::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 109
	trainerbattle_single 109, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowLondon_Trainer1::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 110
	trainerbattle_single 110, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowLondon_Trainer2::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 111
	trainerbattle_single 111, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowLondon_Trainer3::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 112
	trainerbattle_single 112, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowLondon_Trainer4::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 113
	trainerbattle_single 113, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowLondon_Trainer5::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 114
	trainerbattle_single 114, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowLondon_Rival::
	lock
	faceplayer
	msgbox ShadowLondon_RivalText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 115
	trainerbattle_single 115, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	goto Shadow_End
ShadowLondon_RivalText::
	.string "{RIVAL}: I can win this alone.\nLet me prove it.$"
ShadowLondon_RouteExit::
	lock
	faceplayer
	warp MAP_SHADOW_LONDON, 6, 7
	waitstate
	release
	end
ShadowLondon_Keeper::
	lock
	faceplayer
	msgbox Shadow_PartnerText
	goto Shadow_End
	.include "data/maps/ShadowParis/scripts.inc"
	.include "data/maps/ShadowParisRoute/scripts.inc"
ShadowParis_Mission::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 2, Shadow_Locked
	goto_if_gt VAR_SHADOW_STAGE, 2, ShadowParis_Done
	msgbox ShadowParis_Before, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	trainerbattle_single 116, ShadowParis_Intro, ShadowParis_Defeat, ShadowParis_Victory
	goto Shadow_End
ShadowParis_Victory::
	setvar VAR_SHADOW_STAGE, 3
	setflag FLAG_BADGE02_GET
ShadowParis_Done::
 goto_if_set FLAG_0x8C7, ShadowParis_RewardDone
 msgbox Shadow_TMRewardText
 giveitem ITEM_TM03, 1
 goto_if_eq VAR_0x8007, FALSE, Shadow_TMRewardFull
 setflag FLAG_0x8C7
ShadowParis_RewardDone::
	msgbox ShadowParis_After
	goto Shadow_End
ShadowParis_Before::
	.string "MARINE: The courier left a\nsealed research ledger. ECLIPSE\pstole its key and abandoned a\nPIKACHU whose heart is closed.\pWin this match, then meet our\nrescue keeper. Shall we battle?$"
ShadowParis_After::
	.string "MARINE: The CASCADEBADGE is\nyours. The ledger names\pBrussels. Take the rescued\npartner with you if you can.\pCare opens what force cannot.$"
ShadowParis_Intro::
	.string "Your partners are ready. Let us\nbegin.$"
ShadowParis_Defeat::
	.string "The battle is decided.$"
ShadowParis_Next::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 3, Shadow_Locked
	msgbox ShadowParis_NextText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_BRUSSELS, 6, 7
	waitstate
	release
	end
ShadowParis_NextText::
	.string "Travel to BRUSSELS? Your\nprogress is saved normally. Heal\pbefore leaving if you need to.$"
ShadowParis_Previous::
	lock
	faceplayer
	msgbox ShadowParis_PreviousText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_LONDON, 6, 7
	waitstate
	release
	end
ShadowParis_PreviousText::
	.string "Travel to LONDON? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowParis_Route::
	lock
	faceplayer
	warp MAP_SHADOW_PARIS_ROUTE, 15, 20
	waitstate
	release
	end
ShadowParis_Trainer0::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 117
	trainerbattle_single 117, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowParis_Trainer1::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 118
	trainerbattle_single 118, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowParis_Trainer2::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 119
	trainerbattle_single 119, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowParis_Trainer3::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 120
	trainerbattle_single 120, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowParis_Trainer4::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 121
	trainerbattle_single 121, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowParis_Trainer5::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 122
	trainerbattle_single 122, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowParis_Rival::
	lock
	faceplayer
	msgbox ShadowParis_RivalText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 123
	trainerbattle_single 123, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	goto Shadow_End
ShadowParis_RivalText::
	.string "{RIVAL}: I can win this alone.\nLet me prove it.$"
ShadowParis_RouteExit::
	lock
	faceplayer
	warp MAP_SHADOW_PARIS, 6, 7
	waitstate
	release
	end
ShadowParis_Keeper::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 3, Shadow_Locked
	setvar VAR_0x8004, 0
	setvar VAR_0x8005, SPECIES_PIKACHU
	setvar VAR_0x8006, 14
	special Shadow_Rescue
	goto_if_eq VAR_RESULT, 1, Shadow_Rescued
	goto_if_eq VAR_RESULT, 2, Shadow_Full
	msgbox Shadow_AlreadyText
	goto Shadow_End
	.include "data/maps/ShadowBrussels/scripts.inc"
	.include "data/maps/ShadowBrusselsRoute/scripts.inc"
ShadowBrussels_Mission::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 3, Shadow_Locked
	goto_if_gt VAR_SHADOW_STAGE, 3, ShadowBrussels_Done
	msgbox ShadowBrussels_Before, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	trainerbattle_single 124, ShadowBrussels_Intro, ShadowBrussels_Defeat, ShadowBrussels_Victory
	goto Shadow_End
ShadowBrussels_Victory::
	setvar VAR_SHADOW_STAGE, 4
	setflag FLAG_BADGE04_GET
ShadowBrussels_Done::
 goto_if_set FLAG_0x8C8, ShadowBrussels_RewardDone
 msgbox Shadow_TMRewardText
 giveitem ITEM_TM09, 1
 goto_if_eq VAR_0x8007, FALSE, Shadow_TMRewardFull
 setflag FLAG_0x8C8
ShadowBrussels_RewardDone::
	msgbox ShadowBrussels_After
	goto Shadow_End
ShadowBrussels_Before::
	.string "SABINE: ECLIPSE buys League\nfreight permits to move stolen\ppartners. Our garden shelter\nintercepted one shipment. Prove\pyour bond before I entrust you\nwith its manifest. Shall we\pbattle?$"
ShadowBrussels_After::
	.string "SABINE: You earned the\nRAINBOWBADGE. The manifest leads\pto Amsterdam. Their director\nVEIL funds the machines through\pa shipping company.$"
ShadowBrussels_Intro::
	.string "Your partners are ready. Let us\nbegin.$"
ShadowBrussels_Defeat::
	.string "The battle is decided.$"
ShadowBrussels_Next::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 4, Shadow_Locked
	msgbox ShadowBrussels_NextText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_AMSTERDAM, 6, 7
	waitstate
	release
	end
ShadowBrussels_NextText::
	.string "Travel to AMSTERDAM? Your\nprogress is saved normally. Heal\pbefore leaving if you need to.$"
ShadowBrussels_Previous::
	lock
	faceplayer
	msgbox ShadowBrussels_PreviousText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_PARIS, 6, 7
	waitstate
	release
	end
ShadowBrussels_PreviousText::
	.string "Travel to PARIS? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowBrussels_Route::
	lock
	faceplayer
	warp MAP_SHADOW_BRUSSELS_ROUTE, 15, 20
	waitstate
	release
	end
ShadowBrussels_Trainer0::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 125
	trainerbattle_single 125, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowBrussels_Trainer1::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 126
	trainerbattle_single 126, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowBrussels_Trainer2::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 127
	trainerbattle_single 127, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowBrussels_Trainer3::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 128
	trainerbattle_single 128, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowBrussels_Trainer4::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 129
	trainerbattle_single 129, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowBrussels_Trainer5::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 130
	trainerbattle_single 130, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowBrussels_Rival::
	lock
	faceplayer
	msgbox ShadowBrussels_RivalText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 131
	trainerbattle_single 131, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	goto Shadow_End
ShadowBrussels_RivalText::
	.string "{RIVAL}: I can win this alone.\nLet me prove it.$"
ShadowBrussels_RouteExit::
	lock
	faceplayer
	warp MAP_SHADOW_BRUSSELS, 6, 7
	waitstate
	release
	end
ShadowBrussels_Keeper::
	lock
	faceplayer
	msgbox Shadow_PartnerText
	goto Shadow_End
	.include "data/maps/ShadowAmsterdam/scripts.inc"
	.include "data/maps/ShadowAmsterdamRoute/scripts.inc"
ShadowAmsterdam_Mission::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 4, Shadow_Locked
	goto_if_gt VAR_SHADOW_STAGE, 4, ShadowAmsterdam_Done
	msgbox ShadowAmsterdam_Before, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	trainerbattle_single 132, ShadowAmsterdam_Intro, ShadowAmsterdam_Defeat, ShadowAmsterdam_Victory
	goto Shadow_End
ShadowAmsterdam_Victory::
	setvar VAR_SHADOW_STAGE, 5
	setflag FLAG_BADGE03_GET
ShadowAmsterdam_Done::
 goto_if_set FLAG_0x8C9, ShadowAmsterdam_RewardDone
 msgbox Shadow_TMRewardText
 giveitem ITEM_TM34, 1
 goto_if_eq VAR_0x8007, FALSE, Shadow_TMRewardFull
 setflag FLAG_0x8C9
ShadowAmsterdam_RewardDone::
	msgbox ShadowAmsterdam_After
	goto Shadow_End
ShadowAmsterdam_Before::
	.string "MAARTEN: VEIL's machines use a\nsignal that suppresses emotion.\pYour rival chased a freighter\nwithout waiting for us. Earn the\pTHUNDERBADGE, then find them in\nBerlin.\pGround types block Electric moves.\nBelgium has wild NIDORAN.\pTrain one into NIDORINA, then use\na MOON STONE for NIDOQUEEN.\pShall we battle?$"
ShadowAmsterdam_After::
	.string "MAARTEN: The THUNDERBADGE is\nyours. ECLIPSE stole an archive\pfrom Berlin. ADA thinks the\nsignal is much older than this\pcompany.$"
ShadowAmsterdam_Intro::
	.string "Your partners are ready. Let us\nbegin.$"
ShadowAmsterdam_Defeat::
	.string "The battle is decided.$"
ShadowAmsterdam_Next::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 5, Shadow_Locked
	msgbox ShadowAmsterdam_NextText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_BERLIN, 6, 7
	waitstate
	release
	end
ShadowAmsterdam_NextText::
	.string "Travel to BERLIN? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowAmsterdam_Previous::
	lock
	faceplayer
	msgbox ShadowAmsterdam_PreviousText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_BRUSSELS, 6, 7
	waitstate
	release
	end
ShadowAmsterdam_PreviousText::
	.string "Travel to BRUSSELS? Your\nprogress is saved normally. Heal\pbefore leaving if you need to.$"
ShadowAmsterdam_Route::
	lock
	faceplayer
	warp MAP_SHADOW_AMSTERDAM_ROUTE, 15, 20
	waitstate
	release
	end
ShadowAmsterdam_Trainer0::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 133
	trainerbattle_single 133, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAmsterdam_Trainer1::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 134
	trainerbattle_single 134, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAmsterdam_Trainer2::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 135
	trainerbattle_single 135, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAmsterdam_Trainer3::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 136
	trainerbattle_single 136, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAmsterdam_Trainer4::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 137
	trainerbattle_single 137, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAmsterdam_Trainer5::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 138
	trainerbattle_single 138, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAmsterdam_Rival::
	lock
	faceplayer
	msgbox ShadowAmsterdam_RivalText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 139
	trainerbattle_single 139, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	goto Shadow_End
ShadowAmsterdam_RivalText::
	.string "{RIVAL}: I can win this alone.\nLet me prove it.$"
ShadowAmsterdam_RouteExit::
	lock
	faceplayer
	warp MAP_SHADOW_AMSTERDAM, 6, 7
	waitstate
	release
	end
ShadowAmsterdam_Keeper::
	lock
	faceplayer
	msgbox Shadow_PartnerText
	goto Shadow_End
	.include "data/maps/ShadowBerlin/scripts.inc"
	.include "data/maps/ShadowBerlinRoute/scripts.inc"
ShadowBerlin_Mission::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 5, Shadow_Locked
	goto_if_gt VAR_SHADOW_STAGE, 5, ShadowBerlin_Done
	msgbox ShadowBerlin_Before, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	trainerbattle_single 140, ShadowBerlin_Intro, ShadowBerlin_Defeat, ShadowBerlin_Victory
	goto Shadow_End
ShadowBerlin_Victory::
	setvar VAR_SHADOW_STAGE, 6
	setflag FLAG_BADGE05_GET
ShadowBerlin_Done::
 goto_if_set FLAG_0x8CA, ShadowBerlin_RewardDone
 msgbox Shadow_TMRewardText
 giveitem ITEM_TM31, 1
 goto_if_eq VAR_0x8007, FALSE, Shadow_TMRewardFull
 setflag FLAG_0x8CA
ShadowBerlin_RewardDone::
	msgbox ShadowBerlin_After
	goto Shadow_End
ShadowBerlin_Before::
	.string "GRETA: Our archive preserves the\nwork of people who resisted the\pNazi regime. Someone stole a\nwartime laboratory file. German\presistance members risked\neverything to protect their\pneighbors. Help us protect that\nmemory.\pFlying and Psychic moves work\nwell against my Fighting team.\pIf your Flying partner struggles,\ntrain on Brussels routes first.\pPrepare your partners.\nShall we battle?$"
ShadowBerlin_After::
	.string "GRETA: The SOULBADGE is yours.\nYour birthplace never decides\pyour loyalties. ADA traced the\nstolen file to Prague. The\presistance names in it must\nremain protected.$"
ShadowBerlin_Intro::
	.string "Your partners are ready. Let us\nbegin.$"
ShadowBerlin_Defeat::
	.string "The battle is decided.$"
ShadowBerlin_Next::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 6, Shadow_Locked
	msgbox ShadowBerlin_NextText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_PRAGUE, 6, 7
	waitstate
	release
	end
ShadowBerlin_NextText::
	.string "Travel to PRAGUE? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowBerlin_Previous::
	lock
	faceplayer
	msgbox ShadowBerlin_PreviousText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_AMSTERDAM, 6, 7
	waitstate
	release
	end
ShadowBerlin_PreviousText::
	.string "Travel to AMSTERDAM? Your\nprogress is saved normally. Heal\pbefore leaving if you need to.$"
ShadowBerlin_Route::
	lock
	faceplayer
	warp MAP_SHADOW_BERLIN_ROUTE, 15, 20
	waitstate
	release
	end
ShadowBerlin_Trainer0::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 141
	trainerbattle_single 141, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowBerlin_Trainer1::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 142
	trainerbattle_single 142, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowBerlin_Trainer2::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 143
	trainerbattle_single 143, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowBerlin_Trainer3::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 144
	trainerbattle_single 144, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowBerlin_Trainer4::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 145
	trainerbattle_single 145, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowBerlin_Trainer5::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 146
	trainerbattle_single 146, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowBerlin_Rival::
	lock
	faceplayer
	msgbox ShadowBerlin_RivalText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 147
	trainerbattle_single 147, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	goto Shadow_End
ShadowBerlin_RivalText::
	.string "{RIVAL}: I can win this alone.\nLet me prove it.$"
ShadowBerlin_RouteExit::
	lock
	faceplayer
	warp MAP_SHADOW_BERLIN, 6, 7
	waitstate
	release
	end
ShadowBerlin_Keeper::
	lock
	faceplayer
	msgbox Shadow_PartnerText
	goto Shadow_End
	.include "data/maps/ShadowPrague/scripts.inc"
	.include "data/maps/ShadowPragueRoute/scripts.inc"
ShadowPrague_Mission::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 6, Shadow_Locked
	goto_if_gt VAR_SHADOW_STAGE, 6, ShadowPrague_Done
	msgbox ShadowPrague_Before, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	trainerbattle_single 148, ShadowPrague_Intro, ShadowPrague_Defeat, ShadowPrague_Victory
	goto Shadow_End
ShadowPrague_Victory::
	setvar VAR_SHADOW_STAGE, 7
ShadowPrague_Done::
	msgbox ShadowPrague_After
	goto Shadow_End
ShadowPrague_Before::
	.string "ADA: ECLIPSE is testing a shadow\ntransmitter in the old freight\pyard. Your rival tried to\ndestroy it alone and was\pcaptured. Defeat the handler and\nbring everyone out together.\pShall we battle?$"
ShadowPrague_After::
	.string "{RIVAL}: I thought asking for\nhelp meant losing. You came\panyway. The receiver points to\nVienna. From now on we do this\ptogether.$"
ShadowPrague_Intro::
	.string "Your partners are ready. Let us\nbegin.$"
ShadowPrague_Defeat::
	.string "The battle is decided.$"
ShadowPrague_Next::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 7, Shadow_Locked
	msgbox ShadowPrague_NextText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_VIENNA, 6, 7
	waitstate
	release
	end
ShadowPrague_NextText::
	.string "Travel to VIENNA? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowPrague_Previous::
	lock
	faceplayer
	msgbox ShadowPrague_PreviousText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_BERLIN, 6, 7
	waitstate
	release
	end
ShadowPrague_PreviousText::
	.string "Travel to BERLIN? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowPrague_Route::
	lock
	faceplayer
	warp MAP_SHADOW_PRAGUE_ROUTE, 15, 20
	waitstate
	release
	end
ShadowPrague_Trainer0::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 149
	trainerbattle_single 149, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowPrague_Trainer1::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 150
	trainerbattle_single 150, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowPrague_Trainer2::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 151
	trainerbattle_single 151, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowPrague_Trainer3::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 152
	trainerbattle_single 152, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowPrague_Trainer4::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 153
	trainerbattle_single 153, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowPrague_Trainer5::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 154
	trainerbattle_single 154, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowPrague_Rival::
	lock
	faceplayer
	msgbox ShadowPrague_RivalText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 155
	trainerbattle_single 155, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	goto Shadow_End
ShadowPrague_RivalText::
	.string "{RIVAL}: Training together\nhelped me learn. Shall we\pcompare our teams?$"
ShadowPrague_RouteExit::
	lock
	faceplayer
	warp MAP_SHADOW_PRAGUE, 6, 7
	waitstate
	release
	end
ShadowPrague_Keeper::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 7, Shadow_Locked
	setvar VAR_0x8004, 1
	setvar VAR_0x8005, SPECIES_HOUNDOUR
	setvar VAR_0x8006, 29
	special Shadow_Rescue
	goto_if_eq VAR_RESULT, 1, Shadow_Rescued
	goto_if_eq VAR_RESULT, 2, Shadow_Full
	msgbox Shadow_AlreadyText
	goto Shadow_End
	.include "data/maps/ShadowVienna/scripts.inc"
	.include "data/maps/ShadowViennaRoute/scripts.inc"
ShadowVienna_Mission::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 7, Shadow_Locked
	goto_if_gt VAR_SHADOW_STAGE, 7, ShadowVienna_Done
	msgbox ShadowVienna_Before, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	trainerbattle_single 156, ShadowVienna_Intro, ShadowVienna_Defeat, ShadowVienna_Victory
	goto Shadow_End
ShadowVienna_Victory::
	setvar VAR_SHADOW_STAGE, 8
	setflag FLAG_BADGE06_GET
ShadowVienna_Done::
 goto_if_set FLAG_0x8CB, ShadowVienna_RewardDone
 msgbox Shadow_TMRewardText
 giveitem ITEM_TM04, 1
 goto_if_eq VAR_0x8007, FALSE, Shadow_TMRewardFull
 setflag FLAG_0x8CB
ShadowVienna_RewardDone::
	msgbox ShadowVienna_After
	goto Shadow_End
ShadowVienna_Before::
	.string "IRENA: The signal can be unmade,\nbut its original frequency is\pmissing. My psychic partners\nhear a frightened voice inside\pit. Earn the MARSHBADGE; then we\ncan search the Swiss archive.\pShall we battle?$"
ShadowVienna_After::
	.string "IRENA: The MARSHBADGE is yours.\nThe archive's keeper in Zurich\phas a clock that reacts to\nCELEBI. ECLIPSE is trying to use\pit to reach the past.$"
ShadowVienna_Intro::
	.string "Your partners are ready. Let us\nbegin.$"
ShadowVienna_Defeat::
	.string "The battle is decided.$"
ShadowVienna_Next::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 8, Shadow_Locked
	msgbox ShadowVienna_NextText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_ZURICH, 6, 7
	waitstate
	release
	end
ShadowVienna_NextText::
	.string "Travel to ZURICH? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowVienna_Previous::
	lock
	faceplayer
	msgbox ShadowVienna_PreviousText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_PRAGUE, 6, 7
	waitstate
	release
	end
ShadowVienna_PreviousText::
	.string "Travel to PRAGUE? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowVienna_Route::
	lock
	faceplayer
	warp MAP_SHADOW_VIENNA_ROUTE, 15, 20
	waitstate
	release
	end
ShadowVienna_Trainer0::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 157
	trainerbattle_single 157, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowVienna_Trainer1::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 158
	trainerbattle_single 158, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowVienna_Trainer2::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 159
	trainerbattle_single 159, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowVienna_Trainer3::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 160
	trainerbattle_single 160, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowVienna_Trainer4::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 161
	trainerbattle_single 161, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowVienna_Trainer5::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 162
	trainerbattle_single 162, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowVienna_Rival::
	lock
	faceplayer
	msgbox ShadowVienna_RivalText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 163
	trainerbattle_single 163, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	goto Shadow_End
ShadowVienna_RivalText::
	.string "{RIVAL}: Training together\nhelped me learn. Shall we\pcompare our teams?$"
ShadowVienna_RouteExit::
	lock
	faceplayer
	warp MAP_SHADOW_VIENNA, 6, 7
	waitstate
	release
	end
ShadowVienna_Keeper::
	lock
	faceplayer
	msgbox Shadow_PartnerText
	goto Shadow_End
	.include "data/maps/ShadowZurich/scripts.inc"
	.include "data/maps/ShadowZurichRoute/scripts.inc"
ShadowZurich_Mission::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 8, Shadow_Locked
	goto_if_gt VAR_SHADOW_STAGE, 8, ShadowZurich_Done
	msgbox ShadowZurich_Before, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	trainerbattle_single 164, ShadowZurich_Intro, ShadowZurich_Defeat, ShadowZurich_Victory
	goto Shadow_End
ShadowZurich_Victory::
	setvar VAR_SHADOW_STAGE, 9
ShadowZurich_Done::
	msgbox ShadowZurich_After
	goto Shadow_End
ShadowZurich_Before::
	.string "VEIL: Fear creates obedient\npartners. CELEBI will take me to\pthe original machine, and this\ntime nobody will stop its\pbroadcast. Your sentimental\nLeague is already obsolete.\pShall we battle?$"
ShadowZurich_After::
	.string "ADA: VEIL escaped with the\nclock's core. We recovered its\pmap. It names Rome, Madrid and a\nfinal shipping point in Lisbon.\pCELEBI is following the damage\nto time.$"
ShadowZurich_Intro::
	.string "Your partners are ready. Let us\nbegin.$"
ShadowZurich_Defeat::
	.string "The battle is decided.$"
ShadowZurich_Next::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 9, Shadow_Locked
	msgbox ShadowZurich_NextText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_ROME, 6, 7
	waitstate
	release
	end
ShadowZurich_NextText::
	.string "Travel to ROME? Your progress is\nsaved normally. Heal before\pleaving if you need to.$"
ShadowZurich_Previous::
	lock
	faceplayer
	msgbox ShadowZurich_PreviousText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_VIENNA, 6, 7
	waitstate
	release
	end
ShadowZurich_PreviousText::
	.string "Travel to VIENNA? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowZurich_Route::
	lock
	faceplayer
	warp MAP_SHADOW_ZURICH_ROUTE, 15, 20
	waitstate
	release
	end
ShadowZurich_Trainer0::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 165
	trainerbattle_single 165, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowZurich_Trainer1::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 166
	trainerbattle_single 166, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowZurich_Trainer2::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 167
	trainerbattle_single 167, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowZurich_Trainer3::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 168
	trainerbattle_single 168, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowZurich_Trainer4::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 169
	trainerbattle_single 169, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowZurich_Trainer5::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 170
	trainerbattle_single 170, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowZurich_Rival::
	lock
	faceplayer
	msgbox ShadowZurich_RivalText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 171
	trainerbattle_single 171, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	goto Shadow_End
ShadowZurich_RivalText::
	.string "{RIVAL}: Training together\nhelped me learn. Shall we\pcompare our teams?$"
ShadowZurich_RouteExit::
	lock
	faceplayer
	warp MAP_SHADOW_ZURICH, 6, 7
	waitstate
	release
	end
ShadowZurich_Keeper::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 9, Shadow_Locked
	setvar VAR_0x8004, 2
	setvar VAR_0x8005, SPECIES_EEVEE
	setvar VAR_0x8006, 34
	special Shadow_Rescue
	goto_if_eq VAR_RESULT, 1, Shadow_Rescued
	goto_if_eq VAR_RESULT, 2, Shadow_Full
	msgbox Shadow_AlreadyText
	goto Shadow_End
	.include "data/maps/ShadowRome/scripts.inc"
	.include "data/maps/ShadowRomeRoute/scripts.inc"
ShadowRome_Mission::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 9, Shadow_Locked
	goto_if_gt VAR_SHADOW_STAGE, 9, ShadowRome_Done
	msgbox ShadowRome_Before, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	trainerbattle_single 172, ShadowRome_Intro, ShadowRome_Defeat, ShadowRome_Victory
	goto Shadow_End
ShadowRome_Victory::
	setvar VAR_SHADOW_STAGE, 10
	setflag FLAG_BADGE07_GET
ShadowRome_Done::
 goto_if_set FLAG_0x8CC, ShadowRome_RewardDone
 msgbox Shadow_TMRewardText
 giveitem ITEM_TM50, 1
 goto_if_eq VAR_0x8007, FALSE, Shadow_TMRewardFull
 setflag FLAG_0x8CC
ShadowRome_RewardDone::
	msgbox ShadowRome_After
	goto Shadow_End
ShadowRome_Before::
	.string "FLAVIA: ECLIPSE recruits\ntrainers by promising instant\pstrength. My partners grew\nthrough years of trust. The\pVOLCANOBADGE belongs to someone\nwho understands that difference.\pShall we battle?$"
ShadowRome_After::
	.string "FLAVIA: The VOLCANOBADGE is\nyours. A League ranger\pintercepted VEIL's message to\nMadrid. They plan to erase the\ppeople who stopped the original\nexperiments.$"
ShadowRome_Intro::
	.string "Your partners are ready. Let us\nbegin.$"
ShadowRome_Defeat::
	.string "The battle is decided.$"
ShadowRome_Next::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 10, Shadow_Locked
	msgbox ShadowRome_NextText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_MADRID, 6, 7
	waitstate
	release
	end
ShadowRome_NextText::
	.string "Travel to MADRID? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowRome_Previous::
	lock
	faceplayer
	msgbox ShadowRome_PreviousText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_ZURICH, 6, 7
	waitstate
	release
	end
ShadowRome_PreviousText::
	.string "Travel to ZURICH? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowRome_Route::
	lock
	faceplayer
	warp MAP_SHADOW_ROME_ROUTE, 15, 20
	waitstate
	release
	end
ShadowRome_Trainer0::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 173
	trainerbattle_single 173, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowRome_Trainer1::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 174
	trainerbattle_single 174, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowRome_Trainer2::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 175
	trainerbattle_single 175, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowRome_Trainer3::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 176
	trainerbattle_single 176, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowRome_Trainer4::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 177
	trainerbattle_single 177, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowRome_Trainer5::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 178
	trainerbattle_single 178, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowRome_Rival::
	lock
	faceplayer
	msgbox ShadowRome_RivalText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 179
	trainerbattle_single 179, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	goto Shadow_End
ShadowRome_RivalText::
	.string "{RIVAL}: Training together\nhelped me learn. Shall we\pcompare our teams?$"
ShadowRome_RouteExit::
	lock
	faceplayer
	warp MAP_SHADOW_ROME, 6, 7
	waitstate
	release
	end
ShadowRome_Keeper::
	lock
	faceplayer
	msgbox Shadow_PartnerText
	goto Shadow_End
	.include "data/maps/ShadowMadrid/scripts.inc"
	.include "data/maps/ShadowMadridRoute/scripts.inc"
ShadowMadrid_Mission::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 10, Shadow_Locked
	goto_if_gt VAR_SHADOW_STAGE, 10, ShadowMadrid_Done
	msgbox ShadowMadrid_Before, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	trainerbattle_single 180, ShadowMadrid_Intro, ShadowMadrid_Defeat, ShadowMadrid_Victory
	goto Shadow_End
ShadowMadrid_Victory::
	setvar VAR_SHADOW_STAGE, 11
	setflag FLAG_BADGE08_GET
ShadowMadrid_Done::
 goto_if_set FLAG_0x8CD, ShadowMadrid_RewardDone
 msgbox Shadow_TMRewardText
 giveitem ITEM_TM26, 1
 goto_if_eq VAR_0x8007, FALSE, Shadow_TMRewardFull
 setflag FLAG_0x8CD
ShadowMadrid_RewardDone::
	msgbox ShadowMadrid_After
	goto Shadow_End
ShadowMadrid_Before::
	.string "INES: This is your eighth\nchallenge. The EARTHBADGE will\pqualify you for Athens, but\nfirst there are lives to\pprotect. ECLIPSE's ship is\nleaving Lisbon with the clock\pcore. Shall we battle?$"
ShadowMadrid_After::
	.string "INES: All eight badges! The\nLeague can wait. Your rival has\pfound a harbor path in Lisbon.\nStop the ship before VEIL can\preopen the past.$"
ShadowMadrid_Intro::
	.string "Your partners are ready. Let us\nbegin.$"
ShadowMadrid_Defeat::
	.string "The battle is decided.$"
ShadowMadrid_Next::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 11, Shadow_Locked
	msgbox ShadowMadrid_NextText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_LISBON, 6, 7
	waitstate
	release
	end
ShadowMadrid_NextText::
	.string "Travel to LISBON? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowMadrid_Previous::
	lock
	faceplayer
	msgbox ShadowMadrid_PreviousText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_ROME, 6, 7
	waitstate
	release
	end
ShadowMadrid_PreviousText::
	.string "Travel to ROME? Your progress is\nsaved normally. Heal before\pleaving if you need to.$"
ShadowMadrid_Route::
	lock
	faceplayer
	warp MAP_SHADOW_MADRID_ROUTE, 15, 20
	waitstate
	release
	end
ShadowMadrid_Trainer0::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 181
	trainerbattle_single 181, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowMadrid_Trainer1::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 182
	trainerbattle_single 182, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowMadrid_Trainer2::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 183
	trainerbattle_single 183, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowMadrid_Trainer3::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 184
	trainerbattle_single 184, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowMadrid_Trainer4::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 185
	trainerbattle_single 185, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowMadrid_Trainer5::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 186
	trainerbattle_single 186, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowMadrid_Rival::
	lock
	faceplayer
	msgbox ShadowMadrid_RivalText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 187
	trainerbattle_single 187, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	goto Shadow_End
ShadowMadrid_RivalText::
	.string "{RIVAL}: Training together\nhelped me learn. Shall we\pcompare our teams?$"
ShadowMadrid_RouteExit::
	lock
	faceplayer
	warp MAP_SHADOW_MADRID, 6, 7
	waitstate
	release
	end
ShadowMadrid_Keeper::
	lock
	faceplayer
	msgbox Shadow_PartnerText
	goto Shadow_End
	.include "data/maps/ShadowLisbon/scripts.inc"
	.include "data/maps/ShadowLisbonRoute/scripts.inc"
ShadowLisbon_Mission::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 11, Shadow_Locked
	goto_if_gt VAR_SHADOW_STAGE, 11, ShadowLisbon_Done
	msgbox ShadowLisbon_Before, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	trainerbattle_single 188, ShadowLisbon_Intro, ShadowLisbon_Defeat, ShadowLisbon_Victory
	goto Shadow_End
ShadowLisbon_Victory::
	setvar VAR_SHADOW_STAGE, 12
ShadowLisbon_Done::
	msgbox ShadowLisbon_After
	goto Shadow_End
ShadowLisbon_Before::
	.string "{RIVAL}: We will cut the harbor\npower together. You draw the\phandler out; I will stop the\ntransmitter. CELEBI is here.\pSomething on that ship is\ntearing a hole in time. Shall we\pbattle?$"
ShadowLisbon_After::
	.string "ADA: CELEBI opened a path to\n1940. We can stop VEIL's\pfictional shadow experiment and\nprotect its victims. We cannot\perase the real war. CELEBI will\nalways offer a way home.$"
ShadowLisbon_Intro::
	.string "Your partners are ready. Let us\nbegin.$"
ShadowLisbon_Defeat::
	.string "The battle is decided.$"
ShadowLisbon_Next::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 12, Shadow_Locked
	msgbox ShadowLisbon_NextText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_PARIS1940, 6, 7
	waitstate
	release
	end
ShadowLisbon_NextText::
	.string "Travel to PARIS1940? Your\nprogress is saved normally. Heal\pbefore leaving if you need to.$"
ShadowLisbon_Previous::
	lock
	faceplayer
	msgbox ShadowLisbon_PreviousText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_MADRID, 6, 7
	waitstate
	release
	end
ShadowLisbon_PreviousText::
	.string "Travel to MADRID? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowLisbon_Route::
	lock
	faceplayer
	warp MAP_SHADOW_LISBON_ROUTE, 15, 20
	waitstate
	release
	end
ShadowLisbon_Trainer0::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 189
	trainerbattle_single 189, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowLisbon_Trainer1::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 190
	trainerbattle_single 190, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowLisbon_Trainer2::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 191
	trainerbattle_single 191, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowLisbon_Trainer3::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 192
	trainerbattle_single 192, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowLisbon_Trainer4::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 193
	trainerbattle_single 193, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowLisbon_Trainer5::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 194
	trainerbattle_single 194, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowLisbon_Rival::
	lock
	faceplayer
	msgbox ShadowLisbon_RivalText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 195
	trainerbattle_single 195, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	goto Shadow_End
ShadowLisbon_RivalText::
	.string "{RIVAL}: Training together\nhelped me learn. Shall we\pcompare our teams?$"
ShadowLisbon_RouteExit::
	lock
	faceplayer
	warp MAP_SHADOW_LISBON, 6, 7
	waitstate
	release
	end
ShadowLisbon_Keeper::
	lock
	faceplayer
	msgbox Shadow_PartnerText
	goto Shadow_End
	.include "data/maps/ShadowParis1940/scripts.inc"
	.include "data/maps/ShadowParis1940Route/scripts.inc"
ShadowParis1940_Mission::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 12, Shadow_Locked
	goto_if_gt VAR_SHADOW_STAGE, 12, ShadowParis1940_Done
	msgbox ShadowParis1940_Before, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	trainerbattle_single 196, ShadowParis1940_Intro, ShadowParis1940_Defeat, ShadowParis1940_Victory
	goto Shadow_End
ShadowParis1940_Victory::
	setvar VAR_SHADOW_STAGE, 13
ShadowParis1940_Done::
	msgbox ShadowParis1940_After
	goto Shadow_End
ShadowParis1940_Before::
	.string "MIREILLE: Nazi occupation forces\nseized our partners for a secret\pexperiment. We are the\nresistance. Drive off this\ppatrol so our courier can reach\na safe house. CELEBI waits\pbeside the return guide. Shall\nwe battle?$"
ShadowParis1940_After::
	.string "MIREILLE: The courier is safe.\nHer message names a transfer to\pWarsaw in 1943. CELEBI can\nfollow the clock's echoes. Our\pstruggle is for people and their\npartners, never for a flag.$"
ShadowParis1940_Intro::
	.string "Your partners are ready. Let us\nbegin.$"
ShadowParis1940_Defeat::
	.string "The battle is decided.$"
ShadowParis1940_Next::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 13, Shadow_Locked
	msgbox ShadowParis1940_NextText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_WARSAW1943, 6, 7
	waitstate
	release
	end
ShadowParis1940_NextText::
	.string "Travel to WARSAW1943? Your\nprogress is saved normally. Heal\pbefore leaving if you need to.$"
ShadowParis1940_Previous::
	lock
	faceplayer
	msgbox ShadowParis1940_PreviousText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_LISBON, 6, 7
	waitstate
	release
	end
ShadowParis1940_PreviousText::
	.string "Travel to LISBON? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowParis1940_Route::
	lock
	faceplayer
	warp MAP_SHADOW_PARIS1940_ROUTE, 15, 20
	waitstate
	release
	end
ShadowParis1940_Trainer0::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 197
	trainerbattle_single 197, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowParis1940_Trainer1::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 198
	trainerbattle_single 198, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowParis1940_Trainer2::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 199
	trainerbattle_single 199, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowParis1940_Trainer3::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 200
	trainerbattle_single 200, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowParis1940_Trainer4::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 201
	trainerbattle_single 201, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowParis1940_Trainer5::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 202
	trainerbattle_single 202, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowParis1940_RouteExit::
	lock
	faceplayer
	warp MAP_SHADOW_PARIS1940, 6, 7
	waitstate
	release
	end
ShadowParis1940_Keeper::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 13, Shadow_Locked
	setvar VAR_0x8004, 3
	setvar VAR_0x8005, SPECIES_MAREEP
	setvar VAR_0x8006, 43
	special Shadow_Rescue
	goto_if_eq VAR_RESULT, 1, Shadow_Rescued
	goto_if_eq VAR_RESULT, 2, Shadow_Full
	msgbox Shadow_AlreadyText
	goto Shadow_End
ShadowParis1940_Home::
	lock
	faceplayer
	msgbox Shadow_HomeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	warp MAP_SHADOW_LISBON, 6, 7
	waitstate
	release
	end
	.include "data/maps/ShadowWarsaw1943/scripts.inc"
	.include "data/maps/ShadowWarsaw1943Route/scripts.inc"
ShadowWarsaw1943_Mission::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 13, Shadow_Locked
	goto_if_gt VAR_SHADOW_STAGE, 13, ShadowWarsaw1943_Done
	msgbox ShadowWarsaw1943_Before, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	trainerbattle_single 203, ShadowWarsaw1943_Intro, ShadowWarsaw1943_Defeat, ShadowWarsaw1943_Victory
	goto Shadow_End
ShadowWarsaw1943_Victory::
	setvar VAR_SHADOW_STAGE, 14
ShadowWarsaw1943_Done::
	msgbox ShadowWarsaw1943_After
	goto Shadow_End
ShadowWarsaw1943_Before::
	.string "ZOFIA: The underground is moving\nfamilies away from a fictional\presearch depot. Disable its\nshadow controller while we open\pthe exit. The real occupation\nand persecution were human\pcrimes. Our rescue changes this\ninvented operation only. Shall\pwe battle?$"
ShadowWarsaw1943_After::
	.string "ZOFIA: Everyone in the safe\nhouse has a route out. The\pmachine's designer moved to\nBerlin. LENA, a German\presistance courier, can get you\ninto its service wing in 1944.$"
ShadowWarsaw1943_Intro::
	.string "Your partners are ready. Let us\nbegin.$"
ShadowWarsaw1943_Defeat::
	.string "The battle is decided.$"
ShadowWarsaw1943_Next::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 14, Shadow_Locked
	msgbox ShadowWarsaw1943_NextText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_BERLIN1944, 6, 7
	waitstate
	release
	end
ShadowWarsaw1943_NextText::
	.string "Travel to BERLIN1944? Your\nprogress is saved normally. Heal\pbefore leaving if you need to.$"
ShadowWarsaw1943_Previous::
	lock
	faceplayer
	msgbox ShadowWarsaw1943_PreviousText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_PARIS1940, 6, 7
	waitstate
	release
	end
ShadowWarsaw1943_PreviousText::
	.string "Travel to PARIS1940? Your\nprogress is saved normally. Heal\pbefore leaving if you need to.$"
ShadowWarsaw1943_Route::
	lock
	faceplayer
	warp MAP_SHADOW_WARSAW1943_ROUTE, 15, 20
	waitstate
	release
	end
ShadowWarsaw1943_Trainer0::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 204
	trainerbattle_single 204, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowWarsaw1943_Trainer1::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 205
	trainerbattle_single 205, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowWarsaw1943_Trainer2::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 206
	trainerbattle_single 206, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowWarsaw1943_Trainer3::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 207
	trainerbattle_single 207, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowWarsaw1943_Trainer4::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 208
	trainerbattle_single 208, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowWarsaw1943_Trainer5::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 209
	trainerbattle_single 209, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowWarsaw1943_RouteExit::
	lock
	faceplayer
	warp MAP_SHADOW_WARSAW1943, 6, 7
	waitstate
	release
	end
ShadowWarsaw1943_Keeper::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 14, Shadow_Locked
	setvar VAR_0x8004, 4
	setvar VAR_0x8005, SPECIES_LAPRAS
	setvar VAR_0x8006, 45
	special Shadow_Rescue
	goto_if_eq VAR_RESULT, 1, Shadow_Rescued
	goto_if_eq VAR_RESULT, 2, Shadow_Full
	msgbox Shadow_AlreadyText
	goto Shadow_End
ShadowWarsaw1943_Home::
	lock
	faceplayer
	msgbox Shadow_HomeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	warp MAP_SHADOW_LISBON, 6, 7
	waitstate
	release
	end
	.include "data/maps/ShadowBerlin1944/scripts.inc"
	.include "data/maps/ShadowBerlin1944Route/scripts.inc"
ShadowBerlin1944_Mission::
 lock
 faceplayer
 goto_if_ne VAR_EUROPE_HOME_COUNTRY, 3, ShadowBerlin1944_CoverReady
 msgbox Shadow_GermanCoverText
ShadowBerlin1944_CoverReady::
	goto_if_lt VAR_SHADOW_STAGE, 14, Shadow_Locked
	goto_if_gt VAR_SHADOW_STAGE, 14, ShadowBerlin1944_Done
	msgbox ShadowBerlin1944_Before, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	trainerbattle_single 210, ShadowBerlin1944_Intro, ShadowBerlin1944_Defeat, ShadowBerlin1944_Victory
	goto Shadow_End
ShadowBerlin1944_Victory::
	setvar VAR_SHADOW_STAGE, 15
ShadowBerlin1944_Done::
	msgbox ShadowBerlin1944_After
	goto Shadow_End
ShadowBerlin1944_Before::
	.string "LENA: I work inside the\nlaboratory for the resistance.\pYour cover is a repair courier.\nIf you started in Germany, your\plocal knowledge helps us verify\nthe papers. Once inside, refuse\ptheir orders and disable the\nmachine. I will evacuate the\ppartners. Shall we battle?$"
ShadowBerlin1944_After::
	.string "LENA: The controller is\ndestroyed. VEIL stole a copy,\pbut we kept the names of the\nresistance out of his hands. We\phelped this rescue succeed. The\nwar still has its real history.\pGo home and stop him.$"
ShadowBerlin1944_Intro::
	.string "Your partners are ready. Let us\nbegin.$"
ShadowBerlin1944_Defeat::
	.string "The battle is decided.$"
ShadowBerlin1944_Next::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 15, Shadow_Locked
	msgbox ShadowBerlin1944_NextText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_GENEVA, 6, 7
	waitstate
	release
	end
ShadowBerlin1944_NextText::
	.string "Travel to GENEVA? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowBerlin1944_Previous::
	lock
	faceplayer
	msgbox ShadowBerlin1944_PreviousText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_WARSAW1943, 6, 7
	waitstate
	release
	end
ShadowBerlin1944_PreviousText::
	.string "Travel to WARSAW1943? Your\nprogress is saved normally. Heal\pbefore leaving if you need to.$"
ShadowBerlin1944_Route::
	lock
	faceplayer
	warp MAP_SHADOW_BERLIN1944_ROUTE, 15, 20
	waitstate
	release
	end
ShadowBerlin1944_Trainer0::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 211
	trainerbattle_single 211, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowBerlin1944_Trainer1::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 212
	trainerbattle_single 212, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowBerlin1944_Trainer2::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 213
	trainerbattle_single 213, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowBerlin1944_Trainer3::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 214
	trainerbattle_single 214, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowBerlin1944_Trainer4::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 215
	trainerbattle_single 215, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowBerlin1944_Trainer5::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 216
	trainerbattle_single 216, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowBerlin1944_RouteExit::
	lock
	faceplayer
	warp MAP_SHADOW_BERLIN1944, 6, 7
	waitstate
	release
	end
ShadowBerlin1944_Keeper::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 15, Shadow_Locked
	setvar VAR_0x8004, 5
	setvar VAR_0x8005, SPECIES_DRATINI
	setvar VAR_0x8006, 47
	special Shadow_Rescue
	goto_if_eq VAR_RESULT, 1, Shadow_Rescued
	goto_if_eq VAR_RESULT, 2, Shadow_Full
	msgbox Shadow_AlreadyText
	goto Shadow_End
ShadowBerlin1944_Home::
	lock
	faceplayer
	msgbox Shadow_HomeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	warp MAP_SHADOW_LISBON, 6, 7
	waitstate
	release
	end
	.include "data/maps/ShadowGeneva/scripts.inc"
	.include "data/maps/ShadowGenevaRoute/scripts.inc"
ShadowGeneva_Mission::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 15, Shadow_Locked
	goto_if_gt VAR_SHADOW_STAGE, 15, ShadowGeneva_Done
	msgbox ShadowGeneva_Before, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	trainerbattle_single 217, ShadowGeneva_Intro, ShadowGeneva_Defeat, ShadowGeneva_Victory
	goto Shadow_End
ShadowGeneva_Victory::
	setvar VAR_SHADOW_STAGE, 16
ShadowGeneva_Done::
	msgbox ShadowGeneva_After
	goto Shadow_End
ShadowGeneva_Before::
	.string "VEIL: I brought the shadow\nfrequency back. One broadcast\pwill close every heart in the\nLeague. Your rival has shut the\pouter relays, but you will not\nreach the core. Shall we battle?$"
ShadowGeneva_After::
	.string "ADA: It is over. The broadcast\nis broken; the rescued partners\pcan heal. The archive will\npreserve the resistance accounts\pwith care. Your rival is waiting\nin Athens. Finish the journey\pyou began.$"
ShadowGeneva_Intro::
	.string "Your partners are ready. Let us\nbegin.$"
ShadowGeneva_Defeat::
	.string "The battle is decided.$"
ShadowGeneva_Next::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 16, Shadow_Locked
	msgbox ShadowGeneva_NextText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_ATHENS, 6, 7
	waitstate
	release
	end
ShadowGeneva_NextText::
	.string "Travel to ATHENS? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowGeneva_Previous::
	lock
	faceplayer
	msgbox ShadowGeneva_PreviousText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_BERLIN1944, 6, 7
	waitstate
	release
	end
ShadowGeneva_PreviousText::
	.string "Travel to BERLIN1944? Your\nprogress is saved normally. Heal\pbefore leaving if you need to.$"
ShadowGeneva_Route::
	lock
	faceplayer
	warp MAP_SHADOW_GENEVA_ROUTE, 15, 20
	waitstate
	release
	end
ShadowGeneva_Trainer0::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 218
	trainerbattle_single 218, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowGeneva_Trainer1::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 219
	trainerbattle_single 219, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowGeneva_Trainer2::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 220
	trainerbattle_single 220, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowGeneva_Trainer3::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 221
	trainerbattle_single 221, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowGeneva_Trainer4::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 222
	trainerbattle_single 222, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowGeneva_Trainer5::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 223
	trainerbattle_single 223, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowGeneva_RouteExit::
	lock
	faceplayer
	warp MAP_SHADOW_GENEVA, 6, 7
	waitstate
	release
	end
ShadowGeneva_Keeper::
	lock
	faceplayer
	msgbox Shadow_PartnerText
	goto Shadow_End
	.include "data/maps/ShadowAthens/scripts.inc"
	.include "data/maps/ShadowAthensRoute/scripts.inc"
ShadowAthens_Mission::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 16, Shadow_Locked
	goto_if_gt VAR_SHADOW_STAGE, 16, ShadowAthens_Done
	msgbox ShadowAthens_Before, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	trainerbattle_single 224, ShadowAthens_Intro, ShadowAthens_Defeat, ShadowAthens_Victory
	goto Shadow_End
ShadowAthens_Victory::
	setvar VAR_SHADOW_STAGE, 17
ShadowAthens_Done::
	msgbox ShadowAthens_After
	goto Shadow_End
ShadowAthens_Before::
	.string "THALIA: Welcome to the European\nLeague. Eight badges and the\pfreedom of your partners brought\nyou here. Four council members\pstand between you and the final\nrival match. Begin with ice.\pShall we battle?$"
ShadowAthens_After::
	.string "THALIA: First council match\ncomplete. Heal and rest if you\pneed to. NIKOS is waiting at the\nnext chamber.$"
ShadowAthens_Intro::
	.string "Your partners are ready. Let us\nbegin.$"
ShadowAthens_Defeat::
	.string "The battle is decided.$"
ShadowAthens_Next::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 17, Shadow_Locked
	msgbox ShadowAthens_NextText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_ATHENS2, 6, 7
	waitstate
	release
	end
ShadowAthens_NextText::
	.string "Travel to ATHENS2? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowAthens_Previous::
	lock
	faceplayer
	msgbox ShadowAthens_PreviousText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_GENEVA, 6, 7
	waitstate
	release
	end
ShadowAthens_PreviousText::
	.string "Travel to GENEVA? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowAthens_Route::
	lock
	faceplayer
	warp MAP_SHADOW_ATHENS_ROUTE, 15, 20
	waitstate
	release
	end
ShadowAthens_Trainer0::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 225
	trainerbattle_single 225, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAthens_Trainer1::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 226
	trainerbattle_single 226, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAthens_Trainer2::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 227
	trainerbattle_single 227, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAthens_Trainer3::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 228
	trainerbattle_single 228, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAthens_Trainer4::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 229
	trainerbattle_single 229, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAthens_Trainer5::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 230
	trainerbattle_single 230, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAthens_RouteExit::
	lock
	faceplayer
	warp MAP_SHADOW_ATHENS, 6, 7
	waitstate
	release
	end
ShadowAthens_Keeper::
	lock
	faceplayer
	msgbox Shadow_PartnerText
	goto Shadow_End
	.include "data/maps/ShadowAthens2/scripts.inc"
	.include "data/maps/ShadowAthens2Route/scripts.inc"
ShadowAthens2_Mission::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 17, Shadow_Locked
	goto_if_gt VAR_SHADOW_STAGE, 17, ShadowAthens2_Done
	msgbox ShadowAthens2_Before, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	trainerbattle_single 231, ShadowAthens2_Intro, ShadowAthens2_Defeat, ShadowAthens2_Victory
	goto Shadow_End
ShadowAthens2_Victory::
	setvar VAR_SHADOW_STAGE, 18
ShadowAthens2_Done::
	msgbox ShadowAthens2_After
	goto Shadow_End
ShadowAthens2_Before::
	.string "NIKOS: Strength is what you\nchoose to protect. My fighting\pteam will test how you turn that\nchoice into action. Shall we\pbattle?$"
ShadowAthens2_After::
	.string "NIKOS: You passed. ELENI studies\nthe fears that remain after a\pbattle. She is your next\nopponent.$"
ShadowAthens2_Intro::
	.string "Your partners are ready. Let us\nbegin.$"
ShadowAthens2_Defeat::
	.string "The battle is decided.$"
ShadowAthens2_Next::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 18, Shadow_Locked
	msgbox ShadowAthens2_NextText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_ATHENS3, 6, 7
	waitstate
	release
	end
ShadowAthens2_NextText::
	.string "Travel to ATHENS3? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowAthens2_Previous::
	lock
	faceplayer
	msgbox ShadowAthens2_PreviousText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_ATHENS, 6, 7
	waitstate
	release
	end
ShadowAthens2_PreviousText::
	.string "Travel to ATHENS? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowAthens2_Route::
	lock
	faceplayer
	warp MAP_SHADOW_ATHENS2_ROUTE, 15, 20
	waitstate
	release
	end
ShadowAthens2_Trainer0::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 232
	trainerbattle_single 232, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAthens2_Trainer1::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 233
	trainerbattle_single 233, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAthens2_Trainer2::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 234
	trainerbattle_single 234, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAthens2_Trainer3::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 235
	trainerbattle_single 235, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAthens2_Trainer4::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 236
	trainerbattle_single 236, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAthens2_Trainer5::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 237
	trainerbattle_single 237, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAthens2_RouteExit::
	lock
	faceplayer
	warp MAP_SHADOW_ATHENS2, 6, 7
	waitstate
	release
	end
ShadowAthens2_Keeper::
	lock
	faceplayer
	msgbox Shadow_PartnerText
	goto Shadow_End
	.include "data/maps/ShadowAthens3/scripts.inc"
	.include "data/maps/ShadowAthens3Route/scripts.inc"
ShadowAthens3_Mission::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 18, Shadow_Locked
	goto_if_gt VAR_SHADOW_STAGE, 18, ShadowAthens3_Done
	msgbox ShadowAthens3_Before, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	trainerbattle_single 238, ShadowAthens3_Intro, ShadowAthens3_Defeat, ShadowAthens3_Victory
	goto Shadow_End
ShadowAthens3_Victory::
	setvar VAR_SHADOW_STAGE, 19
ShadowAthens3_Done::
	msgbox ShadowAthens3_After
	goto Shadow_End
ShadowAthens3_Before::
	.string "ELENI: Darkness is not a fault\nin a partner. A closed heart is\pan injury. Our ghost and psychic\nteams have learned to trust\pagain. Show me your team's\ncourage. Shall we battle?$"
ShadowAthens3_After::
	.string "ELENI: Your partners know you\nwill stay with them. LEON waits\pin the dragon chamber.$"
ShadowAthens3_Intro::
	.string "Your partners are ready. Let us\nbegin.$"
ShadowAthens3_Defeat::
	.string "The battle is decided.$"
ShadowAthens3_Next::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 19, Shadow_Locked
	msgbox ShadowAthens3_NextText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_ATHENS4, 6, 7
	waitstate
	release
	end
ShadowAthens3_NextText::
	.string "Travel to ATHENS4? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowAthens3_Previous::
	lock
	faceplayer
	msgbox ShadowAthens3_PreviousText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_ATHENS2, 6, 7
	waitstate
	release
	end
ShadowAthens3_PreviousText::
	.string "Travel to ATHENS2? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowAthens3_Route::
	lock
	faceplayer
	warp MAP_SHADOW_ATHENS3_ROUTE, 15, 20
	waitstate
	release
	end
ShadowAthens3_Trainer0::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 239
	trainerbattle_single 239, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAthens3_Trainer1::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 240
	trainerbattle_single 240, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAthens3_Trainer2::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 241
	trainerbattle_single 241, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAthens3_Trainer3::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 242
	trainerbattle_single 242, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAthens3_Trainer4::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 243
	trainerbattle_single 243, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAthens3_Trainer5::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 244
	trainerbattle_single 244, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAthens3_RouteExit::
	lock
	faceplayer
	warp MAP_SHADOW_ATHENS3, 6, 7
	waitstate
	release
	end
ShadowAthens3_Keeper::
	lock
	faceplayer
	msgbox Shadow_PartnerText
	goto Shadow_End
	.include "data/maps/ShadowAthens4/scripts.inc"
	.include "data/maps/ShadowAthens4Route/scripts.inc"
ShadowAthens4_Mission::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 19, Shadow_Locked
	goto_if_gt VAR_SHADOW_STAGE, 19, ShadowAthens4_Done
	msgbox ShadowAthens4_Before, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	trainerbattle_single 245, ShadowAthens4_Intro, ShadowAthens4_Defeat, ShadowAthens4_Victory
	goto Shadow_End
ShadowAthens4_Victory::
	setvar VAR_SHADOW_STAGE, 20
ShadowAthens4_Done::
	msgbox ShadowAthens4_After
	goto Shadow_End
ShadowAthens4_Before::
	.string "LEON: You have crossed countries\nand centuries. One last council\pmatch. Do not mistake a powerful\npartner for a tool. Shall we\pbattle?$"
ShadowAthens4_After::
	.string "LEON: The council recognizes\nyou. Your rival reached the\pchampion's chamber first. Go\nmeet them as equals.$"
ShadowAthens4_Intro::
	.string "Your partners are ready. Let us\nbegin.$"
ShadowAthens4_Defeat::
	.string "The battle is decided.$"
ShadowAthens4_Next::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 20, Shadow_Locked
	msgbox ShadowAthens4_NextText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_CHAMPION, 6, 7
	waitstate
	release
	end
ShadowAthens4_NextText::
	.string "Travel to CHAMPION? Your\nprogress is saved normally. Heal\pbefore leaving if you need to.$"
ShadowAthens4_Previous::
	lock
	faceplayer
	msgbox ShadowAthens4_PreviousText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_ATHENS3, 6, 7
	waitstate
	release
	end
ShadowAthens4_PreviousText::
	.string "Travel to ATHENS3? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowAthens4_Route::
	lock
	faceplayer
	warp MAP_SHADOW_ATHENS4_ROUTE, 15, 20
	waitstate
	release
	end
ShadowAthens4_Trainer0::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 246
	trainerbattle_single 246, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAthens4_Trainer1::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 247
	trainerbattle_single 247, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAthens4_Trainer2::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 248
	trainerbattle_single 248, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAthens4_Trainer3::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 249
	trainerbattle_single 249, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAthens4_Trainer4::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 250
	trainerbattle_single 250, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAthens4_Trainer5::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 251
	trainerbattle_single 251, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowAthens4_RouteExit::
	lock
	faceplayer
	warp MAP_SHADOW_ATHENS4, 6, 7
	waitstate
	release
	end
ShadowAthens4_Keeper::
	lock
	faceplayer
	msgbox Shadow_PartnerText
	goto Shadow_End
	.include "data/maps/ShadowChampion/scripts.inc"
	.include "data/maps/ShadowChampionRoute/scripts.inc"
ShadowChampion_Mission::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 20, Shadow_Locked
	goto_if_gt VAR_SHADOW_STAGE, 20, ShadowChampion_Done
	msgbox ShadowChampion_Before, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	trainerbattle_single 252, ShadowChampion_Intro, ShadowChampion_Defeat, ShadowChampion_Victory
	goto Shadow_End
ShadowChampion_Victory::
	setvar VAR_SHADOW_STAGE, 21
	setflag FLAG_SYS_GAME_CLEAR
ShadowChampion_Done::
	msgbox ShadowChampion_After
	fadescreen FADE_TO_BLACK
	special Shadow_ShowCredits
	waitstate
	goto Shadow_End
ShadowChampion_Before::
	.string "{RIVAL}: I used to think a\nchampion stood alone. Now I know\pwho helped me get here. No\nsecrets, no stolen strength. One\phonest match between us. Ready?\nShall we battle?$"
ShadowChampion_After::
	.string "{RIVAL}: You are the EUROPEAN\nCHAMPION! ADA records our\pjourney: eight badges, partners\nrescued, a resistance network\pprotected, and ECLIPSE defeated.\nCELEBI returns to its forest.\pThe shelters remain open. We\nwill keep traveling together.\pTHE END.$"
ShadowChampion_Intro::
	.string "Your partners are ready. Let us\nbegin.$"
ShadowChampion_Defeat::
	.string "The battle is decided.$"
ShadowChampion_Next::
	lock
	faceplayer
	goto_if_lt VAR_SHADOW_STAGE, 21, Shadow_Locked
	msgbox ShadowChampion_NextText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_CHAMPION, 6, 7
	waitstate
	release
	end
ShadowChampion_NextText::
	.string "Travel to CHAMPION? Your\nprogress is saved normally. Heal\pbefore leaving if you need to.$"
ShadowChampion_Previous::
	lock
	faceplayer
	msgbox ShadowChampion_PreviousText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	closemessage
	warp MAP_SHADOW_ATHENS4, 6, 7
	waitstate
	release
	end
ShadowChampion_PreviousText::
	.string "Travel to ATHENS4? Your progress\nis saved normally. Heal before\pleaving if you need to.$"
ShadowChampion_Route::
	lock
	faceplayer
	warp MAP_SHADOW_CHAMPION_ROUTE, 15, 20
	waitstate
	release
	end
ShadowChampion_Trainer0::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 253
	trainerbattle_single 253, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowChampion_Trainer1::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 254
	trainerbattle_single 254, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowChampion_Trainer2::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 255
	trainerbattle_single 255, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowChampion_Trainer3::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 256
	trainerbattle_single 256, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowChampion_Trainer4::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 257
	trainerbattle_single 257, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowChampion_Trainer5::
	lock
	faceplayer
	msgbox Shadow_PracticeText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Shadow_End
	cleartrainerflag 258
	trainerbattle_single 258, Shadow_PracticeIntroText, Shadow_PracticeDefeatText
	msgbox Shadow_PracticeAfterText
	goto Shadow_End
ShadowChampion_RouteExit::
	lock
	faceplayer
	warp MAP_SHADOW_CHAMPION, 6, 7
	waitstate
	release
	end
ShadowChampion_Keeper::
	lock
	faceplayer
	msgbox Shadow_PartnerText
	goto Shadow_End

Shadow_BaseReturn::
 lock
 faceplayer
 msgbox Shadow_BaseReturnText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 warp MAP_EUROPE_LONDON, 15, 14
 waitstate
 release
 end
Shadow_BaseReturnText::
 .string "Return to modern LONDON?\nYour campaign progress stays saved.\pThe aide can resume your chapter.\nThe clinic has a POKEMON PC.$"

ShadowAmsterdamRoute_Visible::
 lock
 faceplayer
 msgbox ShadowAmsterdamRoute_VisibleText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 special Shadow_StartVisible
 dowildbattle
 removeobject VAR_LAST_TALKED
 release
 end
ShadowAmsterdamRoute_VisibleText::
 .string "A wild POKEMON is here.\nApproach it for a battle?\pYou can catch it with a POKE BALL.\nChoose NO to leave it in peace.$"

ShadowAthens2Route_Visible::
 lock
 faceplayer
 msgbox ShadowAthens2Route_VisibleText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 special Shadow_StartVisible
 dowildbattle
 removeobject VAR_LAST_TALKED
 release
 end
ShadowAthens2Route_VisibleText::
 .string "A wild POKEMON is here.\nApproach it for a battle?\pYou can catch it with a POKE BALL.\nChoose NO to leave it in peace.$"

ShadowAthens3Route_Visible::
 lock
 faceplayer
 msgbox ShadowAthens3Route_VisibleText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 special Shadow_StartVisible
 dowildbattle
 removeobject VAR_LAST_TALKED
 release
 end
ShadowAthens3Route_VisibleText::
 .string "A wild POKEMON is here.\nApproach it for a battle?\pYou can catch it with a POKE BALL.\nChoose NO to leave it in peace.$"

ShadowAthens4Route_Visible::
 lock
 faceplayer
 msgbox ShadowAthens4Route_VisibleText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 special Shadow_StartVisible
 dowildbattle
 removeobject VAR_LAST_TALKED
 release
 end
ShadowAthens4Route_VisibleText::
 .string "A wild POKEMON is here.\nApproach it for a battle?\pYou can catch it with a POKE BALL.\nChoose NO to leave it in peace.$"

ShadowAthensRoute_Visible::
 lock
 faceplayer
 msgbox ShadowAthensRoute_VisibleText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 special Shadow_StartVisible
 dowildbattle
 removeobject VAR_LAST_TALKED
 release
 end
ShadowAthensRoute_VisibleText::
 .string "A wild POKEMON is here.\nApproach it for a battle?\pYou can catch it with a POKE BALL.\nChoose NO to leave it in peace.$"

ShadowBerlin1944Route_Visible::
 lock
 faceplayer
 msgbox ShadowBerlin1944Route_VisibleText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 special Shadow_StartVisible
 dowildbattle
 removeobject VAR_LAST_TALKED
 release
 end
ShadowBerlin1944Route_VisibleText::
 .string "A wild POKEMON is here.\nApproach it for a battle?\pYou can catch it with a POKE BALL.\nChoose NO to leave it in peace.$"

ShadowBerlinRoute_Visible::
 lock
 faceplayer
 msgbox ShadowBerlinRoute_VisibleText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 special Shadow_StartVisible
 dowildbattle
 removeobject VAR_LAST_TALKED
 release
 end
ShadowBerlinRoute_VisibleText::
 .string "A wild POKEMON is here.\nApproach it for a battle?\pYou can catch it with a POKE BALL.\nChoose NO to leave it in peace.$"

ShadowBrusselsRoute_Visible::
 lock
 faceplayer
 msgbox ShadowBrusselsRoute_VisibleText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 special Shadow_StartVisible
 dowildbattle
 removeobject VAR_LAST_TALKED
 release
 end
ShadowBrusselsRoute_VisibleText::
 .string "A wild POKEMON is here.\nApproach it for a battle?\pYou can catch it with a POKE BALL.\nChoose NO to leave it in peace.$"

ShadowChampionRoute_Visible::
 lock
 faceplayer
 msgbox ShadowChampionRoute_VisibleText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 special Shadow_StartVisible
 dowildbattle
 removeobject VAR_LAST_TALKED
 release
 end
ShadowChampionRoute_VisibleText::
 .string "A wild POKEMON is here.\nApproach it for a battle?\pYou can catch it with a POKE BALL.\nChoose NO to leave it in peace.$"

ShadowGenevaRoute_Visible::
 lock
 faceplayer
 msgbox ShadowGenevaRoute_VisibleText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 special Shadow_StartVisible
 dowildbattle
 removeobject VAR_LAST_TALKED
 release
 end
ShadowGenevaRoute_VisibleText::
 .string "A wild POKEMON is here.\nApproach it for a battle?\pYou can catch it with a POKE BALL.\nChoose NO to leave it in peace.$"

ShadowLisbonRoute_Visible::
 lock
 faceplayer
 msgbox ShadowLisbonRoute_VisibleText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 special Shadow_StartVisible
 dowildbattle
 removeobject VAR_LAST_TALKED
 release
 end
ShadowLisbonRoute_VisibleText::
 .string "A wild POKEMON is here.\nApproach it for a battle?\pYou can catch it with a POKE BALL.\nChoose NO to leave it in peace.$"

ShadowLondonRoute_Visible::
 lock
 faceplayer
 msgbox ShadowLondonRoute_VisibleText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 special Shadow_StartVisible
 dowildbattle
 removeobject VAR_LAST_TALKED
 release
 end
ShadowLondonRoute_VisibleText::
 .string "A wild POKEMON is here.\nApproach it for a battle?\pYou can catch it with a POKE BALL.\nChoose NO to leave it in peace.$"

ShadowMadridRoute_Visible::
 lock
 faceplayer
 msgbox ShadowMadridRoute_VisibleText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 special Shadow_StartVisible
 dowildbattle
 removeobject VAR_LAST_TALKED
 release
 end
ShadowMadridRoute_VisibleText::
 .string "A wild POKEMON is here.\nApproach it for a battle?\pYou can catch it with a POKE BALL.\nChoose NO to leave it in peace.$"

ShadowOxfordRoute_Visible::
 lock
 faceplayer
 msgbox ShadowOxfordRoute_VisibleText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 special Shadow_StartVisible
 dowildbattle
 removeobject VAR_LAST_TALKED
 release
 end
ShadowOxfordRoute_VisibleText::
 .string "A wild POKEMON is here.\nApproach it for a battle?\pYou can catch it with a POKE BALL.\nChoose NO to leave it in peace.$"

ShadowParis1940Route_Visible::
 lock
 faceplayer
 msgbox ShadowParis1940Route_VisibleText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 special Shadow_StartVisible
 dowildbattle
 removeobject VAR_LAST_TALKED
 release
 end
ShadowParis1940Route_VisibleText::
 .string "A wild POKEMON is here.\nApproach it for a battle?\pYou can catch it with a POKE BALL.\nChoose NO to leave it in peace.$"

ShadowParisRoute_Visible::
 lock
 faceplayer
 msgbox ShadowParisRoute_VisibleText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 special Shadow_StartVisible
 dowildbattle
 removeobject VAR_LAST_TALKED
 release
 end
ShadowParisRoute_VisibleText::
 .string "A wild POKEMON is here.\nApproach it for a battle?\pYou can catch it with a POKE BALL.\nChoose NO to leave it in peace.$"

ShadowPragueRoute_Visible::
 lock
 faceplayer
 msgbox ShadowPragueRoute_VisibleText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 special Shadow_StartVisible
 dowildbattle
 removeobject VAR_LAST_TALKED
 release
 end
ShadowPragueRoute_VisibleText::
 .string "A wild POKEMON is here.\nApproach it for a battle?\pYou can catch it with a POKE BALL.\nChoose NO to leave it in peace.$"

ShadowRomeRoute_Visible::
 lock
 faceplayer
 msgbox ShadowRomeRoute_VisibleText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 special Shadow_StartVisible
 dowildbattle
 removeobject VAR_LAST_TALKED
 release
 end
ShadowRomeRoute_VisibleText::
 .string "A wild POKEMON is here.\nApproach it for a battle?\pYou can catch it with a POKE BALL.\nChoose NO to leave it in peace.$"

ShadowViennaRoute_Visible::
 lock
 faceplayer
 msgbox ShadowViennaRoute_VisibleText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 special Shadow_StartVisible
 dowildbattle
 removeobject VAR_LAST_TALKED
 release
 end
ShadowViennaRoute_VisibleText::
 .string "A wild POKEMON is here.\nApproach it for a battle?\pYou can catch it with a POKE BALL.\nChoose NO to leave it in peace.$"

ShadowWarsaw1943Route_Visible::
 lock
 faceplayer
 msgbox ShadowWarsaw1943Route_VisibleText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 special Shadow_StartVisible
 dowildbattle
 removeobject VAR_LAST_TALKED
 release
 end
ShadowWarsaw1943Route_VisibleText::
 .string "A wild POKEMON is here.\nApproach it for a battle?\pYou can catch it with a POKE BALL.\nChoose NO to leave it in peace.$"

ShadowZurichRoute_Visible::
 lock
 faceplayer
 msgbox ShadowZurichRoute_VisibleText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 special Shadow_StartVisible
 dowildbattle
 removeobject VAR_LAST_TALKED
 release
 end
ShadowZurichRoute_VisibleText::
 .string "A wild POKEMON is here.\nApproach it for a battle?\pYou can catch it with a POKE BALL.\nChoose NO to leave it in peace.$"

Shadow_GermanCoverText::
 .string "LENA: Your German hometown\nhelps our courier cover hold.\pYou are working for the resistance.\nGet in, then stop the experiment.\pNo order from the Nazis changes\nwho we came here to protect.$"

 .include "data/maps/ContinentLondon/scripts.inc"
 .include "data/maps/ContinentLondonPast/scripts.inc"
 .include "data/maps/ContinentParis/scripts.inc"
 .include "data/maps/ContinentParisPast/scripts.inc"
 .include "data/maps/ContinentBerlin/scripts.inc"
 .include "data/maps/ContinentBerlinPast/scripts.inc"
 .include "data/maps/ContinentBrussels/scripts.inc"
 .include "data/maps/ContinentBrusselsPast/scripts.inc"
 .include "data/maps/ContinentAmsterdam/scripts.inc"
 .include "data/maps/ContinentAmsterdamPast/scripts.inc"
 .include "data/maps/ContinentVienna/scripts.inc"
 .include "data/maps/ContinentViennaPast/scripts.inc"
 .include "data/maps/ContinentPrague/scripts.inc"
 .include "data/maps/ContinentPraguePast/scripts.inc"
 .include "data/maps/ContinentBratislava/scripts.inc"
 .include "data/maps/ContinentBratislavaPast/scripts.inc"
 .include "data/maps/ContinentBern/scripts.inc"
 .include "data/maps/ContinentBernPast/scripts.inc"
 .include "data/maps/ContinentRome/scripts.inc"
 .include "data/maps/ContinentRomePast/scripts.inc"
 .include "data/maps/ContinentAthens/scripts.inc"
 .include "data/maps/ContinentAthensPast/scripts.inc"
 .include "data/maps/ContinentMadrid/scripts.inc"
 .include "data/maps/ContinentMadridPast/scripts.inc"
 .include "data/maps/ContinentLisbon/scripts.inc"
 .include "data/maps/ContinentLisbonPast/scripts.inc"
 .include "data/maps/ContinentWarsaw/scripts.inc"
 .include "data/maps/ContinentWarsawPast/scripts.inc"
 .include "data/maps/ContinentLuxembourg/scripts.inc"
 .include "data/maps/ContinentLuxembourgPast/scripts.inc"
 .include "data/maps/ContinentCopenhagen/scripts.inc"
 .include "data/maps/ContinentCopenhagenPast/scripts.inc"
 .include "data/maps/ContinentOslo/scripts.inc"
 .include "data/maps/ContinentOsloPast/scripts.inc"
 .include "data/maps/ContinentStockholm/scripts.inc"
 .include "data/maps/ContinentStockholmPast/scripts.inc"
 .include "data/maps/ContinentHelsinki/scripts.inc"
 .include "data/maps/ContinentHelsinkiPast/scripts.inc"
 .include "data/maps/ContinentReykjavik/scripts.inc"
 .include "data/maps/ContinentReykjavikPast/scripts.inc"
 .include "data/maps/ContinentDublin/scripts.inc"
 .include "data/maps/ContinentDublinPast/scripts.inc"
 .include "data/maps/ContinentValletta/scripts.inc"
 .include "data/maps/ContinentVallettaPast/scripts.inc"
 .include "data/maps/ContinentBudapest/scripts.inc"
 .include "data/maps/ContinentBudapestPast/scripts.inc"
 .include "data/maps/ContinentBucharest/scripts.inc"
 .include "data/maps/ContinentBucharestPast/scripts.inc"
 .include "data/maps/ContinentSofia/scripts.inc"
 .include "data/maps/ContinentSofiaPast/scripts.inc"
 .include "data/maps/ContinentTirana/scripts.inc"
 .include "data/maps/ContinentTiranaPast/scripts.inc"
 .include "data/maps/ContinentBelgrade/scripts.inc"
 .include "data/maps/ContinentBelgradePast/scripts.inc"
 .include "data/maps/ContinentZagreb/scripts.inc"
 .include "data/maps/ContinentZagrebPast/scripts.inc"
 .include "data/maps/ContinentLjubljana/scripts.inc"
 .include "data/maps/ContinentLjubljanaPast/scripts.inc"
 .include "data/maps/ContinentSarajevo/scripts.inc"
 .include "data/maps/ContinentSarajevoPast/scripts.inc"
 .include "data/maps/ContinentKotor/scripts.inc"
 .include "data/maps/ContinentKotorPast/scripts.inc"
 .include "data/maps/ContinentSkopje/scripts.inc"
 .include "data/maps/ContinentSkopjePast/scripts.inc"
 .include "data/maps/ContinentMoscow/scripts.inc"
 .include "data/maps/ContinentMoscowPast/scripts.inc"
 .include "data/maps/ContinentKyiv/scripts.inc"
 .include "data/maps/ContinentKyivPast/scripts.inc"
 .include "data/maps/ContinentMinsk/scripts.inc"
 .include "data/maps/ContinentMinskPast/scripts.inc"
 .include "data/maps/ContinentVilnius/scripts.inc"
 .include "data/maps/ContinentVilniusPast/scripts.inc"
 .include "data/maps/ContinentRiga/scripts.inc"
 .include "data/maps/ContinentRigaPast/scripts.inc"
 .include "data/maps/ContinentTallinn/scripts.inc"
 .include "data/maps/ContinentTallinnPast/scripts.inc"
 .include "data/maps/ContinentIstanbul/scripts.inc"
 .include "data/maps/ContinentIstanbulPast/scripts.inc"

ContinentLondon_Landmark::
 msgbox ContinentLondon_LandmarkText, MSGBOX_SIGN
 end
ContinentLondon_LandmarkText::
 .string "BIG BEN - LONDON. This is a\ncompact landmark district. The\pstation is south; trainers are\nalong the garden paths.$"
ContinentLondon_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentLondon_KeeperText
 goto Shadow_End
ContinentLondon_KeeperText::
 .string "ADA's network reached London.\nWin the local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentLondon_Battle0::
 lock
 faceplayer
 msgbox ContinentLondon_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 259, ContinentLondon_Battle0Intro, ContinentLondon_Battle0Defeat, ContinentLondon_Battle0Won
ContinentLondon_Battle0Won::
 msgbox ContinentLondon_Battle0After
 goto Shadow_End
ContinentLondon_Battle0Intro::
 .string "London LEAGUE: Our island\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentLondon_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentLondon_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentLondon_Battle1::
 lock
 faceplayer
 msgbox ContinentLondon_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 260, ContinentLondon_Battle1Intro, ContinentLondon_Battle1Defeat, ContinentLondon_Battle1Won
ContinentLondon_Battle1Won::
 msgbox ContinentLondon_Battle1After
 goto Shadow_End
ContinentLondon_Battle1Intro::
 .string "London LEAGUE: Our island\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentLondon_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentLondon_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentLondonPast_Landmark::
 msgbox ContinentLondonPast_LandmarkText, MSGBOX_SIGN
 end
ContinentLondonPast_LandmarkText::
 .string "BIG BEN - LONDON. This is a\ncompact landmark district. The\pstation is south; trainers are\nalong the garden paths. You are\pvisiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentLondonPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentLondonPast_Battle0::
 lock
 faceplayer
 msgbox ContinentLondonPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 261, ContinentLondonPast_Battle0Intro, ContinentLondonPast_Battle0Defeat, ContinentLondonPast_Battle0Won
ContinentLondonPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentLondonPast_Battle0After
 goto Shadow_End
ContinentLondonPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pLondon's couriers. Help us stop\nthe experiment?$"
ContinentLondonPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentLondonPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentParis_Landmark::
 msgbox ContinentParis_LandmarkText, MSGBOX_SIGN
 end
ContinentParis_LandmarkText::
 .string "NOTRE-DAME - PARIS. This is a\ncompact landmark district. The\pstation is south; trainers are\nalong the garden paths.$"
ContinentParis_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentParis_KeeperText
 goto Shadow_End
ContinentParis_KeeperText::
 .string "ADA's network reached Paris.\nWin the local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentParis_Battle0::
 lock
 faceplayer
 msgbox ContinentParis_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 262, ContinentParis_Battle0Intro, ContinentParis_Battle0Defeat, ContinentParis_Battle0Won
ContinentParis_Battle0Won::
 msgbox ContinentParis_Battle0After
 goto Shadow_End
ContinentParis_Battle0Intro::
 .string "Paris LEAGUE: Our river circuit\nwelcomes travelers. Ready for a\plocal battle?$"
ContinentParis_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentParis_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentParis_Battle1::
 lock
 faceplayer
 msgbox ContinentParis_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 263, ContinentParis_Battle1Intro, ContinentParis_Battle1Defeat, ContinentParis_Battle1Won
ContinentParis_Battle1Won::
 msgbox ContinentParis_Battle1After
 goto Shadow_End
ContinentParis_Battle1Intro::
 .string "Paris LEAGUE: Our river circuit\nwelcomes travelers. Ready for a\plocal battle?$"
ContinentParis_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentParis_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentParisPast_Landmark::
 msgbox ContinentParisPast_LandmarkText, MSGBOX_SIGN
 end
ContinentParisPast_LandmarkText::
 .string "NOTRE-DAME - PARIS. This is a\ncompact landmark district. The\pstation is south; trainers are\nalong the garden paths. You are\pvisiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentParisPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentParisPast_Battle0::
 lock
 faceplayer
 msgbox ContinentParisPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 264, ContinentParisPast_Battle0Intro, ContinentParisPast_Battle0Defeat, ContinentParisPast_Battle0Won
ContinentParisPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentParisPast_Battle0After
 goto Shadow_End
ContinentParisPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pParis's couriers. Help us stop\nthe experiment?$"
ContinentParisPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentParisPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentBerlin_Landmark::
 msgbox ContinentBerlin_LandmarkText, MSGBOX_SIGN
 end
ContinentBerlin_LandmarkText::
 .string "BRANDENBURG GATE - BERLIN. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths.$"
ContinentBerlin_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentBerlin_KeeperText
 goto Shadow_End
ContinentBerlin_KeeperText::
 .string "ADA's network reached Berlin.\nWin the local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentBerlin_Battle0::
 lock
 faceplayer
 msgbox ContinentBerlin_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 265, ContinentBerlin_Battle0Intro, ContinentBerlin_Battle0Defeat, ContinentBerlin_Battle0Won
ContinentBerlin_Battle0Won::
 msgbox ContinentBerlin_Battle0After
 goto Shadow_End
ContinentBerlin_Battle0Intro::
 .string "Berlin LEAGUE: Our river\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentBerlin_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentBerlin_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentBerlin_Battle1::
 lock
 faceplayer
 msgbox ContinentBerlin_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 266, ContinentBerlin_Battle1Intro, ContinentBerlin_Battle1Defeat, ContinentBerlin_Battle1Won
ContinentBerlin_Battle1Won::
 msgbox ContinentBerlin_Battle1After
 goto Shadow_End
ContinentBerlin_Battle1Intro::
 .string "Berlin LEAGUE: Our river\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentBerlin_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentBerlin_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentBerlinPast_Landmark::
 msgbox ContinentBerlinPast_LandmarkText, MSGBOX_SIGN
 end
ContinentBerlinPast_LandmarkText::
 .string "BRANDENBURG GATE - BERLIN. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths. You\pare visiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentBerlinPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentBerlinPast_Battle0::
 lock
 faceplayer
 msgbox ContinentBerlinPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 267, ContinentBerlinPast_Battle0Intro, ContinentBerlinPast_Battle0Defeat, ContinentBerlinPast_Battle0Won
ContinentBerlinPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentBerlinPast_Battle0After
 goto Shadow_End
ContinentBerlinPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pBerlin's couriers. Help us stop\nthe experiment?$"
ContinentBerlinPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentBerlinPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentBrussels_Landmark::
 msgbox ContinentBrussels_LandmarkText, MSGBOX_SIGN
 end
ContinentBrussels_LandmarkText::
 .string "GRAND PLACE - BRUSSELS. This is\na compact landmark district.\pThe station is south; trainers\nare along the garden paths.$"
ContinentBrussels_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentBrussels_KeeperText
 goto Shadow_End
ContinentBrussels_KeeperText::
 .string "ADA's network reached Brussels.\nWin the local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentBrussels_Battle0::
 lock
 faceplayer
 msgbox ContinentBrussels_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 268, ContinentBrussels_Battle0Intro, ContinentBrussels_Battle0Defeat, ContinentBrussels_Battle0Won
ContinentBrussels_Battle0Won::
 msgbox ContinentBrussels_Battle0After
 goto Shadow_End
ContinentBrussels_Battle0Intro::
 .string "Brussels LEAGUE: Our garden\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentBrussels_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentBrussels_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentBrussels_Battle1::
 lock
 faceplayer
 msgbox ContinentBrussels_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 269, ContinentBrussels_Battle1Intro, ContinentBrussels_Battle1Defeat, ContinentBrussels_Battle1Won
ContinentBrussels_Battle1Won::
 msgbox ContinentBrussels_Battle1After
 goto Shadow_End
ContinentBrussels_Battle1Intro::
 .string "Brussels LEAGUE: Our garden\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentBrussels_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentBrussels_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentBrusselsPast_Landmark::
 msgbox ContinentBrusselsPast_LandmarkText, MSGBOX_SIGN
 end
ContinentBrusselsPast_LandmarkText::
 .string "GRAND PLACE - BRUSSELS. This is\na compact landmark district.\pThe station is south; trainers\nare along the garden paths. You\pare visiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentBrusselsPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentBrusselsPast_Battle0::
 lock
 faceplayer
 msgbox ContinentBrusselsPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 270, ContinentBrusselsPast_Battle0Intro, ContinentBrusselsPast_Battle0Defeat, ContinentBrusselsPast_Battle0Won
ContinentBrusselsPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentBrusselsPast_Battle0After
 goto Shadow_End
ContinentBrusselsPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pBrussels's couriers. Help us\nstop the experiment?$"
ContinentBrusselsPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentBrusselsPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentAmsterdam_Landmark::
 msgbox ContinentAmsterdam_LandmarkText, MSGBOX_SIGN
 end
ContinentAmsterdam_LandmarkText::
 .string "CANAL HOUSES - AMSTERDAM. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths.$"
ContinentAmsterdam_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentAmsterdam_KeeperText
 goto Shadow_End
ContinentAmsterdam_KeeperText::
 .string "ADA's network reached\nAmsterdam. Win the local\pmatches, then use CELEBI after\nthe Lisbon chapter to visit the\ppast. We are waiting for news\nof our old sanctuary and its\pmissing ledger.$"
ContinentAmsterdam_Battle0::
 lock
 faceplayer
 msgbox ContinentAmsterdam_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 271, ContinentAmsterdam_Battle0Intro, ContinentAmsterdam_Battle0Defeat, ContinentAmsterdam_Battle0Won
ContinentAmsterdam_Battle0Won::
 msgbox ContinentAmsterdam_Battle0After
 goto Shadow_End
ContinentAmsterdam_Battle0Intro::
 .string "Amsterdam LEAGUE: Our river\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentAmsterdam_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentAmsterdam_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentAmsterdam_Battle1::
 lock
 faceplayer
 msgbox ContinentAmsterdam_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 272, ContinentAmsterdam_Battle1Intro, ContinentAmsterdam_Battle1Defeat, ContinentAmsterdam_Battle1Won
ContinentAmsterdam_Battle1Won::
 msgbox ContinentAmsterdam_Battle1After
 goto Shadow_End
ContinentAmsterdam_Battle1Intro::
 .string "Amsterdam LEAGUE: Our river\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentAmsterdam_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentAmsterdam_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentAmsterdamPast_Landmark::
 msgbox ContinentAmsterdamPast_LandmarkText, MSGBOX_SIGN
 end
ContinentAmsterdamPast_LandmarkText::
 .string "CANAL HOUSES - AMSTERDAM. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths. You\pare visiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentAmsterdamPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentAmsterdamPast_Battle0::
 lock
 faceplayer
 msgbox ContinentAmsterdamPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 273, ContinentAmsterdamPast_Battle0Intro, ContinentAmsterdamPast_Battle0Defeat, ContinentAmsterdamPast_Battle0Won
ContinentAmsterdamPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentAmsterdamPast_Battle0After
 goto Shadow_End
ContinentAmsterdamPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pAmsterdam's couriers. Help us\nstop the experiment?$"
ContinentAmsterdamPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentAmsterdamPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentVienna_Landmark::
 msgbox ContinentVienna_LandmarkText, MSGBOX_SIGN
 end
ContinentVienna_LandmarkText::
 .string "ST STEPHEN'S - VIENNA. This is\na compact landmark district.\pThe station is south; trainers\nare along the garden paths.$"
ContinentVienna_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentVienna_KeeperText
 goto Shadow_End
ContinentVienna_KeeperText::
 .string "ADA's network reached Vienna.\nWin the local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentVienna_Battle0::
 lock
 faceplayer
 msgbox ContinentVienna_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 274, ContinentVienna_Battle0Intro, ContinentVienna_Battle0Defeat, ContinentVienna_Battle0Won
ContinentVienna_Battle0Won::
 msgbox ContinentVienna_Battle0After
 goto Shadow_End
ContinentVienna_Battle0Intro::
 .string "Vienna LEAGUE: Our mountain\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentVienna_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentVienna_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentVienna_Battle1::
 lock
 faceplayer
 msgbox ContinentVienna_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 275, ContinentVienna_Battle1Intro, ContinentVienna_Battle1Defeat, ContinentVienna_Battle1Won
ContinentVienna_Battle1Won::
 msgbox ContinentVienna_Battle1After
 goto Shadow_End
ContinentVienna_Battle1Intro::
 .string "Vienna LEAGUE: Our mountain\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentVienna_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentVienna_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentViennaPast_Landmark::
 msgbox ContinentViennaPast_LandmarkText, MSGBOX_SIGN
 end
ContinentViennaPast_LandmarkText::
 .string "ST STEPHEN'S - VIENNA. This is\na compact landmark district.\pThe station is south; trainers\nare along the garden paths. You\pare visiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentViennaPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentViennaPast_Battle0::
 lock
 faceplayer
 msgbox ContinentViennaPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 276, ContinentViennaPast_Battle0Intro, ContinentViennaPast_Battle0Defeat, ContinentViennaPast_Battle0Won
ContinentViennaPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentViennaPast_Battle0After
 goto Shadow_End
ContinentViennaPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pVienna's couriers. Help us stop\nthe experiment?$"
ContinentViennaPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentViennaPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentPrague_Landmark::
 msgbox ContinentPrague_LandmarkText, MSGBOX_SIGN
 end
ContinentPrague_LandmarkText::
 .string "CHARLES BRIDGE - PRAGUE. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths.$"
ContinentPrague_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentPrague_KeeperText
 goto Shadow_End
ContinentPrague_KeeperText::
 .string "ADA's network reached Prague.\nWin the local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentPrague_Battle0::
 lock
 faceplayer
 msgbox ContinentPrague_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 277, ContinentPrague_Battle0Intro, ContinentPrague_Battle0Defeat, ContinentPrague_Battle0Won
ContinentPrague_Battle0Won::
 msgbox ContinentPrague_Battle0After
 goto Shadow_End
ContinentPrague_Battle0Intro::
 .string "Prague LEAGUE: Our river\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentPrague_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentPrague_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentPrague_Battle1::
 lock
 faceplayer
 msgbox ContinentPrague_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 278, ContinentPrague_Battle1Intro, ContinentPrague_Battle1Defeat, ContinentPrague_Battle1Won
ContinentPrague_Battle1Won::
 msgbox ContinentPrague_Battle1After
 goto Shadow_End
ContinentPrague_Battle1Intro::
 .string "Prague LEAGUE: Our river\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentPrague_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentPrague_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentPraguePast_Landmark::
 msgbox ContinentPraguePast_LandmarkText, MSGBOX_SIGN
 end
ContinentPraguePast_LandmarkText::
 .string "CHARLES BRIDGE - PRAGUE. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths. You\pare visiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentPraguePast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentPraguePast_Battle0::
 lock
 faceplayer
 msgbox ContinentPraguePast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 279, ContinentPraguePast_Battle0Intro, ContinentPraguePast_Battle0Defeat, ContinentPraguePast_Battle0Won
ContinentPraguePast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentPraguePast_Battle0After
 goto Shadow_End
ContinentPraguePast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pPrague's couriers. Help us stop\nthe experiment?$"
ContinentPraguePast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentPraguePast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentBratislava_Landmark::
 msgbox ContinentBratislava_LandmarkText, MSGBOX_SIGN
 end
ContinentBratislava_LandmarkText::
 .string "BRATISLAVA CASTLE - BRATISLAVA.\nThis is a compact landmark\pdistrict. The station is south;\ntrainers are along the garden\ppaths.$"
ContinentBratislava_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentBratislava_KeeperText
 goto Shadow_End
ContinentBratislava_KeeperText::
 .string "ADA's network reached\nBratislava. Win the local\pmatches, then use CELEBI after\nthe Lisbon chapter to visit the\ppast. We are waiting for news\nof our old sanctuary and its\pmissing ledger.$"
ContinentBratislava_Battle0::
 lock
 faceplayer
 msgbox ContinentBratislava_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 280, ContinentBratislava_Battle0Intro, ContinentBratislava_Battle0Defeat, ContinentBratislava_Battle0Won
ContinentBratislava_Battle0Won::
 msgbox ContinentBratislava_Battle0After
 goto Shadow_End
ContinentBratislava_Battle0Intro::
 .string "Bratislava LEAGUE: Our mountain\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentBratislava_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentBratislava_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentBratislava_Battle1::
 lock
 faceplayer
 msgbox ContinentBratislava_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 281, ContinentBratislava_Battle1Intro, ContinentBratislava_Battle1Defeat, ContinentBratislava_Battle1Won
ContinentBratislava_Battle1Won::
 msgbox ContinentBratislava_Battle1After
 goto Shadow_End
ContinentBratislava_Battle1Intro::
 .string "Bratislava LEAGUE: Our mountain\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentBratislava_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentBratislava_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentBratislavaPast_Landmark::
 msgbox ContinentBratislavaPast_LandmarkText, MSGBOX_SIGN
 end
ContinentBratislavaPast_LandmarkText::
 .string "BRATISLAVA CASTLE - BRATISLAVA.\nThis is a compact landmark\pdistrict. The station is south;\ntrainers are along the garden\ppaths. You are visiting a\nwartime chapter. Your mission\pconcerns a fictional rescue\nnetwork.$"
ContinentBratislavaPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentBratislavaPast_Battle0::
 lock
 faceplayer
 msgbox ContinentBratislavaPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 282, ContinentBratislavaPast_Battle0Intro, ContinentBratislavaPast_Battle0Defeat, ContinentBratislavaPast_Battle0Won
ContinentBratislavaPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentBratislavaPast_Battle0After
 goto Shadow_End
ContinentBratislavaPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pBratislava's couriers. Help us\nstop the experiment?$"
ContinentBratislavaPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentBratislavaPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentBern_Landmark::
 msgbox ContinentBern_LandmarkText, MSGBOX_SIGN
 end
ContinentBern_LandmarkText::
 .string "ZYTGLOGGE - BERN. This is a\ncompact landmark district. The\pstation is south; trainers are\nalong the garden paths.$"
ContinentBern_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentBern_KeeperText
 goto Shadow_End
ContinentBern_KeeperText::
 .string "ADA's network reached Bern. Win\nthe local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentBern_Battle0::
 lock
 faceplayer
 msgbox ContinentBern_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 283, ContinentBern_Battle0Intro, ContinentBern_Battle0Defeat, ContinentBern_Battle0Won
ContinentBern_Battle0Won::
 msgbox ContinentBern_Battle0After
 goto Shadow_End
ContinentBern_Battle0Intro::
 .string "Bern LEAGUE: Our mountain\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentBern_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentBern_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentBern_Battle1::
 lock
 faceplayer
 msgbox ContinentBern_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 284, ContinentBern_Battle1Intro, ContinentBern_Battle1Defeat, ContinentBern_Battle1Won
ContinentBern_Battle1Won::
 msgbox ContinentBern_Battle1After
 goto Shadow_End
ContinentBern_Battle1Intro::
 .string "Bern LEAGUE: Our mountain\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentBern_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentBern_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentBernPast_Landmark::
 msgbox ContinentBernPast_LandmarkText, MSGBOX_SIGN
 end
ContinentBernPast_LandmarkText::
 .string "ZYTGLOGGE - BERN. This is a\ncompact landmark district. The\pstation is south; trainers are\nalong the garden paths. You are\pvisiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentBernPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentBernPast_Battle0::
 lock
 faceplayer
 msgbox ContinentBernPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 285, ContinentBernPast_Battle0Intro, ContinentBernPast_Battle0Defeat, ContinentBernPast_Battle0Won
ContinentBernPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentBernPast_Battle0After
 goto Shadow_End
ContinentBernPast_Battle0Intro::
 .string "KEEPER: Bern supports a secret\nrefuge. Test your partners\pagainst mine, then help us\nchoose how to preserve the\psanctuary?$"
ContinentBernPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentBernPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentRome_Landmark::
 msgbox ContinentRome_LandmarkText, MSGBOX_SIGN
 end
ContinentRome_LandmarkText::
 .string "COLOSSEUM - ROME. This is a\ncompact landmark district. The\pstation is south; trainers are\nalong the garden paths.$"
ContinentRome_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentRome_KeeperText
 goto Shadow_End
ContinentRome_KeeperText::
 .string "ADA's network reached Rome. Win\nthe local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentRome_Battle0::
 lock
 faceplayer
 msgbox ContinentRome_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 286, ContinentRome_Battle0Intro, ContinentRome_Battle0Defeat, ContinentRome_Battle0Won
ContinentRome_Battle0Won::
 msgbox ContinentRome_Battle0After
 goto Shadow_End
ContinentRome_Battle0Intro::
 .string "Rome LEAGUE: Our coast circuit\nwelcomes travelers. Ready for a\plocal battle?$"
ContinentRome_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentRome_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentRome_Battle1::
 lock
 faceplayer
 msgbox ContinentRome_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 287, ContinentRome_Battle1Intro, ContinentRome_Battle1Defeat, ContinentRome_Battle1Won
ContinentRome_Battle1Won::
 msgbox ContinentRome_Battle1After
 goto Shadow_End
ContinentRome_Battle1Intro::
 .string "Rome LEAGUE: Our coast circuit\nwelcomes travelers. Ready for a\plocal battle?$"
ContinentRome_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentRome_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentRomePast_Landmark::
 msgbox ContinentRomePast_LandmarkText, MSGBOX_SIGN
 end
ContinentRomePast_LandmarkText::
 .string "COLOSSEUM - ROME. This is a\ncompact landmark district. The\pstation is south; trainers are\nalong the garden paths. You are\pvisiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentRomePast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentRomePast_Battle0::
 lock
 faceplayer
 msgbox ContinentRomePast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 288, ContinentRomePast_Battle0Intro, ContinentRomePast_Battle0Defeat, ContinentRomePast_Battle0Won
ContinentRomePast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentRomePast_Battle0After
 goto Shadow_End
ContinentRomePast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pRome's couriers. Help us stop\nthe experiment?$"
ContinentRomePast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentRomePast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentAthens_Landmark::
 msgbox ContinentAthens_LandmarkText, MSGBOX_SIGN
 end
ContinentAthens_LandmarkText::
 .string "ACROPOLIS - ATHENS. This is a\ncompact landmark district. The\pstation is south; trainers are\nalong the garden paths.$"
ContinentAthens_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentAthens_KeeperText
 goto Shadow_End
ContinentAthens_KeeperText::
 .string "ADA's network reached Athens.\nWin the local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentAthens_Battle0::
 lock
 faceplayer
 msgbox ContinentAthens_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 289, ContinentAthens_Battle0Intro, ContinentAthens_Battle0Defeat, ContinentAthens_Battle0Won
ContinentAthens_Battle0Won::
 msgbox ContinentAthens_Battle0After
 goto Shadow_End
ContinentAthens_Battle0Intro::
 .string "Athens LEAGUE: Our coast\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentAthens_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentAthens_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentAthens_Battle1::
 lock
 faceplayer
 msgbox ContinentAthens_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 290, ContinentAthens_Battle1Intro, ContinentAthens_Battle1Defeat, ContinentAthens_Battle1Won
ContinentAthens_Battle1Won::
 msgbox ContinentAthens_Battle1After
 goto Shadow_End
ContinentAthens_Battle1Intro::
 .string "Athens LEAGUE: Our coast\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentAthens_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentAthens_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentAthensPast_Landmark::
 msgbox ContinentAthensPast_LandmarkText, MSGBOX_SIGN
 end
ContinentAthensPast_LandmarkText::
 .string "ACROPOLIS - ATHENS. This is a\ncompact landmark district. The\pstation is south; trainers are\nalong the garden paths. You are\pvisiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentAthensPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentAthensPast_Battle0::
 lock
 faceplayer
 msgbox ContinentAthensPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 291, ContinentAthensPast_Battle0Intro, ContinentAthensPast_Battle0Defeat, ContinentAthensPast_Battle0Won
ContinentAthensPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentAthensPast_Battle0After
 goto Shadow_End
ContinentAthensPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pAthens's couriers. Help us stop\nthe experiment?$"
ContinentAthensPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentAthensPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentMadrid_Landmark::
 msgbox ContinentMadrid_LandmarkText, MSGBOX_SIGN
 end
ContinentMadrid_LandmarkText::
 .string "ROYAL PALACE - MADRID. This is\na compact landmark district.\pThe station is south; trainers\nare along the garden paths.$"
ContinentMadrid_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentMadrid_KeeperText
 goto Shadow_End
ContinentMadrid_KeeperText::
 .string "ADA's network reached Madrid.\nWin the local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentMadrid_Battle0::
 lock
 faceplayer
 msgbox ContinentMadrid_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 292, ContinentMadrid_Battle0Intro, ContinentMadrid_Battle0Defeat, ContinentMadrid_Battle0Won
ContinentMadrid_Battle0Won::
 msgbox ContinentMadrid_Battle0After
 goto Shadow_End
ContinentMadrid_Battle0Intro::
 .string "Madrid LEAGUE: Our garden\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentMadrid_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentMadrid_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentMadrid_Battle1::
 lock
 faceplayer
 msgbox ContinentMadrid_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 293, ContinentMadrid_Battle1Intro, ContinentMadrid_Battle1Defeat, ContinentMadrid_Battle1Won
ContinentMadrid_Battle1Won::
 msgbox ContinentMadrid_Battle1After
 goto Shadow_End
ContinentMadrid_Battle1Intro::
 .string "Madrid LEAGUE: Our garden\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentMadrid_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentMadrid_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentMadridPast_Landmark::
 msgbox ContinentMadridPast_LandmarkText, MSGBOX_SIGN
 end
ContinentMadridPast_LandmarkText::
 .string "ROYAL PALACE - MADRID. This is\na compact landmark district.\pThe station is south; trainers\nare along the garden paths. You\pare visiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentMadridPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentMadridPast_Battle0::
 lock
 faceplayer
 msgbox ContinentMadridPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 294, ContinentMadridPast_Battle0Intro, ContinentMadridPast_Battle0Defeat, ContinentMadridPast_Battle0Won
ContinentMadridPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentMadridPast_Battle0After
 goto Shadow_End
ContinentMadridPast_Battle0Intro::
 .string "KEEPER: Madrid supports a\nsecret refuge. Test your\ppartners against mine, then\nhelp us choose how to preserve\pthe sanctuary?$"
ContinentMadridPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentMadridPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentLisbon_Landmark::
 msgbox ContinentLisbon_LandmarkText, MSGBOX_SIGN
 end
ContinentLisbon_LandmarkText::
 .string "BELEM TOWER - LISBON. This is a\ncompact landmark district. The\pstation is south; trainers are\nalong the garden paths.$"
ContinentLisbon_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentLisbon_KeeperText
 goto Shadow_End
ContinentLisbon_KeeperText::
 .string "ADA's network reached Lisbon.\nWin the local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentLisbon_Battle0::
 lock
 faceplayer
 msgbox ContinentLisbon_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 295, ContinentLisbon_Battle0Intro, ContinentLisbon_Battle0Defeat, ContinentLisbon_Battle0Won
ContinentLisbon_Battle0Won::
 msgbox ContinentLisbon_Battle0After
 goto Shadow_End
ContinentLisbon_Battle0Intro::
 .string "Lisbon LEAGUE: Our coast\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentLisbon_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentLisbon_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentLisbon_Battle1::
 lock
 faceplayer
 msgbox ContinentLisbon_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 296, ContinentLisbon_Battle1Intro, ContinentLisbon_Battle1Defeat, ContinentLisbon_Battle1Won
ContinentLisbon_Battle1Won::
 msgbox ContinentLisbon_Battle1After
 goto Shadow_End
ContinentLisbon_Battle1Intro::
 .string "Lisbon LEAGUE: Our coast\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentLisbon_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentLisbon_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentLisbonPast_Landmark::
 msgbox ContinentLisbonPast_LandmarkText, MSGBOX_SIGN
 end
ContinentLisbonPast_LandmarkText::
 .string "BELEM TOWER - LISBON. This is a\ncompact landmark district. The\pstation is south; trainers are\nalong the garden paths. You are\pvisiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentLisbonPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentLisbonPast_Battle0::
 lock
 faceplayer
 msgbox ContinentLisbonPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 297, ContinentLisbonPast_Battle0Intro, ContinentLisbonPast_Battle0Defeat, ContinentLisbonPast_Battle0Won
ContinentLisbonPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentLisbonPast_Battle0After
 goto Shadow_End
ContinentLisbonPast_Battle0Intro::
 .string "KEEPER: Lisbon supports a\nsecret refuge. Test your\ppartners against mine, then\nhelp us choose how to preserve\pthe sanctuary?$"
ContinentLisbonPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentLisbonPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentWarsaw_Landmark::
 msgbox ContinentWarsaw_LandmarkText, MSGBOX_SIGN
 end
ContinentWarsaw_LandmarkText::
 .string "ROYAL CASTLE - WARSAW. This is\na compact landmark district.\pThe station is south; trainers\nare along the garden paths.$"
ContinentWarsaw_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentWarsaw_KeeperText
 goto Shadow_End
ContinentWarsaw_KeeperText::
 .string "ADA's network reached Warsaw.\nWin the local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentWarsaw_Battle0::
 lock
 faceplayer
 msgbox ContinentWarsaw_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 298, ContinentWarsaw_Battle0Intro, ContinentWarsaw_Battle0Defeat, ContinentWarsaw_Battle0Won
ContinentWarsaw_Battle0Won::
 msgbox ContinentWarsaw_Battle0After
 goto Shadow_End
ContinentWarsaw_Battle0Intro::
 .string "Warsaw LEAGUE: Our river\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentWarsaw_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentWarsaw_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentWarsaw_Battle1::
 lock
 faceplayer
 msgbox ContinentWarsaw_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 299, ContinentWarsaw_Battle1Intro, ContinentWarsaw_Battle1Defeat, ContinentWarsaw_Battle1Won
ContinentWarsaw_Battle1Won::
 msgbox ContinentWarsaw_Battle1After
 goto Shadow_End
ContinentWarsaw_Battle1Intro::
 .string "Warsaw LEAGUE: Our river\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentWarsaw_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentWarsaw_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentWarsawPast_Landmark::
 msgbox ContinentWarsawPast_LandmarkText, MSGBOX_SIGN
 end
ContinentWarsawPast_LandmarkText::
 .string "ROYAL CASTLE - WARSAW. This is\na compact landmark district.\pThe station is south; trainers\nare along the garden paths. You\pare visiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentWarsawPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentWarsawPast_Battle0::
 lock
 faceplayer
 msgbox ContinentWarsawPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 300, ContinentWarsawPast_Battle0Intro, ContinentWarsawPast_Battle0Defeat, ContinentWarsawPast_Battle0Won
ContinentWarsawPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentWarsawPast_Battle0After
 goto Shadow_End
ContinentWarsawPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pWarsaw's couriers. Help us stop\nthe experiment?$"
ContinentWarsawPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentWarsawPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentLuxembourg_Landmark::
 msgbox ContinentLuxembourg_LandmarkText, MSGBOX_SIGN
 end
ContinentLuxembourg_LandmarkText::
 .string "BOCK CASEMATES - LUXEMBOURG.\nThis is a compact landmark\pdistrict. The station is south;\ntrainers are along the garden\ppaths.$"
ContinentLuxembourg_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentLuxembourg_KeeperText
 goto Shadow_End
ContinentLuxembourg_KeeperText::
 .string "ADA's network reached\nLuxembourg. Win the local\pmatches, then use CELEBI after\nthe Lisbon chapter to visit the\ppast. We are waiting for news\nof our old sanctuary and its\pmissing ledger.$"
ContinentLuxembourg_Battle0::
 lock
 faceplayer
 msgbox ContinentLuxembourg_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 301, ContinentLuxembourg_Battle0Intro, ContinentLuxembourg_Battle0Defeat, ContinentLuxembourg_Battle0Won
ContinentLuxembourg_Battle0Won::
 msgbox ContinentLuxembourg_Battle0After
 goto Shadow_End
ContinentLuxembourg_Battle0Intro::
 .string "Luxembourg LEAGUE: Our mountain\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentLuxembourg_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentLuxembourg_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentLuxembourg_Battle1::
 lock
 faceplayer
 msgbox ContinentLuxembourg_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 302, ContinentLuxembourg_Battle1Intro, ContinentLuxembourg_Battle1Defeat, ContinentLuxembourg_Battle1Won
ContinentLuxembourg_Battle1Won::
 msgbox ContinentLuxembourg_Battle1After
 goto Shadow_End
ContinentLuxembourg_Battle1Intro::
 .string "Luxembourg LEAGUE: Our mountain\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentLuxembourg_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentLuxembourg_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentLuxembourgPast_Landmark::
 msgbox ContinentLuxembourgPast_LandmarkText, MSGBOX_SIGN
 end
ContinentLuxembourgPast_LandmarkText::
 .string "BOCK CASEMATES - LUXEMBOURG.\nThis is a compact landmark\pdistrict. The station is south;\ntrainers are along the garden\ppaths. You are visiting a\nwartime chapter. Your mission\pconcerns a fictional rescue\nnetwork.$"
ContinentLuxembourgPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentLuxembourgPast_Battle0::
 lock
 faceplayer
 msgbox ContinentLuxembourgPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 303, ContinentLuxembourgPast_Battle0Intro, ContinentLuxembourgPast_Battle0Defeat, ContinentLuxembourgPast_Battle0Won
ContinentLuxembourgPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentLuxembourgPast_Battle0After
 goto Shadow_End
ContinentLuxembourgPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pLuxembourg's couriers. Help us\nstop the experiment?$"
ContinentLuxembourgPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentLuxembourgPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentCopenhagen_Landmark::
 msgbox ContinentCopenhagen_LandmarkText, MSGBOX_SIGN
 end
ContinentCopenhagen_LandmarkText::
 .string "ROSENBORG CASTLE - COPENHAGEN.\nThis is a compact landmark\pdistrict. The station is south;\ntrainers are along the garden\ppaths.$"
ContinentCopenhagen_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentCopenhagen_KeeperText
 goto Shadow_End
ContinentCopenhagen_KeeperText::
 .string "ADA's network reached\nCopenhagen. Win the local\pmatches, then use CELEBI after\nthe Lisbon chapter to visit the\ppast. We are waiting for news\nof our old sanctuary and its\pmissing ledger.$"
ContinentCopenhagen_Battle0::
 lock
 faceplayer
 msgbox ContinentCopenhagen_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 304, ContinentCopenhagen_Battle0Intro, ContinentCopenhagen_Battle0Defeat, ContinentCopenhagen_Battle0Won
ContinentCopenhagen_Battle0Won::
 msgbox ContinentCopenhagen_Battle0After
 goto Shadow_End
ContinentCopenhagen_Battle0Intro::
 .string "Copenhagen LEAGUE: Our coast\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentCopenhagen_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentCopenhagen_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentCopenhagen_Battle1::
 lock
 faceplayer
 msgbox ContinentCopenhagen_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 305, ContinentCopenhagen_Battle1Intro, ContinentCopenhagen_Battle1Defeat, ContinentCopenhagen_Battle1Won
ContinentCopenhagen_Battle1Won::
 msgbox ContinentCopenhagen_Battle1After
 goto Shadow_End
ContinentCopenhagen_Battle1Intro::
 .string "Copenhagen LEAGUE: Our coast\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentCopenhagen_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentCopenhagen_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentCopenhagenPast_Landmark::
 msgbox ContinentCopenhagenPast_LandmarkText, MSGBOX_SIGN
 end
ContinentCopenhagenPast_LandmarkText::
 .string "ROSENBORG CASTLE - COPENHAGEN.\nThis is a compact landmark\pdistrict. The station is south;\ntrainers are along the garden\ppaths. You are visiting a\nwartime chapter. Your mission\pconcerns a fictional rescue\nnetwork.$"
ContinentCopenhagenPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentCopenhagenPast_Battle0::
 lock
 faceplayer
 msgbox ContinentCopenhagenPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 306, ContinentCopenhagenPast_Battle0Intro, ContinentCopenhagenPast_Battle0Defeat, ContinentCopenhagenPast_Battle0Won
ContinentCopenhagenPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentCopenhagenPast_Battle0After
 goto Shadow_End
ContinentCopenhagenPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pCopenhagen's couriers. Help us\nstop the experiment?$"
ContinentCopenhagenPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentCopenhagenPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentOslo_Landmark::
 msgbox ContinentOslo_LandmarkText, MSGBOX_SIGN
 end
ContinentOslo_LandmarkText::
 .string "AKERSHUS FORTRESS - OSLO. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths.$"
ContinentOslo_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentOslo_KeeperText
 goto Shadow_End
ContinentOslo_KeeperText::
 .string "ADA's network reached Oslo. Win\nthe local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentOslo_Battle0::
 lock
 faceplayer
 msgbox ContinentOslo_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 307, ContinentOslo_Battle0Intro, ContinentOslo_Battle0Defeat, ContinentOslo_Battle0Won
ContinentOslo_Battle0Won::
 msgbox ContinentOslo_Battle0After
 goto Shadow_End
ContinentOslo_Battle0Intro::
 .string "Oslo LEAGUE: Our coast circuit\nwelcomes travelers. Ready for a\plocal battle?$"
ContinentOslo_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentOslo_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentOslo_Battle1::
 lock
 faceplayer
 msgbox ContinentOslo_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 308, ContinentOslo_Battle1Intro, ContinentOslo_Battle1Defeat, ContinentOslo_Battle1Won
ContinentOslo_Battle1Won::
 msgbox ContinentOslo_Battle1After
 goto Shadow_End
ContinentOslo_Battle1Intro::
 .string "Oslo LEAGUE: Our coast circuit\nwelcomes travelers. Ready for a\plocal battle?$"
ContinentOslo_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentOslo_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentOsloPast_Landmark::
 msgbox ContinentOsloPast_LandmarkText, MSGBOX_SIGN
 end
ContinentOsloPast_LandmarkText::
 .string "AKERSHUS FORTRESS - OSLO. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths. You\pare visiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentOsloPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentOsloPast_Battle0::
 lock
 faceplayer
 msgbox ContinentOsloPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 309, ContinentOsloPast_Battle0Intro, ContinentOsloPast_Battle0Defeat, ContinentOsloPast_Battle0Won
ContinentOsloPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentOsloPast_Battle0After
 goto Shadow_End
ContinentOsloPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pOslo's couriers. Help us stop\nthe experiment?$"
ContinentOsloPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentOsloPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentStockholm_Landmark::
 msgbox ContinentStockholm_LandmarkText, MSGBOX_SIGN
 end
ContinentStockholm_LandmarkText::
 .string "CITY HALL - STOCKHOLM. This is\na compact landmark district.\pThe station is south; trainers\nare along the garden paths.$"
ContinentStockholm_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentStockholm_KeeperText
 goto Shadow_End
ContinentStockholm_KeeperText::
 .string "ADA's network reached\nStockholm. Win the local\pmatches, then use CELEBI after\nthe Lisbon chapter to visit the\ppast. We are waiting for news\nof our old sanctuary and its\pmissing ledger.$"
ContinentStockholm_Battle0::
 lock
 faceplayer
 msgbox ContinentStockholm_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 310, ContinentStockholm_Battle0Intro, ContinentStockholm_Battle0Defeat, ContinentStockholm_Battle0Won
ContinentStockholm_Battle0Won::
 msgbox ContinentStockholm_Battle0After
 goto Shadow_End
ContinentStockholm_Battle0Intro::
 .string "Stockholm LEAGUE: Our island\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentStockholm_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentStockholm_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentStockholm_Battle1::
 lock
 faceplayer
 msgbox ContinentStockholm_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 311, ContinentStockholm_Battle1Intro, ContinentStockholm_Battle1Defeat, ContinentStockholm_Battle1Won
ContinentStockholm_Battle1Won::
 msgbox ContinentStockholm_Battle1After
 goto Shadow_End
ContinentStockholm_Battle1Intro::
 .string "Stockholm LEAGUE: Our island\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentStockholm_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentStockholm_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentStockholmPast_Landmark::
 msgbox ContinentStockholmPast_LandmarkText, MSGBOX_SIGN
 end
ContinentStockholmPast_LandmarkText::
 .string "CITY HALL - STOCKHOLM. This is\na compact landmark district.\pThe station is south; trainers\nare along the garden paths. You\pare visiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentStockholmPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentStockholmPast_Battle0::
 lock
 faceplayer
 msgbox ContinentStockholmPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 312, ContinentStockholmPast_Battle0Intro, ContinentStockholmPast_Battle0Defeat, ContinentStockholmPast_Battle0Won
ContinentStockholmPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentStockholmPast_Battle0After
 goto Shadow_End
ContinentStockholmPast_Battle0Intro::
 .string "KEEPER: Stockholm supports a\nsecret refuge. Test your\ppartners against mine, then\nhelp us choose how to preserve\pthe sanctuary?$"
ContinentStockholmPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentStockholmPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentHelsinki_Landmark::
 msgbox ContinentHelsinki_LandmarkText, MSGBOX_SIGN
 end
ContinentHelsinki_LandmarkText::
 .string "HELSINKI CATHEDRAL - HELSINKI.\nThis is a compact landmark\pdistrict. The station is south;\ntrainers are along the garden\ppaths.$"
ContinentHelsinki_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentHelsinki_KeeperText
 goto Shadow_End
ContinentHelsinki_KeeperText::
 .string "ADA's network reached Helsinki.\nWin the local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentHelsinki_Battle0::
 lock
 faceplayer
 msgbox ContinentHelsinki_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 313, ContinentHelsinki_Battle0Intro, ContinentHelsinki_Battle0Defeat, ContinentHelsinki_Battle0Won
ContinentHelsinki_Battle0Won::
 msgbox ContinentHelsinki_Battle0After
 goto Shadow_End
ContinentHelsinki_Battle0Intro::
 .string "Helsinki LEAGUE: Our coast\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentHelsinki_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentHelsinki_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentHelsinki_Battle1::
 lock
 faceplayer
 msgbox ContinentHelsinki_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 314, ContinentHelsinki_Battle1Intro, ContinentHelsinki_Battle1Defeat, ContinentHelsinki_Battle1Won
ContinentHelsinki_Battle1Won::
 msgbox ContinentHelsinki_Battle1After
 goto Shadow_End
ContinentHelsinki_Battle1Intro::
 .string "Helsinki LEAGUE: Our coast\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentHelsinki_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentHelsinki_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentHelsinkiPast_Landmark::
 msgbox ContinentHelsinkiPast_LandmarkText, MSGBOX_SIGN
 end
ContinentHelsinkiPast_LandmarkText::
 .string "HELSINKI CATHEDRAL - HELSINKI.\nThis is a compact landmark\pdistrict. The station is south;\ntrainers are along the garden\ppaths. You are visiting a\nwartime chapter. Your mission\pconcerns a fictional rescue\nnetwork.$"
ContinentHelsinkiPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentHelsinkiPast_Battle0::
 lock
 faceplayer
 msgbox ContinentHelsinkiPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 315, ContinentHelsinkiPast_Battle0Intro, ContinentHelsinkiPast_Battle0Defeat, ContinentHelsinkiPast_Battle0Won
ContinentHelsinkiPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentHelsinkiPast_Battle0After
 goto Shadow_End
ContinentHelsinkiPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pHelsinki's couriers. Help us\nstop the experiment?$"
ContinentHelsinkiPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentHelsinkiPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentReykjavik_Landmark::
 msgbox ContinentReykjavik_LandmarkText, MSGBOX_SIGN
 end
ContinentReykjavik_LandmarkText::
 .string "PARLIAMENT HOUSE - REYKJAVIK.\nThis is a compact landmark\pdistrict. The station is south;\ntrainers are along the garden\ppaths.$"
ContinentReykjavik_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentReykjavik_KeeperText
 goto Shadow_End
ContinentReykjavik_KeeperText::
 .string "ADA's network reached\nReykjavik. Win the local\pmatches, then use CELEBI after\nthe Lisbon chapter to visit the\ppast. We are waiting for news\nof our old sanctuary and its\pmissing ledger.$"
ContinentReykjavik_Battle0::
 lock
 faceplayer
 msgbox ContinentReykjavik_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 316, ContinentReykjavik_Battle0Intro, ContinentReykjavik_Battle0Defeat, ContinentReykjavik_Battle0Won
ContinentReykjavik_Battle0Won::
 msgbox ContinentReykjavik_Battle0After
 goto Shadow_End
ContinentReykjavik_Battle0Intro::
 .string "Reykjavik LEAGUE: Our island\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentReykjavik_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentReykjavik_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentReykjavik_Battle1::
 lock
 faceplayer
 msgbox ContinentReykjavik_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 317, ContinentReykjavik_Battle1Intro, ContinentReykjavik_Battle1Defeat, ContinentReykjavik_Battle1Won
ContinentReykjavik_Battle1Won::
 msgbox ContinentReykjavik_Battle1After
 goto Shadow_End
ContinentReykjavik_Battle1Intro::
 .string "Reykjavik LEAGUE: Our island\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentReykjavik_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentReykjavik_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentReykjavikPast_Landmark::
 msgbox ContinentReykjavikPast_LandmarkText, MSGBOX_SIGN
 end
ContinentReykjavikPast_LandmarkText::
 .string "PARLIAMENT HOUSE - REYKJAVIK.\nThis is a compact landmark\pdistrict. The station is south;\ntrainers are along the garden\ppaths. You are visiting a\nwartime chapter. Your mission\pconcerns a fictional rescue\nnetwork.$"
ContinentReykjavikPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentReykjavikPast_Battle0::
 lock
 faceplayer
 msgbox ContinentReykjavikPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 318, ContinentReykjavikPast_Battle0Intro, ContinentReykjavikPast_Battle0Defeat, ContinentReykjavikPast_Battle0Won
ContinentReykjavikPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentReykjavikPast_Battle0After
 goto Shadow_End
ContinentReykjavikPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pReykjavik's couriers. Help us\nstop the experiment?$"
ContinentReykjavikPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentReykjavikPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentDublin_Landmark::
 msgbox ContinentDublin_LandmarkText, MSGBOX_SIGN
 end
ContinentDublin_LandmarkText::
 .string "TRINITY COLLEGE - DUBLIN. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths.$"
ContinentDublin_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentDublin_KeeperText
 goto Shadow_End
ContinentDublin_KeeperText::
 .string "ADA's network reached Dublin.\nWin the local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentDublin_Battle0::
 lock
 faceplayer
 msgbox ContinentDublin_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 319, ContinentDublin_Battle0Intro, ContinentDublin_Battle0Defeat, ContinentDublin_Battle0Won
ContinentDublin_Battle0Won::
 msgbox ContinentDublin_Battle0After
 goto Shadow_End
ContinentDublin_Battle0Intro::
 .string "Dublin LEAGUE: Our river\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentDublin_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentDublin_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentDublin_Battle1::
 lock
 faceplayer
 msgbox ContinentDublin_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 320, ContinentDublin_Battle1Intro, ContinentDublin_Battle1Defeat, ContinentDublin_Battle1Won
ContinentDublin_Battle1Won::
 msgbox ContinentDublin_Battle1After
 goto Shadow_End
ContinentDublin_Battle1Intro::
 .string "Dublin LEAGUE: Our river\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentDublin_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentDublin_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentDublinPast_Landmark::
 msgbox ContinentDublinPast_LandmarkText, MSGBOX_SIGN
 end
ContinentDublinPast_LandmarkText::
 .string "TRINITY COLLEGE - DUBLIN. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths. You\pare visiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentDublinPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentDublinPast_Battle0::
 lock
 faceplayer
 msgbox ContinentDublinPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 321, ContinentDublinPast_Battle0Intro, ContinentDublinPast_Battle0Defeat, ContinentDublinPast_Battle0Won
ContinentDublinPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentDublinPast_Battle0After
 goto Shadow_End
ContinentDublinPast_Battle0Intro::
 .string "KEEPER: Dublin supports a\nsecret refuge. Test your\ppartners against mine, then\nhelp us choose how to preserve\pthe sanctuary?$"
ContinentDublinPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentDublinPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentValletta_Landmark::
 msgbox ContinentValletta_LandmarkText, MSGBOX_SIGN
 end
ContinentValletta_LandmarkText::
 .string "FORT ST ELMO - VALLETTA. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths.$"
ContinentValletta_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentValletta_KeeperText
 goto Shadow_End
ContinentValletta_KeeperText::
 .string "ADA's network reached Valletta.\nWin the local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentValletta_Battle0::
 lock
 faceplayer
 msgbox ContinentValletta_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 322, ContinentValletta_Battle0Intro, ContinentValletta_Battle0Defeat, ContinentValletta_Battle0Won
ContinentValletta_Battle0Won::
 msgbox ContinentValletta_Battle0After
 goto Shadow_End
ContinentValletta_Battle0Intro::
 .string "Valletta LEAGUE: Our island\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentValletta_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentValletta_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentValletta_Battle1::
 lock
 faceplayer
 msgbox ContinentValletta_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 323, ContinentValletta_Battle1Intro, ContinentValletta_Battle1Defeat, ContinentValletta_Battle1Won
ContinentValletta_Battle1Won::
 msgbox ContinentValletta_Battle1After
 goto Shadow_End
ContinentValletta_Battle1Intro::
 .string "Valletta LEAGUE: Our island\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentValletta_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentValletta_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentVallettaPast_Landmark::
 msgbox ContinentVallettaPast_LandmarkText, MSGBOX_SIGN
 end
ContinentVallettaPast_LandmarkText::
 .string "FORT ST ELMO - VALLETTA. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths. You\pare visiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentVallettaPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentVallettaPast_Battle0::
 lock
 faceplayer
 msgbox ContinentVallettaPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 324, ContinentVallettaPast_Battle0Intro, ContinentVallettaPast_Battle0Defeat, ContinentVallettaPast_Battle0Won
ContinentVallettaPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentVallettaPast_Battle0After
 goto Shadow_End
ContinentVallettaPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pValletta's couriers. Help us\nstop the experiment?$"
ContinentVallettaPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentVallettaPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentBudapest_Landmark::
 msgbox ContinentBudapest_LandmarkText, MSGBOX_SIGN
 end
ContinentBudapest_LandmarkText::
 .string "PARLIAMENT - BUDAPEST. This is\na compact landmark district.\pThe station is south; trainers\nare along the garden paths.$"
ContinentBudapest_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentBudapest_KeeperText
 goto Shadow_End
ContinentBudapest_KeeperText::
 .string "ADA's network reached Budapest.\nWin the local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentBudapest_Battle0::
 lock
 faceplayer
 msgbox ContinentBudapest_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 325, ContinentBudapest_Battle0Intro, ContinentBudapest_Battle0Defeat, ContinentBudapest_Battle0Won
ContinentBudapest_Battle0Won::
 msgbox ContinentBudapest_Battle0After
 goto Shadow_End
ContinentBudapest_Battle0Intro::
 .string "Budapest LEAGUE: Our river\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentBudapest_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentBudapest_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentBudapest_Battle1::
 lock
 faceplayer
 msgbox ContinentBudapest_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 326, ContinentBudapest_Battle1Intro, ContinentBudapest_Battle1Defeat, ContinentBudapest_Battle1Won
ContinentBudapest_Battle1Won::
 msgbox ContinentBudapest_Battle1After
 goto Shadow_End
ContinentBudapest_Battle1Intro::
 .string "Budapest LEAGUE: Our river\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentBudapest_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentBudapest_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentBudapestPast_Landmark::
 msgbox ContinentBudapestPast_LandmarkText, MSGBOX_SIGN
 end
ContinentBudapestPast_LandmarkText::
 .string "PARLIAMENT - BUDAPEST. This is\na compact landmark district.\pThe station is south; trainers\nare along the garden paths. You\pare visiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentBudapestPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentBudapestPast_Battle0::
 lock
 faceplayer
 msgbox ContinentBudapestPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 327, ContinentBudapestPast_Battle0Intro, ContinentBudapestPast_Battle0Defeat, ContinentBudapestPast_Battle0Won
ContinentBudapestPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentBudapestPast_Battle0After
 goto Shadow_End
ContinentBudapestPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pBudapest's couriers. Help us\nstop the experiment?$"
ContinentBudapestPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentBudapestPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentBucharest_Landmark::
 msgbox ContinentBucharest_LandmarkText, MSGBOX_SIGN
 end
ContinentBucharest_LandmarkText::
 .string "ROMANIAN ATHENAEUM - BUCHAREST.\nThis is a compact landmark\pdistrict. The station is south;\ntrainers are along the garden\ppaths.$"
ContinentBucharest_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentBucharest_KeeperText
 goto Shadow_End
ContinentBucharest_KeeperText::
 .string "ADA's network reached\nBucharest. Win the local\pmatches, then use CELEBI after\nthe Lisbon chapter to visit the\ppast. We are waiting for news\nof our old sanctuary and its\pmissing ledger.$"
ContinentBucharest_Battle0::
 lock
 faceplayer
 msgbox ContinentBucharest_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 328, ContinentBucharest_Battle0Intro, ContinentBucharest_Battle0Defeat, ContinentBucharest_Battle0Won
ContinentBucharest_Battle0Won::
 msgbox ContinentBucharest_Battle0After
 goto Shadow_End
ContinentBucharest_Battle0Intro::
 .string "Bucharest LEAGUE: Our garden\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentBucharest_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentBucharest_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentBucharest_Battle1::
 lock
 faceplayer
 msgbox ContinentBucharest_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 329, ContinentBucharest_Battle1Intro, ContinentBucharest_Battle1Defeat, ContinentBucharest_Battle1Won
ContinentBucharest_Battle1Won::
 msgbox ContinentBucharest_Battle1After
 goto Shadow_End
ContinentBucharest_Battle1Intro::
 .string "Bucharest LEAGUE: Our garden\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentBucharest_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentBucharest_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentBucharestPast_Landmark::
 msgbox ContinentBucharestPast_LandmarkText, MSGBOX_SIGN
 end
ContinentBucharestPast_LandmarkText::
 .string "ROMANIAN ATHENAEUM - BUCHAREST.\nThis is a compact landmark\pdistrict. The station is south;\ntrainers are along the garden\ppaths. You are visiting a\nwartime chapter. Your mission\pconcerns a fictional rescue\nnetwork.$"
ContinentBucharestPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentBucharestPast_Battle0::
 lock
 faceplayer
 msgbox ContinentBucharestPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 330, ContinentBucharestPast_Battle0Intro, ContinentBucharestPast_Battle0Defeat, ContinentBucharestPast_Battle0Won
ContinentBucharestPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentBucharestPast_Battle0After
 goto Shadow_End
ContinentBucharestPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pBucharest's couriers. Help us\nstop the experiment?$"
ContinentBucharestPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentBucharestPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentSofia_Landmark::
 msgbox ContinentSofia_LandmarkText, MSGBOX_SIGN
 end
ContinentSofia_LandmarkText::
 .string "ALEXANDER NEVSKY - SOFIA. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths.$"
ContinentSofia_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentSofia_KeeperText
 goto Shadow_End
ContinentSofia_KeeperText::
 .string "ADA's network reached Sofia.\nWin the local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentSofia_Battle0::
 lock
 faceplayer
 msgbox ContinentSofia_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 331, ContinentSofia_Battle0Intro, ContinentSofia_Battle0Defeat, ContinentSofia_Battle0Won
ContinentSofia_Battle0Won::
 msgbox ContinentSofia_Battle0After
 goto Shadow_End
ContinentSofia_Battle0Intro::
 .string "Sofia LEAGUE: Our mountain\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentSofia_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentSofia_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentSofia_Battle1::
 lock
 faceplayer
 msgbox ContinentSofia_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 332, ContinentSofia_Battle1Intro, ContinentSofia_Battle1Defeat, ContinentSofia_Battle1Won
ContinentSofia_Battle1Won::
 msgbox ContinentSofia_Battle1After
 goto Shadow_End
ContinentSofia_Battle1Intro::
 .string "Sofia LEAGUE: Our mountain\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentSofia_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentSofia_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentSofiaPast_Landmark::
 msgbox ContinentSofiaPast_LandmarkText, MSGBOX_SIGN
 end
ContinentSofiaPast_LandmarkText::
 .string "ALEXANDER NEVSKY - SOFIA. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths. You\pare visiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentSofiaPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentSofiaPast_Battle0::
 lock
 faceplayer
 msgbox ContinentSofiaPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 333, ContinentSofiaPast_Battle0Intro, ContinentSofiaPast_Battle0Defeat, ContinentSofiaPast_Battle0Won
ContinentSofiaPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentSofiaPast_Battle0After
 goto Shadow_End
ContinentSofiaPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pSofia's couriers. Help us stop\nthe experiment?$"
ContinentSofiaPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentSofiaPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentTirana_Landmark::
 msgbox ContinentTirana_LandmarkText, MSGBOX_SIGN
 end
ContinentTirana_LandmarkText::
 .string "ET'HEM BEY MOSQUE - TIRANA.\nThis is a compact landmark\pdistrict. The station is south;\ntrainers are along the garden\ppaths.$"
ContinentTirana_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentTirana_KeeperText
 goto Shadow_End
ContinentTirana_KeeperText::
 .string "ADA's network reached Tirana.\nWin the local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentTirana_Battle0::
 lock
 faceplayer
 msgbox ContinentTirana_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 334, ContinentTirana_Battle0Intro, ContinentTirana_Battle0Defeat, ContinentTirana_Battle0Won
ContinentTirana_Battle0Won::
 msgbox ContinentTirana_Battle0After
 goto Shadow_End
ContinentTirana_Battle0Intro::
 .string "Tirana LEAGUE: Our mountain\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentTirana_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentTirana_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentTirana_Battle1::
 lock
 faceplayer
 msgbox ContinentTirana_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 335, ContinentTirana_Battle1Intro, ContinentTirana_Battle1Defeat, ContinentTirana_Battle1Won
ContinentTirana_Battle1Won::
 msgbox ContinentTirana_Battle1After
 goto Shadow_End
ContinentTirana_Battle1Intro::
 .string "Tirana LEAGUE: Our mountain\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentTirana_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentTirana_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentTiranaPast_Landmark::
 msgbox ContinentTiranaPast_LandmarkText, MSGBOX_SIGN
 end
ContinentTiranaPast_LandmarkText::
 .string "ET'HEM BEY MOSQUE - TIRANA.\nThis is a compact landmark\pdistrict. The station is south;\ntrainers are along the garden\ppaths. You are visiting a\nwartime chapter. Your mission\pconcerns a fictional rescue\nnetwork.$"
ContinentTiranaPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentTiranaPast_Battle0::
 lock
 faceplayer
 msgbox ContinentTiranaPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 336, ContinentTiranaPast_Battle0Intro, ContinentTiranaPast_Battle0Defeat, ContinentTiranaPast_Battle0Won
ContinentTiranaPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentTiranaPast_Battle0After
 goto Shadow_End
ContinentTiranaPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pTirana's couriers. Help us stop\nthe experiment?$"
ContinentTiranaPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentTiranaPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentBelgrade_Landmark::
 msgbox ContinentBelgrade_LandmarkText, MSGBOX_SIGN
 end
ContinentBelgrade_LandmarkText::
 .string "BELGRADE FORTRESS - BELGRADE.\nThis is a compact landmark\pdistrict. The station is south;\ntrainers are along the garden\ppaths.$"
ContinentBelgrade_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentBelgrade_KeeperText
 goto Shadow_End
ContinentBelgrade_KeeperText::
 .string "ADA's network reached Belgrade.\nWin the local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentBelgrade_Battle0::
 lock
 faceplayer
 msgbox ContinentBelgrade_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 337, ContinentBelgrade_Battle0Intro, ContinentBelgrade_Battle0Defeat, ContinentBelgrade_Battle0Won
ContinentBelgrade_Battle0Won::
 msgbox ContinentBelgrade_Battle0After
 goto Shadow_End
ContinentBelgrade_Battle0Intro::
 .string "Belgrade LEAGUE: Our river\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentBelgrade_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentBelgrade_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentBelgrade_Battle1::
 lock
 faceplayer
 msgbox ContinentBelgrade_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 338, ContinentBelgrade_Battle1Intro, ContinentBelgrade_Battle1Defeat, ContinentBelgrade_Battle1Won
ContinentBelgrade_Battle1Won::
 msgbox ContinentBelgrade_Battle1After
 goto Shadow_End
ContinentBelgrade_Battle1Intro::
 .string "Belgrade LEAGUE: Our river\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentBelgrade_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentBelgrade_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentBelgradePast_Landmark::
 msgbox ContinentBelgradePast_LandmarkText, MSGBOX_SIGN
 end
ContinentBelgradePast_LandmarkText::
 .string "BELGRADE FORTRESS - BELGRADE.\nThis is a compact landmark\pdistrict. The station is south;\ntrainers are along the garden\ppaths. You are visiting a\nwartime chapter. Your mission\pconcerns a fictional rescue\nnetwork.$"
ContinentBelgradePast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentBelgradePast_Battle0::
 lock
 faceplayer
 msgbox ContinentBelgradePast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 339, ContinentBelgradePast_Battle0Intro, ContinentBelgradePast_Battle0Defeat, ContinentBelgradePast_Battle0Won
ContinentBelgradePast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentBelgradePast_Battle0After
 goto Shadow_End
ContinentBelgradePast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pBelgrade's couriers. Help us\nstop the experiment?$"
ContinentBelgradePast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentBelgradePast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentZagreb_Landmark::
 msgbox ContinentZagreb_LandmarkText, MSGBOX_SIGN
 end
ContinentZagreb_LandmarkText::
 .string "ST MARK'S CHURCH - ZAGREB. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths.$"
ContinentZagreb_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentZagreb_KeeperText
 goto Shadow_End
ContinentZagreb_KeeperText::
 .string "ADA's network reached Zagreb.\nWin the local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentZagreb_Battle0::
 lock
 faceplayer
 msgbox ContinentZagreb_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 340, ContinentZagreb_Battle0Intro, ContinentZagreb_Battle0Defeat, ContinentZagreb_Battle0Won
ContinentZagreb_Battle0Won::
 msgbox ContinentZagreb_Battle0After
 goto Shadow_End
ContinentZagreb_Battle0Intro::
 .string "Zagreb LEAGUE: Our garden\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentZagreb_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentZagreb_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentZagreb_Battle1::
 lock
 faceplayer
 msgbox ContinentZagreb_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 341, ContinentZagreb_Battle1Intro, ContinentZagreb_Battle1Defeat, ContinentZagreb_Battle1Won
ContinentZagreb_Battle1Won::
 msgbox ContinentZagreb_Battle1After
 goto Shadow_End
ContinentZagreb_Battle1Intro::
 .string "Zagreb LEAGUE: Our garden\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentZagreb_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentZagreb_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentZagrebPast_Landmark::
 msgbox ContinentZagrebPast_LandmarkText, MSGBOX_SIGN
 end
ContinentZagrebPast_LandmarkText::
 .string "ST MARK'S CHURCH - ZAGREB. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths. You\pare visiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentZagrebPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentZagrebPast_Battle0::
 lock
 faceplayer
 msgbox ContinentZagrebPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 342, ContinentZagrebPast_Battle0Intro, ContinentZagrebPast_Battle0Defeat, ContinentZagrebPast_Battle0Won
ContinentZagrebPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentZagrebPast_Battle0After
 goto Shadow_End
ContinentZagrebPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pZagreb's couriers. Help us stop\nthe experiment?$"
ContinentZagrebPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentZagrebPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentLjubljana_Landmark::
 msgbox ContinentLjubljana_LandmarkText, MSGBOX_SIGN
 end
ContinentLjubljana_LandmarkText::
 .string "TRIPLE BRIDGE - LJUBLJANA. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths.$"
ContinentLjubljana_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentLjubljana_KeeperText
 goto Shadow_End
ContinentLjubljana_KeeperText::
 .string "ADA's network reached\nLjubljana. Win the local\pmatches, then use CELEBI after\nthe Lisbon chapter to visit the\ppast. We are waiting for news\nof our old sanctuary and its\pmissing ledger.$"
ContinentLjubljana_Battle0::
 lock
 faceplayer
 msgbox ContinentLjubljana_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 343, ContinentLjubljana_Battle0Intro, ContinentLjubljana_Battle0Defeat, ContinentLjubljana_Battle0Won
ContinentLjubljana_Battle0Won::
 msgbox ContinentLjubljana_Battle0After
 goto Shadow_End
ContinentLjubljana_Battle0Intro::
 .string "Ljubljana LEAGUE: Our river\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentLjubljana_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentLjubljana_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentLjubljana_Battle1::
 lock
 faceplayer
 msgbox ContinentLjubljana_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 344, ContinentLjubljana_Battle1Intro, ContinentLjubljana_Battle1Defeat, ContinentLjubljana_Battle1Won
ContinentLjubljana_Battle1Won::
 msgbox ContinentLjubljana_Battle1After
 goto Shadow_End
ContinentLjubljana_Battle1Intro::
 .string "Ljubljana LEAGUE: Our river\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentLjubljana_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentLjubljana_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentLjubljanaPast_Landmark::
 msgbox ContinentLjubljanaPast_LandmarkText, MSGBOX_SIGN
 end
ContinentLjubljanaPast_LandmarkText::
 .string "TRIPLE BRIDGE - LJUBLJANA. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths. You\pare visiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentLjubljanaPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentLjubljanaPast_Battle0::
 lock
 faceplayer
 msgbox ContinentLjubljanaPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 345, ContinentLjubljanaPast_Battle0Intro, ContinentLjubljanaPast_Battle0Defeat, ContinentLjubljanaPast_Battle0Won
ContinentLjubljanaPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentLjubljanaPast_Battle0After
 goto Shadow_End
ContinentLjubljanaPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pLjubljana's couriers. Help us\nstop the experiment?$"
ContinentLjubljanaPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentLjubljanaPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentSarajevo_Landmark::
 msgbox ContinentSarajevo_LandmarkText, MSGBOX_SIGN
 end
ContinentSarajevo_LandmarkText::
 .string "LATIN BRIDGE - SARAJEVO. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths.$"
ContinentSarajevo_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentSarajevo_KeeperText
 goto Shadow_End
ContinentSarajevo_KeeperText::
 .string "ADA's network reached Sarajevo.\nWin the local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentSarajevo_Battle0::
 lock
 faceplayer
 msgbox ContinentSarajevo_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 346, ContinentSarajevo_Battle0Intro, ContinentSarajevo_Battle0Defeat, ContinentSarajevo_Battle0Won
ContinentSarajevo_Battle0Won::
 msgbox ContinentSarajevo_Battle0After
 goto Shadow_End
ContinentSarajevo_Battle0Intro::
 .string "Sarajevo LEAGUE: Our mountain\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentSarajevo_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentSarajevo_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentSarajevo_Battle1::
 lock
 faceplayer
 msgbox ContinentSarajevo_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 347, ContinentSarajevo_Battle1Intro, ContinentSarajevo_Battle1Defeat, ContinentSarajevo_Battle1Won
ContinentSarajevo_Battle1Won::
 msgbox ContinentSarajevo_Battle1After
 goto Shadow_End
ContinentSarajevo_Battle1Intro::
 .string "Sarajevo LEAGUE: Our mountain\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentSarajevo_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentSarajevo_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentSarajevoPast_Landmark::
 msgbox ContinentSarajevoPast_LandmarkText, MSGBOX_SIGN
 end
ContinentSarajevoPast_LandmarkText::
 .string "LATIN BRIDGE - SARAJEVO. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths. You\pare visiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentSarajevoPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentSarajevoPast_Battle0::
 lock
 faceplayer
 msgbox ContinentSarajevoPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 348, ContinentSarajevoPast_Battle0Intro, ContinentSarajevoPast_Battle0Defeat, ContinentSarajevoPast_Battle0Won
ContinentSarajevoPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentSarajevoPast_Battle0After
 goto Shadow_End
ContinentSarajevoPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pSarajevo's couriers. Help us\nstop the experiment?$"
ContinentSarajevoPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentSarajevoPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentKotor_Landmark::
 msgbox ContinentKotor_LandmarkText, MSGBOX_SIGN
 end
ContinentKotor_LandmarkText::
 .string "KOTOR CITY WALLS - KOTOR. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths.$"
ContinentKotor_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentKotor_KeeperText
 goto Shadow_End
ContinentKotor_KeeperText::
 .string "ADA's network reached Kotor.\nWin the local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentKotor_Battle0::
 lock
 faceplayer
 msgbox ContinentKotor_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 349, ContinentKotor_Battle0Intro, ContinentKotor_Battle0Defeat, ContinentKotor_Battle0Won
ContinentKotor_Battle0Won::
 msgbox ContinentKotor_Battle0After
 goto Shadow_End
ContinentKotor_Battle0Intro::
 .string "Kotor LEAGUE: Our coast circuit\nwelcomes travelers. Ready for a\plocal battle?$"
ContinentKotor_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentKotor_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentKotor_Battle1::
 lock
 faceplayer
 msgbox ContinentKotor_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 350, ContinentKotor_Battle1Intro, ContinentKotor_Battle1Defeat, ContinentKotor_Battle1Won
ContinentKotor_Battle1Won::
 msgbox ContinentKotor_Battle1After
 goto Shadow_End
ContinentKotor_Battle1Intro::
 .string "Kotor LEAGUE: Our coast circuit\nwelcomes travelers. Ready for a\plocal battle?$"
ContinentKotor_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentKotor_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentKotorPast_Landmark::
 msgbox ContinentKotorPast_LandmarkText, MSGBOX_SIGN
 end
ContinentKotorPast_LandmarkText::
 .string "KOTOR CITY WALLS - KOTOR. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths. You\pare visiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentKotorPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentKotorPast_Battle0::
 lock
 faceplayer
 msgbox ContinentKotorPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 351, ContinentKotorPast_Battle0Intro, ContinentKotorPast_Battle0Defeat, ContinentKotorPast_Battle0Won
ContinentKotorPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentKotorPast_Battle0After
 goto Shadow_End
ContinentKotorPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pKotor's couriers. Help us stop\nthe experiment?$"
ContinentKotorPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentKotorPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentSkopje_Landmark::
 msgbox ContinentSkopje_LandmarkText, MSGBOX_SIGN
 end
ContinentSkopje_LandmarkText::
 .string "STONE BRIDGE - SKOPJE. This is\na compact landmark district.\pThe station is south; trainers\nare along the garden paths.$"
ContinentSkopje_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentSkopje_KeeperText
 goto Shadow_End
ContinentSkopje_KeeperText::
 .string "ADA's network reached Skopje.\nWin the local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentSkopje_Battle0::
 lock
 faceplayer
 msgbox ContinentSkopje_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 352, ContinentSkopje_Battle0Intro, ContinentSkopje_Battle0Defeat, ContinentSkopje_Battle0Won
ContinentSkopje_Battle0Won::
 msgbox ContinentSkopje_Battle0After
 goto Shadow_End
ContinentSkopje_Battle0Intro::
 .string "Skopje LEAGUE: Our river\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentSkopje_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentSkopje_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentSkopje_Battle1::
 lock
 faceplayer
 msgbox ContinentSkopje_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 353, ContinentSkopje_Battle1Intro, ContinentSkopje_Battle1Defeat, ContinentSkopje_Battle1Won
ContinentSkopje_Battle1Won::
 msgbox ContinentSkopje_Battle1After
 goto Shadow_End
ContinentSkopje_Battle1Intro::
 .string "Skopje LEAGUE: Our river\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentSkopje_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentSkopje_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentSkopjePast_Landmark::
 msgbox ContinentSkopjePast_LandmarkText, MSGBOX_SIGN
 end
ContinentSkopjePast_LandmarkText::
 .string "STONE BRIDGE - SKOPJE. This is\na compact landmark district.\pThe station is south; trainers\nare along the garden paths. You\pare visiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentSkopjePast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentSkopjePast_Battle0::
 lock
 faceplayer
 msgbox ContinentSkopjePast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 354, ContinentSkopjePast_Battle0Intro, ContinentSkopjePast_Battle0Defeat, ContinentSkopjePast_Battle0Won
ContinentSkopjePast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentSkopjePast_Battle0After
 goto Shadow_End
ContinentSkopjePast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pSkopje's couriers. Help us stop\nthe experiment?$"
ContinentSkopjePast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentSkopjePast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentMoscow_Landmark::
 msgbox ContinentMoscow_LandmarkText, MSGBOX_SIGN
 end
ContinentMoscow_LandmarkText::
 .string "ST BASIL'S - MOSCOW. This is a\ncompact landmark district. The\pstation is south; trainers are\nalong the garden paths.$"
ContinentMoscow_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentMoscow_KeeperText
 goto Shadow_End
ContinentMoscow_KeeperText::
 .string "ADA's network reached Moscow.\nWin the local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentMoscow_Battle0::
 lock
 faceplayer
 msgbox ContinentMoscow_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 355, ContinentMoscow_Battle0Intro, ContinentMoscow_Battle0Defeat, ContinentMoscow_Battle0Won
ContinentMoscow_Battle0Won::
 msgbox ContinentMoscow_Battle0After
 goto Shadow_End
ContinentMoscow_Battle0Intro::
 .string "Moscow LEAGUE: Our river\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentMoscow_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentMoscow_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentMoscow_Battle1::
 lock
 faceplayer
 msgbox ContinentMoscow_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 356, ContinentMoscow_Battle1Intro, ContinentMoscow_Battle1Defeat, ContinentMoscow_Battle1Won
ContinentMoscow_Battle1Won::
 msgbox ContinentMoscow_Battle1After
 goto Shadow_End
ContinentMoscow_Battle1Intro::
 .string "Moscow LEAGUE: Our river\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentMoscow_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentMoscow_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentMoscowPast_Landmark::
 msgbox ContinentMoscowPast_LandmarkText, MSGBOX_SIGN
 end
ContinentMoscowPast_LandmarkText::
 .string "ST BASIL'S - MOSCOW. This is a\ncompact landmark district. The\pstation is south; trainers are\nalong the garden paths. You are\pvisiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentMoscowPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentMoscowPast_Battle0::
 lock
 faceplayer
 msgbox ContinentMoscowPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 357, ContinentMoscowPast_Battle0Intro, ContinentMoscowPast_Battle0Defeat, ContinentMoscowPast_Battle0Won
ContinentMoscowPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentMoscowPast_Battle0After
 goto Shadow_End
ContinentMoscowPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pMoscow's couriers. Help us stop\nthe experiment?$"
ContinentMoscowPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentMoscowPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentKyiv_Landmark::
 msgbox ContinentKyiv_LandmarkText, MSGBOX_SIGN
 end
ContinentKyiv_LandmarkText::
 .string "ST SOPHIA - KYIV. This is a\ncompact landmark district. The\pstation is south; trainers are\nalong the garden paths.$"
ContinentKyiv_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentKyiv_KeeperText
 goto Shadow_End
ContinentKyiv_KeeperText::
 .string "ADA's network reached Kyiv. Win\nthe local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentKyiv_Battle0::
 lock
 faceplayer
 msgbox ContinentKyiv_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 358, ContinentKyiv_Battle0Intro, ContinentKyiv_Battle0Defeat, ContinentKyiv_Battle0Won
ContinentKyiv_Battle0Won::
 msgbox ContinentKyiv_Battle0After
 goto Shadow_End
ContinentKyiv_Battle0Intro::
 .string "Kyiv LEAGUE: Our river circuit\nwelcomes travelers. Ready for a\plocal battle?$"
ContinentKyiv_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentKyiv_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentKyiv_Battle1::
 lock
 faceplayer
 msgbox ContinentKyiv_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 359, ContinentKyiv_Battle1Intro, ContinentKyiv_Battle1Defeat, ContinentKyiv_Battle1Won
ContinentKyiv_Battle1Won::
 msgbox ContinentKyiv_Battle1After
 goto Shadow_End
ContinentKyiv_Battle1Intro::
 .string "Kyiv LEAGUE: Our river circuit\nwelcomes travelers. Ready for a\plocal battle?$"
ContinentKyiv_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentKyiv_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentKyivPast_Landmark::
 msgbox ContinentKyivPast_LandmarkText, MSGBOX_SIGN
 end
ContinentKyivPast_LandmarkText::
 .string "ST SOPHIA - KYIV. This is a\ncompact landmark district. The\pstation is south; trainers are\nalong the garden paths. You are\pvisiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentKyivPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentKyivPast_Battle0::
 lock
 faceplayer
 msgbox ContinentKyivPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 360, ContinentKyivPast_Battle0Intro, ContinentKyivPast_Battle0Defeat, ContinentKyivPast_Battle0Won
ContinentKyivPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentKyivPast_Battle0After
 goto Shadow_End
ContinentKyivPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pKyiv's couriers. Help us stop\nthe experiment?$"
ContinentKyivPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentKyivPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentMinsk_Landmark::
 msgbox ContinentMinsk_LandmarkText, MSGBOX_SIGN
 end
ContinentMinsk_LandmarkText::
 .string "NEMIGA DISTRICT - MINSK. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths.$"
ContinentMinsk_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentMinsk_KeeperText
 goto Shadow_End
ContinentMinsk_KeeperText::
 .string "ADA's network reached Minsk.\nWin the local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentMinsk_Battle0::
 lock
 faceplayer
 msgbox ContinentMinsk_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 361, ContinentMinsk_Battle0Intro, ContinentMinsk_Battle0Defeat, ContinentMinsk_Battle0Won
ContinentMinsk_Battle0Won::
 msgbox ContinentMinsk_Battle0After
 goto Shadow_End
ContinentMinsk_Battle0Intro::
 .string "Minsk LEAGUE: Our river circuit\nwelcomes travelers. Ready for a\plocal battle?$"
ContinentMinsk_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentMinsk_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentMinsk_Battle1::
 lock
 faceplayer
 msgbox ContinentMinsk_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 362, ContinentMinsk_Battle1Intro, ContinentMinsk_Battle1Defeat, ContinentMinsk_Battle1Won
ContinentMinsk_Battle1Won::
 msgbox ContinentMinsk_Battle1After
 goto Shadow_End
ContinentMinsk_Battle1Intro::
 .string "Minsk LEAGUE: Our river circuit\nwelcomes travelers. Ready for a\plocal battle?$"
ContinentMinsk_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentMinsk_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentMinskPast_Landmark::
 msgbox ContinentMinskPast_LandmarkText, MSGBOX_SIGN
 end
ContinentMinskPast_LandmarkText::
 .string "NEMIGA DISTRICT - MINSK. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths. You\pare visiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentMinskPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentMinskPast_Battle0::
 lock
 faceplayer
 msgbox ContinentMinskPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 363, ContinentMinskPast_Battle0Intro, ContinentMinskPast_Battle0Defeat, ContinentMinskPast_Battle0Won
ContinentMinskPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentMinskPast_Battle0After
 goto Shadow_End
ContinentMinskPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pMinsk's couriers. Help us stop\nthe experiment?$"
ContinentMinskPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentMinskPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentVilnius_Landmark::
 msgbox ContinentVilnius_LandmarkText, MSGBOX_SIGN
 end
ContinentVilnius_LandmarkText::
 .string "GEDIMINAS TOWER - VILNIUS. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths.$"
ContinentVilnius_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentVilnius_KeeperText
 goto Shadow_End
ContinentVilnius_KeeperText::
 .string "ADA's network reached Vilnius.\nWin the local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentVilnius_Battle0::
 lock
 faceplayer
 msgbox ContinentVilnius_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 364, ContinentVilnius_Battle0Intro, ContinentVilnius_Battle0Defeat, ContinentVilnius_Battle0Won
ContinentVilnius_Battle0Won::
 msgbox ContinentVilnius_Battle0After
 goto Shadow_End
ContinentVilnius_Battle0Intro::
 .string "Vilnius LEAGUE: Our garden\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentVilnius_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentVilnius_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentVilnius_Battle1::
 lock
 faceplayer
 msgbox ContinentVilnius_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 365, ContinentVilnius_Battle1Intro, ContinentVilnius_Battle1Defeat, ContinentVilnius_Battle1Won
ContinentVilnius_Battle1Won::
 msgbox ContinentVilnius_Battle1After
 goto Shadow_End
ContinentVilnius_Battle1Intro::
 .string "Vilnius LEAGUE: Our garden\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentVilnius_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentVilnius_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentVilniusPast_Landmark::
 msgbox ContinentVilniusPast_LandmarkText, MSGBOX_SIGN
 end
ContinentVilniusPast_LandmarkText::
 .string "GEDIMINAS TOWER - VILNIUS. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths. You\pare visiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentVilniusPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentVilniusPast_Battle0::
 lock
 faceplayer
 msgbox ContinentVilniusPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 366, ContinentVilniusPast_Battle0Intro, ContinentVilniusPast_Battle0Defeat, ContinentVilniusPast_Battle0Won
ContinentVilniusPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentVilniusPast_Battle0After
 goto Shadow_End
ContinentVilniusPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pVilnius's couriers. Help us\nstop the experiment?$"
ContinentVilniusPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentVilniusPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentRiga_Landmark::
 msgbox ContinentRiga_LandmarkText, MSGBOX_SIGN
 end
ContinentRiga_LandmarkText::
 .string "HOUSE OF BLACKHEADS - RIGA.\nThis is a compact landmark\pdistrict. The station is south;\ntrainers are along the garden\ppaths.$"
ContinentRiga_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentRiga_KeeperText
 goto Shadow_End
ContinentRiga_KeeperText::
 .string "ADA's network reached Riga. Win\nthe local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentRiga_Battle0::
 lock
 faceplayer
 msgbox ContinentRiga_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 367, ContinentRiga_Battle0Intro, ContinentRiga_Battle0Defeat, ContinentRiga_Battle0Won
ContinentRiga_Battle0Won::
 msgbox ContinentRiga_Battle0After
 goto Shadow_End
ContinentRiga_Battle0Intro::
 .string "Riga LEAGUE: Our river circuit\nwelcomes travelers. Ready for a\plocal battle?$"
ContinentRiga_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentRiga_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentRiga_Battle1::
 lock
 faceplayer
 msgbox ContinentRiga_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 368, ContinentRiga_Battle1Intro, ContinentRiga_Battle1Defeat, ContinentRiga_Battle1Won
ContinentRiga_Battle1Won::
 msgbox ContinentRiga_Battle1After
 goto Shadow_End
ContinentRiga_Battle1Intro::
 .string "Riga LEAGUE: Our river circuit\nwelcomes travelers. Ready for a\plocal battle?$"
ContinentRiga_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentRiga_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentRigaPast_Landmark::
 msgbox ContinentRigaPast_LandmarkText, MSGBOX_SIGN
 end
ContinentRigaPast_LandmarkText::
 .string "HOUSE OF BLACKHEADS - RIGA.\nThis is a compact landmark\pdistrict. The station is south;\ntrainers are along the garden\ppaths. You are visiting a\nwartime chapter. Your mission\pconcerns a fictional rescue\nnetwork.$"
ContinentRigaPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentRigaPast_Battle0::
 lock
 faceplayer
 msgbox ContinentRigaPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 369, ContinentRigaPast_Battle0Intro, ContinentRigaPast_Battle0Defeat, ContinentRigaPast_Battle0Won
ContinentRigaPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentRigaPast_Battle0After
 goto Shadow_End
ContinentRigaPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pRiga's couriers. Help us stop\nthe experiment?$"
ContinentRigaPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentRigaPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentTallinn_Landmark::
 msgbox ContinentTallinn_LandmarkText, MSGBOX_SIGN
 end
ContinentTallinn_LandmarkText::
 .string "TOWN HALL - TALLINN. This is a\ncompact landmark district. The\pstation is south; trainers are\nalong the garden paths.$"
ContinentTallinn_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentTallinn_KeeperText
 goto Shadow_End
ContinentTallinn_KeeperText::
 .string "ADA's network reached Tallinn.\nWin the local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentTallinn_Battle0::
 lock
 faceplayer
 msgbox ContinentTallinn_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 370, ContinentTallinn_Battle0Intro, ContinentTallinn_Battle0Defeat, ContinentTallinn_Battle0Won
ContinentTallinn_Battle0Won::
 msgbox ContinentTallinn_Battle0After
 goto Shadow_End
ContinentTallinn_Battle0Intro::
 .string "Tallinn LEAGUE: Our coast\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentTallinn_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentTallinn_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentTallinn_Battle1::
 lock
 faceplayer
 msgbox ContinentTallinn_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 371, ContinentTallinn_Battle1Intro, ContinentTallinn_Battle1Defeat, ContinentTallinn_Battle1Won
ContinentTallinn_Battle1Won::
 msgbox ContinentTallinn_Battle1After
 goto Shadow_End
ContinentTallinn_Battle1Intro::
 .string "Tallinn LEAGUE: Our coast\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentTallinn_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentTallinn_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentTallinnPast_Landmark::
 msgbox ContinentTallinnPast_LandmarkText, MSGBOX_SIGN
 end
ContinentTallinnPast_LandmarkText::
 .string "TOWN HALL - TALLINN. This is a\ncompact landmark district. The\pstation is south; trainers are\nalong the garden paths. You are\pvisiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentTallinnPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentTallinnPast_Battle0::
 lock
 faceplayer
 msgbox ContinentTallinnPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 372, ContinentTallinnPast_Battle0Intro, ContinentTallinnPast_Battle0Defeat, ContinentTallinnPast_Battle0Won
ContinentTallinnPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentTallinnPast_Battle0After
 goto Shadow_End
ContinentTallinnPast_Battle0Intro::
 .string "RESISTANCE: An infiltrator is\nusing closed hearts to threaten\pTallinn's couriers. Help us\nstop the experiment?$"
ContinentTallinnPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentTallinnPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
ContinentIstanbul_Landmark::
 msgbox ContinentIstanbul_LandmarkText, MSGBOX_SIGN
 end
ContinentIstanbul_LandmarkText::
 .string "HAGIA SOPHIA - ISTANBUL. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths.$"
ContinentIstanbul_Keeper::
 lock
 faceplayer
 special Shadow_CountryMemory
 goto_if_eq VAR_RESULT, 1, Shadow_CountryGarden
 goto_if_eq VAR_RESULT, 2, Shadow_CountryArchive
 msgbox ContinentIstanbul_KeeperText
 goto Shadow_End
ContinentIstanbul_KeeperText::
 .string "ADA's network reached Istanbul.\nWin the local matches, then use\pCELEBI after the Lisbon chapter\nto visit the past. We are\pwaiting for news of our old\nsanctuary and its missing\pledger.$"
ContinentIstanbul_Battle0::
 lock
 faceplayer
 msgbox ContinentIstanbul_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 373, ContinentIstanbul_Battle0Intro, ContinentIstanbul_Battle0Defeat, ContinentIstanbul_Battle0Won
ContinentIstanbul_Battle0Won::
 msgbox ContinentIstanbul_Battle0After
 goto Shadow_End
ContinentIstanbul_Battle0Intro::
 .string "Istanbul LEAGUE: Our coast\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentIstanbul_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentIstanbul_Battle0After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentIstanbul_Battle1::
 lock
 faceplayer
 msgbox ContinentIstanbul_Battle1Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 374, ContinentIstanbul_Battle1Intro, ContinentIstanbul_Battle1Defeat, ContinentIstanbul_Battle1Won
ContinentIstanbul_Battle1Won::
 msgbox ContinentIstanbul_Battle1After
 goto Shadow_End
ContinentIstanbul_Battle1Intro::
 .string "Istanbul LEAGUE: Our coast\ncircuit welcomes travelers.\pReady for a local battle?$"
ContinentIstanbul_Battle1Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentIstanbul_Battle1After::
 .string "Our circuit is always open for\npractice. Learn from defeat and\preturn when you are ready.$"
ContinentIstanbulPast_Landmark::
 msgbox ContinentIstanbulPast_LandmarkText, MSGBOX_SIGN
 end
ContinentIstanbulPast_LandmarkText::
 .string "HAGIA SOPHIA - ISTANBUL. This\nis a compact landmark district.\pThe station is south; trainers\nare along the garden paths. You\pare visiting a wartime chapter.\nYour mission concerns a\pfictional rescue network.$"
ContinentIstanbulPast_Keeper::
 lock
 faceplayer
 special Shadow_CountryStatus
 goto_if_eq VAR_RESULT, 0, Shadow_CountryUncleared
 goto Shadow_CountryChoice
ContinentIstanbulPast_Battle0::
 lock
 faceplayer
 msgbox ContinentIstanbulPast_Battle0Intro, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 trainerbattle_single 375, ContinentIstanbulPast_Battle0Intro, ContinentIstanbulPast_Battle0Defeat, ContinentIstanbulPast_Battle0Won
ContinentIstanbulPast_Battle0Won::
 special Shadow_CountryClear
 msgbox ContinentIstanbulPast_Battle0After
 goto Shadow_End
ContinentIstanbulPast_Battle0Intro::
 .string "KEEPER: Istanbul supports a\nsecret refuge. Test your\ppartners against mine, then\nhelp us choose how to preserve\pthe sanctuary?$"
ContinentIstanbulPast_Battle0Defeat::
 .string "You stood beside your partners.\nWe yield.$"
ContinentIstanbulPast_Battle0After::
 .string "The sanctuary is safe. Speak to\nits keeper to choose what\psurvives into the future.$"
Shadow_WorldMenu::
 lock
 faceplayer
 msgbox Shadow_WorldIntro
 multichoice 0, 0, MULTICHOICE_SHADOW_WORLD_0, FALSE
 goto_if_eq VAR_RESULT, 0, Shadow_WorldRegion0
 goto_if_eq VAR_RESULT, 1, Shadow_WorldRegion1
 goto_if_eq VAR_RESULT, 2, Shadow_WorldRegion2
 goto_if_eq VAR_RESULT, 3, Shadow_WorldRegion3
 goto_if_eq VAR_RESULT, 4, Shadow_WorldRegion4
 goto_if_eq VAR_RESULT, 5, Shadow_WorldRegion5
 goto Shadow_End
Shadow_WorldIntro::
 .string "EUROPE PASSPORT: Choose a\nregion, then your destination.\pCELEBI travels between eras\nafter the Lisbon mission. B\pcancels.$"
Shadow_WorldRegion0::
 multichoice 0, 0, MULTICHOICE_SHADOW_WORLD_1, FALSE
 goto_if_eq VAR_RESULT, 0, Shadow_WorldGo0
 goto_if_eq VAR_RESULT, 1, Shadow_WorldGo1
 goto_if_eq VAR_RESULT, 2, Shadow_WorldGo2
 goto_if_eq VAR_RESULT, 3, Shadow_WorldGo3
 goto_if_eq VAR_RESULT, 4, Shadow_WorldGo4
 goto_if_eq VAR_RESULT, 5, Shadow_WorldGo5
 goto_if_eq VAR_RESULT, 6, Shadow_WorldGo6
 goto_if_eq VAR_RESULT, 7, Shadow_WorldGo7
 goto Shadow_End
Shadow_WorldRegion1::
 multichoice 0, 0, MULTICHOICE_SHADOW_WORLD_2, FALSE
 goto_if_eq VAR_RESULT, 0, Shadow_WorldGo8
 goto_if_eq VAR_RESULT, 1, Shadow_WorldGo9
 goto_if_eq VAR_RESULT, 2, Shadow_WorldGo10
 goto_if_eq VAR_RESULT, 3, Shadow_WorldGo11
 goto_if_eq VAR_RESULT, 4, Shadow_WorldGo12
 goto_if_eq VAR_RESULT, 5, Shadow_WorldGo13
 goto_if_eq VAR_RESULT, 6, Shadow_WorldGo14
 goto Shadow_End
Shadow_WorldRegion2::
 multichoice 0, 0, MULTICHOICE_SHADOW_WORLD_3, FALSE
 goto_if_eq VAR_RESULT, 0, Shadow_WorldGo15
 goto_if_eq VAR_RESULT, 1, Shadow_WorldGo16
 goto_if_eq VAR_RESULT, 2, Shadow_WorldGo17
 goto_if_eq VAR_RESULT, 3, Shadow_WorldGo18
 goto_if_eq VAR_RESULT, 4, Shadow_WorldGo19
 goto_if_eq VAR_RESULT, 5, Shadow_WorldGo20
 goto_if_eq VAR_RESULT, 6, Shadow_WorldGo21
 goto Shadow_End
Shadow_WorldRegion3::
 multichoice 0, 0, MULTICHOICE_SHADOW_WORLD_4, FALSE
 goto_if_eq VAR_RESULT, 0, Shadow_WorldGo22
 goto_if_eq VAR_RESULT, 1, Shadow_WorldGo23
 goto_if_eq VAR_RESULT, 2, Shadow_WorldGo24
 goto_if_eq VAR_RESULT, 3, Shadow_WorldGo25
 goto_if_eq VAR_RESULT, 4, Shadow_WorldGo26
 goto_if_eq VAR_RESULT, 5, Shadow_WorldGo27
 goto Shadow_End
Shadow_WorldRegion4::
 multichoice 0, 0, MULTICHOICE_SHADOW_WORLD_5, FALSE
 goto_if_eq VAR_RESULT, 0, Shadow_WorldGo28
 goto_if_eq VAR_RESULT, 1, Shadow_WorldGo29
 goto_if_eq VAR_RESULT, 2, Shadow_WorldGo30
 goto_if_eq VAR_RESULT, 3, Shadow_WorldGo31
 goto Shadow_End
Shadow_WorldRegion5::
 multichoice 0, 0, MULTICHOICE_SHADOW_WORLD_6, FALSE
 goto_if_eq VAR_RESULT, 0, Shadow_WorldGo32
 goto_if_eq VAR_RESULT, 1, Shadow_WorldGo33
 goto_if_eq VAR_RESULT, 2, Shadow_WorldGo34
 goto_if_eq VAR_RESULT, 3, Shadow_WorldGo35
 goto_if_eq VAR_RESULT, 4, Shadow_WorldGo36
 goto_if_eq VAR_RESULT, 5, Shadow_WorldGo37
 goto_if_eq VAR_RESULT, 6, Shadow_WorldGo38
 goto Shadow_End
Shadow_WorldGo0::
 warp MAP_CONTINENT_LONDON, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo1::
 warp MAP_CONTINENT_PARIS, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo2::
 warp MAP_CONTINENT_BERLIN, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo3::
 warp MAP_CONTINENT_BRUSSELS, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo4::
 warp MAP_CONTINENT_AMSTERDAM, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo5::
 warp MAP_CONTINENT_VIENNA, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo6::
 warp MAP_CONTINENT_PRAGUE, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo7::
 warp MAP_CONTINENT_BRATISLAVA, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo8::
 warp MAP_CONTINENT_BERN, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo9::
 warp MAP_CONTINENT_ROME, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo10::
 warp MAP_CONTINENT_ATHENS, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo11::
 warp MAP_CONTINENT_MADRID, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo12::
 warp MAP_CONTINENT_LISBON, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo13::
 warp MAP_CONTINENT_WARSAW, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo14::
 warp MAP_CONTINENT_LUXEMBOURG, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo15::
 warp MAP_CONTINENT_COPENHAGEN, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo16::
 warp MAP_CONTINENT_OSLO, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo17::
 warp MAP_CONTINENT_STOCKHOLM, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo18::
 warp MAP_CONTINENT_HELSINKI, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo19::
 warp MAP_CONTINENT_REYKJAVIK, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo20::
 warp MAP_CONTINENT_DUBLIN, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo21::
 warp MAP_CONTINENT_VALLETTA, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo22::
 warp MAP_CONTINENT_BUDAPEST, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo23::
 warp MAP_CONTINENT_BUCHAREST, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo24::
 warp MAP_CONTINENT_SOFIA, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo25::
 warp MAP_CONTINENT_TIRANA, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo26::
 warp MAP_CONTINENT_BELGRADE, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo27::
 warp MAP_CONTINENT_ZAGREB, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo28::
 warp MAP_CONTINENT_LJUBLJANA, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo29::
 warp MAP_CONTINENT_SARAJEVO, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo30::
 warp MAP_CONTINENT_KOTOR, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo31::
 warp MAP_CONTINENT_SKOPJE, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo32::
 warp MAP_CONTINENT_MOSCOW, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo33::
 warp MAP_CONTINENT_KYIV, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo34::
 warp MAP_CONTINENT_MINSK, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo35::
 warp MAP_CONTINENT_VILNIUS, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo36::
 warp MAP_CONTINENT_RIGA, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo37::
 warp MAP_CONTINENT_TALLINN, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_WorldGo38::
 warp MAP_CONTINENT_ISTANBUL, -1, 15, 30
 waitstate
 goto Shadow_End
Shadow_CountryTime::
 lock
 faceplayer
 goto_if_lt VAR_SHADOW_STAGE, 12, Shadow_TimeLocked
 msgbox Shadow_TimeOffer, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 special Shadow_CountryTravel
 waitstate
 goto Shadow_End
Shadow_TimeLocked::
 msgbox Shadow_TimeLockedText
 goto Shadow_End
Shadow_CountryChoice::
 special Shadow_CountryMemory
 goto_if_ne VAR_RESULT, 0, Shadow_ChoiceDone
 msgbox Shadow_ChoiceOffer, MSGBOX_YESNO
 setvar VAR_0x8004, 1
 goto_if_eq VAR_RESULT, YES, Shadow_ChoiceCommit
 setvar VAR_0x8004, 2
Shadow_ChoiceCommit::
 special Shadow_CountryDecide
 msgbox Shadow_ChoiceSaved
 goto Shadow_End
Shadow_ChoiceDone::
 msgbox Shadow_ChoiceDoneText
 goto Shadow_End
Shadow_CountryUncleared::
 msgbox Shadow_UnclearedText
 goto Shadow_End
Shadow_CountryGarden::
 msgbox Shadow_GardenText
 goto Shadow_End
Shadow_CountryArchive::
 msgbox Shadow_ArchiveText
 goto Shadow_End
Shadow_VisibleWild::
 lock
 faceplayer
 msgbox Shadow_VisibleText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 special Shadow_StartVisible
 dowildbattle
 removeobject VAR_LAST_TALKED
 goto Shadow_End
Shadow_TimeOffer::
 .string "CELEBI: Cross to the other era\nof this city? Your decisions\pstay with the timeline. You can\nreturn whenever you choose.$"
Shadow_TimeLockedText::
 .string "ADA must stabilize the time\nanchor at Lisbon. Continue the\pbadge journey first.$"
Shadow_ChoiceOffer::
 .string "KEEPER: Preserve the living\nsanctuary? YES saves its garden\pand rare partners. NO preserves\nthe research archive and its\pworkshop instead. This decision\ncannot be changed.$"
Shadow_ChoiceSaved::
 .string "The anchor remembers your\nchoice. Return through CELEBI\pto see what survived.$"
Shadow_ChoiceDoneText::
 .string "Your decision is already\nanchored. This place will carry\pyour memory into the future.$"
Shadow_UnclearedText::
 .string "The refuge is threatened. Win\nthe wartime battle north of the\pstation first.$"
Shadow_GardenText::
 .string "My family remembers a traveler\nwho saved this sanctuary. The\pgarden still blooms. EEVEE\nreturned to its habitat, and\pour eastern path is open.$"
Shadow_ArchiveText::
 .string "The garden became an archive.\nThe old research was preserved\pwithout repeating its cruelty.\nVOLTORB now thrives beside the\pworkshop. Our eastern path is\nopen.$"
Shadow_VisibleText::
 .string "A wild partner is exploring\nhere. Approach it for a battle?\pYou may catch it with a POKE\nBALL.$"

Shadow_NetworkFinale::
 lock
 faceplayer
 special Shadow_NetworkStatus
 goto_if_lt VAR_RESULT, 39, Shadow_NetworkPending
 goto_if_eq VAR_SHADOW_NETWORK_REWARD, 1, Shadow_NetworkThanks
 giveitem ITEM_MASTER_BALL, 1
 goto_if_eq VAR_RESULT, 0, Shadow_End
 setvar VAR_SHADOW_NETWORK_REWARD, 1
Shadow_NetworkThanks::
 msgbox Shadow_NetworkCompleteText
 goto Shadow_End
Shadow_NetworkPending::
 msgbox Shadow_NetworkPendingText
 goto Shadow_End
Shadow_NetworkPendingText::
 .string "ADA: {STR_VAR_1} of 39 local memories\nare anchored. Revisit each country\pthrough its station and CELEBI.\nProtect its wartime refuge, then\pchoose the future with its keeper.\nEvery community deserves a say.$"
Shadow_NetworkCompleteText::
 .string "ADA: All 39 communities have\nchosen their futures. The shadow\pnetwork has become a rescue\nnetwork. We keep the records of\pthe harm, and care for those who\nsurvived. Your journey gave these\pplaces partners, not weapons.\nThe League will remember you.$"

Shadow_Storage::
 lock
 faceplayer
 msgbox Shadow_StorageText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, Shadow_End
 special ShowPokemonStorageSystemPC
 waitstate
 msgbox Shadow_StorageReturnText
 goto Shadow_End
Shadow_StorageText::
 .string "Our partner relay reaches your\nPOKEMON storage across both eras.\pWould you like to manage your team?$"
Shadow_StorageReturnText::
 .string "Your partners are safe with us.\nCome back whenever you need them.$"

Shadow_TMRewardText::
 .string "Your badge comes with this TM.\nTeach it to a compatible partner\pand try a new battle strategy!$"
Shadow_TMRewardFull::
 msgbox Shadow_TMRewardFullText
 goto Shadow_End
Shadow_TMRewardFullText::
 .string "There is no room for your TM.\nMake space, then talk to me again.\pYour badge and reward are safe.$"
