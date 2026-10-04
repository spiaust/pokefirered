EuropeBerlinLibrary_MapScripts::
 .byte 0

EuropeBerlinLibrary_Enter::
 lockall
 msgbox EuropeBerlinLibrary_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeBerlinLibrary_End
 closemessage
 warp MAP_EUROPE_BERLIN_LIBRARY, 5, 7
 waitstate
 releaseall
 end

EuropeBerlinLibrary_Exit::
 lockall
 warp MAP_EUROPE_BERLIN, 51, 32
 waitstate
 releaseall
 end

EuropeBerlinLibrary_End::
 releaseall
 end

EuropeBerlinLibrary_EntryText::
 .string "NEIGHBORHOOD READING ROOM\n"
 .string "Come in and browse the records?$"

EuropeBerlinLibrary_Librarian::
 lock
 faceplayer
 msgbox EuropeBerlinLibrary_LibrarianText, MSGBOX_DEFAULT
 release
 end

EuropeBerlinLibrary_LibrarianText::
 .string "Welcome! These are local records.\n"
 .string "People write down what they notice.\p"
 .string "A garden, a journey, a helping hand:\n"
 .string "small stories deserve a place too.$"

EuropeBerlinLibrary_GardenBook::
 lock
 faceplayer
 msgbox EuropeBerlinLibrary_GardenBookText, MSGBOX_DEFAULT
 release
 end

EuropeBerlinLibrary_GardenBookText::
 .string "A shared garden log.\n"
 .string "ODDISH rests in the shaded beds.\p"
 .string "Each neighbor tends a small patch.\n"
 .string "Together, they keep the court green.$"

EuropeBerlinLibrary_HistoryBook::
 lock
 faceplayer
 msgbox EuropeBerlinLibrary_HistoryBookText, MSGBOX_DEFAULT
 release
 end

EuropeBerlinLibrary_HistoryBookText::
 .string "A notebook of neighborhood memories.\n"
 .string "Visitors once brought field notes\p"
 .string "from journeys across EUROPE.\n"
 .string "Care connected one place to another.$"
