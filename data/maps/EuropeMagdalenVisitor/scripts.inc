EuropeMagdalenVisitor_MapScripts::
 .byte 0

EuropeMagdalenVisitor_Enter::
 lockall
 msgbox EuropeMagdalenVisitor_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeMagdalenVisitor_End
 closemessage
 warp MAP_EUROPE_MAGDALEN_VISITOR, 5, 7
 waitstate
 releaseall
 end

EuropeMagdalenVisitor_Exit::
 lockall
 warp MAP_EUROPE_OXFORD, 51, 11
 waitstate
 releaseall
 end

EuropeMagdalenVisitor_End::
 releaseall
 end

EuropeMagdalenVisitor_EntryText::
 .string "MAGDALEN VISITOR ROOM\n"
 .string "Step inside and browse the displays?$"

EuropeMagdalenVisitor_Guide::
 lock
 faceplayer
 msgbox EuropeMagdalenVisitor_GuideText, MSGBOX_DEFAULT
 release
 end

EuropeMagdalenVisitor_GuideText::
 .string "Welcome to the MAGDALEN visitor room!\n"
 .string "Browse the tower and river displays.\p"
 .string "The CHERWELL paths are outside.\n"
 .string "Pause quietly to watch river POKEMON.\p"
 .string "Leave through the south doorway.\n"
 .string "You return to the MAGDALEN approach.$"

EuropeMagdalenVisitor_GardenExhibit::
 lock
 faceplayer
 msgbox EuropeMagdalenVisitor_GardenExhibitText, MSGBOX_DEFAULT
 release
 end

EuropeMagdalenVisitor_GardenExhibitText::
 .string "A drawing shows the tower silhouette.\n"
 .string "Compare its outline from the street.\p"
 .string "The display is for quiet visitors.\n"
 .string "Leave the tower drawing on the desk.$"

EuropeMagdalenVisitor_RiverExhibit::
 lock
 faceplayer
 msgbox EuropeMagdalenVisitor_RiverExhibitText, MSGBOX_DEFAULT
 release
 end

EuropeMagdalenVisitor_RiverExhibitText::
 .string "A path plan follows the CHERWELL.\n"
 .string "The meadow paths lie to the south.\p"
 .string "The station is east of the square.\n"
 .string "The free clinic is on its west side.$"
