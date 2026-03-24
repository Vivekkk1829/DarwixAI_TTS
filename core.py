from transformers import pipeline
import pyttsx3


classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=7
)


def detect_emotion_and_intensity(text):
    result = classifier(text)[0]

    result = sorted(result, key=lambda x: x['score'], reverse=True)

    emotion = result[0]['label']


    if len(result) > 1:
        intensity = result[0]['score'] - result[1]['score']
    else:
        intensity = result[0]['score']

    return emotion, intensity, result



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



def apply_intensity(emotion, intensity):
    base = get_base_params(emotion)

    rate = base["rate"]
    volume = base["volume"]
    pitch = base["pitch"]

    rate_range = 40
    volume_range = 0.3
    pitch_range = 50

    
    if emotion == "joy":
        rate += intensity * rate_range
    elif emotion == "surprise":
        rate += intensity * (rate_range + 20)  
    elif emotion == "anger":
        rate += intensity * rate_range
    elif emotion == "sadness":
        rate -= intensity * rate_range
    elif emotion == "fear":
        rate += intensity * (rate_range / 2)
    else:  
        rate += intensity * (rate_range / 3)

   
    if emotion in ["joy", "anger", "surprise"]:
        volume += intensity * volume_range
    elif emotion == "sadness":
        volume -= intensity * volume_range
    elif emotion == "fear":
        volume += intensity * (volume_range / 2)
    else:
        volume += intensity * (volume_range / 3)

    volume = max(0.3, min(volume, 1.0))

  
    if emotion in ["joy", "surprise"]:
        pitch += intensity * pitch_range
    elif emotion == "sadness":
        pitch -= intensity * pitch_range
    elif emotion == "fear":
        pitch -= intensity * (pitch_range / 2)
    elif emotion == "anger":
        pitch += intensity * (pitch_range / 3)
    else:
        pitch += intensity * (pitch_range / 4)

    return {
        "rate": int(rate),
        "volume": round(volume, 2),
        "pitch": int(pitch)
    }



def generate_audio(text, params, file_path="output.mp3"):
    engine = pyttsx3.init()

    engine.setProperty('rate', params['rate'])
    engine.setProperty('volume', params['volume'])


    try:
        engine.setProperty('pitch', params['pitch'])
    except:
        pass

    engine.save_to_file(text, file_path)
    engine.runAndWait()

    return file_path



def process_text(text):
    emotion, intensity, full_result = detect_emotion_and_intensity(text)

    params = apply_intensity(emotion, intensity)

    audio_file = generate_audio(text, params)

    return {
        "emotion": emotion,
        "intensity": round(float(intensity), 3),
        "voice_params": params,
        "audio_file": audio_file
    }



if __name__ == "__main__":
    text = "I am extremely happy today!"
    result = process_text(text)

    print(result)