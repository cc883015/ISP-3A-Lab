#ifndef IMAGING_TYPES_H
#define IMAGING_TYPES_H

#include <stddef.h>

typedef struct {
    int width;
    int height;
    int channels; /* 1 = gray/raw, 3 = RGB */
    float *data;  /* row-major, interleaved RGB */
} ImgF32;

typedef struct {
    float exposure;
    float gain;
} AeState;

typedef struct {
    float r_gain;
    float g_gain;
    float b_gain;
} AwbGains;

#endif
