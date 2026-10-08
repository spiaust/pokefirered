EuropeEiffelVisitor_MapScripts::
 .byte 0

EuropeEiffelVisitor_Enter::
 lockall
 msgbox EuropeEiffelVisitor_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeEiffelVisitor_End
 closemessage
 warp MAP_EUROPE_EIFFEL_VISITOR, 5, 7
 waitstate
 releaseall
 end

EuropeEiffelVisitor_Exit::
 lockall
 warp MAP_EUROPE_PARIS, 9, 37
 waitstate
 releaseall
 end

EuropeEiffelVisitor_End::
 releaseall
 end

EuropeEiffelVisitor_EntryText::
 .string "EIFFEL VISITOR ROOM\n"
 .string "Step inside and browse the exhibits?$"

EuropeEiffelVisitor_Guide::
 lock
 faceplayer
 msgbox EuropeEiffelVisitor_GuideText, MSGBOX_DEFAULT
 release
 end

EuropeEiffelVisitor_GuideText::
 .string "Welcome to our visitor room!\n"
 .string "The garden and river are nearby.\p"
 .string "Our exhibits show how field notes\n"
 .string "begin with careful observation.\p"
 .string "Leave through the south doorway.\n"
 .string "Follow paths north to the square.\p"
 .string "Station: east side of the square.\n"
 .string "Free clinic: west side of the square.$"

EuropeEiffelVisitor_GardenExhibit::
 lock
 faceplayer
 msgbox EuropeEiffelVisitor_GardenExhibitText, MSGBOX_DEFAULT
 release
 end

EuropeEiffelVisitor_GardenExhibitText::
 .string "A sketch of the CHAMP DE MARS.\n"
 .string "Watch a patch of flowers quietly.\p"
 .string "Which POKEMON visit? When do they\n"
 .string "rest? Leave their shelter undisturbed.$"

EuropeEiffelVisitor_RiverExhibit::
 lock
 faceplayer
 msgbox EuropeEiffelVisitor_RiverExhibitText, MSGBOX_DEFAULT
 release
 end

EuropeEiffelVisitor_RiverExhibitText::
 .string "A sketch follows the SEINE east.\n"
 .string "Record what you see along the banks.\p"
 .string "Cross by the bridges and keep the\n"
 .string "water and riverside paths clean.$"
