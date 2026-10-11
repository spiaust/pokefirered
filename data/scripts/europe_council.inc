@ Separate post-story championship. Native save layout is unchanged.
EuropeCouncil_Reception::
 lock
 faceplayer
 goto_if_ne VAR_EUROPE_MAIN_CONCLUDED, 1, EuropeCouncil_Locked
 msgbox EuropeCouncil_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeCouncil_End
 closemessage
 warp MAP_EUROPE_COUNCIL_HALL, 5, 7
 waitstate
 release
 end
EuropeCouncil_Locked::
 msgbox EuropeCouncil_LockedText
 goto EuropeCouncil_End
EuropeCouncil_Exit::
 lockall
 warp MAP_EUROPE_LONDON_READING_ROOM, 5, 7
 waitstate
 releaseall
 end
EuropeCouncil_Nurse::
 lock
 faceplayer
 special HealPlayerParty
 msgbox EuropeCouncil_HealText
 goto EuropeCouncil_End
EuropeCouncil_Steward::
 lock
 faceplayer
 goto_if_eq VAR_EUROPE_COUNCIL_TITLE, 1, EuropeCouncil_Reward
 goto_if_eq VAR_EUROPE_COUNCIL_STAGE, 5, EuropeCouncil_Replay
 msgbox EuropeCouncil_RulesText
 goto EuropeCouncil_Next
EuropeCouncil_Next::
 goto_if_eq VAR_EUROPE_COUNCIL_STAGE, 0, EuropeCouncil_Next0
 goto_if_eq VAR_EUROPE_COUNCIL_STAGE, 1, EuropeCouncil_Next1
 goto_if_eq VAR_EUROPE_COUNCIL_STAGE, 2, EuropeCouncil_Next2
 goto_if_eq VAR_EUROPE_COUNCIL_STAGE, 3, EuropeCouncil_Next3
 msgbox EuropeCouncil_Next4Text
 goto EuropeCouncil_End
EuropeCouncil_Replay::
 msgbox EuropeCouncil_ReplayText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeCouncil_End
 setvar VAR_EUROPE_COUNCIL_STAGE, 0
 msgbox EuropeCouncil_RestartText
 goto EuropeCouncil_End
EuropeCouncil_End::
 release
 end
EuropeCouncil_Alfred::
 lock
 faceplayer
 goto_if_ne VAR_EUROPE_MAIN_CONCLUDED, 1, EuropeCouncil_Locked
 goto_if_lt VAR_EUROPE_COUNCIL_STAGE, 0, EuropeCouncil_Order
 goto_if_gt VAR_EUROPE_COUNCIL_STAGE, 0, EuropeCouncil_Beaten
 msgbox EuropeCouncil_AlfredOfferText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeCouncil_End
 cleartrainerflag TRAINER_EUROPE_COUNCIL_ALFRED
 trainerbattle_single TRAINER_EUROPE_COUNCIL_ALFRED, EuropeCouncil_AlfredIntroText, EuropeCouncil_AlfredDefeatText, EuropeCouncil_AlfredVictory
 goto EuropeCouncil_End
EuropeCouncil_AlfredVictory::
 setvar VAR_EUROPE_COUNCIL_STAGE, 1
 msgbox EuropeCouncil_WinText
 goto EuropeCouncil_Next
EuropeCouncil_Solene::
 lock
 faceplayer
 goto_if_ne VAR_EUROPE_MAIN_CONCLUDED, 1, EuropeCouncil_Locked
 goto_if_lt VAR_EUROPE_COUNCIL_STAGE, 1, EuropeCouncil_Order
 goto_if_gt VAR_EUROPE_COUNCIL_STAGE, 1, EuropeCouncil_Beaten
 msgbox EuropeCouncil_SoleneOfferText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeCouncil_End
 cleartrainerflag TRAINER_EUROPE_COUNCIL_SOLENE
 trainerbattle_single TRAINER_EUROPE_COUNCIL_SOLENE, EuropeCouncil_SoleneIntroText, EuropeCouncil_SoleneDefeatText, EuropeCouncil_SoleneVictory
 goto EuropeCouncil_End
EuropeCouncil_SoleneVictory::
 setvar VAR_EUROPE_COUNCIL_STAGE, 2
 msgbox EuropeCouncil_WinText
 goto EuropeCouncil_Next
EuropeCouncil_Otmar::
 lock
 faceplayer
 goto_if_ne VAR_EUROPE_MAIN_CONCLUDED, 1, EuropeCouncil_Locked
 goto_if_lt VAR_EUROPE_COUNCIL_STAGE, 2, EuropeCouncil_Order
 goto_if_gt VAR_EUROPE_COUNCIL_STAGE, 2, EuropeCouncil_Beaten
 msgbox EuropeCouncil_OtmarOfferText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeCouncil_End
 cleartrainerflag TRAINER_EUROPE_COUNCIL_OTMAR
 trainerbattle_single TRAINER_EUROPE_COUNCIL_OTMAR, EuropeCouncil_OtmarIntroText, EuropeCouncil_OtmarDefeatText, EuropeCouncil_OtmarVictory
 goto EuropeCouncil_End
EuropeCouncil_OtmarVictory::
 setvar VAR_EUROPE_COUNCIL_STAGE, 3
 msgbox EuropeCouncil_WinText
 goto EuropeCouncil_Next
EuropeCouncil_Elara::
 lock
 faceplayer
 goto_if_ne VAR_EUROPE_MAIN_CONCLUDED, 1, EuropeCouncil_Locked
 goto_if_lt VAR_EUROPE_COUNCIL_STAGE, 3, EuropeCouncil_Order
 goto_if_gt VAR_EUROPE_COUNCIL_STAGE, 3, EuropeCouncil_Beaten
 msgbox EuropeCouncil_ElaraOfferText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeCouncil_End
 cleartrainerflag TRAINER_EUROPE_COUNCIL_ELARA
 trainerbattle_single TRAINER_EUROPE_COUNCIL_ELARA, EuropeCouncil_ElaraIntroText, EuropeCouncil_ElaraDefeatText, EuropeCouncil_ElaraVictory
 goto EuropeCouncil_End
EuropeCouncil_ElaraVictory::
 setvar VAR_EUROPE_COUNCIL_STAGE, 4
 msgbox EuropeCouncil_WinText
 goto EuropeCouncil_Next
EuropeCouncil_Rowan::
 lock
 faceplayer
 goto_if_ne VAR_EUROPE_MAIN_CONCLUDED, 1, EuropeCouncil_Locked
 goto_if_lt VAR_EUROPE_COUNCIL_STAGE, 4, EuropeCouncil_Order
 goto_if_gt VAR_EUROPE_COUNCIL_STAGE, 4, EuropeCouncil_Beaten
 msgbox EuropeCouncil_RowanOfferText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeCouncil_End
 cleartrainerflag TRAINER_EUROPE_COUNCIL_ROWAN
 trainerbattle_single TRAINER_EUROPE_COUNCIL_ROWAN, EuropeCouncil_RowanIntroText, EuropeCouncil_RowanDefeatText, EuropeCouncil_RowanVictory
 goto EuropeCouncil_End
EuropeCouncil_RowanVictory::
 setvar VAR_EUROPE_COUNCIL_STAGE, 5
 goto_if_ne VAR_EUROPE_COUNCIL_TITLE, 0, EuropeCouncil_Conclusion
 setvar VAR_EUROPE_COUNCIL_TITLE, 1
EuropeCouncil_Conclusion::
 msgbox EuropeCouncil_ChampionText
 goto_if_eq VAR_EUROPE_COUNCIL_TITLE, 2, EuropeCouncil_End
EuropeCouncil_Reward::
 checkitemspace ITEM_RARE_CANDY, 1
 goto_if_eq VAR_RESULT, FALSE, EuropeCouncil_Full
 giveitem ITEM_RARE_CANDY, 1
 setvar VAR_EUROPE_COUNCIL_TITLE, 2
 msgbox EuropeCouncil_RewardText
 goto EuropeCouncil_End
EuropeCouncil_Full::
 msgbox EuropeCouncil_FullText
 goto EuropeCouncil_End
EuropeCouncil_Order::
 msgbox EuropeCouncil_OrderText
 goto EuropeCouncil_Next
EuropeCouncil_Beaten::
 msgbox EuropeCouncil_BeatenText
 goto EuropeCouncil_End
EuropeCouncil_Next0::
 msgbox EuropeCouncil_Next0Text
 goto EuropeCouncil_End
EuropeCouncil_Next1::
 msgbox EuropeCouncil_Next1Text
 goto EuropeCouncil_End
EuropeCouncil_Next2::
 msgbox EuropeCouncil_Next2Text
 goto EuropeCouncil_End
EuropeCouncil_Next3::
 msgbox EuropeCouncil_Next3Text
 goto EuropeCouncil_End
EuropeCouncil_EntryText::
 .string "EUROPEAN COUNCIL HALL\n"
 .string "Four members, then the CHAMPION.\p"
 .string "Levels 18-23. Free healing inside.\n"
 .string "Save or leave between battles.\p"
 .string "Your cleared matches stay cleared.\n"
 .string "Enter the COUNCIL HALL?$"
EuropeCouncil_LockedText::
 .string "First finish ADA's CELEBI journey.\n"
 .string "Read her final report in OXFORD.\p"
 .string "The COUNCIL opens after her ending.\n"
 .string "Your existing adventures stay safe.$"
EuropeCouncil_HealText::
 .string "Your partners are fully rested!\n"
 .string "Healing is free between matches.$"
EuropeCouncil_RulesText::
 .string "Face four COUNCIL members in order,\n"
 .string "then challenge CHAMPION ROWAN.\p"
 .string "Teams range from levels 18 to 23.\n"
 .string "Practice with COACH IVO in this hall.\p"
 .string "The nurse heals HP, status and PP.\n"
 .string "The shop sells stronger healing.\p"
 .string "Save or leave between matches.\n"
 .string "Losing keeps your cleared matches.\p"
 .string "A loss uses normal blackout rules.\n"
 .string "Return here from the LONDON clinic.$"
EuropeCouncil_ReplayText::
 .string "EUROPEAN COUNCIL CHAMPION!\n"
 .string "Your title and first prize are safe.\p"
 .string "Start another five-match circuit?\n"
 .string "The first prize is awarded once.$"
EuropeCouncil_RestartText::
 .string "A new circuit begins with ALFRED.\n"
 .string "Your CHAMPION title stays recorded!$"
EuropeCouncil_OrderText::
 .string "Please follow the COUNCIL order.\n"
 .string "The steward can name your next match.$"
EuropeCouncil_BeatenText::
 .string "This match is cleared for this run.\n"
 .string "Speak to the steward for directions.$"
EuropeCouncil_WinText::
 .string "COUNCIL victory recorded!\n"
 .string "Heal before your next match.$"
EuropeCouncil_ChampionText::
 .string "EUROPEAN COUNCIL CHAMPION!\p"
 .string "Three nations' voices, one journey.\n"
 .string "Your partners have earned our respect.\p"
 .string "The championship is complete!\n"
 .string "Your title is recorded in your save.\p"
 .string "Speak to the steward to play again.\n"
 .string "Your first prize can be claimed once.$"
EuropeCouncil_RewardText::
 .string "Take this RARE CANDY as our first\n"
 .string "championship prize. Well done!$"
EuropeCouncil_FullText::
 .string "Your CHAMPION title is already safe.\n"
 .string "Make room for one RARE CANDY.\p"
 .string "Return to the steward for your prize.\n"
 .string "No further battle is required.$"
EuropeCouncil_AlfredOfferText::
 .string "I am ALFRED,\n"
 .string "ENGLAND's CROWN OF THE SKIES.\p"
 .string "These are ceremonial COUNCIL titles.\n"
 .string "Our partners rule only the arena.\p"
 .string "Match 1 of 5. Ready to battle?$"
EuropeCouncil_AlfredIntroText::
 .string "Let our partners show their strength!$"
EuropeCouncil_AlfredDefeatText::
 .string "Your teamwork deserves this victory!$"
EuropeCouncil_Next0Text::
 .string "Next: ALFRED, COUNCIL 1.\n"
 .string "North row: leftmost trainer.$"
EuropeCouncil_SoleneOfferText::
 .string "I am SOLENE,\n"
 .string "FRANCE's GARDEN REGENT.\p"
 .string "Match 2 of 5. Ready to battle?$"
EuropeCouncil_SoleneIntroText::
 .string "Let our partners show their strength!$"
EuropeCouncil_SoleneDefeatText::
 .string "Your teamwork deserves this victory!$"
EuropeCouncil_Next1Text::
 .string "Next: SOLENE, COUNCIL 2.\n"
 .string "North row: second trainer.$"
EuropeCouncil_OtmarOfferText::
 .string "I am OTMAR,\n"
 .string "GERMANY's IRON WARDEN.\p"
 .string "Match 3 of 5. Ready to battle?$"
EuropeCouncil_OtmarIntroText::
 .string "Let our partners show their strength!$"
EuropeCouncil_OtmarDefeatText::
 .string "Your teamwork deserves this victory!$"
EuropeCouncil_Next2Text::
 .string "Next: OTMAR, COUNCIL 3.\n"
 .string "North row: middle trainer.$"
EuropeCouncil_ElaraOfferText::
 .string "I am ELARA,\n"
 .string "the ALLIANCE's RIVER GUARDIAN.\p"
 .string "Match 4 of 5. Ready to battle?$"
EuropeCouncil_ElaraIntroText::
 .string "Let our partners show their strength!$"
EuropeCouncil_ElaraDefeatText::
 .string "Your teamwork deserves this victory!$"
EuropeCouncil_Next3Text::
 .string "Next: ELARA, COUNCIL 4.\n"
 .string "North row: fourth trainer.$"
EuropeCouncil_RowanOfferText::
 .string "I am ROWAN,\n"
 .string "the COUNCIL CHAMPION.\p"
 .string "Match 5 of 5. Ready to battle?$"
EuropeCouncil_RowanIntroText::
 .string "Let our partners show their strength!$"
EuropeCouncil_RowanDefeatText::
 .string "Your teamwork deserves this victory!$"
EuropeCouncil_Next4Text::
 .string "Next: ROWAN, CHAMPION.\n"
 .string "North row: rightmost trainer.$"

EuropeCouncil_Coach::
 lock
 faceplayer
 goto_if_ne VAR_EUROPE_MAIN_CONCLUDED, 1, EuropeCouncil_Locked
 msgbox EuropeCouncil_CoachOfferText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeCouncil_End
 special HealPlayerParty
 cleartrainerflag TRAINER_EUROPE_COUNCIL_COACH
 trainerbattle_single TRAINER_EUROPE_COUNCIL_COACH, EuropeCouncil_CoachIntroText, EuropeCouncil_CoachDefeatText, EuropeCouncil_CoachVictory
 goto EuropeCouncil_End
EuropeCouncil_CoachVictory::
 special HealPlayerParty
 msgbox EuropeCouncil_CoachWinText
 goto EuropeCouncil_End
EuropeCouncil_CoachOfferText::
 .string "I am IVO, the practice coach.\n"
 .string "My partners are levels 14 to 16.\p"
 .string "Your team heals before each bout,\n"
 .string "and after each practice victory.\p"
 .string "Earn normal experience and prizes.\n"
 .string "Practice never changes Council order.\p"
 .string "Repeat as often as you need.\n"
 .string "Ready for a practice battle?$"
EuropeCouncil_CoachIntroText::
 .string "Practice makes a stronger partnership!$"
EuropeCouncil_CoachDefeatText::
 .string "Good work! Your partners are growing!$"
EuropeCouncil_CoachWinText::
 .string "Your partners are healed again.\n"
 .string "Come back whenever you need practice.\p"
 .string "Aim for a team around levels 22-25\n"
 .string "before facing the CHAMPION.$"

EuropeCouncil_Shop::
 goto_if_questlog EventScript_ReleaseEnd
 lock
 faceplayer
 message EuropeCouncil_ShopWelcomeText
 waitmessage
 pokemart EuropeCouncil_ShopItems
 msgbox EuropeCouncil_ShopGoodbyeText
 goto EuropeCouncil_End
 .align 2
EuropeCouncil_ShopItems::
 .2byte ITEM_SUPER_POTION
 .2byte ITEM_ANTIDOTE
 .2byte ITEM_PARALYZE_HEAL
 .2byte ITEM_AWAKENING
 .2byte ITEM_POKE_BALL
 .2byte ITEM_NONE
EuropeCouncil_ShopWelcomeText::
 .string "COUNCIL SUPPLIES\n"
 .string "SUPER POTIONS restore 50 HP.\p"
 .string "They cost 700 each.\n"
 .string "Practice prizes can fund your supplies.$"
EuropeCouncil_ShopGoodbyeText::
 .string "Use your BAG to heal during battle.\n"
 .string "Our nurse provides free care outside.$"
