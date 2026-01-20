import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()

def test_connection():
    keys_str = os.getenv("GOOGLE_API_KEYS", "")
    single_key = os.getenv("GOOGLE_API_KEY", "")
    
    keys = []
    if keys_str:
        keys.extend([k.strip() for k in keys_str.split(",") if k.strip()])
    if single_key and single_key not in keys:
        keys.append(single_key)
        
    print(f"Found {len(keys)} API Keys.")
    
    log_file = open("ai_debug.log", "w", encoding="utf-8")
    
    if not keys:
        msg = "❌ No API Keys found in environment!"
        print(msg)
        log_file.write(msg + "\n")
        return

    models = ["gemini-3-flash", "gemini-2.5-flash"]
    
    for key in keys:
        masked_key = key[:5] + "..." + key[-3:]
        print(f"Testing Key: {masked_key}")
        log_file.write(f"\nTesting Key: {masked_key}\n")
        
        for model_name in models:
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel(model_name)
                print(f"  Requesting {model_name}...")
                response = model.generate_content("Hello, can you hear me?", stream=False)
                
                if response and response.text:
                    msg = f"  ✅ Success with {model_name}: {response.text[:20]}..."
                    print(msg)
                    log_file.write(msg + "\n")
                    # If one works, we are good, but let's test others to see full picture
            except Exception as e:
                msg = f"  ❌ Failed with {model_name}: {str(e)}"
                print(msg)
                log_file.write(msg + "\n")
                
    log_file.close()
    print("Test complete. Check ai_debug.log")

if __name__ == "__main__":
    test_connection()
