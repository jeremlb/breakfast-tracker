#!/usr/bin/env bash
set -e
echo "======= DEPLOY ON GOOGLE APP ENGINE ======"
gcloud config set project breakfast-tracker
gcloud app deploy < Y
