import os
import whisper

def transcribe_video_to_text(video_path):
    """Converts a video file to a high-quality word-to-word transcript using Whisper."""
    # Load the Whisper model (use 'base', 'medium', or 'large' for better accuracy)
    print("Loading Whisper model...")
    model = whisper.load_model("large")

    # Transcribe the video file directly with timestamps enabled for long-form transcription
    print(f"Transcribing video: {video_path}")
    result = model.transcribe(video_path, return_timestamps=True)

    # Extract the transcription text
    transcript = result["text"]
    print("Transcription complete.")

    # Save the transcript to a file
    transcript_file = os.path.splitext(video_path)[0] + "_transcript.txt"
    with open(transcript_file, "w", encoding="utf-8") as f:
        f.write(transcript)

    print(f"Transcript saved to: {transcript_file}")
    return transcript

if __name__ == "__main__":
    # Specify the video file name directly in the code
    video_path = "example_video.mp4"  # Replace with your video file name

    if not os.path.exists(video_path):
        print("Error: Video file does not exist.")
    else:
        # Generate transcript
        transcript = transcribe_video_to_text(video_path)
