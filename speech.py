import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
from faster_whisper import WhisperModel
from moviepy.editor import VideoFileClip


model_size="large-v3"

model = WhisperModel(model_size,device="cpu",compute_type="int8")


video = VideoFileClip("2.mp4")
audio_path = "2.wav"
video.audio.write_audiofile(audio_path)

# segments, info = model.transcribe("audio.mp3", beam_size=5)
segments, info = model.transcribe("2.wav", beam_size=5)

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))