#include "imaging/ae.h"

#include <math.h>

float img_mean_luma(const ImgF32 *rgb) {
    double acc = 0.0;
    size_t n = (size_t)rgb->width * (size_t)rgb->height;
    for (size_t i = 0; i < n; ++i) {
        const float *p = rgb->data + i * (size_t)rgb->channels;
        acc += 0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2];
    }
    return (float)(acc / (double)n);
}

AeState ae_step(const ImgF32 *rgb, AeState state, float target) {
    float current = img_mean_luma(rgb);
    AeState next = state;
    if (current < 1e-6f) {
        next.exposure = 8.f;
        return next;
    }
    float ratio = powf(target / current, 0.7f);
    next.exposure = state.exposure * ratio;
    if (next.exposure < 0.05f) next.exposure = 0.05f;
    if (next.exposure > 8.f) next.exposure = 8.f;
    return next;
}
