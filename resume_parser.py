import PyPDF2
import docx

def extract_text(file_path):
    text = ""
    
    if file_path.endswith(".pdf"):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
                
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text
    
    else:
        print("ERROR ,Please Enter the file type correctly !!!")
        return
            
    return text

# x=extract_text(r"C:\Users\ranev\Desktop\Vijayendra_Rane_Resume.docx")
# print(x)