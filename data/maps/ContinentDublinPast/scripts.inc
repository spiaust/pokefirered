ContinentDublinPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentDublinPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentDublinPast_Transition
 .byte 0
ContinentDublinPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentDublinPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
