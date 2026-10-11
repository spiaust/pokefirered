ContinentStockholm_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentStockholm_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentStockholm_Transition
 .byte 0
ContinentStockholm_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentStockholm_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
