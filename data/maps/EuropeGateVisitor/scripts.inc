EuropeGateVisitor_MapScripts::
 .byte 0

EuropeGateVisitor_Enter::
 lockall
 msgbox EuropeGateVisitor_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeGateVisitor_End
 closemessage
 warp MAP_EUROPE_GATE_VISITOR, 5, 7
 waitstate
 releaseall
 end

EuropeGateVisitor_Exit::
 lockall
 warp MAP_EUROPE_BERLIN, 19, 37
 waitstate
 releaseall
 end

EuropeGateVisitor_End::
 releaseall
 end

EuropeGateVisitor_EntryText::
 .string "GATE VISITOR ROOM\n"
 .string "Come inside and browse the displays?$"

EuropeGateVisitor_Guide::
 lock
 faceplayer
 msgbox EuropeGateVisitor_GuideText, MSGBOX_DEFAULT
 release
 end

EuropeGateVisitor_GuideText::
 .string "Welcome to our GATE visitor room!\n"
 .string "Our walks connect places and people.\p"
 .string "The garden lies west of the GATE.\n"
 .string "The courtyard rooms lie east.\p"
 .string "Leave through the south doorway.\n"
 .string "Follow paths north to the square.\p"
 .string "Station: east side of the square.\n"
 .string "Free clinic: west side of the square.$"

EuropeGateVisitor_GardenPanel::
 lock
 faceplayer
 msgbox EuropeGateVisitor_GardenPanelText, MSGBOX_DEFAULT
 release
 end

EuropeGateVisitor_GardenPanelText::
 .string "A sketch links the garden paths.\n"
 .string "Pause beside the flower beds.\p"
 .string "Watch which POKEMON visit them,\n"
 .string "then leave their shelter undisturbed.$"

EuropeGateVisitor_CourtPanel::
 lock
 faceplayer
 msgbox EuropeGateVisitor_CourtPanelText, MSGBOX_DEFAULT
 release
 end

EuropeGateVisitor_CourtPanelText::
 .string "A map follows the boulevard east.\n"
 .string "The courtyard shares books and tools.\p"
 .string "Walk the lanes and visit the rooms.\n"
 .string "Small acts of care connect neighbors.$"

