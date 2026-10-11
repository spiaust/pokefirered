# USA companion transfer: pending coordination

The European main game and its local expansion do not depend on USA transfer. On 2026-10-10, the user confirmed that no folder or repository exists for the USA companion game yet. Transfer is deferred until that game has a defined engine and an implementation to integrate with.

Before implementing transfer, inspect the actual companion project and settle these points:

- Engine, platform, ROM/build identification and Pokemon/move/item identifiers.
- Save layout, versioning, checksums, encryption and available extension space.
- Transfer scope: player identity, party, inventory, cosmetics, money and independent quest progress.
- A supported departure/arrival/return flow, with backups, clear incompatibility handling and round-trip tests on copied saves.

Ordinary Pokemon trading alone cannot move a player between separate worlds. A confirmed protocol or combined-build approach must be implemented and verified in both projects. No cross-project changes or transfer compatibility are claimed by this European release.
