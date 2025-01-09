import asyncio
import soundfile as sf
import numpy as np
import os
import speech_recognition as sr

async def transcribe_chunk(chunk_name, recognizer, index):
    """Asynchronously transcribe a single audio chunk."""
    try:
        with sr.AudioFile(chunk_name) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            return index, text
    except sr.UnknownValueError:
        return index, ""
    except sr.RequestError as e:
        print(f"Speech recognition service error for chunk {index}: {e}")
        return index, ""

async def transcribe_audio_async(file_path, chunk_length_seconds=30):
    """Asynchronously transcribe an audio file."""
    # Load the audio file
    data, samplerate = sf.read(file_path)
    total_duration_seconds = len(data) / samplerate

    # Split the audio into chunks
    chunk_samples = int(chunk_length_seconds * samplerate)
    num_chunks = int(np.ceil(len(data) / chunk_samples))

    # Directory to store chunks
    chunk_dir = "audio_chunks"
    os.makedirs(chunk_dir, exist_ok=True)

    # Save chunks to files
    chunk_names = []
    for i in range(num_chunks):
        start_sample = i * chunk_samples
        end_sample = min(start_sample + chunk_samples, len(data))
        chunk_data = data[start_sample:end_sample]
        chunk_name = os.path.join(chunk_dir, f"chunk_{i}.wav")
        sf.write(chunk_name, chunk_data, samplerate)
        chunk_names.append((chunk_name, i))

    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Transcribe chunks asynchronously
    tasks = [transcribe_chunk(chunk_name, recognizer, index) for chunk_name, index in chunk_names]
    results = await asyncio.gather(*tasks)

    # Combine results in the correct order
    results.sort(key=lambda x: x[0])  # Sort by index
    full_transcript = " ".join(text for _, text in results)

    # Clean up chunk files
    for chunk_file in os.listdir(chunk_dir):
        os.remove(os.path.join(chunk_dir, chunk_file))
    os.rmdir(chunk_dir)

    print(full_transcript)

    return full_transcript

# To run the async function
# transcript = asyncio.run(transcribe_audio_async("path_to_audio_file.wav"))
if __name__ =="__main__":
    asyncio.run(transcribe_audio_async("/home/muhd/Ai-Board-YIC/3. ml features/updated-VTP/one year of studying (it was a mistake)/converted_audio.mp3"))
