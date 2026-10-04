EuropeBerlinHome_MapScripts::
 .byte 0

EuropeBerlinHome_Enter::
 lockall
 msgbox EuropeBerlinHome_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeBerlinHome_End
 closemessage
 warp MAP_EUROPE_BERLIN_HOME, 5, 7
 waitstate
 releaseall
 end

EuropeBerlinHome_Exit::
 lockall
 warp MAP_EUROPE_BERLIN, 43, 32
 waitstate
 releaseall
 end

EuropeBerlinHome_Host::
 lock
 faceplayer
 msgbox EuropeBerlinHome_HostText, MSGBOX_DEFAULT
 release
 end

EuropeBerlinHome_Notebook::
 lock
 msgbox EuropeBerlinHome_NotebookText, MSGBOX_DEFAULT
 release
 end

EuropeBerlinHome_End::
 releaseall
 end

EuropeBerlinHome_EntryText::
 .string "A neighbor has opened their home.\n"
 .string "Visit the sitting room?$"

EuropeBerlinHome_HostText::
 .string "Welcome! Rest your feet a moment.\n"
 .string "Our garden is a shared little joy.\p"
 .string "Neighbors take turns tending it.\n"
 .string "Small acts of care add up.$"

EuropeBerlinHome_NotebookText::
 .string "A notebook of garden observations.\n"
 .string "ODDISH prefers the shaded beds.\p"
 .string "Leave the southern lane clear,\n"
 .string "so everyone can reach the flowers.$"
