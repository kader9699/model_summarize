import streamlit as st
import requests
import time

# Ton API token Hugging Face
API_TOKEN = "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"

# Paramètres de l'API Hugging Face
headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}
API_URL = "https://api-inference.huggingface.co/models/google/long-t5-tglobal-base"

# Fonction pour envoyer des requêtes à l'API Hugging Face
@st.cache_resource
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Fonction pour attendre que le modèle soit prêt
def wait_for_model():
    while True:
        result = query({"inputs": "test"})
        if "error" in result and "loading" in result["error"]:
            st.write("Le modèle est en cours de chargement, réessai dans 10 secondes...")
            time.sleep(10)
        else:
            return result

# Vérifier si le modèle est prêt
result = wait_for_model()

# Titre de l'application
st.title("Document Summarization")

# Choix entre écrire du texte ou soumettre un fichier
option = st.radio("Choisissez une option :", ('Écrire du texte', 'Soumettre un fichier'), horizontal=True)

# Option pour écrire du texte
if option == 'Écrire du texte':
    document = st.text_area("Écrivez votre texte ici:")
    st.subheader("Résumé")
    if st.button("Résumer"):
        if document.strip() != "":  # Vérifier si le texte n'est pas vide
            with st.spinner("Génération du résumé..."):
                # Utilisation du modèle de résumé
                final_result = query({"inputs": document, "parameters": {"min_length": 100, "max_length": 350}})
                st.success("Résumé généré avec succès !")
                st.write(final_result)
        else:
            st.warning("Veuillez écrire un texte avant de générer un résumé.")

# Option pour soumettre un fichier
elif option == 'Soumettre un fichier':
    uploaded_file = st.file_uploader("Choisissez un fichier texte", type=["txt"])
    if uploaded_file is not None:
        # Lecture du contenu du fichier
        document = uploaded_file.read().decode("utf-8")
        st.subheader("Résumé")
        if st.button("Résumer"):
            with st.spinner("Génération du résumé..."):
                # Utilisation du modèle de résumé
                final_result = query({"inputs": document, "parameters": {"min_length": 100, "max_length": 350}})
                st.success("Résumé généré avec succès !")
                st.write(final_result)

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
