#include "imaging/bayer.h"
#include "imaging/img.h"

ImgF32 *rgb_to_bayer_rggb(const ImgF32 *rgb) {
    ImgF32 *raw = img_create(rgb->width, rgb->height, 1);
    if (!raw) {
        return NULL;
    }
    for (int y = 0; y < rgb->height; ++y) {
        for (int x = 0; x < rgb->width; ++x) {
            const float *p = img_at_c(rgb, y, x);
            float v;
            if ((y % 2) == 0 && (x % 2) == 0) {
                v = p[0];
            } else if ((y % 2) == 1 && (x % 2) == 1) {
                v = p[2];
            } else {
                v = p[1];
            }
            img_at(raw, y, x)[0] = v;
        }
    }
    return raw;
}
