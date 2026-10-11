ContinentCopenhagen_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentCopenhagen_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentCopenhagen_Transition
 .byte 0
ContinentCopenhagen_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentCopenhagen_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
