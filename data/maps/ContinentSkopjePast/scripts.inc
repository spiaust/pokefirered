ContinentSkopjePast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentSkopjePast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentSkopjePast_Transition
 .byte 0
ContinentSkopjePast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentSkopjePast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
