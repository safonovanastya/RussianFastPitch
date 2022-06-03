#!/usr/bin/env bash

set -e

scripts/download_cmudict.sh

DATA_DIR="RUSLAN"
RUSLAN_ARCH="RUSLAN.tar.gz"
RUSLAN_URL="https://drive.google.com/uc?id=1ePWBbq0NSqLLYnoFAPuFxa_xAuL0TfWW"

if [ ! -d ${DATA_DIR} ]; then
  echo "Downloading ${RUSLAN_ARCH} ..."
  gdown ${RUSLAN_URL}
  echo "Extracting ${RUSLAN_ARCH} ..."
  tar -xzvf ${RUSLAN_ARCH} -C ${DATA_DIR}
  rm -f ${RUSLAN_ARCH}
fi
