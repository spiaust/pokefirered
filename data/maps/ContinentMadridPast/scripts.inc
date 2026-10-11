ContinentMadridPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentMadridPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentMadridPast_Transition
 .byte 0
ContinentMadridPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentMadridPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
