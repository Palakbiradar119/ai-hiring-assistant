import pdfplumber
import io

def extract_text_from_pdf(pdf_file):
    """
    Extracts text from an uploaded PDF file.
    Handles Streamlit UploadedFile objects.
    """
    try:
        # If it's bytes, wrap in BytesIO
        if isinstance(pdf_file, bytes):
            pdf_file = io.BytesIO(pdf_file)

        # If it's a Streamlit UploadedFile or any file-like object
        elif hasattr(pdf_file, 'read'):
            content = pdf_file.read()
            pdf_file = io.BytesIO(content)

        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        if not text.strip():
            return "Could not extract text from PDF"

        return text.strip()

    except Exception as e:
        return f"Error reading PDF: {str(e)}"