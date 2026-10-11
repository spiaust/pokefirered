EuropeLondonReadingRoom_MapScripts::
 .byte 0

EuropeLondonReadingRoom_Enter::
 lockall
 msgbox EuropeLondonReadingRoom_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeLondonReadingRoom_End
 closemessage
 warp MAP_EUROPE_LONDON_READING_ROOM, 5, 7
 waitstate
 releaseall
 end

EuropeLondonReadingRoom_Exit::
 lockall
 warp MAP_EUROPE_LONDON, 55, 33
 waitstate
 releaseall
 end

EuropeLondonReadingRoom_Host::
 lock
 faceplayer
 msgbox EuropeLondonReadingRoom_HostText, MSGBOX_DEFAULT
 release
 end

EuropeLondonReadingRoom_Notebook::
 lock
 msgbox EuropeLondonReadingRoom_NotebookText, MSGBOX_DEFAULT
 release
 end

EuropeLondonReadingRoom_Books::
 lockall
 msgbox EuropeLondonReadingRoom_BooksText, MSGBOX_DEFAULT
 releaseall
 end

EuropeLondonReadingRoom_BooksText::
 .string "A cabinet of well-read books.\n"
 .string "Neighbors leave notes in the margins.\p"
 .string "A label says: Share a favorite walk,\n"
 .string "and help the next visitor explore.$"

EuropeLondonReadingRoom_End::
 releaseall
 end

EuropeLondonReadingRoom_EntryText::
 .string "READING ROOM / COUNCIL RECEPTION\n"
 .string "Visit the reading room?$"

EuropeLondonReadingRoom_HostText::
 .string "Welcome to our reading room.\n"
 .string "I collect notes about local walks.\p"
 .string "The bridges link both riverbanks.\n"
 .string "Take your time and enjoy the view.\p"
 .string "Leave south, then follow the lane\n"
 .string "west to the EYE and its gallery.$"

EuropeLondonReadingRoom_NotebookText::
 .string "A notebook of riverside walks.\n"
 .string "West: the EYE and its gallery.\p"
 .string "Cross the bridges for WESTMINSTER.\n"
 .string "The garden loop leads back here.$"
