CC      ?= cc
CFLAGS  ?= -std=c99 -Wall -Wextra -O2 -Iinclude
SRC      = src/isp/img.c src/isp/bayer.c src/isp/demosaic.c \
           src/aaa/ae.c src/aaa/awb.c src/aaa/af.c src/metrics/snr.c
DEMOS    = demo_pipeline demo_ae demo_awb demo_af demo_snr

.PHONY: all clean

all: $(addprefix bin/,$(DEMOS))

bin/%: demos/%.c $(SRC)
	mkdir -p bin
	$(CC) $(CFLAGS) -o $@ $^ -lm

clean:
	rm -rf bin
