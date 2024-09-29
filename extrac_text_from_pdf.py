import fitz  
import re

def extract_text_from_pdf(uploaded_file):
    # Ouvrir le fichier PDF
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    
    # Initialiser une variable pour stocker le texte
    full_text = ""

    # Lire chaque page du document PDF
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        full_text += page.get_text()

    pdf_document.close()
    
    # Expression régulière pour extraire le texte entre l'introduction et la conclusion
    # Amélioration des expressions régulières pour tenir compte des majuscules
    intro_pattern = r"(Introduction|introduction|INTRODUCTION|Introduction\s*[\.:]?)"
    conclusion_pattern = r"(Conclusion|conclusions|FIN|conclusion|fin\s*[\.:]?)"
    
    # Trouver l'index de début et de fin
    intro_match = re.search(intro_pattern, full_text)
    conclusion_match = re.search(conclusion_pattern, full_text)

    if intro_match and conclusion_match:
        # Extraire le texte entre l'introduction et la conclusion
        start_index = intro_match.end()
        end_index = conclusion_match.start()
        extracted_text = full_text[start_index:end_index].strip()
        return extracted_text
    else:
        return "Introduction ou conclusion non trouvée."
