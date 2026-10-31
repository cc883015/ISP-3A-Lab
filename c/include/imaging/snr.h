#ifndef IMAGING_SNR_H
#define IMAGING_SNR_H

#include "imaging/types.h"

float patch_snr_db(const ImgF32 *rgb, int y0, int x0, int size);

#endif
