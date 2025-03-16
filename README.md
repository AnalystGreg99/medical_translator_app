# 🏥 Healthcare Translation Web App with Generative AI  

## 📌 Overview  

This project is a **real-time multilingual translation web app** designed for healthcare providers and patients. It leverages **Groq API** to provide:  

✅ **Speech-to-Text** – Converts spoken words into text using AI-powered transcription.  
✅ **Real-Time Translation** – Translates text while preserving medical terminology.  
✅ **Text-to-Speech** – Generates and plays back translated speech.  
✅ **Dual Transcript Display** – Shows both original and translated text side by side.  
✅ **Mobile-Friendly UI** – Built using **Streamlit**, ensuring a responsive design.  
✅ **Secure & Private** – No data storage; ensures patient confidentiality.  

---

## 🚀 Features  

### 🔹 **Core Functionalities**  
- **Voice Input** – Users can upload an audio file (WAV/MP3).  
- **Real-Time Transcription** – Speech is converted to text.  
- **Language Selection** – Users choose the translation language (e.g., Spanish, French, Chinese).  
- **Instant Translation** – The transcribed text is translated into the selected language.  
- **Audio Playback** – The translated text is converted into speech and played back.  

### 🔹 **Technical Highlights**  
- **Built with Streamlit** – A fast and interactive UI.  
- **Uses Groq API** – For high-quality AI-powered translation and text-to-speech.  
- **Deployed on Koyeb** – Ensures a scalable and serverless hosting environment.  
- **Fast Response Time** – Optimized for real-time interactions.  

---

## 🛠️ Tech Stack  

| Component       | Technology |
|----------------|------------|
| **Frontend & Backend** | Streamlit (Python) |
| **APIs**       | Groq API (Speech-to-Text, Translation, Text-to-Speech) |
| **Hosting**    | Koyeb (Serverless Deployment) |
| **Security**   | HTTPS, No data storage, Basic rate limiting |

---

## 🖥️ Installation & Setup  

### 1️⃣ **Clone the Repository**  
```bash
git clone https://github.com/yourusername/healthcare-translator.git
cd healthcare-translator
```

### 2️⃣ **Install Dependencies**  
```bash
pip install -r requirements.txt
```

### 3️⃣ **Set Up API Key**  
Before running the app, set your **Groq API key**:  
#### On Linux/Mac:
```bash
export GROQ_API_KEY="your_api_key_here"
```
#### On Windows (CMD):
```bash
set GROQ_API_KEY="your_api_key_here"
```

### 4️⃣ **Run the Streamlit App**  
```bash
streamlit run app.py
```

---

## 🌍 Deployment on Koyeb  

### 1️⃣ **Push the Project to GitHub**  
```bash
git add .
git commit -m "Initial commit"
git push -u origin main
```

### 2️⃣ **Deploy on Koyeb**  
- Go to [Koyeb](https://www.koyeb.com/).  
- Create a **new service** and connect your GitHub repository.  
- Set **GROQ_API_KEY** as an **environment variable** in Koyeb.  
- Deploy the service 🚀.  

---

## 📖 Usage Guide  

1️⃣ **Upload an Audio File** – Select and upload a **WAV/MP3** file.  
2️⃣ **Select Target Language** – Choose a translation language (e.g., **Spanish, French, German**).  
3️⃣ **View Real-Time Transcript** – Original and translated text appear instantly.  
4️⃣ **Click "Play Translation"** – Hear the translated text as speech.  

---

## 📊 Evaluation Metrics  

✅ **Accuracy of Speech-to-Text** – Ensures correct transcription of medical terminology.  
✅ **Translation Quality** – Verifies meaningful translations in different languages.  
✅ **Audio Playback Quality** – Checks text-to-speech clarity and pronunciation.  
✅ **Performance & Latency** – Measures response time for real-time interactions.  
✅ **User Experience** – Tests mobile responsiveness and intuitive UI.  

---

## 📅 Project Milestones  

| Milestone           | Description | Status |
|---------------------|------------|--------|
| Setup Environment  | Install dependencies and configure API keys | ✅ Completed |
| Develop Core Features | Implement speech-to-text, translation, and text-to-speech | ✅ Completed |
| Build Streamlit UI  | Create an intuitive and mobile-friendly interface | ✅ Completed |
| Testing & Debugging | Ensure API calls function correctly, improve UX | ✅ Completed |
| Deploy on Koyeb     | Host live prototype for accessibility | ✅ Completed |
| Submit Assignment  | Provide prototype link, documentation, and guide | 🚀 Pending |

---

## 📌 Known Issues & Fixes  

### **❌ OMP: Error #15: Initializing libiomp5md.dll**
If you get an **OpenMP runtime error**, fix it by running:  
```bash
pip install --upgrade --force-reinstall numpy --no-cache-dir
```
or set this environment variable before running the app:  
```bash
set KMP_DUPLICATE_LIB_OK=TRUE
```

### **❌ App Not Fully Mobile-Friendly?**
If UI elements are too small on mobile:  
- Use **Streamlit’s `st.container()`** for better layout.  
- Add **custom CSS** for improved styling:  
```python
st.markdown("""
    <style>
        .block-container { padding: 10px !important; }
    </style>
""", unsafe_allow_html=True)
```

---

## 🎥 Demo & Submission  

📌 **Live Demo Link**: [Your Koyeb Deployment URL]  
📌 **Video Presentation**: [Loom/YouTube Link]  

---

## 👨‍💻 Developed By  

👤 **[Your Name]**  
📧 [Your Email]  
🔗 [Your LinkedIn / GitHub Profile]  

---

### 🚀 **Let's Break Language Barriers in Healthcare!** 🏥  
