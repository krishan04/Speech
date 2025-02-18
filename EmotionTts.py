import torch
from transformers import pipeline
import os
import hashlib
from TTS.api import TTS
from pydub import AudioSegment
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# ✅ Define directories
CACHE_DIR = "cache"
AUDIO_DIR = "uploads/audio"
MUSIC_DIR = "music"
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(MUSIC_DIR, exist_ok=True)

# ✅ Load pre-trained emotion detection model
emotion_classifier = pipeline(
    "text-classification",
    model="bhadresh-savani/distilbert-base-uncased-emotion",
    return_all_scores=False,
    device=0  # Use GPU if available
)

# ✅ Load Coqui TTS model
tts = TTS(model_name="tts_models/en/ljspeech/vits")

# ✅ Emotion-to-music mapping
music_map = {
    "joy": f"{MUSIC_DIR}/happy.mp3",
    "sadness": f"{MUSIC_DIR}/sad.mp3",
    "fear": f"{MUSIC_DIR}/suspense.mp3",
    "anger": f"{MUSIC_DIR}/intense.mp3",
    "surprise": f"{MUSIC_DIR}/exciting.mp3",
}

def get_hashed_filename(text):
    """Generates a unique hash for a given text to use as a filename."""
    return hashlib.md5(text.encode()).hexdigest()

def detect_emotion(text):
    """Detects dominant emotion in a given text."""
    result = emotion_classifier(text)
    return result[0]['label']

def text_to_speech(text, output_file):
    """Converts text to speech and caches the result."""
    if os.path.exists(output_file):
        print(f"✅ Using cached TTS file: {output_file}")
        return
    
    print(f"🎙️ Generating speech for: {text[:50]}...")
    tts.tts_to_file(text=text, file_path=output_file)

def merge_audio(narration_file, music_file, output_file):
    """Merges TTS narration with background music."""
    narration = AudioSegment.from_wav(narration_file)
    music = AudioSegment.from_mp3(music_file).set_frame_rate(narration.frame_rate)
    music = music - 10   # Lower volume of background music
    combined = narration.overlay(music, loop=True)
    combined.export(output_file, format="mp3")
    print(f"🎵 Merged audio saved: {output_file}")

def clean_cache(directory, max_size_mb=500):
    """Deletes the oldest cached files if cache size exceeds max_size_mb."""
    files = [os.path.join(directory, f) for f in os.listdir(directory)]
    total_size = sum(os.path.getsize(f) for f in files) / (1024 * 1024)

    if total_size > max_size_mb:
        files.sort(key=os.path.getctime)  # Sort by creation time (oldest first)
        while total_size > max_size_mb and files:
            oldest_file = files.pop(0)
            total_size -= os.path.getsize(oldest_file) / (1024 * 1024)
            os.remove(oldest_file)
            print(f"🗑️ Deleted old cache file: {oldest_file}")

def process_novel(novel_id, paragraphs):
    """Processes a novel paragraph by paragraph, generating speech and merging audio."""
    novel_audio_dir = f"{AUDIO_DIR}/{novel_id}"
    os.makedirs(novel_audio_dir, exist_ok=True)

    audio_files = []
    for idx, paragraph in enumerate(paragraphs):
        # Step 1: Detect emotion
        emotion = detect_emotion(paragraph)
        print(f"📝 Paragraph {idx+1}: Detected Emotion -> {emotion}")

        # Step 2: Generate TTS file
        hashed_filename = get_hashed_filename(paragraph)
        tts_output = f"{novel_audio_dir}/{hashed_filename}.wav"
        text_to_speech(paragraph, tts_output)
        audio_files.append(tts_output)

        # Step 3: Merge with background music
        music_file = music_map.get(emotion, f"{MUSIC_DIR}/sad.mp3")
        final_para_audio = f"{novel_audio_dir}/para_{idx+1}.mp3"
        merge_audio(tts_output, music_file, final_para_audio)

    # Step 4: Merge all paragraphs into final audiobook
    final_audiobook = f"{novel_audio_dir}/final_audiobook.mp3"
    merge_audio_files(audio_files, final_audiobook)
    print(f"📚 Final audiobook saved at: {final_audiobook}")

    # Step 5: Cleanup cache
    clean_cache(CACHE_DIR)

def merge_audio_files(audio_files, output_file):
    """Merges multiple audio files into a final audiobook."""
    if not audio_files:
        print("❌ No audio files to merge.")
        return

    final_audio = AudioSegment.empty()
    for file in audio_files:
        audio = AudioSegment.from_wav(file)
        final_audio += audio  # Append each paragraph's audio

    final_audio.export(output_file, format="mp3")
    print(f"🎧 Final audiobook created: {output_file}")

# Sample Novel Processing
novel_id = 1
sample_paragraphs = ["He knew exactly where Han Sen was. What is so special about you, exactly?” Xie Qing eyed Han Sen with suspicion. They couldn’t get their hands free.Han Sen held onto the lid like the rest, pretending he was suffering the same fate. He believed that sooner or later he could make Ji Yanran fall in love with him.But now, first he needed to beat this despicable and shameless bastard to approach his goddess.Li Yufeng was hitting the spots with all he had, thinking that if he went faster and raise the difference to six or seven points, then the effect might be even better.But when Li Yufeng was reaching for a spot again, all spots suddenly disappeared.",
"""Nine-Headed Bird, hearing Han Sen answer him so quickly, grew even more suspicious. In fact, I bet you have no idea what kind of creature Ning Yue was asking you to kill," Zhu Ting sighed and said."Isn't it just a sacred-blood creature?" Han Sen's heart leapt, but his face remained still."Sacred-blood creature? How long has he been practicing Teeth Knife? Bai Wuchang could scarcely believe it.
"""]

process_novel(novel_id, sample_paragraphs)