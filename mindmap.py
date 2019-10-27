import sys

from google.cloud.speech_v1 import enums

from dictation.dictate import async_dictate
from processing.sanitize import sanitize
from processing.analyze import textrank, similarity

def run(gs_file_uri, dry_run=False, dry_run_file=None):
    if not dry_run:
        dictation_parts = async_dictate(gs_file_uri, enums.RecognitionConfig.AudioEncoding.FLAC, 16000, "en-US")
        dictation = ''.join(dictation_parts)
    else:
        assert(dry_run_file != None)
        with open(dry_run_file) as f:
            dictation = f.read()
    
    print(dictation)

    print("====================")

    sanitized_dictation = sanitize(dictation)

    print(sanitized_dictation)

    print("====================")

    kw_w_pairs = textrank(sanitized_dictation, topn=20)
    print(kw_w_pairs)

    print("====================")

    sim_mat = similarity(kw_w_pairs)
    print(sim_mat)

run(sys.argv[1], dry_run=True, dry_run_file="./resources/how_trees_bend_the_law_of_physics.txt")
