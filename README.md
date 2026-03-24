# 🎙 Emotion-Aware Text-to-Speech System

##  Project Overview

This project converts input text into speech while dynamically adapting the voice based on the detected emotion and its intensity.

It uses a transformer-based emotion classification model to analyze text and then maps the detected emotion to voice parameters such as speech rate, volume, and pitch. The final output is an audio file that reflects the emotional tone of the input.

---

##  Features

* Emotion detection using a pretrained transformer model
* Intensity calculation based on probability distribution
* Emotion-driven voice modulation (rate, pitch, volume)
* End-to-end pipeline: Text → Emotion → Audio
* Simple web interface using FastAPI

---

##  Tech Stack

* Python
* FastAPI (backend)
* HuggingFace Transformers (NLP model)
* pyttsx3 (Text-to-Speech)

---

##  Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-link>
cd <project-folder>
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
uvicorn main:app --reload
```

### 5. Open in Browser

```
http://127.0.0.1:8000
```

---

##  Project Structure

```
project/
│── core.py        # Emotion + TTS logic
│── main.py        # FastAPI app
│── templates/
│     └── index.html
│── requirements.txt
```

---

##  Design Choices

### 1. Emotion Detection

We use a pretrained transformer model:

```
j-hartmann/emotion-english-distilroberta-base
```

This model outputs a probability distribution over emotions.

---

### 2. Intensity Calculation

Instead of using raw probability, intensity is computed as:

```
Intensity = Top Score - Second Top Score
```

**Why?**

* Captures confidence gap between emotions
* More robust than using raw probability alone

---

### 3. Emotion → Voice Mapping

Each emotion is mapped to base voice parameters:

| Emotion  | Rate      | Volume | Pitch  |
| -------- | --------- | ------ | ------ |
| Joy      | High      | High   | High   |
| Sadness  | Low       | Low    | Low    |
| Anger    | High      | High   | Medium |
| Fear     | Medium    | Medium | Low    |
| Surprise | Very High | High   | High   |
| Neutral  | Medium    | Medium | Medium |

---

### 4. Intensity Modulation

Voice parameters are dynamically adjusted using intensity:

* **Rate**

  * Increased for energetic emotions (joy, anger)
  * Decreased for sadness

* **Volume**

  * Scales with intensity (capped at 1.0)

* **Pitch**

  * Increased for joy/surprise
  * Decreased for sadness
  * Slight variation for others

---

### 5. Design Rationale

* Separating `core.py` (logic) and `main.py` (API) improves modularity
* Using probability gap ensures more stable intensity estimation
* Emotion-based modulation creates more natural and expressive speech

---

##  Limitations

* pyttsx3 has limited pitch control (system dependent)
* Voice realism is lower compared to modern APIs (e.g., ElevenLabs)
* No speaker consistency or advanced prosody control

---

## 🔮 Future Improvements

* Integrate ElevenLabs / Google TTS for better voice quality
* Add real-time streaming audio
* Improve emotion detection with contextual understanding
* Add frontend enhancements (animations, waveform)

---

##  Example

Input:

```
"I am very happy today because I got a job!"
```

Output:

* Emotion: Joy
* Intensity: High
* Audio: Fast, energetic, high-pitch voice

---

##  Author

Vivek K
