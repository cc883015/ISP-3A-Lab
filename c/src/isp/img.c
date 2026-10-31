#include "imaging/img.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

ImgF32 *img_create(int width, int height, int channels) {
    ImgF32 *img = (ImgF32 *)calloc(1, sizeof(ImgF32));
    if (!img) {
        return NULL;
    }
    img->width = width;
    img->height = height;
    img->channels = channels;
    img->data = (float *)calloc((size_t)width * (size_t)height * (size_t)channels, sizeof(float));
    if (!img->data) {
        free(img);
        return NULL;
    }
    return img;
}

void img_free(ImgF32 *img) {
    if (!img) {
        return;
    }
    free(img->data);
    free(img);
}

float *img_at(ImgF32 *img, int y, int x) {
    return img->data + ((size_t)y * (size_t)img->width + (size_t)x) * (size_t)img->channels;
}

const float *img_at_c(const ImgF32 *img, int y, int x) {
    return img->data + ((size_t)y * (size_t)img->width + (size_t)x) * (size_t)img->channels;
}

int img_write_ppm(const ImgF32 *img, const char *path) {
    FILE *fp = fopen(path, "wb");
    if (!fp) {
        return -1;
    }
    fprintf(fp, "P6\n%d %d\n255\n", img->width, img->height);
    for (int y = 0; y < img->height; ++y) {
        for (int x = 0; x < img->width; ++x) {
            const float *p = img_at_c(img, y, x);
            unsigned char pix[3];
            if (img->channels == 1) {
                float v = p[0];
                if (v < 0.f) v = 0.f;
                if (v > 1.f) v = 1.f;
                pix[0] = pix[1] = pix[2] = (unsigned char)(v * 255.f + 0.5f);
            } else {
                for (int c = 0; c < 3; ++c) {
                    float v = p[c];
                    if (v < 0.f) v = 0.f;
                    if (v > 1.f) v = 1.f;
                    pix[c] = (unsigned char)(v * 255.f + 0.5f);
                }
            }
            fwrite(pix, 1, 3, fp);
        }
    }
    fclose(fp);
    return 0;
}

ImgF32 *img_make_chart(int width, int height) {
    static const float colors[24][3] = {
        {0.46f, 0.33f, 0.26f}, {0.77f, 0.58f, 0.50f}, {0.36f, 0.48f, 0.61f},
        {0.35f, 0.45f, 0.26f}, {0.50f, 0.47f, 0.67f}, {0.35f, 0.61f, 0.56f},
        {0.86f, 0.48f, 0.18f}, {0.28f, 0.36f, 0.65f}, {0.76f, 0.33f, 0.38f},
        {0.36f, 0.23f, 0.42f}, {0.62f, 0.73f, 0.25f}, {0.90f, 0.63f, 0.10f},
        {0.16f, 0.24f, 0.53f}, {0.22f, 0.57f, 0.27f}, {0.69f, 0.16f, 0.16f},
        {0.93f, 0.80f, 0.08f}, {0.73f, 0.33f, 0.60f}, {0.00f, 0.53f, 0.66f},
        {0.96f, 0.96f, 0.96f}, {0.63f, 0.63f, 0.63f}, {0.38f, 0.38f, 0.38f},
        {0.20f, 0.20f, 0.20f}, {0.10f, 0.10f, 0.10f}, {0.05f, 0.05f, 0.05f},
    };
    ImgF32 *img = img_create(width, height, 3);
    if (!img) {
        return NULL;
    }
    int ph = height / 4;
    int pw = width / 6;
    for (int i = 0; i < 24; ++i) {
        int r = i / 6;
        int c = i % 6;
        for (int y = r * ph; y < (r + 1) * ph && y < height; ++y) {
            for (int x = c * pw; x < (c + 1) * pw && x < width; ++x) {
                float *p = img_at(img, y, x);
                p[0] = colors[i][0];
                p[1] = colors[i][1];
                p[2] = colors[i][2];
            }
        }
    }
    return img;
}
