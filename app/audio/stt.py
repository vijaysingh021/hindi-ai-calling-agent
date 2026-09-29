from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu", compute_type="int8")

def transcribe_audio(audio_file_path):
    print(f"[Log] ऑडियो सुना जा रहा है: {audio_file_path} ...")
    
    # initial_prompt मॉडल को इशारा देता है कि आउटपुट इसी लिपि (देवनागरी) में देना है
    segments, info = model.transcribe(
        audio_file_path, 
        beam_size=5, 
        language="hi",
        initial_prompt="नमस्ते, मैं एक हिंदी सहायक हूँ।",
        condition_on_previous_text=False
    )
    
    text = ""
    for segment in segments:
        text += segment.text + " "
        
    return text.strip()

if __name__ == "__main__":
    result = transcribe_audio("test_output.mp3")
    print(f"\n[Result] ऑडियो से निकला टेक्स्ट: {result}")