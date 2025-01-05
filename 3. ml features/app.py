import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from pydub import AudioSegment
import speech_recognition as sr
from transformers import pipeline
from langdetect import detect
from googletrans import Translator
from fpdf import FPDF
import pytesseract

# Create output directory
def create_output_folder():
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder

# Step 1: Extract Audio and Generate Transcript
def extract_audio(video_path, output_audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(output_audio_path)

def generate_transcript(audio_path):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(audio_path)
    temp_wav = "temp.wav"
    audio.export(temp_wav, format="wav")
    
    with sr.AudioFile(temp_wav) as source:
        audio_data = recognizer.record(source)
        transcript = recognizer.recognize_google(audio_data)
    
    os.remove(temp_wav)
    return transcript

# Step 2: Summarize Transcript
def summarize_text(text):
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return summary[0]['summary_text']

# Step 3: Process PDF Content
def process_pdf_content(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as pdf_file:
        text = pytesseract.image_to_string(pdf_file)
    return text

# Step 4: Multilingual Support
def translate_text(text, target_languages):
    translations = {}
    for lang in target_languages:
        translations[lang] = translator.translate(text, dest=lang).text
    return translations

# Main Workflow
def process_inputs(video_path, pdf_path):
    output_folder = create_output_folder()

    audio_path = os.path.join(output_folder, "output_audio.mp3")
    transcript_path = os.path.join(output_folder, "transcript.txt")
    transcript_summary_path = os.path.join(output_folder, "transcript_summary.txt")
    whiteboard_text_path = os.path.join(output_folder, "whiteboard_text.txt")
    whiteboard_summary_path = os.path.join(output_folder, "whiteboard_summary.txt")
    translations_path = os.path.join(output_folder, "translations.txt")

    print("Extracting audio...")
    extract_audio(video_path, audio_path)
    print("Generating transcript...")
    transcript = generate_transcript(audio_path)
    with open(transcript_path, 'w') as file:
        file.write(transcript)

    print("Summarizing transcript...")
    transcript_summary = summarize_text(transcript)
    with open(transcript_summary_path, 'w') as file:
        file.write(transcript_summary)

    print("Processing PDF content...")
    whiteboard_text = process_pdf_content(pdf_path)
    whiteboard_summary = summarize_text(whiteboard_text)
    with open(whiteboard_text_path, 'w') as file:
        file.write(whiteboard_text)
    with open(whiteboard_summary_path, 'w') as file:
        file.write(whiteboard_summary)

    print("Detecting language and translating...")
    original_language = detect(transcript)
    if original_language != "en":
        transcript = translator.translate(transcript, dest="en").text

    target_languages = ["hi", "mr", "gu"]
    translations = {
        "transcript": translate_text(transcript, target_languages),
        "summary": translate_text(transcript_summary, target_languages),
        "whiteboard": translate_text(whiteboard_summary, target_languages),
    }

    with open(translations_path, 'w') as file:
        for key, lang_translations in translations.items():
            file.write(f"\n=== {key.upper()} TRANSLATIONS ===\n")
            for lang, text in lang_translations.items():
                file.write(f"\nLanguage: {lang}\n{text}\n")

    print("Processing complete. Results saved to output folder.")

if __name__ == "__main__":
    print("Loading summarizer...")
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    translator = Translator()

    video_file = "input_video.mp4"  # Replace with your video file path
    pdf_file = "whiteboard.pdf"  # Replace with your PDF file path
    process_inputs(video_file, pdf_file)
