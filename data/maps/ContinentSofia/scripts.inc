ContinentSofia_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentSofia_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentSofia_Transition
 .byte 0
ContinentSofia_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentSofia_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
