EuropeChateauVisitor_MapScripts::
 .byte 0

EuropeChateauVisitor_Enter::
 lockall
 msgbox EuropeChateauVisitor_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeChateauVisitor_End
 closemessage
 warp MAP_EUROPE_CHATEAU_VISITOR, 5, 7
 waitstate
 releaseall
 end

EuropeChateauVisitor_Exit::
 lockall
 warp MAP_EUROPE_CHANTILLY, 51, 11
 waitstate
 releaseall
 end

EuropeChateauVisitor_End::
 releaseall
 end

EuropeChateauVisitor_EntryText::
 .string "CHATEAU VISITOR ROOM\n"
 .string "Step inside and browse the displays?$"

EuropeChateauVisitor_Guide::
 lock
 faceplayer
 msgbox EuropeChateauVisitor_GuideText, MSGBOX_DEFAULT
 release
 end

EuropeChateauVisitor_GuideText::
 .string "Welcome to the CHATEAU visitor room!\n"
 .string "Browse the garden and moat displays.\p"
 .string "The garden paths and moat are outside.\n"
 .string "Please keep the water and paths clean.\p"
 .string "Leave through the south doorway.\n"
 .string "You return to the CHATEAU court.$"

EuropeChateauVisitor_GardenExhibit::
 lock
 faceplayer
 msgbox EuropeChateauVisitor_GardenExhibitText, MSGBOX_DEFAULT
 release
 end

EuropeChateauVisitor_GardenExhibitText::
 .string "A garden plan shows paths and water.\n"
 .string "Watch quietly for visiting POKEMON.\p"
 .string "Keep notes without disturbing nests.\n"
 .string "Leave flowers for the next visitor.$"

EuropeChateauVisitor_RiverExhibit::
 lock
 faceplayer
 msgbox EuropeChateauVisitor_RiverExhibitText, MSGBOX_DEFAULT
 release
 end

EuropeChateauVisitor_RiverExhibitText::
 .string "A sketch follows the CHATEAU moat.\n"
 .string "Bridges lead back to the town paths.\p"
 .string "The station is east of the square.\n"
 .string "The free clinic is on its west side.$"
