#!/usr/bin/env bash

set -e

: ${MODEL_DIR:="pretrained_waveglow"}
MODEL="checkpoint_WaveGlow_550.pt"
MODEL_ZIP="checkpoint_WaveGlow_550.pt.zip"
MODEL_URL="https://drive.google.com/uc?id=1R75q5O5UpOlnYgdL0BwCmToOmnEiS1vk"

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
