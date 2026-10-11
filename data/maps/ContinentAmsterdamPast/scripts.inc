ContinentAmsterdamPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentAmsterdamPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentAmsterdamPast_Transition
 .byte 0
ContinentAmsterdamPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentAmsterdamPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
