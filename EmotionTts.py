import subprocess
from TTS.api import TTS
from transformers import pipeline
from pydub import AudioSegment
import os

# Load TTS model
tts = TTS(model_name="tts_models/en/ljspeech/fast_pitch")

# Load emotion detection model
emotion_classifier = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions", top_k=1)

# Emotion to Music Mapping
EMOTION_MUSIC_MAP = {
    "joy": "music/uplifting_acoustic.mp3",
    "pride": "music/uplifting_acoustic.mp3",
    "optimism": "music/upbeat_pop.mp3",
    "excitement": "music/upbeat_pop.mp3",
    "anger": "music/heavy_drums.mp3",
    "disgust": "music/heavy_drums.mp3",
    "sadness": "music/soft_piano.mp3",
    "grief": "music/soft_piano.mp3",
    "fear": "music/dark_ambient.mp3",
    "nervousness": "music/dark_ambient.mp3",
    "suspense": "music/dark_ambient.mp3",
    "surprise": "music/mysterious_orchestral.mp3",
    "curiosity": "music/mysterious_orchestral.mp3",
    "love": "music/soft_jazz.mp3",
    "romance": "music/soft_jazz.mp3",
    "neutral": "music/soft_jazz.mp3"
}

# Emotion to SoX Modulation
EMOTION_SOX_MAP = {
    "joy": {"speed": 1.2, "pitch": 100},
    "sadness": {"speed": 0.85, "pitch": -100},
    "anger": {"speed": 1.3, "pitch": 150},
    "fear": {"speed": 0.9, "pitch": 100},
    "surprise": {"speed": 1.1, "pitch": 110},
    "neutral": {"speed": 1.0, "pitch": 0},
}

def generate_speech(text):
    """Generate speech and return temp file path."""
    temp_audio = "temp_speech.wav"
    tts.tts_to_file(text=text, file_path=temp_audio)
    return temp_audio

def modulate_voice(input_path, emotion):
    """Apply SoX voice modulation and return output path."""
    sox_settings = EMOTION_SOX_MAP.get(emotion, {"speed": 1.0, "pitch": 0})
    output_path = "modulated_speech.wav"
    
    sox_command = [
        "sox", input_path, output_path,
        "pitch", str(sox_settings["pitch"]),
        "tempo", str(sox_settings["speed"])
    ]
    subprocess.run(sox_command, check=True)
    os.remove(input_path)  # Remove original speech file to save space
    return output_path

def process_text(text):
    """Generate speech, detect emotion, and apply modulation."""
    temp_audio = generate_speech(text)
    
    emotion_result = emotion_classifier(text)[0]
    emotion = emotion_result[0]['label']
    print(f"Detected Emotion: {emotion}")
    
    return modulate_voice(temp_audio, emotion), emotion

def mix_audio(narration_path, emotion, output_path="final_output.wav"):
    """Mix narration with appropriate background music dynamically."""
    music_path = EMOTION_MUSIC_MAP.get(emotion, "music/soft_jazz.mp3")  # Default fallback
    
    narration = AudioSegment.from_file(narration_path)
    music = AudioSegment.from_file(music_path)
    
    # Adjust music volume based on emotion intensity
    volume_adjustment = -10 if emotion in ["joy", "optimism", "love"] else -15 if emotion in ["fear", "suspense"] else -20
    music = music[:len(narration)].apply_gain(volume_adjustment)
    
    # Add fade-in/fade-out for smooth transitions
    narration = narration.fade_in(500).fade_out(500)
    
    final_audio = narration.overlay(music)
    final_audio.export(output_path, format="wav")
    os.remove(narration_path)  # Remove temp narration file
    print(f"Mixed audio saved to: {output_path}")

# Example usage
narration_file, detected_emotion = process_text("Its fragility and stern rigidity rendered it almost unusable as a weapon or electrical component. I am happy of it.")
mix_audio(narration_file, detected_emotion)
