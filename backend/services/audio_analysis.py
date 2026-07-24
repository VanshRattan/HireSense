import whisper
import os
import re

# Load the model only once when module is loaded. Using 'small' for better speech recognition accuracy.
try:
    model = whisper.load_model("small")
except Exception as e:
    print(f"Failed to load whisper model: {e}")
    model = None

FILLER_WORDS = ["um", "uh", "like", "you know", "so", "actually", "basically", "right"]

def analyze_audio(audio_path: str):
    """
    Transcribes audio and extracts filler word statistics.
    """
    if model is None:
        return {"error": "Model not loaded", "transcript": "", "filler_stats": {}}
        
    try:
        result = model.transcribe(audio_path)
        transcript = result["text"]
    except Exception as e:
        print(f"Whisper transcription failed: {e}")
        transcript = f"Transcription failed: {e}"
    
    # Simple filler word counting using regex (case-insensitive words)
    filler_stats = {}
    total_fillers = 0
    words = [w.strip(".,!?").lower() for w in transcript.split()]
    
    for word in words:
        if word in FILLER_WORDS:
            filler_stats[word] = filler_stats.get(word, 0) + 1
            total_fillers += 1
            
    # Also check multi-word fillers
    transcript_lower = transcript.lower()
    for fw in ["you know", "i mean"]:
        count = transcript_lower.count(fw)
        if count > 0:
            filler_stats[fw] = count
            total_fillers += count

    return {
        "transcript": transcript,
        "filler_words_used": filler_stats,
        "filler_word_count": total_fillers
    }
