import sys
import os
import webbrowser

from google.cloud.speech_v1 import enums

from dictation.dictate import async_dictate
from processing.sanitize import sanitize
from processing.analyze import textrank, similarity, closest_match
from utils.py_to_json import generate_json_pair
from utils.knit import knit

def run(gs_file_uri, title, num_keywords, searchword, dry_run=False, dry_run_file=None):

    print("[MindMap-Main][0/6] Waiting for dictation to complete...")

    if not dry_run:
        dictation_parts = async_dictate(gs_file_uri, enums.RecognitionConfig.AudioEncoding.FLAC, 16000, "en-US")
        dictation = ''.join(dictation_parts)
    else:
        assert(dry_run_file != None)
        with open(dry_run_file) as f:
            dictation = f.read()

    print("[MindMap-Main][1/6] Dictation received, sanitizing...")

    sanitized_dictation = sanitize(dictation)

    print("[MindMap-Main][2/6] Generating "+str(num_keywords)+" keyword-weight pairs via TextRank...")

    kw_w_pairs = textrank(sanitized_dictation, topn=num_keywords)

    print("[MindMap-Main][3/6] Calculating similarity between keywords...")

    sim_mat = similarity(kw_w_pairs)

    print("[MindMap-Main][4/6] Matching search term to keywords...")

    (match_kw, match_score) = closest_match(kw_w_pairs, searchword)

    print("[MindMap-Main][5/6] Preparing for output...")

    (nodes_list, edges_list) = generate_json_pair(kw_w_pairs, sim_mat)

    replacement_map = {
        "MINDMAP_TITLE_MATCH": title,
        "MINDMAP_SEARCH_WORD_MATCH": searchword,
        "MINDMAP_MOST_RELEVANT_MATCH": match_kw,
        "MINDMAP_BEST_MATCH_SCORE": "{0:.0%}".format(match_score),
        "MINDMAP_FREQMAP_MATCH": nodes_list,
        "MINDMAP_ADJMAT_MATCH": edges_list,
        "MINDMAP_TRANSCRIPTION_MATCH": sanitized_dictation
    }

    script_path = os.path.dirname(os.path.realpath(__file__))

    knit(script_path+"/index.html", script_path+"/"+title+".html", replacement_map)

    print("[MindMap-Main][6/6] Output completed. Opening in web browser...")

    url = "file://"+script_path+"/"+title+".html"
    webbrowser.open(url, new=2) 

run(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], dry_run=False)
