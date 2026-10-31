#ifndef IMAGING_DEMOSAIC_H
#define IMAGING_DEMOSAIC_H

#include "imaging/types.h"

ImgF32 *demosaic_bilinear_rggb(const ImgF32 *raw);

#endif
