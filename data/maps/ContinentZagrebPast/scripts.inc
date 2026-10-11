ContinentZagrebPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentZagrebPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentZagrebPast_Transition
 .byte 0
ContinentZagrebPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentZagrebPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
