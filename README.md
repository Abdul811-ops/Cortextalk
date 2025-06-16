# Cortextalk
# 🧠 AI Neural Language Tutor

Welcome to the **AI Neural Language Tutor** — an interactive, multilingual, VR-themed language learning app built with **Streamlit**, **Speech Recognition**, and **AI-powered feedback**.

> Learn Spanish 🇪🇸, French 🇫🇷, and German 🇩🇪 with immersive levels, real-time voice input, and smart TTS pronunciation support!

---

## 🚀 Features

- 🎤 **Speech Recognition** – Practice pronunciation via voice input  
- 🔊 **Text-to-Speech** – Hear native-like pronunciati
# 🧠 AI Neural Language Tutor

Welcome to the *AI Neural Language Tutor* — an interactive, multilingual, VR-themed language learning app built with *Streamlit, **Speech Recognition, and **AI-powered feedback*.

> Learn Spanish 🇪🇸, French 🇫🇷, and German 🇩🇪 with immersive levels, real-time voice input, and smart TTS pronunciation support!

---

## 🚀 Features

- 🎤 *Speech Recognition* – Practice pronunciation via voice input  
- 🔊 *Text-to-Speech* – Hear native-like pronunciations in real-time  
- 🧠 *AI-Level Feedback* – Smart response checking + streaks + accuracy  
- 🧩 *Levels 1–3* – Vocabulary, Grammar, Conversation, Fill-in-the-Blank  
- 🧬 *VR Design* – Holographic effects, floating particles, neural themes  
- 📊 *Progress Tracking* – Monitor your learning journey with detailed analytics
- 💬 *Chat History* – Tracks your progress & interactions
- 🌍 *Multi-language Support* – Switch between Spanish, French, and German seamlessly

---

## 🌐 Live Demo

> [🚀 Launch on Streamlit Cloud](https://share.streamlit.io/your-username/your-repo-name/main/ai_tutor.py)  
(Replace this with your actual deployment link)

---

## 🛠 Installation & Setup

### Prerequisites
- Python 3.7+
- Microphone access for speech recognition
- Internet connection for AI features

### Quick Start
bash
# Clone the repository
git clone https://github.com/your-username/ai-neural-language-tutor.git
cd ai-neural-language-tutor

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run ai_tutor.py


### Alternative Installation with Virtual Environment
bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run ai_tutor.py


---

## 📦 Dependencies

Create a requirements.txt file with the following packages:

txt
streamlit>=1.28.0
speech-recognition>=3.10.0
pyttsx3>=2.90
openai>=1.0.0
streamlit-webrtc>=0.47.0
numpy>=1.24.0
pandas>=2.0.0
plotly>=5.15.0
gtts>=2.3.0
pygame>=2.5.0


---

## 🎮 How to Use

### 1. *Choose Your Language*
Select from Spanish 🇪🇸, French 🇫🇷, or German 🇩🇪

### 2. *Select Learning Level*
- *Level 1*: Basic vocabulary and phrases
- *Level 2*: Grammar structures and sentence formation  
- *Level 3*: Advanced conversation and complex expressions

### 3. *Practice Methods*
- *Voice Input*: Click the microphone and speak your answer
- *Text Input*: Type your responses for grammar exercises
- *Listening*: Hear native pronunciations and repeat

### 4. *Track Progress*
- View your accuracy scores
- Monitor learning streaks
- Review chat history and mistakes

---

## 🧬 Technical Architecture

### Core Components

ai_tutor.py                 # Main application file
├── speech_recognition/     # Voice input processing
├── tts_engine/            # Text-to-speech functionality  
├── ai_feedback/           # AI-powered response evaluation
├── level_management/      # Learning progression system
├── ui_components/         # VR-themed interface elements
└── data_storage/          # Progress tracking and history


### Key Technologies
- *Streamlit*: Web app framework
- *SpeechRecognition*: Voice input processing
- *pyttsx3/gTTS*: Text-to-speech engines
- *OpenAI API*: AI-powered feedback and corrections
- *Plotly*: Interactive progress visualizations

---

## 🎨 VR Theme Features

- *Holographic Effects*: CSS animations and gradients
- *Floating Particles*: Dynamic background animations  
- *Neural Network Visuals*: Brain-inspired UI elements
- *Neon Color Scheme*: Futuristic purple/blue/cyan palette
- *3D Transitions*: Smooth hover and click effects

---

## 🔧 Configuration

### API Keys Setup
Create a .env file in the root directory:
env
OPENAI_API_KEY=your_openai_api_key_here
SPEECH_API_KEY=your_speech_api_key_here


### Customization Options
- *Languages*: Add new languages in config.py
- *Difficulty*: Modify level progression in levels.py
- *Themes*: Customize VR styling in styles.css
- *Voice Settings*: Adjust TTS parameters in tts_config.py

---

## 📊 Learning Levels Breakdown

| Level | Focus Area | Skills Developed | Example Activities |
|-------|------------|------------------|-------------------|
| *Level 1* | Vocabulary | Basic words, greetings, numbers | Word matching, pronunciation |
| *Level 2* | Grammar | Sentence structure, verb conjugation | Fill-in-the-blank, corrections |
| *Level 3* | Conversation | Dialogue, complex expressions | Role-play, story completion |

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. *Fork the repository*
2. *Create a feature branch*: git checkout -b feature/amazing-feature
3. *Commit changes*: git commit -m 'Add amazing feature'
4. *Push to branch*: git push origin feature/amazing-feature
5. *Open a Pull Request*

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include unit tests for new features
- Update README for significant changes

---

## 🐛 Troubleshooting

### Common Issues

*Microphone not working:*
- Check browser permissions for microphone access
- Ensure your microphone is properly connected
- Try refreshing the page

*Speech recognition errors:*
- Speak clearly and at moderate pace
- Check internet connection
- Verify microphone input levels

*TTS not playing:*
- Check browser audio settings
- Ensure speakers/headphones are connected
- Try different TTS engines in settings

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- *Streamlit Team* for the amazing web framework
- *OpenAI* for AI-powered language processing
- *Speech Recognition Community* for voice input capabilities
- *Language Learning Enthusiasts* who inspired this project

---

## 📞 Support & Contact

- *Issues*: [GitHub Issues](https://github.com/your-username/ai-neural-language-tutor/issues)
- *Discussions*: [GitHub Discussions](https://github.com/your-username/ai-neural-language-tutor/discussions)
- *Email*: your-email@example.com

---

## 🔮 Future Roadmap

- [ ] *Mobile App Version* (React Native)
- [ ] *More Languages* (Italian, Portuguese, Japanese)
- [ ] *Multiplayer Mode* (Compete with friends)
- [ ] *AR/VR Integration* (Immersive environments)
- [ ] *Offline Mode* (Local AI processing)
- [ ] *Gamification* (Achievements, leaderboards)

---

<div align="center">

*Happy Learning! 🧠✨*

Made with ❤ and lots of ☕

</div>
