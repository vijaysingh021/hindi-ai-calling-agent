import time
import asyncio
import edge_tts
from app.sheets.google_sheet import get_leads, update_lead
from app.ai.agent import generate_response
from app.audio.stt import transcribe_audio
from app.audio.tts import speak

# Codespace में माइक नहीं होता, इसलिए हम आपकी टाइपिंग को ऑडियो में बदलकर STT को टेस्ट करेंगे
def simulate_customer_audio(text, filename="customer_voice.mp3"):
    async def _gen():
        comm = edge_tts.Communicate(text, "hi-IN-MadhurNeural") # ग्राहक के लिए लड़के की आवाज़
        await comm.save(filename)
    asyncio.run(_gen())
    return filename

def run_campaign():
    leads = get_leads()
    print(f"\n[System] Total {len(leads)} leads मिली हैं।\n")

    for lead in leads:
        if lead.get('Status') == 'Pending':
            lead_id = lead.get('ID')
            name = lead.get('Name')
            phone = lead.get('Phone')
            
            print("="*50)
            print(f"📞 [State: CALLING] {name} ({phone})")
            time.sleep(1) 
            print(f"🟢 [State: CONNECTED]")
            
            conversation_history = []
            
            # 1. AI Introduction
            print("\n[State: SPEAKING - AI Introduction]")
            intro = f"नमस्ते {name} जी, मैं एक AI assistant हूँ। क्या मेरी बात आपसे हो सकती है?"
            speak(intro, "ai_intro.mp3")
            conversation_history.append({"role": "assistant", "content": intro})
            
            # 2. Customer Speaks (आप टर्मिनल में टाइप करेंगे)
            print("\n[State: LISTENING - Customer]")
            user_input = input("🗣️ आप (Customer) क्या कहना चाहेंगे? (यहाँ टाइप करें): ")
            
            # आपकी टाइपिंग को ऑडियो में बदला जा रहा है ताकि STT सुन सके
            cust_audio_file = simulate_customer_audio(user_input, "customer_voice.mp3")
            customer_text = transcribe_audio(cust_audio_file)
            print(f"📝 STT ने सुना: {customer_text}")
            
            # 3. AI Brain
            print("\n[State: THINKING - AI Brain]")
            ai_reply = generate_response(conversation_history, customer_text)
            
            # 4. AI Speaks
            print("\n[State: SPEAKING - AI Reply]")
            speak(ai_reply, "ai_reply.mp3")
            
            print(f"\n🔴 [State: COMPLETED] Call disconnected with {name}.")
            
            # 5. Database Update
            print("\n[State: UPDATING DATABASE]")
            update_lead(lead_id, "Completed", "Interested")
            
            print("="*50 + "\n")
            
            # अभी के लिए सिर्फ 1 कॉल टेस्ट करेंगे
            break 

if __name__ == "__main__":
    print("🚀 Starting REAL AI Calling Campaign...")
    run_campaign()