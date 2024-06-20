//
// Created by Ymymym on 2024/6/3.
//

#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <cstdint>

#define STB_IMAGE_IMPLEMENTATION

#include "stb_image.h"

uint8_t palette[8 * 3] = {
        0, 0, 0,
        255, 255, 255,
        67, 138, 28,
        100, 64, 255,
        191, 0, 0,
        255, 243, 56,
        232, 126, 0,
        194, 164, 244
};

int depalette(uint8_t *color) {
    int p;
    int mindiff = 100000000;
    int bestc = 0;
    for (p = 0; p < sizeof(palette) / 3; p++) {
        int diffr = ((int) color[0]) - ((int) palette[p * 3 + 0]);
        int diffg = ((int) color[1]) - ((int) palette[p * 3 + 1]);
        int diffb = ((int) color[2]) - ((int) palette[p * 3 + 2]);
        int diff = (diffr * diffr) + (diffg * diffg) + (diffb * diffb);
        if (diff < mindiff) {
            mindiff = diff;
            bestc = p;
        }
    }
    return bestc;
}

/**
 * bmp img to bin
 * @param argc
 * @param argv
 * @return
 */
int main(int argc, char **argv) {
    if (argc < 3)
    {
        fprintf(stderr, "Usage: converter [image file] [out file]\n");
        printf("Press Enter to exit.");
        // if hava error ,server while pause
//        getchar();
        return -1;
    }
    int x, y, n;
    unsigned char *data = stbi_load(argv[1], &x, &y, &n, 0);
    if (!data) {
        fprintf(stderr, "Error: Can't open image.\n");
        printf("Press Enter to exit.");
//        getchar();
        return -6;
    }
    if ((x != 600) && (x != 640) && (x != 800)) {
        fprintf(stderr, "Error: Image dimensions must be 600*448/640*400/800*480.\n");
        printf("Press Enter to exit.");
//        getchar();
        return -2;
    }
    if (x == 600 && y > 448) {
        y = 448;
    }
    if (x == 640 && y > 400) {
        y = 400;
    }
    if (x == 800 && y > 480) {
        y = 480;
    }
    int i, j;
//    FILE *fout = NULL;
    int num = 0;
    unsigned char *retData = (unsigned char *) malloc(x * y / 2 * sizeof(unsigned char));
    for (j = 0; j < y; j++) {
        for (i = 0; i < x / 2; i++) {
            int c1 = depalette(data + n * (i * 2 + x * j));
            int c2 = depalette(data + n * (i * 2 + x * j + 1));
            char uc = c2 | (c1 << 4);
            retData[num++] = uc;
        }
    }
//    printf("%s", argv[3]);
    FILE *file = fopen(argv[2], "wb");
    if (file == NULL) {
        fprintf(stderr, "无法打开文件\n");
        exit(1);
    }
    fwrite(retData, sizeof(unsigned char), x * y / 2, file);
    stbi_image_free(data);
    return 0;
}

