#include "imaging/awb.h"

AwbGains awb_gray_world(const ImgF32 *rgb) {
    double r = 0.0, g = 0.0, b = 0.0;
    size_t n = (size_t)rgb->width * (size_t)rgb->height;
    for (size_t i = 0; i < n; ++i) {
        const float *p = rgb->data + i * 3;
        r += p[0];
        g += p[1];
        b += p[2];
    }
    r /= (double)n;
    g /= (double)n;
    b /= (double)n;
    AwbGains gains;
    gains.r_gain = (float)(g / (r > 1e-6 ? r : 1e-6));
    gains.g_gain = 1.f;
    gains.b_gain = (float)(g / (b > 1e-6 ? b : 1e-6));
    return gains;
}

void awb_apply(ImgF32 *rgb, AwbGains gains) {
    size_t n = (size_t)rgb->width * (size_t)rgb->height;
    for (size_t i = 0; i < n; ++i) {
        float *p = rgb->data + i * 3;
        p[0] *= gains.r_gain;
        p[1] *= gains.g_gain;
        p[2] *= gains.b_gain;
        if (p[0] > 1.f) p[0] = 1.f;
        if (p[1] > 1.f) p[1] = 1.f;
        if (p[2] > 1.f) p[2] = 1.f;
    }
}
