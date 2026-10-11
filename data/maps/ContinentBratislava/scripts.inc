ContinentBratislava_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentBratislava_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentBratislava_Transition
 .byte 0
ContinentBratislava_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentBratislava_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
