import pandas as pd
import subprocess
import os
import time

def load_leads():
    lead_file = 'leads.csv'
    if not os.path.exists(lead_file):
        print(f"[-] त्रुटि: {lead_file} नहीं मिली!")
        return None
    
    df = pd.read_csv(lead_file)
    print(f"[+] कुल {len(df)} लीड्स सफलतापूर्वक लोड हो गई हैं।")
    return df

def trigger_call_to_lead(phone, name="Customer"):
    print(f"\n[*] कॉलिंग शुरू: {name} (एक्सटेंशन/नंबर: {phone})...")
    
    # Asterisk के जरिए कॉल ट्रिगर करना (हम फिक्स की गई ऑडियो फाइल का इस्तेमाल कर रहे हैं)
    cmd = f'sudo asterisk -rx "channel originate PJSIP/1001 application Playback customer_voice_fixed"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"[+] {name} को कॉल सफलतापूर्वक भेज दी गई है!")
    else:
        print(f"[-] कॉल भेजने में विफल: {result.stderr}")

def start_campaign():
    df = load_leads()
    if df is None or df.empty:
        print("[-] कॉलिंग के लिए कोई लीड उपलब्ध नहीं है।")
        return

    print("\n🚀 AI कॉलिंग कैंपेन शुरू हो रहा है...")
    print("----------------------------------------")
    
    # यहाँ हम सुरक्षा के लिए पहली कुछ लीड्स पर टेस्ट लूप चला सकते हैं
    # (आप चाहें तो range(len(df)) करके सभी 110 लीड्स पर चला सकते हैं)
    for index, row in df.iterrows():
        # मान लेते हैं कि CSV में 'phone' और 'name' नाम के कॉलम हैं 
        # (अगर कॉलम के नाम अलग हों, तो आप इन्हें बदल सकते हैं)
        phone = str(row.get('phone', '1001'))
        name = str(row.get('name', f'Lead_{index+1}'))
        
        trigger_call_to_lead(phone, name)
        
        # अगली कॉल से पहले 5 सेकंड का इंतज़ार (ताकि कॉल ओवरलैप न हो)
        print("[*] अगली कॉल से पहले 5 सेकंड का विश्राम...")
        time.sleep(5)
        
        # डेमो के लिए फिलहाल हम पहली 3 लीड्स के बाद रोक रहे हैं, 
        # सभी 110 पर चलाने के लिए इस ब्रेक को हटा सकते हैं।
        if index >= 2:
            print("\n[!] डेमो कैंपेन पूरा हुआ (पहली 3 लीड्स टेस्ट की गईं)।")
            break

    print("----------------------------------------")
    print("[+] कैंपेन समाप्त।")

if __name__ == "__main__":
    start_campaign()
