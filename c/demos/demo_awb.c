#include "imaging/awb.h"
#include "imaging/img.h"

#include <stdio.h>

int main(void) {
    ImgF32 *img = img_make_chart(180, 120);
    size_t n = (size_t)img->width * (size_t)img->height;
    for (size_t i = 0; i < n; ++i) {
        float *p = img->data + i * 3;
        p[0] *= 1.25f;
        p[2] *= 0.70f;
        if (p[0] > 1.f) p[0] = 1.f;
    }
    AwbGains g = awb_gray_world(img);
    printf("gray_world R=%.3f G=%.3f B=%.3f\n", g.r_gain, g.g_gain, g.b_gain);
    awb_apply(img, g);
    printf("after apply mean luma path ready\n");
    img_free(img);
    return 0;
}
