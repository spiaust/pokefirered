#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export LD_LIBRARY_PATH="$PWD/.local-tools/cmake/root/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
CMAKE="$PWD/.local-tools/cmake/root/usr/bin/cmake"
"$CMAKE" -S .local-tools/mgba-src -B .local-tools/mgba-build \
    -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DLIBMGBA_ONLY=ON \
    -DM_CORE_GB=OFF -DCMAKE_POSITION_INDEPENDENT_CODE=ON
"$CMAKE" --build .local-tools/mgba-build -j 8
gcc -shared -fPIC -O2 -I.local-tools/mgba-src/include \
    -I.local-tools/mgba-build/include scripts/emulator_bridge.c \
    .local-tools/mgba-build/libmgba.a -lpng -lz -lm -lpthread \
    -o .local-tools/emulator_bridge.so
