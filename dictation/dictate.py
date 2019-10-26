import logging
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums


def async_dictate(storage_uri, encoding):
    """
    Transcribe long audio file from Cloud Storage using asynchronous speech
    recognition

    Args:
      storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
    """

    client = speech_v1.SpeechClient()

    # storage_uri = 'gs://cloud-samples-data/speech/brooklyn_bridge.raw'

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 16000

    # The language of the supplied audio
    language_code = "en-US"
    
    config = {
        "sample_rate_hertz": sample_rate_hertz,
        "language_code": language_code,
        "encoding": encoding,
    }
    audio = {"uri": storage_uri}

    operation = client.long_running_recognize(config, audio)

    logging.info("Waiting for dictation results...")
    response = operation.result()

    text = []
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        text.append(format(alternative.transcript))
    
    logging.info("Dictation successful.")
    
    return text
