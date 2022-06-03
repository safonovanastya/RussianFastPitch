#!/usr/bin/env bash

set -e

: ${DATA_DIR:=RUSLAN}
: ${ARGS="--extract-mels"}

python prepare_dataset.py \
--wav-text-filelists filelists/short_ruslan_train.txt \
                          filelists/short_ruslan_val.txt \
    --n-workers 16 \
    --batch-size 1 \
    --dataset-path $DATA_DIR \
    --extract-pitch \
    --f0-method pyin \
    $ARGS
