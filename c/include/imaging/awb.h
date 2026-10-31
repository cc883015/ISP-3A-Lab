#ifndef IMAGING_AWB_H
#define IMAGING_AWB_H

#include "imaging/types.h"

AwbGains awb_gray_world(const ImgF32 *rgb);
void awb_apply(ImgF32 *rgb, AwbGains gains);

#endif
