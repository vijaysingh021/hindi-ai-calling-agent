import subprocess
import time

def trigger_ai_call(extension="1001"):
    print(f"[*] AI कॉलिंग इंजन शुरू हो रहा है... एक्सटेंशन {extension} पर कॉल मिलाई जा रही है...")
    
    # Asterisk को कमांड भेजें कि वह PJSIP/1001 पर कॉल करे और 'hello-world' या ऑडियो चलाए
    cmd = f'sudo asterisk -rx "channel originate PJSIP/{extension} application Playback hello-world"'
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("[+] कॉल सफलतापूर्वक ट्रिगर हो गई है! कृपया अपना MizuDroid ऐप चेक करें।")
    else:
        print("[-] कॉल करने में समस्या आई:", result.stderr)

if __name__ == "__main__":
    trigger_ai_call()
