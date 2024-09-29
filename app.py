import streamlit as st
# Use a pipeline as a high-level helper
from transformers import pipeline
import torch
from text_preprocessing import clean_scientific_text
from extrac_text_from_pdf import extract_text_from_pdf

# Fonction pour envoyer des requêtes à l'API Hugging Face
@st.cache_resource
def load_summarization_model():
    # Chargement du modèle Hugging Face
    return pipeline("summarization", model="kader99/led-base-16384-finetuned-arxiv")


pipe = load_summarization_model()
# Titre de l'application
st.title("Document Summarization")
# 8
final_result = "we propose a tuner , suitable for adaptive control and  adaptive filtering applications , that sets the second derivative of the parameter estimates rather than the first derivative as is done in the overwhelming majority of the literature . comparative stability and performance analyses are presented . "
#final_result = "for fixed integers and, we consider the admissible sequences of lattice paths in a colored square given in. each admissible sequence of paths can be associated with a partition of. we show that the number of self - conjugate admissible sequences of paths associated with is equal to the number of standard young tableaux of partitions of with height less than or equal to. we extend this result to include the non - conjugate admissible sequences of paths and show that the number of all such admissible sequences of paths is equal to the sum of squares of the number of standard young tableaux of partitions of with height less than or equal to."
# Choix entre écrire du texte ou soumettre un fichier
option = st.radio("Choisissez une option :", ('Écrire du texte', 'Soumettre un fichier'), horizontal=True)

# Option pour écrire du texte
if option == 'Écrire du texte':
    document = st.text_area("Écrivez votre texte ici:")
    clean_document = clean_scientific_text(document,2000)
    st.subheader("Résumé")
    if st.button("Résumer"):
        if document.strip() != "":  # Vérifier si le texte n'est pas vide
            with st.spinner("Génération du résumé..."):
                # Utilisation du modèle de résumé
                summary = pipe(clean_document, min_length=100, max_length=350)
                st.success("Résumé généré avec succès !")
                st.write(summary[0]['summary_text'])
        else:
            st.warning("Veuillez écrire un texte avant de générer un résumé.")

# Option pour soumettre un fichier
elif option == 'Soumettre un fichier':
    uploaded_file = st.file_uploader("Choisissez un fichier texte", type=["txt","pdf","docx"])
    if uploaded_file is not None:
        # Lecture du contenu du fichier
        document =  extract_text_from_pdf(uploaded_file)
        clean_document = clean_scientific_text(document,2000)
        #document = uploaded_file.read().decode("utf-8")
        st.subheader("Résumé")
        if st.button("Résumer"):
            with st.spinner("Génération du résumé..."):
                # Utilisation du modèle de résumé
                summary = pipe(clean_document, min_length=100, max_length=350)
                st.success("Résumé généré avec succès !")
                st.write(summary[0]['summary_text'])
                #st.write(clean_document)

# Ajouter un footer pour styliser la fin de la page
st.markdown("""
    <style>
    footer {visibility: hidden;}
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        text-align: center;
        padding: 10px;
        font-size: 12px;
        color: #333;
    }
    </style>
    <div class="footer">
        <p>Document Summarization App - Powered by Abdourahamane</p>
    </div>
""", unsafe_allow_html=True)
