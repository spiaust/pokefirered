EuropeRadcliffeVisitor_MapScripts::
 .byte 0

EuropeRadcliffeVisitor_Enter::
 lockall
 msgbox EuropeRadcliffeVisitor_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeRadcliffeVisitor_End
 closemessage
 warp MAP_EUROPE_RADCLIFFE_VISITOR, 5, 7
 waitstate
 releaseall
 end

EuropeRadcliffeVisitor_Exit::
 lockall
 warp MAP_EUROPE_OXFORD, 38, 10
 waitstate
 releaseall
 end

EuropeRadcliffeVisitor_End::
 releaseall
 end

EuropeRadcliffeVisitor_EntryText::
 .string "RADCLIFFE VISITOR ROOM\n"
 .string "Step inside and browse the displays?$"

EuropeRadcliffeVisitor_Guide::
 lock
 faceplayer
 msgbox EuropeRadcliffeVisitor_GuideText, MSGBOX_DEFAULT
 release
 end

EuropeRadcliffeVisitor_GuideText::
 .string "Welcome to the RADCLIFFE room!\n"
 .string "Browse the notes beside the shelves.\p"
 .string "This is a quiet room for reading.\n"
 .string "Share the tables with other visitors.\p"
 .string "Leave through the south doorway.\n"
 .string "You return to RADCLIFFE SQUARE.$"

EuropeRadcliffeVisitor_ReadingExhibit::
 lock
 faceplayer
 msgbox EuropeRadcliffeVisitor_ReadingExhibitText, MSGBOX_DEFAULT
 release
 end

EuropeRadcliffeVisitor_ReadingExhibitText::
 .string "A notebook records careful sightings.\n"
 .string "Write where and when you saw POKEMON.\p"
 .string "Compare notes before drawing a map.\n"
 .string "Leave the books for the next reader.$"

EuropeRadcliffeVisitor_ObservationExhibit::
 lock
 faceplayer
 msgbox EuropeRadcliffeVisitor_ObservationExhibitText, MSGBOX_DEFAULT
 release
 end

EuropeRadcliffeVisitor_ObservationExhibitText::
 .string "A sketch shows the CHERWELL bridges.\n"
 .string "MAGDALEN lies east of the square.\p"
 .string "The station is east of the square.\n"
 .string "The free clinic is on its west side.$"
