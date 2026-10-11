ContinentBucharest_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, ContinentBucharest_Load
 map_script MAP_SCRIPT_ON_TRANSITION, ContinentBucharest_Transition
 .byte 0
ContinentBucharest_Load::
 special Shadow_PrepareVisible
 special Shadow_ApplyTimeline
 end
ContinentBucharest_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
