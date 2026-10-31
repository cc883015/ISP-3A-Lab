#include "imaging/bayer.h"
#include "imaging/demosaic.h"
#include "imaging/img.h"

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>

int main(void) {
    mkdir("output", 0755);
    mkdir("output/c", 0755);

    ImgF32 *src = img_make_chart(240, 160);
    ImgF32 *raw = rgb_to_bayer_rggb(src);
    ImgF32 *rgb = demosaic_bilinear_rggb(raw);

    double acc = 0.0;
    size_t n = (size_t)src->width * (size_t)src->height * 3;
    for (size_t i = 0; i < n; ++i) {
        acc += fabs((double)rgb->data[i] - (double)src->data[i]);
    }
    printf("C demosaic MAE vs source RGB = %.4f\n", acc / (double)n);

    img_write_ppm(src, "output/c/demo_pipeline_src.ppm");
    img_write_ppm(raw, "output/c/demo_pipeline_raw.ppm");
    img_write_ppm(rgb, "output/c/demo_pipeline_rgb.ppm");
    printf("wrote output/c/demo_pipeline_*.ppm\n");

    img_free(src);
    img_free(raw);
    img_free(rgb);
    return 0;
}
