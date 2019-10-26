from dictation.dictate import async_dictate
from google.cloud.speech_v1 import enums

async_dictate('gs://mindmap-speeches/barackobamafirstweeklyaddressARXE.flac', enums.RecognitionConfig.AudioEncoding.FLAC)