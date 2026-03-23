from transformers import pipeline
import pyttsx3

# load model once
classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    temperature=0,
    top_k=7
)

# -----------------------------
# 1. Emotion + Intensity Detection
# -----------------------------
def detect_emotion_and_intensity(text):
    result = classifier(text)[0]

    # sort by score
    result = sorted(result, key=lambda x: x['score'], reverse=True)

    emotion = result[0]['label']

    # non-rule intensity (distribution gap)
    if len(result) > 1:
        intensity = result[0]['score'] 
    else:
        intensity = result[0]['score']

    return emotion, intensity, result


# -----------------------------
# 2. Base Voice Mapping
# -----------------------------
def get_base_params(emotion):
    base_map = {
        "joy": {"rate": 170, "volume": 0.9, "pitch": 150},
        "sadness": {"rate": 130, "volume": 0.6, "pitch": 90},
        "anger": {"rate": 180, "volume": 1.0, "pitch": 110},
        "fear": {"rate": 140, "volume": 0.7, "pitch": 100},
        "surprise": {"rate": 200, "volume": 1.0, "pitch": 160},
        "neutral": {"rate": 160, "volume": 0.8, "pitch": 120}
    }

    return base_map.get(emotion, base_map["neutral"])


# -----------------------------
# 3. Apply Intensity Modulation
# -----------------------------
def apply_intensity(emotion, intensity):
    base = get_base_params(emotion)

    rate_range = 35
    volume_range = 0.3
    pitch_range = 60

    # RATE
    if emotion == "sadness":
        rate = int(base["rate"] - intensity * 40)
    else:
        rate = int(base["rate"] + intensity * rate_range)

    # VOLUME
    volume = base["volume"] + intensity * volume_range
    volume = min(volume, 1.0)

    # PITCH (emotion-specific)
    if emotion in ["joy", "surprise"]:
        pitch = int(base["pitch"] + intensity * pitch_range)
    elif emotion == "sadness":
        pitch = int(base["pitch"] - intensity * pitch_range)
    else:
        pitch = int(base["pitch"] + intensity * (pitch_range / 2))

    return {
        "rate": rate,
        "volume": volume,
        "pitch": pitch
    }


# -----------------------------
# 4. Generate Audio
# -----------------------------
def generate_audio(text, params, file_path="output.mp3"):
    engine = pyttsx3.init()

    engine.setProperty('rate', params['rate'])
    engine.setProperty('volume', params['volume'])

    # ⚠️ pitch support is system dependent
    try:
        engine.setProperty('pitch', params['pitch'])
    except:
        pass

    engine.save_to_file(text, file_path)
    engine.runAndWait()

    return file_path


# -----------------------------
# 5. Full Pipeline
# -----------------------------
def process_text(text):
    emotion, intensity, full_result = detect_emotion_and_intensity(text)

    params = apply_intensity(emotion, intensity)

    audio_file = generate_audio(text, params)

    return {
        "emotion": emotion,
        "intensity": round(float(intensity), 3),
        "voice_params": params,
        "audio_file": audio_file,
        "raw_model_output": full_result
    }


# -----------------------------
# TEST
# -----------------------------
if __name__ == "__main__":
    text = "Revan is watching  a movie"
    result = process_text(text)

    print(result)