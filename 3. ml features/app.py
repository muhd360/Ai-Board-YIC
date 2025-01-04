import os
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import speech_recognition as sr
from transformers import pipeline
from langdetect import detect
from googletrans import Translator
from fpdf import FPDF
import pytesseract

# Initialize LLM and Translator
summarizer = pipeline("summarization")
translator = Translator()

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

# Step 3: Process PDF Content (Whiteboard Content)
def process_pdf_content(pdf_path):
    text = ""
    images = pytesseract.image_to_pdf_or_hocr(pdf_path, extension='pdf')
    for page_text in pytesseract.image_to_string(pdf_path, extension='pdf').split('\n\n'):
        text += page_text
    return text

# Step 4: Multilingual Support
def translate_text(text, target_languages):
    translations = {}
    for lang in target_languages:
        translations[lang] = translator.translate(text, dest=lang).text
    return translations

# Main Workflow
def process_inputs(video_path, pdf_path):
    # Define output paths
    audio_path = "output_audio.mp3"

    # Step 1: Extract audio and transcript
    print("Extracting audio...")
    extract_audio(video_path, audio_path)
    print("Generating transcript...")
    transcript = generate_transcript(audio_path)

    # Step 2: Summarize transcript
    print("Summarizing transcript...")
    transcript_summary = summarize_text(transcript)

    # Step 3: Process PDF content
    print("Processing whiteboard content from PDF...")
    whiteboard_text = process_pdf_content(pdf_path)
    whiteboard_summary = summarize_text(whiteboard_text)

    # Step 4: Detect language and translate
    print("Detecting language...")
    original_language = detect(transcript)
    translations = {}

    if original_language != "en":
        print(f"Translating transcript from {original_language} to English...")
        transcript = translator.translate(transcript, dest="en").text

    print("Translating content to multiple languages...")
    target_languages = ["hi", "mr", "gu"]  # Hindi, Marathi, Gujarati
    translations['transcript'] = translate_text(transcript, target_languages)
    translations['summary'] = translate_text(transcript_summary, target_languages)
    translations['whiteboard'] = translate_text(whiteboard_summary, target_languages)

    # Output results
    print("Processing complete.")
    return {
        "transcript": transcript,
        "transcript_summary": transcript_summary,
        "whiteboard_text": whiteboard_text,
        "whiteboard_summary": whiteboard_summary,
        "translations": translations
    }

# Example Usage
if __name__ == "__main__":
    video_file = "input_video.mp4"  # Replace with your video file path
    pdf_file = "whiteboard.pdf"  # Replace with your PDF file path
    results = process_inputs(video_file, pdf_file)

    print("Transcript:", results["transcript"])
    print("Transcript Summary:", results["transcript_summary"])
    print("Whiteboard Content:", results["whiteboard_text"])
    print("Whiteboard Summary:", results["whiteboard_summary"])
    print("Translations:", results["translations"])


#pip install moviepy pydub speechrecognition transformers langdetect googletrans==4.0.0-rc1 fpdf pytesseract
#use the aboce command to install all the dependencies