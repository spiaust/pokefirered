ContinentAmsterdam_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentAmsterdam_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentAmsterdam_Transition
 .byte 0
ContinentAmsterdam_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentAmsterdam_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
