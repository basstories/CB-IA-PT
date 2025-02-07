
import os
import sys
import subprocess
import spacy
import streamlit as st
import streamlit as st
import spacy
import requests
import pyttsx3
import threading
from transformers import pipeline
import xml.etree.ElementTree as ET
from rapidfuzz import process
from googletrans import Translator

# ⚠️ Configuration des clés API (Remplace ces valeurs par tes vraies clés)
NEWS_API_KEY = "f31f2e9fbd95493bb2333e92d1eaa1f0"

# Configuration des logs
st.set_page_config(page_title="Chatbot IA", layout="wide")

# Charger le modèle SpaCy une seule fois
@st.cache_resource
def load_nlp():
    try:
        # Tente de charger le modèle normalement
        return spacy.load("en_core_web_sm")
    except OSError:
        # Si le modèle n'est pas trouvé, on le télécharge dans un dossier local accessible
        st.info("Le modèle 'en_core_web_sm' n'est pas installé. Téléchargement dans un dossier local...")
        
        # Définir un dossier local pour les données SpaCy (vous avez les droits d'écriture ici)
        local_data_dir = os.path.join(os.getcwd(), "spacy_data")
        os.makedirs(local_data_dir, exist_ok=True)
        
        # Indiquer à SpaCy d'utiliser ce dossier pour stocker et rechercher les modèles
        os.environ["SPACY_DATA"] = local_data_dir
        
        # Télécharger le modèle via la commande intégrée de SpaCy
        spacy.cli.download("en_core_web_sm", False, "--user")
        
        # Charger à nouveau le modèle une fois téléchargé
        return spacy.load("en_core_web_sm")
    return spacy.load("en_core_web_sm")


nlp = load_nlp()

# Charger un modèle Hugging Face accessible sans restriction
@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model="facebook/blenderbot-400M-distill")

chatbot_model = load_model()
translator = Translator()

def generate_huggingface_response(user_input):
    response = chatbot_model(user_input, max_length=150, num_return_sequences=1, do_sample=True)
    return response[0]["generated_text"]

# Fonction de synthèse vocale avec choix de la voix
def speak(text, voice_gender="female"):
    def run():
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
        if voice_gender == "male":
            engine.setProperty("voice", voices[0].id)
        else:
            engine.setProperty("voice", voices[1].id)
        engine.say(text)
        engine.runAndWait()
    thread = threading.Thread(target=run)
    thread.start()

# Fonction pour récupérer les actualités générales
def fetch_news():
    url = f"https://newsapi.org/v2/top-headlines?category=technology&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        articles = response.json().get("articles", [])[:5]
        return "\n".join(f"{idx + 1}. {article['title']} - {article['source']['name']}" for idx, article in enumerate(articles)) or "Aucune actualité trouvée."
    except requests.RequestException as e:
        return "Erreur lors de la récupération des actualités."

# Fonction pour récupérer les dernières recherches en IA via ArXiv
def fetch_ai_research():
    url = "http://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=5"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.text
        root = ET.fromstring(data)
        papers = root.findall(".//{http://www.w3.org/2005/Atom}entry")

        if not papers:
            return "Aucune recherche récente sur l'IA trouvée."

        results = []
        for idx, paper in enumerate(papers):
            title = paper.find("{http://www.w3.org/2005/Atom}title").text
            link = paper.find("{http://www.w3.org/2005/Atom}id").text
            results.append(f"{idx + 1}. {title} - [Lien]({link})")

        return "\n".join(results)

    except requests.RequestException as e:
        return f"Erreur lors de la récupération des recherches IA : {e}"

# Définition des intentions
intents = {
    "greetings": ["hello", "hi", "hey", "good morning", "good evening"],
    "farewell": ["bye", "goodbye", "see you", "take care"],
    "question_ai": ["tell me about AI", "what is artificial intelligence", "explain machine learning"],
    "general_help": ["can you help me", "i need assistance", "how do i", "what should i do"],
    "question_news": ["tell me the news", "what's happening today", "latest news", "current events"]
}

# Réponses pré-enregistrées
responses = {
    "greetings": "Hi there! How can I assist you?",
    "farewell": "Goodbye! Have a great day!",
    "question_ai": "Artificial Intelligence involves training machines to simulate human intelligence.",
    "general_help": "I'm here to assist! What do you need help with?",
    "unknown": "I'm not sure how to respond to that. Could you rephrase?"
}

# Initialisation du contexte utilisateur et historique
st.session_state.setdefault("context", {"last_intent": None})
st.session_state.setdefault("history", [])
st.session_state.setdefault("loaded", False)

# Fonction de détection d'intention (avec tolérance aux fautes)
def detect_intent(user_input):
    user_input = user_input.lower().strip()
    best_match = None
    best_score = 0

    for intent, phrases in intents.items():
        result = process.extractOne(user_input, phrases)  # Récupère un tuple
        if result:
            match, score = result[:2]  # Ignorer les valeurs supplémentaires
            if score > best_score:
                best_match = intent
                best_score = score

    return best_match if best_score > 80 else st.session_state["context"].get("last_intent", "unknown")

# Traduction des réponses
def translate_text(text, target_language):
    try:
        translated = translator.translate(text, dest=target_language)
        return translated.text
    except Exception as e:
        return f"Erreur de traduction : {e}"

# Génération de réponse
def generate_response(user_input, mode):
    intent = detect_intent(user_input)
    if intent == "question_news":
        with st.spinner("Récupération des actualités..."):
            return fetch_news()
    elif mode == "IA (GPT)":
        return generate_huggingface_response(user_input)
    return responses.get(intent, "Sorry, I don't understand that.")

# Page de démarrage
if not st.session_state["loaded"]:
    st.markdown("# 🤖 Bienvenue dans votre Chatbot IA futuriste ! 🚀")
    st.markdown("### 💡 Voici ce que je peux faire :")
    st.markdown("- 📡 **Actualités IA** : Explore les dernières recherches.")
    st.markdown("- 🗣️ **Synthèse vocale** : Écoute mes réponses.")
    st.markdown("- 🤝 **Modes de réponse** : IA ou pré-enregistrées.")
    st.markdown("---")
    st.button("➡️ Commencer", on_click=lambda: st.session_state.update({"loaded": True}))
    st.stop()

# Interface utilisateur avec disposition améliorée
st.markdown("# 🤖 Chatbot IA")
st.markdown("### 💬 Bienvenue dans votre assistant conversationnel !")

col1, col2 = st.columns([2, 1])

with col1:
    user_input = st.chat_input("💬 Écrivez votre message...")
    if user_input:
        response_mode = st.session_state.get("response_mode", "Réponses pré-enregistrées")
        target_language = st.session_state.get("target_language", "fr")
        voice_gender = st.session_state.get("voice_gender", "female")

        st.session_state["history"].append(("user", user_input))
        response = generate_response(user_input, response_mode)

        # Traduire la réponse si nécessaire
        translated_response = translate_text(response, target_language)
        st.session_state["history"].append(("assistant", translated_response))

        st.chat_message("user").write(user_input)
        st.chat_message("assistant").write(translated_response)

        # Lecture vocale si activée
        if st.session_state.get("use_tts", False):
            speak(translated_response, voice_gender)

with col2:
    st.sidebar.title("🔧 Options")
    # Choix du mode de réponse
    st.sidebar.markdown("### Mode de réponse")
    response_mode = st.sidebar.radio("Choisir le mode :", ["Réponses pré-enregistrées", "IA (GPT)"])
    st.session_state["response_mode"] = response_mode

    # Options supplémentaires
    st.sidebar.markdown("### Synthèse vocale")
    use_tts = st.sidebar.checkbox("🔊 Activer la synthèse vocale", value=False)
    st.session_state["use_tts"] = use_tts
    if use_tts:
        voice_gender = st.sidebar.radio("Choisir la voix :", ["female", "male"])
        st.session_state["voice_gender"] = voice_gender

    # Traduction
    st.sidebar.markdown("### Traduction")
    target_language = st.sidebar.selectbox("🌐 Langue des réponses :", ["fr", "en", "es", "de"])
    st.session_state["target_language"] = target_language

    # Actions supplémentaires
    st.sidebar.markdown("### Actions")
    if st.sidebar.button("📡 Dernières actualités IA"):
        st.sidebar.write(fetch_ai_research())
    if st.sidebar.button("📰 Actualités générales"):
        st.sidebar.write(fetch_news())
    if st.sidebar.button("🗑️ Réinitialiser la conversation"):
        st.session_state["history"].clear()
        st.session_state["context"] = {"last_intent": None}
        st.sidebar.write("🔄 Chatbot : La conversation a été réinitialisée.")





