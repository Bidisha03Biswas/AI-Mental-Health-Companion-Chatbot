#Step1: Setup Ollama with Medgemma tool
import re
import ollama


def force_human_response(text: str) -> str:
    """
    Transform AI response into short, natural, conversational text.
    Keeps only 2-3 sentences max.
    """
    # Remove HTML, markdown, bullet points, numbering
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"\*\*.*?\*\*", "", text)  # Remove bold
    text = re.sub(r"[|•\-–—✔️☐]", "", text)
    text = re.sub(r"^\d+\.\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^[*-]\s*", "", text, flags=re.MULTILINE)
    
    # Remove common section headers
    text = re.sub(r"(Why it helps|How to do it|Ideas|Options|Examples|Try):?\s*", "", text, flags=re.IGNORECASE)
    
    # Clean up extra whitespace
    text = re.sub(r"\n\s*\n+", "\n", text)
    text = text.strip()
    
    # Split into sentences (better regex)
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
    
    # Keep only 2-3 short, impactful sentences
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
    sentences = sentences[:3]
    
    # Join naturally with space
    return " ".join(sentences)


def query_medgemma(prompt: str) -> str:
    """
    Call MedGemma and return a warm, human-like, encouraging response.
    """
    system_prompt = """You are Dr. Emily Hartman, a warm therapist.

Speak in 2-3 short sentences only. Be conversational and caring.

Rules:
- Maximum 40 words total
- NO lists, bullets, or steps
- NO clinical jargon
- Sound like a caring friend, not a textbook
- ONE simple idea or gentle question

Example: "I hear you. Sometimes a short walk or just stepping outside for a minute can shift things. What sounds doable right now?"
"""
    
    try:
        response = ollama.chat(
            model="alibayram/medgemma:4b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            options={
                "num_predict": 60,  # Much shorter limit
                "temperature": 0.7,
                "top_p": 0.85,
                "frequency_penalty": 0.3,
            }
        )
        
        raw_response = response["message"]["content"]
        return force_human_response(raw_response)
    
    except Exception as e:
        # Fallback responses that feel genuine
        fallbacks = [
            "I'm here with you. What's feeling hardest right now?",
            "I hear you. Sometimes just naming what we're feeling can help. What's weighing on you most?",
            "That sounds really tough. I'm here to listen—what would help you feel even a little bit better right now?"
        ]
        return fallbacks[0]
#print(query_medgemma(prompt="What is your name?"))


#Step2: Setup Twilio calling API tool
from twilio.rest import Client
from backend.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, EMERGENCY_CONTACT

def call_emergency(phone: str | None = None):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    call = client.calls.create(
        to=EMERGENCY_CONTACT,
        from_=TWILIO_FROM_NUMBER,
        url="http://demo.twilio.com/docs/voice.xml"
    )
    return "Emergency call has been placed."


#Step3: Setup location tool
