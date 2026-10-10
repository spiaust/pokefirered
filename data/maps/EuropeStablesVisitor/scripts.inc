EuropeStablesVisitor_MapScripts::
 .byte 0

EuropeStablesVisitor_Enter::
 lockall
 msgbox EuropeStablesVisitor_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeStablesVisitor_End
 closemessage
 warp MAP_EUROPE_STABLES_VISITOR, 5, 7
 waitstate
 releaseall
 end

EuropeStablesVisitor_Exit::
 lockall
 warp MAP_EUROPE_CHANTILLY, 38, 19
 waitstate
 releaseall
 end

EuropeStablesVisitor_End::
 releaseall
 end

EuropeStablesVisitor_EntryText::
 .string "STABLES VISITOR ROOM\n"
 .string "Step inside and browse the displays?$"

EuropeStablesVisitor_Guide::
 lock
 faceplayer
 msgbox EuropeStablesVisitor_GuideText, MSGBOX_DEFAULT
 release
 end

EuropeStablesVisitor_GuideText::
 .string "Welcome to the STABLES visitor room!\n"
 .string "Browse care notes beside the benches.\p"
 .string "The estate paths are outside.\n"
 .string "Give resting POKEMON plenty of space.\p"
 .string "Leave through the south doorway.\n"
 .string "You return to the STABLES path.$"

EuropeStablesVisitor_GardenExhibit::
 lock
 faceplayer
 msgbox EuropeStablesVisitor_GardenExhibitText, MSGBOX_DEFAULT
 release
 end

EuropeStablesVisitor_GardenExhibitText::
 .string "A care board lists water and rest.\n"
 .string "Travelling POKEMON need breaks too.\p"
 .string "Ask before approaching an animal.\n"
 .string "Keep paths clear for the caretakers.$"

EuropeStablesVisitor_RiverExhibit::
 lock
 faceplayer
 msgbox EuropeStablesVisitor_RiverExhibitText, MSGBOX_DEFAULT
 release
 end

EuropeStablesVisitor_RiverExhibitText::
 .string "An estate plan marks the moat bridge.\n"
 .string "The CHATEAU lies north of here.\p"
 .string "The station is east of the square.\n"
 .string "The free clinic is on its west side.$"
