

from elevenlabs import ElevenLabs, play, save

# 1. Initialize the client with your API key
client = ElevenLabs(
    api_key="sk_53e4091a63c2f282c6b09c7b85c9fb98106238ef7c962414" # Replace with your actual API key
)

# 2. Call the text-to-speech endpoint
audio_stream = client.text_to_speech.convert(
    text="Hello world! This is a test of the ElevenLabs API.",
    voice_id="JBFqnCBsd6RMkjVDRZzb", # This is the ID for the default voice "Rachel"
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128"
)

audio_bytes = b"".join(audio_stream)

# 4. Save the audio to an MP3 file FIRST (always works)
save(audio_bytes, "output.mp3")
print("Audio saved successfully to output.mp3!")


# sk_53e4091a63c2f282c6b09c7b85c9fb98106238ef7c962414