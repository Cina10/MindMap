import sys

from dictation.dictate import async_dictate
from processing.sanitize import sanitize
from google.cloud.speech_v1 import enums

def run(gs_file_uri, dry_run=False, dry_run_file=None):
    if not dry_run:
        dictation_parts = async_dictate(gs_file_uri, enums.RecognitionConfig.AudioEncoding.FLAC, 16000, "en-US")
        dictation = ''.join(dictation_parts)
    else:
        assert(dry_run_file != None)
        with open(dry_run_file) as f:
            dictation = f.read()

    sanitized_dictation = sanitize(dictation)

    print(sanitized_dictation)

run(sys.argv[1], dry_run=True, dry_run_file="./resources/comics_that_ask_what_if.txt")
