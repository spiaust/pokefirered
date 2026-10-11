ContinentHelsinki_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentHelsinki_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentHelsinki_Transition
 .byte 0
ContinentHelsinki_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentHelsinki_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
