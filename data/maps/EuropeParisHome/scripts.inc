EuropeParisHome_MapScripts::
 .byte 0

EuropeParisHome_Enter::
 lockall
 msgbox EuropeParisHome_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeParisHome_End
 closemessage
 warp MAP_EUROPE_PARIS_HOME, 5, 7
 waitstate
 releaseall
 end

EuropeParisHome_Exit::
 lockall
 warp MAP_EUROPE_PARIS, 45, 39
 waitstate
 releaseall
 end

EuropeParisHome_Host::
 lock
 faceplayer
 msgbox EuropeParisHome_HostText, MSGBOX_DEFAULT
 release
 end

EuropeParisHome_Notebook::
 lock
 msgbox EuropeParisHome_NotebookText, MSGBOX_DEFAULT
 release
 end

EuropeParisHome_Display::
 lockall
 msgbox EuropeParisHome_DisplayText, MSGBOX_DEFAULT
 releaseall
 end

EuropeParisHome_DisplayText::
 .string "Three sketches show the same river.\n"
 .string "Morning, midday and evening light.\p"
 .string "Look closely at familiar places.\n"
 .string "There is always something new to see.$"

EuropeParisHome_End::
 releaseall
 end

EuropeParisHome_EntryText::
 .string "A neighbor welcomes visitors.\n"
 .string "Visit the sketch room?$"

EuropeParisHome_HostText::
 .string "Welcome! I collect local sketches.\n"
 .string "The river gives us new views daily.\p"
 .string "The display holds three river views.\n"
 .string "Take a look before your next walk.\p"
 .string "The blue-roofed home to the east\n"
 .string "has a garden workroom to visit.$"

EuropeParisHome_NotebookText::
 .string "A sketchbook of the river and gardens.\n"
 .string "One page shows PSYDUCK resting.\p"
 .string "Another shows neighbors at work,\n"
 .string "caring for the flower beds together.$"
