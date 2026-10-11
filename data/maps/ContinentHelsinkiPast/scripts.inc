ContinentHelsinkiPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentHelsinkiPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentHelsinkiPast_Transition
 .byte 0
ContinentHelsinkiPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentHelsinkiPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
