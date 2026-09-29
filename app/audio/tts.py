import asyncio
import edge_tts

def speak(text, output_file="ai_voice.mp3"):
    print(f"[Log] AI बोल रहा है: {text}")
    
    async def _generate():
        # hi-IN-SwaraNeural एक बहुत ही नेचुरल हिंदी फीमेल आवाज़ है
        communicate = edge_tts.Communicate(text, "hi-IN-SwaraNeural")
        await communicate.save(output_file)
        
    asyncio.run(_generate())
    print(f"[Log] Audio सेव हो गई: {output_file}")
    return output_file

if __name__ == "__main__":
    test_text = "नमस्ते। मैं आपका AI सहायक हूँ। आप कैसे हैं?"
    speak(test_text, "test_output.mp3")