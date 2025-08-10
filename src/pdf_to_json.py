import json
import PyPDF2
import re
from typing import List, Dict

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text content from PDF file
    """
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def parse_email_content(text: str) -> List[Dict[str, str]]:
    """
    Parse extracted text and convert to email dataset format
    """
    emails = []
    
    # Split text into potential email sections
    # This is a basic parser - you may need to adjust based on your PDF structure
    sections = re.split(r'\n\s*\n', text)
    
    for i, section in enumerate(sections):
        if len(section.strip()) < 20:  # Skip very short sections
            continue
            
        # Try to identify subject and body
        lines = section.strip().split('\n')
        
        # Basic heuristics for email structure
        subject = ""
        body = ""
        
        if len(lines) > 0:
            # First line might be subject
            first_line = lines[0].strip()
            if len(first_line) < 100:  # Likely a subject
                subject = first_line
                body = '\n'.join(lines[1:]).strip()
            else:
                # Treat entire section as body
                subject = f"Email {i+1}"
                body = section.strip()
        
        # Clean up text
        subject = re.sub(r'\s+', ' ', subject).strip()
        body = re.sub(r'\s+', ' ', body).strip()
        
        if body:  # Only add if there's actual content
            # Determine category and tone based on content
            category = determine_category(subject + " " + body)
            tone = determine_tone(subject + " " + body)
            
            emails.append({
                "subject": subject,
                "body": body,
                "category": category,
                "tone": tone
            })
    
    return emails

def determine_category(text: str) -> str:
    """
    Determine email category based on content
    """
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['meeting', 'schedule', 'appointment', 'calendar']):
        return 'meeting'
    elif any(word in text_lower for word in ['thank', 'appreciate', 'grateful']):
        return 'thank_you'
    elif any(word in text_lower for word in ['business', 'proposal', 'contract', 'deal']):
        return 'business'
    elif any(word in text_lower for word in ['support', 'help', 'issue', 'problem']):
        return 'customer_service'
    elif any(word in text_lower for word in ['network', 'connect', 'introduction']):
        return 'networking'
    else:
        return 'general'

def determine_tone(text: str) -> str:
    """
    Determine email tone based on content
    """
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['urgent', 'asap', 'immediately', 'emergency']):
        return 'urgent'
    elif any(word in text_lower for word in ['sorry', 'apologize', 'mistake', 'error']):
        return 'apologetic'
    elif any(word in text_lower for word in ['hi', 'hello', 'hope', 'best']):
        return 'friendly'
    elif any(word in text_lower for word in ['dear', 'sincerely', 'respectfully']):
        return 'formal'
    else:
        return 'neutral'

def main():
    pdf_path = "Untitled document.pdf"
    json_path = "finetune_dataset.json"
    
    print("Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)
    
    if not text:
        print("Failed to extract text from PDF")
        return
    
    print(f"Extracted {len(text)} characters from PDF")
    
    print("Parsing email content...")
    emails = parse_email_content(text)
    
    print(f"Found {len(emails)} email entries")
    
    # Save to JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(emails, f, indent=2, ensure_ascii=False)
    
    print(f"Saved dataset to {json_path}")
    
    # Display first few entries
    print("\nFirst 3 entries:")
    for i, email in enumerate(emails[:3]):
        print(f"\nEmail {i+1}:")
        print(f"Subject: {email['subject'][:50]}...")
        print(f"Body: {email['body'][:100]}...")
        print(f"Category: {email['category']}")
        print(f"Tone: {email['tone']}")

if __name__ == "__main__":
    main()