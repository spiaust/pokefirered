ContinentMinskPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentMinskPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentMinskPast_Transition
 .byte 0
ContinentMinskPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentMinskPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
