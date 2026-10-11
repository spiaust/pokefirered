ContinentSofiaPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentSofiaPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentSofiaPast_Transition
 .byte 0
ContinentSofiaPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentSofiaPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
