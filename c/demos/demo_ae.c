#include "imaging/ae.h"
#include "imaging/img.h"

#include <stdio.h>

int main(void) {
    ImgF32 *scene = img_make_chart(180, 120);
    size_t n = (size_t)scene->width * (size_t)scene->height * 3;
    for (size_t i = 0; i < n; ++i) {
        scene->data[i] *= 0.20f;
    }

    AeState state = {0.40f, 1.0f};
    printf("frame  exposure  luma\n");
    for (int i = 0; i < 8; ++i) {
        ImgF32 *frame = img_create(scene->width, scene->height, 3);
        for (size_t k = 0; k < n; ++k) {
            float v = scene->data[k] * state.exposure;
            frame->data[k] = v > 1.f ? 1.f : v;
        }
        float y = img_mean_luma(frame);
        printf("%5d  %8.3f  %.3f\n", i, state.exposure, y);
        state = ae_step(frame, state, 0.36f);
        img_free(frame);
    }
    return 0;
}
