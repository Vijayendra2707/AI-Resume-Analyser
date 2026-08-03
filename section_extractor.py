import re

def extract_relevant_section(text):
    text_lower = text.lower()

    patterns = [
        r"(skills[\s\S]{0,600})",
        r"(technical skills[\s\S]{0,600})",
        r"(technologies[\s\S]{0,600})",
        r"(tools[\s\S]{0,600})",
        r"(requirements[\s\S]{0,600})",
        r"(qualifications[\s\S]{0,600})",
        r"(responsibilities[\s\S]{0,600})"
    ]

    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            return match.group(0)

    # fallback
    return text[:600]