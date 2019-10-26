import sys

from dictation.dictate import async_dictate
from google.cloud.speech_v1 import enums

def run(gs_file_uri):
    print(gs_file_uri)
    dictation = async_dictate(gs_file_uri, enums.RecognitionConfig.AudioEncoding.FLAC, 16000, "en-US")

    for d in dictation:
        print(d)
        print()

run(sys.argv[1])
