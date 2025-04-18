# whisper_gpt_analyzer.py — Audio download via yt-dlp, offline Vosk transcription, and GPT-based clip analysis
import os
import tempfile
import subprocess
from yt_dlp import YoutubeDL
import openai
from dotenv import load_dotenv
import wave
import json
from vosk import Model, KaldiRecognizer

# Load environment variables from .env if available
load_dotenv()

# Load your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("OpenAI API key not set. Please set OPENAI_API_KEY in your environment or .env file.")

# Determine base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Auto-detect Vosk model folder (must start with 'vosk-model')
model_dir = None
for entry in os.listdir(BASE_DIR):
    if entry.startswith("vosk-model") and os.path.isdir(os.path.join(BASE_DIR, entry)):
        model_dir = os.path.join(BASE_DIR, entry)
        break
if not model_dir:
    raise RuntimeError(
        f"Vosk model folder not found in {BASE_DIR}. "
        "Please download a Vosk model (e.g. vosk-model-small-en-us-0.15) and unpack it here."
    )
# Load the Vosk model
vosk_model = Model(model_dir)


def download_audio_from_url(video_url):
    """
    Download the audio stream of a YouTube video using yt_dlp and return the file path.
    """
    temp_dir = tempfile.gettempdir()
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(temp_dir, 'audio_%(id)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        filename = ydl.prepare_filename(info)
    return filename


def transcribe_audio(audio_path):
    """
    Transcribe the audio file offline using Vosk and return transcript segments.
    Converts non-WAV audio to WAV via ffmpeg.
    Each segment is a dict with 'start', 'end', and 'text'.
    """
    # Convert to WAV if necessary
    if not audio_path.lower().endswith('.wav'):
        wav_path = os.path.splitext(audio_path)[0] + '.wav'
        # ffmpeg conversion: mono, 16kHz
        subprocess.run([
            'ffmpeg', '-y', '-i', audio_path,
            '-ar', '16000', '-ac', '1', wav_path
        ], check=True)
    else:
        wav_path = audio_path

    wf = wave.open(wav_path, "rb")
    rec = KaldiRecognizer(vosk_model, wf.getframerate())
    segments = []
    while True:
        data = wf.readframes(4000)
        if not data:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            if 'result' in res:
                start = res['result'][0]['start']
                end = res['result'][-1]['end']
                text = res.get('text', '')
                segments.append({'start': start, 'end': end, 'text': text})
    final = json.loads(rec.FinalResult())
    if 'result' in final:
        start = final['result'][0]['start']
        end = final['result'][-1]['end']
        text = final.get('text', '')
        segments.append({'start': start, 'end': end, 'text': text})
    wf.close()
    return segments


def analyze_with_gpt(segments):
    """
    Send transcript segments to GPT-3.5-Turbo to score and pick top 2 clips.
    """
    transcript_text = "\n".join([
        f"[{seg['start']:.1f}-{seg['end']:.1f}] {seg['text']}" for seg in segments
    ])
    prompt = (
        "You are a viral content expert. Rate each transcript segment on a scale of 1-10 for viral potential, "
        "then return the top 2 segments with their start/end timestamps.\n\n" + transcript_text
    )
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI that selects the most viral moments."},
            {"role": "user",   "content": prompt}
        ],
        temperature=0.7
    )
    return resp.choices[0].message.content


def analyze_video(video_url):
    """
    Full pipeline: download audio, transcribe offline, analyze with GPT, and print results.
    """
    print(f"[ANALYZER] Processing video: {video_url}")
    audio_path = download_audio_from_url(video_url)
    print(f"[ANALYZER] Audio downloaded to: {audio_path}")
    segments = transcribe_audio(audio_path)
    print(f"[ANALYZER] Transcribed {len(segments)} segments.")
    analysis = analyze_with_gpt(segments)
    print("[ANALYZER] Top moments and scores:")
    print(analysis)
