from transformers import pipeline

# Load the Whisper large model
transcriber = pipeline(model="openai/whisper-large")

# Transcribe the audio file
result = transcriber("input_video.mp4")

# Extract and print the transcription
transcript = result["text"]
print("Transcription complete.")
print(transcript)

# Save the transcript to a file
transcript_file = "example_video_transcript.txt"
with open(transcript_file, "w", encoding="utf-8") as f:
    f.write(transcript)

print(f"Transcript saved to: {transcript_file}")
