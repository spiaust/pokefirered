ContinentLondonPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentLondonPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentLondonPast_Transition
 .byte 0
ContinentLondonPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentLondonPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
