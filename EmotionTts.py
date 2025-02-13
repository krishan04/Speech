import torch
from transformers import pipeline
import os
import hashlib
import soundfile as sf
import numpy as np
# import coqui_tts
from TTS.api import TTS
from pydub import AudioSegment
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def get_hashed_filename(text):
    """Generates a unique hash for a given text to use as a filename."""
    return hashlib.md5(text.encode()).hexdigest()

# Load pre-trained emotion detection model
emotion_classifier = pipeline(
    "text-classification", 
    model="bhadresh-savani/distilbert-base-uncased-emotion", 
    return_all_scores=False, 
    device=0  # Use GPU if available
)

def detect_emotion(text):
    """Detects dominant emotion in a given text."""
    result = emotion_classifier(text)
    return result[0]['label']

# Define emotion-to-music mapping
music_map = {
    "joy": "Speech/music/happy.mp3",
    "sadness": "Speech/music/sad.mp3",
    "fear": "Speech/music/suspense.mp3",
    "anger": "Speech/music/intense.mp3",
    "surprise": "Speech/music/exciting.mp3"
    # "neutral": "music/neutral.mp3"
}

tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
def text_to_speech(text, output_file):
    """Converts text to speech using Coqui TTS and saves to file if not cached."""
    if os.path.exists(output_file):
        print(f"Using cached TTS file: {output_file}")
        return
    tts.tts_to_file(text=text, file_path=output_file)

def merge_audio(narration_file, music_file, output_file):
    """Merges TTS narration with background music."""
    narration = AudioSegment.from_wav(narration_file)
    music = AudioSegment.from_mp3(music_file).set_frame_rate(narration.frame_rate)
    music = music - 10  # Lower volume of music
    combined = narration.overlay(music, loop=True)
    combined.export(output_file, format="mp3")

def clean_cache(cache_dir, max_size_mb=500):
    """Deletes the oldest cached files if cache size exceeds max_size_mb."""
    files = [os.path.join(cache_dir, f) for f in os.listdir(cache_dir)]
    total_size = sum(os.path.getsize(f) for f in files) / (1024 * 1024)
    
    if total_size > max_size_mb:
        files.sort(key=os.path.getctime)  # Sort by creation time (oldest first)
        while total_size > max_size_mb and files:
            oldest_file = files.pop(0)
            total_size -= os.path.getsize(oldest_file) / (1024 * 1024)
            os.remove(oldest_file)
            print(f"Deleted old cached file: {oldest_file}")

# Sample input
novel_text = "She felt his fingers brush against hers, a soft, lingering touch that sent warmth rushing through her veins. The world around them faded—no city lights, no distant chatter, just the quiet melody of their unspoken words. His eyes held hers, deep and unwavering, as if searching for a home he had always known but never found. And in that moment, under the silver glow of the moon, she knew—love wasn’t in grand gestures or whispered promises. It was in the way his hand found hers, steady and sure, as if it had belonged there all along."

# Step 1: Detect emotion
emotion = detect_emotion(novel_text)
print(f"Detected Emotion: {emotion} hhhhhhhhhhhhhjfhjhfjdhfjhdfdshfdjf")

# Step 2: Convert text to speech (with caching)
cache_dir = "cache"
os.makedirs(cache_dir, exist_ok=True)
hashed_filename = get_hashed_filename(novel_text)
tts_output = f"{cache_dir}/{hashed_filename}.wav"
text_to_speech(novel_text, tts_output)

# Step 3: Assign background music based on emotion
music_file = music_map.get(emotion, "music/sad.mp3")

# Step 4: Merge narration with background music
final_output = "final_audiobook.mp3"
merge_audio(tts_output, music_file, final_output)

# Step 5: Cleanup cache
clean_cache(cache_dir)

print("Audio processing complete. Check final_audiobook.mp3")