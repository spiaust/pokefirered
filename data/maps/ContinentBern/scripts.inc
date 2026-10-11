ContinentBern_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentBern_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentBern_Transition
 .byte 0
ContinentBern_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentBern_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
