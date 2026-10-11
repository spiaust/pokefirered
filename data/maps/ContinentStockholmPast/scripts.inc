ContinentStockholmPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentStockholmPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentStockholmPast_Transition
 .byte 0
ContinentStockholmPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentStockholmPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
