import json
import os
from dotenv import load_dotenv
from groq import Groq
from resume_parser import extract_text
from preprocess import preprocess_text

load_dotenv()  # loads .env file
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)
def extract_skills_llm(text):
    prompt = f"""
    ROLE: Technical Recruiter & NLP Expert.
    TASK: Extract and categorize technical skills from the text.
    
    FORMAT: Return ONLY a valid JSON object with these keys STRICTLY:
    - "technical_skills": Programming languages, frameworks, libraries.
    - "tools": Software, platforms, hardware, IDEs.
    - "concepts": Theoretical knowledge, domains, methodologies.
    - If Skill is HTML5 then write html etc  
    - No words or things should be repeated in all 3 keys , i.e , only present in 1 key ONLY.

    RULES:
    - Values must be lists of lowercase strings.
    - Ignore soft skills.
    
    TEXT: {text}
    """
    
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.1, # Lower temperature for stricter formatting
            response_format={"type": "json_object"} # Force JSON mode
        )
        
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Extraction Error: {e}")
        return {"technical_skills": [], "tools": [], "concepts": []}