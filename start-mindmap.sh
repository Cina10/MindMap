#!/bin/bash

## MindMap: To Transcribe, Visualize, and Inspire
## Authors: floor people, chair people, bed people
VERSION=1.0rc2

# Dependencies: youtube-dl, sox, python3, google-cloud-sdk(gsutil, gcloud, etc.), spacy, nltk, textacy, numpy

# Google Application Credentials
export GOOGLE_APPLICATION_CREDENTIALS="./confidential/MindMap-c4dd617c1818.json"

# Specify binary paths
YOUTUBE_DL_PATH=/usr/bin/youtube-dl
SOX_PATH=/usr/bin/sox
PYTHON3_PATH=/home/allen/Programs/anaconda3/envs/mindmap/bin/python
GSUTIL_PATH=/usr/bin/gsutil
MINDMAP_PATH=./mindmap.py

echo "MindMap: To Transcribe, Visualize, and Inspire"
echo "Authors: floor people, chair people, bed people"
echo "Version: ${VERSION}"
echo
echo "Please name your project:"
read TITLE
echo "Please enter the video URL:"
read VIDEO_URL
echo "Please enter the number of keywords:"
read NUM_KEYWORDS
echo "Please enter a term you would like to search in the video:"
read SEARCHWORD

# Specify video and audio URI/path, create temp directory
echo
echo "[MindMap] Preparing..."
TMP_DIR_PATH=$(mktemp -d -t mindmap-video-XXXXXXXXXX)
DOWNLOADED_AUDIO_PATH="${TMP_DIR_PATH}/downloaded-audio"
CONVERTED_AUDIO_PATH="${TMP_DIR_PATH}/converted-audio.flac"
CLOUD_STORE_BUCKET="gs://mindmap-speeches"
AUDIO_GS_UUID=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c10)
AUDIO_GS_URI="${CLOUD_STORE_BUCKET}/${AUDIO_GS_UUID}.flac"

# Download audio of the video specified, store in FLAC encoding
echo
echo "[MindMap] Downloading audio..."
${YOUTUBE_DL_PATH} ${VIDEO_URL} -x --audio-format "wav" -o "${DOWNLOADED_AUDIO_PATH}.%(ext)s"
${SOX_PATH} "${DOWNLOADED_AUDIO_PATH}.wav" --rate 16k --bits 16 --channels 1 ${CONVERTED_AUDIO_PATH}

# Upload audio file to cloud storage
echo
echo "[MindMap] Uploading audio to Google Cloud..."
${GSUTIL_PATH} cp ${CONVERTED_AUDIO_PATH} "${AUDIO_GS_URI}"

# Call Mindmap
echo
echo "[MindMap] Invoking main program..."
${PYTHON3_PATH} ${MINDMAP_PATH} "${AUDIO_GS_URI}" "${TITLE}" "${NUM_KEYWORDS}" "${SEARCHWORD}"
