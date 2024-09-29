import re
import nltk
import contractions

# Vérifie si le tokenizer punkt est déjà téléchargé


nltk.download('punkt', quiet=True)
nltk.download('punkt_tab')
def clean_scientific_text(text, max_words=2000):
    # 1. Conversion du texte en minuscules
    text = text.lower()
    # 2. Suppression des balises HTML
    text = re.sub(r'<.*?>', '', text) 
    # 3. Suppression des citations scientifiques (ex: [1], (Doe et al., 2020), etc.)
    text = re.sub(r'\[\d+\]', '', text)  # Suppression des références de type [1]
    text = re.sub(r'\([^()]*\d{4}[^()]*\)', '', text)
    text = re.sub(r'\b\w+ et al\., \d{4}\b', '', text)
    text = re.sub(r'\b\d+\s*([kK]|[mM])?\b', '', text) 
    text = re.sub(r'\(.*?\d{4}.*?\)', '', text)  # Suppression des références de type (Doe et al., 2020)
    # 4. Suppression des caractères non désirés, y compris les underscores (_)
    text = re.sub(r'[^a-zA-Z0-9\s.,]', '', text)  # On garde seulement les caractères alphanumériques et ponctuation
    text = re.sub(r'_', '', text)  # Suppression des underscores   
    # 5. Suppression des espaces multiples
    text = re.sub(r'\s+', ' ', text).strip()  # Remplace les espaces multiples par un seul espace et enlève les espaces en début et fin
    # 6. Normalisation de certains caractères spéciaux ou abréviations communes (ex: &, %, $)
    text = text.replace('&', 'and')  # Exemple de remplacement
    # 7. Gestion des contractions
    text = contractions.fix(text)
    text = re.sub(r'\b(?!(a|e|i|o|u|à|è|ì|ò|ù|â|ê|î|ô|û|ä|ë|ï|ö|ü))\w\b', '', text)
    # 7. Limitation à un nombre maximum de mots (ex: 2000 mots)
    words = nltk.word_tokenize(text)
    if len(words) > max_words:
        words = words[:max_words]
    # 8. Reconstitution du texte à partir des mots sélectionnés
    cleaned_text = ' '.join(words)
    
    return cleaned_text