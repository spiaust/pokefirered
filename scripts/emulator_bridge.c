// Small mGBA bridge used by the gameplay integration tests.
#include <mgba/core/core.h>
#include <mgba/core/log.h>
#include <mgba-util/vfs.h>
#include <png.h>
#include <fcntl.h>
#include <stdlib.h>

static struct mCore *core;
static color_t pixels[240 * 160];
static void test_log(struct mLogger *logger, int category, enum mLogLevel level,
                     const char *format, va_list args)
{
    (void)logger;
    (void)category;
    if (level == mLOG_FATAL || level == mLOG_ERROR) {
        vfprintf(stderr, format, args);
        fputc('\n', stderr);
        if (core) {
            const char *registers[] = {"r0", "r1", "r2", "r3", "r4", "sp", "lr", "pc"};
            for (unsigned i = 0; i < sizeof(registers) / sizeof(*registers); i++) {
                uint32_t value = 0;
                core->readRegister(core, registers[i], &value);
                fprintf(stderr, "%s=%08X ", registers[i], value);
            }
            fputc('\n', stderr);
        }
        // A bad CPU jump can prevent runFrame from returning. Fail immediately
        // so a broken ROM cannot flood logs or hang the integration test.
        exit(2);
    }
}
static struct mLogger logger = { .log = test_log };

int emulator_open(const char *path)
{
    mLogSetDefaultLogger(&logger);
    core = mCoreCreate(mPLATFORM_GBA);
    if (!core || !core->init(core)) return 0;
    mCoreInitConfig(core, NULL);
    core->setVideoBuffer(core, pixels, 240);
    if (!mCoreLoadFile(core, path)) return 0;
    core->reset(core);
    return 1;
}

void emulator_frames(unsigned keys, unsigned count)
{
    core->setKeys(core, keys);
    while (count--) core->runFrame(core);
}

unsigned emulator_read(unsigned address, unsigned size)
{
    if (size == 1) return core->busRead8(core, address);
    if (size == 2) return core->busRead16(core, address);
    return core->busRead32(core, address);
}

void emulator_write(unsigned address, unsigned value, unsigned size)
{
    if (size == 1) core->busWrite8(core, address, value);
    else if (size == 2) core->busWrite16(core, address, value);
    else core->busWrite32(core, address, value);
}

int emulator_state(const char *path, int load)
{
    size_t size = core->stateSize(core);
    void *state = malloc(size);
    FILE *file = fopen(path, load ? "rb" : "wb");
    int ok = 0;
    if (file) {
        if (load) ok = fread(state, 1, size, file) == size && core->loadState(core, state);
        else ok = core->saveState(core, state) && fwrite(state, 1, size, file) == size;
        fclose(file);
    }
    free(state);
    return ok;
}

int emulator_screenshot(const char *path)
{
    unsigned char rgb[240 * 160 * 3];
    for (unsigned i = 0; i < 240 * 160; i++) {
        rgb[i * 3] = pixels[i] & 255;
        rgb[i * 3 + 1] = (pixels[i] >> 8) & 255;
        rgb[i * 3 + 2] = (pixels[i] >> 16) & 255;
    }
    png_image image = {0};
    image.version = PNG_IMAGE_VERSION;
    image.width = 240;
    image.height = 160;
    image.format = PNG_FORMAT_RGB;
    return png_image_write_to_file(&image, path, 0, rgb, 0, NULL);
}

void emulator_close(void)
{
    mCoreConfigDeinit(&core->config);
    core->deinit(core);
    core = NULL;
}

int emulator_battery(const char *path, int load)
{
    FILE *file = fopen(path, load ? "rb" : "wb");
    if (!file) return 0;
    void *data = NULL;
    size_t size;
    int ok;
    if (load) {
        fseek(file, 0, SEEK_END);
        size = ftell(file);
        rewind(file);
        data = malloc(size);
        ok = fread(data, 1, size, file) == size
            && core->savedataRestore(core, data, size, false);
        if (ok) core->reset(core);
    } else {
        size = core->savedataClone(core, &data);
        ok = size > 0 && fwrite(data, 1, size, file) == size;
    }
    free(data);
    fclose(file);
    return ok;
}
