#include "imaging/demosaic.h"
#include "imaging/img.h"

static float sample_raw(const ImgF32 *raw, int y, int x) {
    if (y < 0) y = 0;
    if (x < 0) x = 0;
    if (y >= raw->height) y = raw->height - 1;
    if (x >= raw->width) x = raw->width - 1;
    return img_at_c(raw, y, x)[0];
}

ImgF32 *demosaic_bilinear_rggb(const ImgF32 *raw) {
    ImgF32 *rgb = img_create(raw->width, raw->height, 3);
    if (!rgb) {
        return NULL;
    }
    for (int y = 0; y < raw->height; ++y) {
        for (int x = 0; x < raw->width; ++x) {
            float *p = img_at(rgb, y, x);
            int even_y = (y % 2) == 0;
            int even_x = (x % 2) == 0;
            if (even_y && even_x) {
                p[0] = sample_raw(raw, y, x);
                p[1] = 0.25f * (sample_raw(raw, y, x - 1) + sample_raw(raw, y, x + 1)
                                + sample_raw(raw, y - 1, x) + sample_raw(raw, y + 1, x));
                p[2] = 0.25f * (sample_raw(raw, y - 1, x - 1) + sample_raw(raw, y - 1, x + 1)
                                + sample_raw(raw, y + 1, x - 1) + sample_raw(raw, y + 1, x + 1));
            } else if (even_y && !even_x) {
                p[0] = 0.5f * (sample_raw(raw, y, x - 1) + sample_raw(raw, y, x + 1));
                p[1] = sample_raw(raw, y, x);
                p[2] = 0.5f * (sample_raw(raw, y - 1, x) + sample_raw(raw, y + 1, x));
            } else if (!even_y && even_x) {
                p[0] = 0.5f * (sample_raw(raw, y - 1, x) + sample_raw(raw, y + 1, x));
                p[1] = sample_raw(raw, y, x);
                p[2] = 0.5f * (sample_raw(raw, y, x - 1) + sample_raw(raw, y, x + 1));
            } else {
                p[0] = 0.25f * (sample_raw(raw, y - 1, x - 1) + sample_raw(raw, y - 1, x + 1)
                                + sample_raw(raw, y + 1, x - 1) + sample_raw(raw, y + 1, x + 1));
                p[1] = 0.25f * (sample_raw(raw, y, x - 1) + sample_raw(raw, y, x + 1)
                                + sample_raw(raw, y - 1, x) + sample_raw(raw, y + 1, x));
                p[2] = sample_raw(raw, y, x);
            }
        }
    }
    return rgb;
}
