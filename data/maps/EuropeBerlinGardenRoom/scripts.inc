EuropeBerlinGardenRoom_MapScripts::
 .byte 0

EuropeBerlinGardenRoom_Enter::
 lockall
 msgbox EuropeBerlinGardenRoom_EntryText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, EuropeBerlinGardenRoom_End
 closemessage
 warp MAP_EUROPE_BERLIN_GARDEN_ROOM, 5, 7
 waitstate
 releaseall
 end

EuropeBerlinGardenRoom_Exit::
 lockall
 warp MAP_EUROPE_BERLIN, 58, 32
 waitstate
 releaseall
 end

EuropeBerlinGardenRoom_End::
 releaseall
 end

EuropeBerlinGardenRoom_EntryText::
 .string "COURTYARD GARDEN WORKROOM\n"
 .string "Come in and see how we tend it?$"

EuropeBerlinGardenRoom_Gardener::
 lock
 faceplayer
 msgbox EuropeBerlinGardenRoom_GardenerText, MSGBOX_DEFAULT
 release
 end

EuropeBerlinGardenRoom_GardenerText::
 .string "Welcome to our garden workroom!\n"
 .string "We share tools and planting plans.\p"
 .string "Watch the beds, then make notes.\n"
 .string "Good care starts with noticing.$"

EuropeBerlinGardenRoom_Tools::
 lock
 faceplayer
 msgbox EuropeBerlinGardenRoom_ToolsText, MSGBOX_DEFAULT
 release
 end

EuropeBerlinGardenRoom_ToolsText::
 .string "Clean tools are ready on the bench.\n"
 .string "Use a light touch around the roots.\p"
 .string "Return each tool when you finish,\n"
 .string "so the next neighbor can use it.$"

EuropeBerlinGardenRoom_PlantingPlan::
 lock
 faceplayer
 msgbox EuropeBerlinGardenRoom_PlantingPlanText, MSGBOX_DEFAULT
 release
 end

EuropeBerlinGardenRoom_PlantingPlanText::
 .string "A sketch of the courtyard beds.\n"
 .string "Keep the shaded patches for ODDISH.\p"
 .string "Leave the lanes open for visitors.\n"
 .string "The reading room keeps our records.$"
