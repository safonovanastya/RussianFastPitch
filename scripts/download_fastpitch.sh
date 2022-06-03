#!/usr/bin/env bash

set -e

# # Grapheme-level w/o energy conditioning
# MODEL_ZIP="FastPitch_checkpoint_1000.pt.zip"
# MODEL="FastPitch_checkpoint_1000.pt"
# MODEL_URL="https://drive.google.com/uc?id=1aL9SXIjlJ5nQVD6LV5BI3DiQWVo8k2oi"
# MODEL_DIR="../pretrained_fastpitch"

# Phoneme-level w/ energy conditioning
: ${MODEL_DIR:="pretrained_fastpitch"}
: ${MODEL_ZIP:="FastPitch_checkpoint_1000.pt.zip"}
: ${MODEL:="FastPitch_checkpoint_1000.pt"}
: ${MODEL_URL:="https://drive.google.com/uc?id=1aL9SXIjlJ5nQVD6LV5BI3DiQWVo8k2oi"}

mkdir -p "$MODEL_DIR"

if [ ! -f "${MODEL_DIR}/${MODEL_ZIP}" ]; then
  echo "Downloading ${MODEL_ZIP} ..."
  gdown ${MODEL_URL} -O ${MODEL_DIR}/${MODEL_ZIP} \
       || { echo "ERROR: Failed to download ${MODEL_ZIP} from NGC"; exit 1; }
fi

if [ ! -f "${MODEL_DIR}/${MODEL}" ]; then
  echo "Extracting ${MODEL} ..."
  unzip -qo ${MODEL_DIR}/${MODEL_ZIP} -d ${MODEL_DIR} \
        || { echo "ERROR: Failed to extract ${MODEL_ZIP}"; exit 1; }

  echo "OK"

else
  echo "${MODEL} already downloaded."
fi
