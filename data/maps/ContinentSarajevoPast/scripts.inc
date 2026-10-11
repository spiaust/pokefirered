ContinentSarajevoPast_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentSarajevoPast_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentSarajevoPast_Transition
 .byte 0
ContinentSarajevoPast_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentSarajevoPast_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
