import sys
import os

from google.cloud.speech_v1 import enums

from dictation.dictate import async_dictate
from processing.sanitize import sanitize
from processing.analyze import textrank, similarity, closest_match
from utils.py_to_json import generate_json_pair
from utils.knit import knit

def run(gs_file_uri, title, num_keywords, searchword, dry_run=False, dry_run_file=None):
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

    kw_w_pairs = textrank(sanitized_dictation, topn=num_keywords)
    print(kw_w_pairs)

    print("====================")

    sim_mat = similarity(kw_w_pairs)
    print(sim_mat)

    print("====================")

    (match_kw, match_score) = closest_match(kw_w_pairs, searchword)
    print(match_kw, match_score)

    print("====================")

    (nodes_list, edges_list) = generate_json_pair(kw_w_pairs, sim_mat)

    replacement_map = {
        "MINDMAP_SEARCH_WORD_MATCH": searchword,
        "MINDMAP_MOST_RELEVANT_MATCH": match_kw,
        "MINDMAP_BEST_MATCH_SCORE": "{0:.0%}".format(match_score),
        "MINDMAP_FREQMAP_MATCH": nodes_list,
        "MINDMAP_ADJMAT_MATCH": edges_list,
        "MINDMAP_TRANSCRIPTION_MATCH": sanitized_dictation
    }

    script_path = os.path.dirname(os.path.realpath(__file__))

    knit(script_path+"/index.html", script_path+"/"+title+".html", replacement_map)

run(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], dry_run=True, dry_run_file="./resources/how_trees_bend_the_law_of_physics.txt")
