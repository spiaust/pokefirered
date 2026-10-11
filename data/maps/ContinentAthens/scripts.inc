ContinentAthens_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentAthens_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentAthens_Transition
 .byte 0
ContinentAthens_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentAthens_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
