import os
from google.cloud import texttospeech
from dotenv import load_dotenv

load_dotenv()

client = texttospeech.TextToSpeechClient()
output_path = "output.mp3"

def text_to_speech(text):
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=os.getenv("LANG_CODE"),
        name=os.getenv("VOICE_NAME")
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    with open(output_path, "wb") as out:
        out.write(response.audio_content)

    return output_path
