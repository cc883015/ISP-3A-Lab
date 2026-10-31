#include "imaging/snr.h"

#include <math.h>

float patch_snr_db(const ImgF32 *rgb, int y0, int x0, int size) {
    double sum = 0.0, sum2 = 0.0;
    int n = 0;
    for (int y = y0; y < y0 + size && y < rgb->height; ++y) {
        for (int x = x0; x < x0 + size && x < rgb->width; ++x) {
            const float *p = rgb->data + ((size_t)y * (size_t)rgb->width + (size_t)x) * (size_t)rgb->channels;
            double yv = 0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2];
            sum += yv;
            sum2 += yv * yv;
            ++n;
        }
    }
    if (n == 0) {
        return 0.f;
    }
    double mean = sum / n;
    double var = sum2 / n - mean * mean;
    if (var < 1e-12) {
        return 99.f;
    }
    return (float)(20.0 * log10(mean / sqrt(var)));
}
