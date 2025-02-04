import os
import numpy as np
import soundfile as sf
import sounddevice as sd
from fpdf import FPDF
from googletrans import Translator
import speech_recognition as sr
import subprocess

def find_mp4(folder_path):
    """
    Find all MP4 files in the specified folder and its subfolders.
    """
    mp4_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".mp4"):
                mp4_files.append(os.path.join(root, file))


    return mp4_files[0]

def convert_mp4_to_mp3(mp4_path, mp3_path):
    """
    Convert an MP4 file to MP3 format.
    """
    print(f"Converting {mp4_path} to {mp3_path}...")

    # Use ffmpeg to extract audio from the MP4 file and save it as a temporary WAV file
    wav_temp_path = mp4_path.replace(".mp4", "_temp.wav")
    subprocess.run(["ffmpeg", "-i", mp4_path, "-vn", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2", wav_temp_path])

    # Read the temporary WAV file using soundfile
    data, samplerate = sf.read(wav_temp_path)

    # Export the audio data to an MP3 file (using soundfile)
    sf.write(mp3_path, data, samplerate, format='mp3')

    # Clean up the temporary WAV file
    os.remove(wav_temp_path)

    print("Conversion complete.")

def transcribe_audio(file_path, chunk_length_seconds=30):
    """
    Split a long audio file into smaller chunks, then transcribe each chunk using SpeechRecognition.
    """
    # Load the audio file
    data, samplerate = sf.read(file_path)
    total_duration_seconds = len(data) / samplerate

    # Split the audio into chunks
    chunk_samples = int(chunk_length_seconds * samplerate)
    num_chunks = int(np.ceil(len(data) / chunk_samples))

    # Directory to store chunks
    chunk_dir = "audio_chunks"
    os.makedirs(chunk_dir, exist_ok=True)

    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Transcribe each chunk and combine results
    transcripts = []
    for i in range(num_chunks):
        start_sample = i * chunk_samples
        end_sample = min(start_sample + chunk_samples, len(data))

        chunk_data = data[start_sample:end_sample]
        chunk_name = os.path.join(chunk_dir, f"chunk_{i}.wav")
        
        # Save chunk to a file
        sf.write(chunk_name, chunk_data, samplerate)
        print(f"Processing chunk {i+1}/{num_chunks}: {chunk_name}")

        # Transcribe chunk
        try:
            with sr.AudioFile(chunk_name) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio)  # Using Google Speech-to-Text
                transcripts.append(text)
                print(f"Chunk {i+1} transcription: {text}")
        except sr.UnknownValueError:
            print(f"Chunk {i+1} could not be transcribed.")
        except sr.RequestError as e:
            print(f"Speech recognition service error: {e}")

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
    for lang_code in languages:
        print(f"Translating into {languages[lang_code]}...")
        translation = translator.translate(transcript, dest=lang_code).text
        translations[lang_code] = translation
    return translations

def save_to_pdf(filename, content, font_path="NotoSans-Regular.ttf"):
    """
    Save the given content to a PDF file.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.add_font('CustomFont', '', font_path, uni=True)  # Ensure proper rendering of UTF-8 text
    pdf.set_font("CustomFont", size=12)

    # Split content into lines to prevent text from overflowing the page
    lines = content.split("\n")
    for line in lines:
        pdf.multi_cell(0, 10, line)

    pdf.output(filename)
    print(f"Saved to {filename}")

# Main function to run
if __name__ == "__main__":
    input_file =find_mp4("/home/muhd/Ai-Board-YIC/3. ml features/2. Video To Transcript with Trl/old nonsense")  # Replace with your MP4 file path
    base_filename = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = os.path.join(os.getcwd(), base_filename)
    os.makedirs(output_dir, exist_ok=True)

    mp3_file = os.path.join(output_dir, "converted_audio.mp3")

    # Step 1: Convert MP4 to MP3
    convert_mp4_to_mp3(input_file, mp3_file)

    # Step 2: Transcribe the MP3 file
    transcript = transcribe_audio(mp3_file, chunk_length_seconds=30)

    # Step 3: Save the English transcript
    eng_file = os.path.join(output_dir, f"{base_filename}-eng.pdf")
    save_to_pdf(eng_file, transcript)

    # Step 4: Translate the transcript into multiple languages
    languages = {
        'hi': 'Hindi',
        'mr': 'Marathi',
        'gu': 'Gujarati',
        'bn': 'Bengali',
        'te': 'Telugu',
        'ta': 'Tamil',
        'ur': 'Urdu',
        'kn': 'Kannada',
        'ml': 'Malayalam',
        'pa': 'Punjabi',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'ja': 'Japanese',
        'zh-cn': 'Chinese (Simplified)',
        'ar': 'Arabic'
    }

    # Map fonts for specific languages
    font_map = {
        'hi': "NotoSansDevanagari-Regular.ttf",
        'mr': "NotoSansDevanagari-Regular.ttf",
        'gu': "NotoSansGujarati-Regular.ttf",
        'bn': "NotoSansBengali-Regular.ttf",
        'te': "NotoSansTelugu-Regular.ttf",
        'ta': "NotoSansTamil-Regular.ttf",
        'ur': "NotoSansArabic-Regular.ttf",
        'kn': "NotoSansKannada-Regular.ttf",
        'ml': "NotoSansMalayalam-Regular.ttf",
        'pa': "NotoSansGurmukhi-Regular.ttf",
        'ja': "NotoSansJP-Regular.ttf",
        'zh-cn': "NotoSansSC-Regular.ttf",
        'ar': "NotoSansArabic-Regular.ttf"
    }

    translations = translate_transcript(transcript, languages)

    # Step 5: Save translations
    for lang_code, translation in translations.items():
        lang_name = languages[lang_code].lower()
        font_path = font_map.get(lang_code, "NotoSans-Regular.ttf")  # Default font
        translation_file = os.path.join(output_dir, f"{base_filename}-{lang_name}.pdf")
        save_to_pdf(translation_file, translation, font_path=font_path)

    # Step 6: Clean up the converted MP3 file
    if os.path.exists(mp3_file):
        os.remove(mp3_file)
