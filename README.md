<<<<<<< HEAD
# chatbot-ia-portfolio
 Chatbot IA interactif avec Streamlit, NLP et API d’actualités IA
# 🧠 Chatbot IA - Portfolio Project

## 📌 **Présentation du projet**
### 🎯 Objectif
Ce projet est un **Chatbot IA interactif** conçu pour répondre aux utilisateurs avec :
✅ **Des réponses pré-enregistrées** avec tolérance aux fautes.
✅ **Une génération de réponses IA** avec un modèle de Hugging Face.
✅ **L'affichage d'actualités en IA et en technologie**.
✅ **Une synthèse vocale** pour lire les réponses à haute voix.
✅ **Une option de traduction** pour répondre dans différentes langues.

Ce chatbot est un **projet personnel** destiné à être inclus dans un **portfolio pour des candidatures en Master IA**.

---

## ⚙️ **Technologies utilisées et choix techniques**
📌 **Langages & Frameworks** :
- **Python** → Langage principal du chatbot.
- **Streamlit** → Interface utilisateur interactive et facile à déployer.
- **SpaCy** → NLP pour la gestion des intentions, car il est performant et léger.
- **Hugging Face Transformers** → Génération de texte avancée pour avoir des réponses plus naturelles.
- **Pyttsx3** → Synthèse vocale qui fonctionne en local sans dépendre d'API externes.
- **Rapidfuzz** → Permet la tolérance aux fautes dans la compréhension des intentions de l'utilisateur.
- **Googletrans** → Ajout de la traduction pour rendre le chatbot plus accessible.
- **Requests** → Utilisé pour récupérer des données depuis des API (NewsAPI et ArXiv).

📌 **Pourquoi ces choix ?**
- **Streamlit** : Facile à utiliser pour créer une interface sans avoir à gérer du front-end complexe.
- **SpaCy au lieu de NLTK** : Plus rapide et mieux optimisé pour le NLP moderne.
- **Hugging Face au lieu d’OpenAI GPT** : Gratuit et plus facile à intégrer sans nécessiter une clé API payante.
- **Rapidfuzz au lieu d’une simple recherche string** : Permet une meilleure tolérance aux fautes et améliore la compréhension des intentions.
- **Googletrans au lieu d’API payantes** : Gratuit et fonctionnel pour une traduction simple.

---

## 💻 **Installation et exécution du chatbot**
### 🔧 **Prérequis**
- **Python 3.8+** doit être installé.
- **Les bibliothèques nécessaires doivent être installées**.

### 📥 **Installation des dépendances**
Ouvrez un terminal et exécutez :
```bash
pip install streamlit spacy transformers pyttsx3 requests rapidfuzz googletrans
```

### 🚀 **Lancer le chatbot**
```bash
streamlit run chatbot.py
```

---

## 🚀 **Fonctionnalités détaillées et évolutions**

### **1️⃣ Réponses pré-enregistrées** 🎤
- Initialement, le chatbot ne comprenait que des phrases précises.
- **Amélioration :** Utilisation de `Rapidfuzz` pour permettre une tolérance aux fautes.

### **2️⃣ Réponses IA avec Hugging Face** 🤖
- Avant, les réponses étaient uniquement statiques.
- **Amélioration :** Ajout d'un modèle Hugging Face pour générer des réponses plus variées.

### **3️⃣ Actualités IA & Tech** 📰
- Initialement, seul un résumé des actualités générales était affiché.
- **Amélioration :** Ajout des **recherches en IA via ArXiv** pour une pertinence accrue.

### **4️⃣ Synthèse vocale** 🔊
- Initialement, la synthèse vocale lisait toutes les réponses.
- **Amélioration :** Ajout d'un **choix de voix masculine ou féminine**.

### **5️⃣ Traduction des réponses** 🌍
- Initialement, pas de traduction.
- **Amélioration :** Ajout d’un bouton pour choisir la langue des réponses.

---

## 🛠️ **Problèmes rencontrés & solutions détaillées**

### ❌ Erreur `ModuleNotFoundError` sur `rapidfuzz`
- **Pourquoi ?** La bibliothèque n'était pas installée par défaut.
- ✅ **Solution** : Installer la bonne version `pip install rapidfuzz==2.13.0`.

### ❌ Tolérance aux fautes (`extractOne()`) qui plante
- **Pourquoi ?** `extractOne()` retournait plus de valeurs que prévu.
- ✅ **Solution** : Modifier `detect_intent()` pour gérer les résultats correctement.

### ❌ Traduction avec `googletrans` qui ne fonctionne pas
- **Pourquoi ?** Certaines versions de `googletrans` sont instables.
- ✅ **Solution** : Tester `deep-translator` en alternative.

### ❌ API NewsAPI qui ne retourne rien
- **Pourquoi ?** Problème d’authentification avec la clé API.
- ✅ **Solution** : Vérifier la **clé API et la connexion Internet**.

---

## 🏗️ **Historique du développement**
- **Version 1** : Réponses pré-enregistrées uniquement.
- **Version 2** : Ajout d’un modèle IA (Hugging Face).
- **Version 3** : Ajout des actualités IA et NewsAPI.
- **Version 4** : Intégration de la synthèse vocale et traduction.
- **Version finale** : Amélioration de l’interface, correction des erreurs.

---

## 🔥 **Prochaines améliorations possibles**
- **Sauvegarder l’historique des conversations**.
- **Ajouter un "Mode Expert"** pour des réponses plus détaillées.
- **Déployer le chatbot en ligne** via **Streamlit Cloud**.

---

## 🌍 **Liens utiles & crédits**
📌 **Sources utilisées** :
- [Documentation Streamlit](https://docs.streamlit.io/)
- [Documentation SpaCy](https://spacy.io/)
- [Hugging Face Models](https://huggingface.co/transformers/)
- [Googletrans](https://pypi.org/project/googletrans/)



# ChatbotIA
=======
# CB-IA-PT

Ceci est le fichier README pour mon projet Chatbot IA.
>>>>>>> 38d46e2 (Initialisation du projet et ajout des fichiers)
