import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Fonction pour charger le modèle et le tokenizer (mis en cache)
@st.cache_resource
def load_model():
    model_name = "google/long-t5-tglobal-base"
    #model_name = "model/"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

# Charger le modèle et le tokenizer une seule fois
tokenizer, model = load_model()

# Interface Streamlit
st.title("Résumé de Texte avec Long T5")

# Entrée du texte à résumer
input_text = st.text_area("Entrez votre texte ici :", height=300)

# Bouton pour lancer la génération du résumé
if st.button("Générer le résumé"):
    if input_text:
        # Préparer les données pour le modèle
        inputs = tokenizer(input_text, return_tensors="pt", max_length=2000, truncation=True)
        
        # Générer le résumé
        summary_ids = model.generate(inputs["input_ids"], max_length=300, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        
        # Afficher le résumé généré
        st.subheader("Résumé Généré :")
        st.write(summary)
    else:
        st.error("Veuillez entrer du texte à résumer.")

