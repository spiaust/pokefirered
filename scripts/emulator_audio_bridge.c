// Optional soundtrack recorder; regular gameplay tests keep their existing bridge.
#include "emulator_bridge.c"
#include <mgba/core/blip_buf.h>

int emulator_record_pcm(const char *path, unsigned frames)
{
    FILE *file = fopen(path, "wb");
    if (!file) return 0;
    core->setAudioBufferSize(core, 2048);
    struct blip_t *left = core->getAudioChannel(core, 0);
    struct blip_t *right = core->getAudioChannel(core, 1);
    blip_set_rates(left, core->frequency(core), 32768);
    blip_set_rates(right, core->frequency(core), 32768);
    blip_clear(left); blip_clear(right);
    core->setKeys(core, 0);
    unsigned total = 0;
    while (frames--)
    {
        short stereo[4096];
        core->runFrame(core);
        int count = blip_samples_avail(left);
        if (count > 2048) count = 2048;
        int a = blip_read_samples(left, stereo, count, 1);
        int b = blip_read_samples(right, stereo + 1, count, 1);
        if (a != b || fwrite(stereo, sizeof(short) * 2, a, file) != (size_t)a)
        { fclose(file); return 0; }
        total += a;
    }
    fclose(file);
    return total;
}
