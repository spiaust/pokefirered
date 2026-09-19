#!/usr/bin/env bash
# Build on Linux's native filesystem; keep source and outputs in the workspace.
set -euo pipefail
cd "$(dirname "$0")/.."
project_root="$PWD"
mkdir -p .local-tools
cache_record=.local-tools/linux-build-path.txt
build_cache=""
new_cache=0
cache_parent="$HOME/.cache"
mkdir -p "$cache_parent"
if [[ -f "$cache_record" ]]; then
    build_cache=$(cat "$cache_record")
fi
if [[ "$build_cache" != "$cache_parent"/pokemon-europe-build.* || ! -d "$build_cache" || ! -O "$build_cache" ]]; then
    build_cache=$(mktemp -d "$cache_parent/pokemon-europe-build.XXXXXX")
    new_cache=1
    printf '%s\n' "$build_cache" > "$cache_record"
fi
if [[ "${2:-}" != --windows-manifests ]]; then
    git ls-files -z --cached --others --exclude-standard > .local-tools/build-inputs.txt
    { git diff --name-only -z HEAD; git ls-files -z --others --exclude-standard; } > .local-tools/dirty-inputs.txt
fi
python3 - "$project_root" "$build_cache" "$new_cache" <<'PY'
from pathlib import Path
import sys
root, cache = map(Path, sys.argv[1:3])
new = set((root / '.local-tools/build-inputs.txt').read_bytes().split(b'\0')) - {b''}
manifest = cache / '.source-manifest'
old = set(manifest.read_bytes().split(b'\0')) - {b''} if manifest.exists() else set()
for name in old - new:
    target = cache / name.decode()
    if not target.resolve().is_relative_to(cache.resolve()):
        raise RuntimeError('Invalid cached source path')
    if target.is_file():
        target.unlink()
manifest.write_bytes(b'\0'.join(sorted(new)) + b'\0')
dirty = set((root / '.local-tools/dirty-inputs.txt').read_bytes().split(b'\0')) - {b''}
dirty_manifest = cache / '.dirty-manifest'
previous = set(dirty_manifest.read_bytes().split(b'\0')) - {b''} if dirty_manifest.exists() else set()
to_copy = new if sys.argv[3] == '1' else (dirty | previous) & new
(root / '.local-tools/sync-inputs.txt').write_bytes(b'\0'.join(sorted(to_copy)) + b'\0')
dirty_manifest.write_bytes(b'\0'.join(sorted(dirty)) + b'\0')
PY
if [[ "$new_cache" == 1 && "${2:-}" == --windows-manifests ]]; then
    tar -xf .local-tools/source-inputs.tar -C "$build_cache"
else
    rsync -a --from0 --files-from=.local-tools/sync-inputs.txt ./ "$build_cache/"
fi
if [[ ! -f "$build_cache/tools/agbcc/bin/agbcc" ]]; then
    rsync -a tools/agbcc/ "$build_cache/tools/agbcc/"
fi
cd "$build_cache"
make -j8 "${1:-all}"
arm-none-eabi-nm -n pokefirered.elf > pokefirered.sym
cp pokefirered.gba pokefirered.elf pokefirered.map pokefirered.sym "$project_root/"
