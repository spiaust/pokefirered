ContinentRigaPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentRigaPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentRigaPast_Transition
 .byte 0
ContinentRigaPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentRigaPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
