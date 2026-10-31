#include "imaging/af.h"
#include "imaging/img.h"

#include <stdio.h>
#include <stdlib.h>

static void box_blur(ImgF32 *img, int radius) {
    ImgF32 *tmp = img_create(img->width, img->height, 3);
    size_t n = (size_t)img->width * (size_t)img->height * 3;
    for (size_t i = 0; i < n; ++i) {
        tmp->data[i] = img->data[i];
    }
    for (int y = 0; y < img->height; ++y) {
        for (int x = 0; x < img->width; ++x) {
            float acc[3] = {0, 0, 0};
            int count = 0;
            for (int dy = -radius; dy <= radius; ++dy) {
                int yy = y + dy;
                if (yy < 0 || yy >= img->height) continue;
                for (int dx = -radius; dx <= radius; ++dx) {
                    int xx = x + dx;
                    if (xx < 0 || xx >= img->width) continue;
                    const float *p = img_at_c(tmp, yy, xx);
                    acc[0] += p[0];
                    acc[1] += p[1];
                    acc[2] += p[2];
                    ++count;
                }
            }
            float *o = img_at(img, y, x);
            o[0] = acc[0] / (float)count;
            o[1] = acc[1] / (float)count;
            o[2] = acc[2] / (float)count;
        }
    }
    img_free(tmp);
}

int main(void) {
    printf("radius  tenengrad\n");
    for (int radius = 4; radius >= 0; --radius) {
        ImgF32 *img = img_make_chart(160, 120);
        if (radius > 0) {
            box_blur(img, radius);
        }
        printf("%6d  %.4f\n", radius, af_tenengrad(img));
        img_free(img);
    }
    return 0;
}
