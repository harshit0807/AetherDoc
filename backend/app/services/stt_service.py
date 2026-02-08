from google.cloud import speech
from typing import Generator

def streaming_transcribe(audio_generator: Generator[bytes, None, None]):
    """
    Receives a generator of audio chunks and yields transcripts
    """

    client = speech.SpeechClient()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk)
        for chunk in audio_generator
    )

    responses = client.streaming_recognize(
        config=streaming_config,
        requests=requests
    )

    for response in responses:
        for result in response.results:
            if result.is_final:
                yield result.alternatives[0].transcript
