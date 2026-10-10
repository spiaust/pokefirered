EuropePalaceVisitor_MapScripts::
 .byte 0

EuropePalaceVisitor_Enter::
 lockall
 msgbox EuropePalaceVisitor_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropePalaceVisitor_End
 closemessage
 warp MAP_EUROPE_PALACE_VISITOR, 5, 7
 waitstate
 releaseall
 end

EuropePalaceVisitor_Exit::
 lockall
 warp MAP_EUROPE_ORANIENBURG, 48, 9
 waitstate
 releaseall
 end

EuropePalaceVisitor_End::
 releaseall
 end

EuropePalaceVisitor_EntryText::
 .string "PALACE VISITOR ROOM\n"
 .string "Step inside and browse the displays?$"

EuropePalaceVisitor_Guide::
 lock
 faceplayer
 msgbox EuropePalaceVisitor_GuideText, MSGBOX_DEFAULT
 release
 end

EuropePalaceVisitor_GuideText::
 .string "Welcome to the PALACE visitor room!\n"
 .string "Browse the park and HAVEL displays.\p"
 .string "The park and Havel are outside.\n"
 .string "Please keep the water and paths clean.\p"
 .string "Leave through the south doorway.\n"
 .string "You return to the PALACE court.$"

EuropePalaceVisitor_GardenExhibit::
 lock
 faceplayer
 msgbox EuropePalaceVisitor_GardenExhibitText, MSGBOX_DEFAULT
 release
 end

EuropePalaceVisitor_GardenExhibitText::
 .string "A garden plan shows paths and water.\n"
 .string "Watch quietly for visiting POKEMON.\p"
 .string "Keep notes without disturbing nests.\n"
 .string "Leave flowers for the next visitor.$"

EuropePalaceVisitor_RiverExhibit::
 lock
 faceplayer
 msgbox EuropePalaceVisitor_RiverExhibitText, MSGBOX_DEFAULT
 release
 end

EuropePalaceVisitor_RiverExhibitText::
 .string "A sketch follows the HAVEL river.\n"
 .string "Town bridges link the river banks.\p"
 .string "The station is east of the square.\n"
 .string "The free clinic is on its west side.$"
