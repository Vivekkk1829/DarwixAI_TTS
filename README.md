# 🎙 Emotion-Aware Text-to-Speech System

##  Project Overview

This project converts input text into speech while dynamically adapting the voice based on the detected emotion and its intensity.

It uses a transformer-based emotion classification model to analyze text and then maps the detected emotion to voice parameters such as speech rate, volume, and pitch. The final output is an audio file that reflects the emotional tone of the input.

---

##  Features

* Emotion detection using a pretrained transformer model
* Intensity calculation based on probability distribution
* Emotion-driven voice modulation (rate, pitch, volume)
* End-to-end pipeline: **Text → Emotion → Audio**
* Simple web interface using FastAPI

---

##  Tech Stack

* Python
* FastAPI (Backend)
* HuggingFace Transformers (NLP Model)
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
│── core.py        # Emotion detection + TTS logic
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

* The model outputs a **probability distribution over emotions**
* It is based on **DistilRoBERTa**, a distilled version of RoBERTa

**Why DistilRoBERTa instead of RoBERTa?**

* ~40% smaller
* ~60% faster
* Retains ~95% of performance

 Ideal for **real-time inference with low computational cost**

---

### 2. Intensity Calculation

Instead of using raw probability, intensity is computed as:

```
Intensity = Top Score - Second Top Score
```

**Core idea of this approach ?**

* We are not just interested in what emotion is predicted, but how confident the model is compared to other possible emotions.
* This helps in determining how much to vary pitch, rate, and volume based on the confidence of the detected emotion.
* More robust than using a single probability

---

### 3. Emotion → Voice Mapping

| Emotion  | Rate      | Volume | Pitch  |
| -------- | --------- | ------ | ------ |
| Joy      | High      | High   | High   |
| Sadness  | Low       | Low    | Low    |
| Anger    | High      | High   | Medium |
| Fear     | Medium    | Medium | Low    |
| Surprise | Very High | High   | High   |
| Neutral  | Medium    | Medium | Medium |

**Why this approach ?**
* Fast and lightweight
* Deterministic and consistent
* Simple to modify

**Trade-off ?**
* This is not fully adaptive approach it cannot capture subtle variations in emotions.

**Better approach ?**
* We can use machine learning models in the future to learn voice modulation patterns from data, enabling more accurate and nuanced speech generation.



---

### 4. Intensity Modulation

* **Rate**

  * Increased for energetic emotions (joy, anger)
  * Decreased for sadness

* **Volume**

  * Scales with intensity (capped at 1.0)

* **Pitch**

  * Increased for joy and surprise
  * Decreased for sadness
  * Slight variation for others

---

### 5. Design Rationale

* Separation of logic (`core.py`) and API (`main.py`) improves modularity
* Probability gap ensures stable intensity estimation
* Rule-based mapping avoids unnecessary ML complexity
* Produces more natural and expressive speech

---

##  Limitations

* pyttsx3 provides limited and system-dependent control over pitch and does not support SSML, which restricts advanced features like phoneme-level control, prosody tuning, and expressive speech synthesis.
* Lower voice realism compared to modern APIs (e.g., ElevenLabs)
* No speaker consistency or advanced prosody control

---

##  Future Improvements

* Integrate ElevenLabs / Google TTS
* Add real-time streaming
* Intgerate SSML
* Improve contextual emotion detection
* Enhance UI with animations

---

##  Example

**Input:**

```
"I am very happy today because I got a job!"
```

**Output:**

* Emotion: Joy
* Intensity: High
* Audio: Fast, energetic, high-pitch voice

---


