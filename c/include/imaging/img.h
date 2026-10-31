#ifndef IMAGING_IMG_H
#define IMAGING_IMG_H

#include "imaging/types.h"

ImgF32 *img_create(int width, int height, int channels);
void img_free(ImgF32 *img);
float *img_at(ImgF32 *img, int y, int x);
const float *img_at_c(const ImgF32 *img, int y, int x);
int img_write_ppm(const ImgF32 *img, const char *path);
ImgF32 *img_make_chart(int width, int height);

#endif
