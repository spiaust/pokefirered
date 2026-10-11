#ifndef GUARD_SHADOW_CAMPAIGN_H
#define GUARD_SHADOW_CAMPAIGN_H
bool8 Shadow_IsPast(void);
void Shadow_BeginEncounter(void);
void Shadow_PrepareVisible(void);
void Shadow_StartVisible(void);
void Shadow_Resume(void);
void Shadow_Rescue(void);
void Shadow_TryPurify(void);
bool8 Shadow_IsEnemyTrainer(u16 trainer);
void Shadow_CountryStatus(void);
void Shadow_CountryClear(void);
void Shadow_CountryMemory(void);
void Shadow_CountryDecide(void);
void Shadow_CountryTravel(void);
void Shadow_ApplyTimeline(void);
const u8 *Shadow_GetCountryMapName(u16 section);
void Shadow_ApplyChallenge(void);
void Shadow_VisibleFieldStep(void);
void Shadow_NetworkStatus(void);
struct Pokemon;
void Shadow_RivalPartner(struct Pokemon *party, u8 count, bool8 opening);
void Shadow_ShowCredits(void);
void Eclipse_KrakowPrepare(void);
void Eclipse_PolandMemory(void);
#endif
