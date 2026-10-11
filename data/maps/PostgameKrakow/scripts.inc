PostgameKrakow_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, PostgameKrakow_Load
 map_script MAP_SCRIPT_ON_TRANSITION, PostgameKrakow_Transition
 .byte 0
PostgameKrakow_Load::
 special Eclipse_KrakowPrepare
 end
PostgameKrakow_Transition::
 setrespawn HEAL_LOCATION_EUROPE_LONDON
 end
