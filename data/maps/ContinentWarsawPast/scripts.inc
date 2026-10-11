ContinentWarsawPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentWarsawPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentWarsawPast_Transition
 .byte 0
ContinentWarsawPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentWarsawPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
