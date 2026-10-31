#include "imaging/af.h"
#include "imaging/img.h"

static float luma_px(const ImgF32 *rgb, int y, int x) {
    if (y < 0) y = 0;
    if (x < 0) x = 0;
    if (y >= rgb->height) y = rgb->height - 1;
    if (x >= rgb->width) x = rgb->width - 1;
    const float *p = img_at_c(rgb, y, x);
    return 0.2126f * p[0] + 0.7152f * p[1] + 0.0722f * p[2];
}

float af_tenengrad(const ImgF32 *rgb) {
    double acc = 0.0;
    int count = 0;
    for (int y = 1; y < rgb->height - 1; ++y) {
        for (int x = 1; x < rgb->width - 1; ++x) {
            float gx = -luma_px(rgb, y - 1, x - 1) + luma_px(rgb, y - 1, x + 1)
                       - 2.f * luma_px(rgb, y, x - 1) + 2.f * luma_px(rgb, y, x + 1)
                       - luma_px(rgb, y + 1, x - 1) + luma_px(rgb, y + 1, x + 1);
            float gy = -luma_px(rgb, y - 1, x - 1) - 2.f * luma_px(rgb, y - 1, x)
                       - luma_px(rgb, y - 1, x + 1) + luma_px(rgb, y + 1, x - 1)
                       + 2.f * luma_px(rgb, y + 1, x) + luma_px(rgb, y + 1, x + 1);
            acc += (double)(gx * gx + gy * gy);
            ++count;
        }
    }
    return (float)(acc / (double)count);
}
