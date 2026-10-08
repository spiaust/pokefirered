EuropeLondonEyeGallery_MapScripts::
 .byte 0

EuropeLondonEyeGallery_Enter::
 lockall
 msgbox EuropeLondonEyeGallery_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeLondonEyeGallery_End
 closemessage
 warp MAP_EUROPE_LONDON_EYE_GALLERY, 5, 7
 waitstate
 releaseall
 end

EuropeLondonEyeGallery_Exit::
 lockall
 warp MAP_EUROPE_LONDON, 29, 29
 waitstate
 releaseall
 end

EuropeLondonEyeGallery_End::
 releaseall
 end

EuropeLondonEyeGallery_EntryText::
 .string "LONDON EYE VISITOR GALLERY\n"
 .string "Come inside and browse the displays?$"

EuropeLondonEyeGallery_Attendant::
 lock
 faceplayer
 msgbox EuropeLondonEyeGallery_AttendantText, MSGBOX_DEFAULT
 release
 end

EuropeLondonEyeGallery_AttendantText::
 .string "Welcome to our riverside gallery!\n"
 .string "The SOUTH BANK paths link gardens\p"
 .string "and bridges. Look at the displays,\n"
 .string "then explore the walks outside.\p"
 .string "Leave through the south doorway.\n"
 .string "Follow paths north to the square.\p"
 .string "Station: east side of the square.\n"
 .string "Free clinic: west side of the square.$"

EuropeLondonEyeGallery_GardenPanel::
 lock
 faceplayer
 msgbox EuropeLondonEyeGallery_GardenPanelText, MSGBOX_DEFAULT
 release
 end

EuropeLondonEyeGallery_GardenPanelText::
 .string "A sketch of the SOUTH BANK gardens.\n"
 .string "Quiet paths circle the flower beds.\p"
 .string "Watch the POKEMON without disturbing\n"
 .string "their resting places or the plants.$"

EuropeLondonEyeGallery_BridgePanel::
 lock
 faceplayer
 msgbox EuropeLondonEyeGallery_BridgePanelText, MSGBOX_DEFAULT
 release
 end

EuropeLondonEyeGallery_BridgePanelText::
 .string "A map marks the two river crossings.\n"
 .string "Green rails: WESTMINSTER BRIDGE.\p"
 .string "Red rails: the southern crossing.\n"
 .string "Both connect the riverside walks.$"
