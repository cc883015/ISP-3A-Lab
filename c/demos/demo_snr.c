#include "imaging/img.h"
#include "imaging/snr.h"

#include <stdio.h>
#include <stdlib.h>

int main(void) {
    ImgF32 *img = img_create(80, 80, 3);
    for (int i = 0; i < 80 * 80 * 3; ++i) {
        img->data[i] = 0.42f + ((float)(rand() % 1000) / 1000.f - 0.5f) * 0.06f;
    }
    printf("patch SNR = %.2f dB\n", patch_snr_db(img, 20, 20, 30));
    img_free(img);
    return 0;
}
