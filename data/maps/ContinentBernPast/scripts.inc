ContinentBernPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentBernPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentBernPast_Transition
 .byte 0
ContinentBernPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentBernPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
