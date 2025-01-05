import whisper
from pydub import AudioSegment
from pydub.utils import make_chunks
from googletrans import Translator
import os

def convert_mp4_to_mp3(mp4_path, mp3_path):
    """
    Convert an MP4 file to MP3 format.
    """
    print(f"Converting {mp4_path} to {mp3_path}...")
    audio = AudioSegment.from_file(mp4_path, format="mp4")
    audio.export(mp3_path, format="mp3")
    print("Conversion complete.")

def transcribe_long_audio(file_path, chunk_length_seconds=30):
    """
    Transcribe long audio files by splitting them into smaller chunks.
    """
    # Load the Whisper model
    model = whisper.load_model("base")  # Use "base", "small", "medium", or "large"

    # Load the audio file
    audio = AudioSegment.from_file(file_path)
    
    # Convert chunk length to milliseconds
    chunk_length_ms = chunk_length_seconds * 1000

    # Split the audio into chunks
    chunks = make_chunks(audio, chunk_length_ms)

    # Directory to store chunks
    chunk_dir = "audio_chunks"
    os.makedirs(chunk_dir, exist_ok=True)

    # Transcribe each chunk and combine results
    transcripts = []
    for i, chunk in enumerate(chunks):
        chunk_name = os.path.join(chunk_dir, f"chunk_{i}.mp3")
        chunk.export(chunk_name, format="mp3")
        
        print(f"Transcribing chunk {i+1}/{len(chunks)}: {chunk_name}")
        result = model.transcribe(chunk_name)
        transcripts.append(result["text"])
    
    # Combine all transcripts into one
    full_transcript = " ".join(transcripts)

    # Clean up chunk files
    for chunk_file in os.listdir(chunk_dir):
        os.remove(os.path.join(chunk_dir, chunk_file))
    os.rmdir(chunk_dir)

    return full_transcript

def translate_transcript(transcript, languages):
    """
    Translate the transcript into the specified languages.
    """
    translator = Translator()
    translations = {}
    for language in languages:
        print(f"Translating into {language}...")
        translation = translator.translate(transcript, dest=language).text
        translations[language] = translation
    return translations

# Main function to run
if __name__ == "__main__":
    input_file = "path_to_your_video_file.mp4"  # Replace with your MP4 file path
    mp3_file = "converted_audio.mp3"

    # Step 1: Convert MP4 to MP3
    convert_mp4_to_mp3(input_file, mp3_file)

    # Step 2: Transcribe the MP3 file
    transcript = transcribe_long_audio(mp3_file, chunk_length_seconds=30)

    # Step 3: Clean up the converted MP3 file
    if os.path.exists(mp3_file):
        os.remove(mp3_file)

    # Step 4: Translate the transcript into Hindi, Marathi, and Gujarati
    languages = {"hi": "Hindi", "mr": "Marathi", "gu": "Gujarati"}
    translations = translate_transcript(transcript, languages.keys())

    # Print the full transcript and translations
    print("\n=== Full Transcript ===\n")
    print(transcript)

    print("\n=== Translations ===\n")
    for lang_code, translation in translations.items():
        print(f"{languages[lang_code]} Translation:\n{translation}\n")
