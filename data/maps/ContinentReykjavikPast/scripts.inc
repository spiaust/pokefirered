ContinentReykjavikPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentReykjavikPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentReykjavikPast_Transition
 .byte 0
ContinentReykjavikPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentReykjavikPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
