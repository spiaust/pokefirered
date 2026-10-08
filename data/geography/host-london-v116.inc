EuropeLondonHome_MapScripts::
 .byte 0

EuropeLondonHome_Enter::
 lockall
 msgbox EuropeLondonHome_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeLondonHome_End
 closemessage
 warp MAP_EUROPE_LONDON_HOME, 5, 7
 waitstate
 releaseall
 end

EuropeLondonHome_Exit::
 lockall
 warp MAP_EUROPE_LONDON, 45, 33
 waitstate
 releaseall
 end

EuropeLondonHome_Host::
 lock
 faceplayer
 msgbox EuropeLondonHome_HostText, MSGBOX_DEFAULT
 release
 end

EuropeLondonHome_Notebook::
 lock
 msgbox EuropeLondonHome_NotebookText, MSGBOX_DEFAULT
 release
 end

EuropeLondonHome_Album::
 lock
 msgbox EuropeLondonHome_AlbumText, MSGBOX_DEFAULT
 release
 end

EuropeLondonHome_AlbumText::
 .string "An album of neighborhood photos.\n"
 .string "The first shows a bare garden bed.\p"
 .string "Later photos show spring flowers\n"
 .string "and neighbors watering together.\p"
 .string "A note: Every season, a little care\n"
 .string "makes this lane feel like home.$"

EuropeLondonHome_End::
 releaseall
 end

EuropeLondonHome_EntryText::
 .string "A neighbor has opened their home.\n"
 .string "Visit the sitting room?$"

EuropeLondonHome_HostText::
 .string "Welcome! Rest your feet a moment.\n"
 .string "Our photo album is on the table.\p"
 .string "We take turns looking after the beds.\n"
 .string "Small acts of care add up.$"

EuropeLondonHome_NotebookText::
 .string "A notebook of garden observations.\n"
 .string "JIGGLYPUFF rests near the EYE.\p"
 .string "Keep the public paths clear,\n"
 .string "so visitors can circle the gardens.$"
