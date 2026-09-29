import os
from groq import Groq
from dotenv import load_dotenv
from app.ai.prompts import SYSTEM_PROMPT

# .env file se API key load karna
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_response(conversation_history, customer_message):
    print(f"[Log] Customer: {customer_message}")
    print(f"[Log] AI soch raha hai...")
    
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": customer_message})

    try:
        # यहाँ आपकी लिस्ट का नया एक्टिव मॉडल सेट किया गया है
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="qwen/qwen3.8-27b", 
            temperature=0.5,
            max_tokens=150
        )
        reply = chat_completion.choices[0].message.content
        return reply
    except Exception as e:
        print(f"Error: {e}")
        return "माफ़ कीजिए, मुझे आपकी बात समझ नहीं आई।"

if __name__ == "__main__":
    test_reply = generate_response([], "हेलो, मुझे आपके सिस्टम के बारे में जानना है।")
    print(f"[Log] AI ka asli Jawab: {test_reply}")