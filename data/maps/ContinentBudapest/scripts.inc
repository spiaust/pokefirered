ContinentBudapest_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentBudapest_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentBudapest_Transition
 .byte 0
ContinentBudapest_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentBudapest_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
