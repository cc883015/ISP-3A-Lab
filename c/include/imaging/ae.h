#ifndef IMAGING_AE_H
#define IMAGING_AE_H

#include "imaging/types.h"

float img_mean_luma(const ImgF32 *rgb);
AeState ae_step(const ImgF32 *rgb, AeState state, float target);

#endif
