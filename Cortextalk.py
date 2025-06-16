import streamlit as st
import speech_recognition as sr
import random
import torch
import numpy as np
import io
import threading
from datetime import datetime
import time
import json
import pyttsx3
import base64
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="AI Language Tutor",
    page_icon="🗣",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced sample prompts data with complete structure for all languages
sample_prompts = {
    'es': {
        'level_1': [
            {'type': 'vocabulary', 'word': 'hello', 'context': 'A greeting when you meet someone', 'translation': 'hola', 'audio_text': 'OH-lah'},
            {'type': 'vocabulary', 'word': 'goodbye', 'context': 'A farewell when you leave', 'translation': 'adiós', 'audio_text': 'ah-DYOHS'},
            {'type': 'vocabulary', 'word': 'thank you', 'context': 'Expression of gratitude', 'translation': 'gracias', 'audio_text': 'GRAH-see-ahs'},
            {'type': 'vocabulary', 'word': 'water', 'context': 'A clear liquid we drink', 'translation': 'agua', 'audio_text': 'AH-gwah'},
            {'type': 'vocabulary', 'word': 'food', 'context': 'What we eat to survive', 'translation': 'comida', 'audio_text': 'koh-MEE-dah'},
            {'type': 'vocabulary', 'word': 'house', 'context': 'A place where people live', 'translation': 'casa', 'audio_text': 'KAH-sah'},
            {'type': 'vocabulary', 'word': 'friend', 'context': 'Someone you like and trust', 'translation': 'amigo', 'audio_text': 'ah-MEE-goh'},
            {'type': 'vocabulary', 'word': 'family', 'context': 'Your relatives', 'translation': 'familia', 'audio_text': 'fah-MEE-lee-ah'},
            {'type': 'fill_blank', 'sentence': 'Hola, ¿cómo _____?', 'options': ['estás', 'comes', 'vives'], 'correct': 'estás', 'translation': 'Hello, how are you?'},
            {'type': 'fill_blank', 'sentence': 'Me gusta la _____.', 'options': ['comida', 'correr', 'azul'], 'correct': 'comida', 'translation': 'I like the food.'},
        ],
        'level_2': [
            {'type': 'grammar', 'prompt': 'How do you say "I am happy" in Spanish?', 'answer': 'estoy feliz', 'explanation': 'Use "estoy" for temporary states'},
            {'type': 'grammar', 'prompt': 'What is the Spanish word for "beautiful" (feminine)?', 'answer': 'bella', 'explanation': 'Adjectives must match gender'},
            {'type': 'translation', 'english': 'The red car', 'translation': 'el carro rojo', 'explanation': 'Adjectives come after nouns in Spanish'},
            {'type': 'fill_blank', 'sentence': 'Yo _____ estudiante.', 'options': ['soy', 'estoy', 'tengo'], 'correct': 'soy', 'translation': 'I am a student.'},
            {'type': 'fill_blank', 'sentence': '¿_____ años tienes?', 'options': ['Cuántos', 'Cuándo', 'Dónde'], 'correct': 'Cuántos', 'translation': 'How old are you?'},
        ],
        'level_3': [
            {'type': 'conversation', 'prompt': 'How do you ask someone their name politely?', 'answer': '¿cómo te llamas?', 'alternative': '¿cuál es tu nombre?'},
            {'type': 'conversation', 'prompt': 'How do you say "I am from India"?', 'answer': 'soy de india', 'alternative': 'vengo de india'},
            {'type': 'story_completion', 'context': 'María goes to a restaurant', 'prompt': 'Complete: "Buenos días, ¿qué _____ hoy?"', 'answer': 'quiere', 'translation': 'Good morning, what do you want today?'},
            {'type': 'conversation', 'prompt': 'How do you say "Where is the bathroom?"', 'answer': '¿dónde está el baño?', 'alternative': '¿dónde queda el baño?'},
            {'type': 'conversation', 'prompt': 'How do you ask "How much does it cost?"', 'answer': '¿cuánto cuesta?', 'alternative': '¿cuál es el precio?'},
        ]
    },
    'fr': {
        'level_1': [
            {'type': 'vocabulary', 'word': 'hello', 'context': 'A greeting when you meet someone', 'translation': 'bonjour', 'audio_text': 'bon-ZHOOR'},
            {'type': 'vocabulary', 'word': 'goodbye', 'context': 'A farewell when you leave', 'translation': 'au revoir', 'audio_text': 'oh ruh-VWAHR'},
            {'type': 'vocabulary', 'word': 'thank you', 'context': 'Expression of gratitude', 'translation': 'merci', 'audio_text': 'mer-SEE'},
            {'type': 'vocabulary', 'word': 'water', 'context': 'A clear liquid we drink', 'translation': 'eau', 'audio_text': 'OH'},
            {'type': 'vocabulary', 'word': 'food', 'context': 'What we eat to survive', 'translation': 'nourriture', 'audio_text': 'noor-ree-TOOR'},
            {'type': 'vocabulary', 'word': 'house', 'context': 'A place where people live', 'translation': 'maison', 'audio_text': 'meh-ZOHN'},
            {'type': 'vocabulary', 'word': 'friend', 'context': 'Someone you like and trust', 'translation': 'ami', 'audio_text': 'ah-MEE'},
            {'type': 'vocabulary', 'word': 'family', 'context': 'Your relatives', 'translation': 'famille', 'audio_text': 'fah-MEEL'},
            {'type': 'fill_blank', 'sentence': 'Comment _____ vous?', 'options': ['allez', 'mangez', 'dormez'], 'correct': 'allez', 'translation': 'How are you?'},
            {'type': 'fill_blank', 'sentence': 'Je _____ français.', 'options': ['parle', 'mange', 'dors'], 'correct': 'parle', 'translation': 'I speak French.'},
        ],
        'level_2': [
            {'type': 'grammar', 'prompt': 'How do you say "I am" in French?', 'answer': 'je suis', 'explanation': 'Use "je suis" for permanent states'},
            {'type': 'translation', 'english': 'The house', 'translation': 'la maison', 'explanation': 'House is feminine in French'},
            {'type': 'grammar', 'prompt': 'How do you say "I have" in French?', 'answer': 'j\'ai', 'explanation': 'Use "j\'ai" for possession'},
            {'type': 'fill_blank', 'sentence': 'Elle _____ belle.', 'options': ['est', 'a', 'va'], 'correct': 'est', 'translation': 'She is beautiful.'},
            {'type': 'fill_blank', 'sentence': 'Nous _____ français.', 'options': ['parlons', 'mangeons', 'allons'], 'correct': 'parlons', 'translation': 'We speak French.'},
        ],
        'level_3': [
            {'type': 'conversation', 'prompt': 'How do you ask "What is your name?"', 'answer': 'comment vous appelez-vous?', 'alternative': 'quel est votre nom?'},
            {'type': 'conversation', 'prompt': 'How do you say "I am from France"?', 'answer': 'je viens de france', 'alternative': 'je suis de france'},
            {'type': 'conversation', 'prompt': 'How do you ask "Where is the station?"', 'answer': 'où est la gare?', 'alternative': 'où se trouve la gare?'},
            {'type': 'conversation', 'prompt': 'How do you say "I would like"?', 'answer': 'je voudrais', 'alternative': 'j\'aimerais'},
            {'type': 'story_completion', 'context': 'At a café', 'prompt': 'Complete: "Je voudrais un _____, s\'il vous plaît."', 'answer': 'café', 'translation': 'I would like a coffee, please.'},
        ]
    },
    'de': {
        'level_1': [
            {'type': 'vocabulary', 'word': 'hello', 'context': 'A greeting when you meet someone', 'translation': 'hallo', 'audio_text': 'HAH-loh'},
            {'type': 'vocabulary', 'word': 'goodbye', 'context': 'A farewell when you leave', 'translation': 'auf wiedersehen', 'audio_text': 'owf VEE-der-zayn'},
            {'type': 'vocabulary', 'word': 'thank you', 'context': 'Expression of gratitude', 'translation': 'danke', 'audio_text': 'DAHN-kuh'},
            {'type': 'vocabulary', 'word': 'water', 'context': 'A clear liquid we drink', 'translation': 'wasser', 'audio_text': 'VAH-ser'},
            {'type': 'vocabulary', 'word': 'food', 'context': 'What we eat to survive', 'translation': 'essen', 'audio_text': 'EH-sen'},
            {'type': 'vocabulary', 'word': 'house', 'context': 'A place where people live', 'translation': 'haus', 'audio_text': 'HOWS'},
            {'type': 'vocabulary', 'word': 'friend', 'context': 'Someone you like and trust', 'translation': 'freund', 'audio_text': 'FROYNT'},
            {'type': 'vocabulary', 'word': 'family', 'context': 'Your relatives', 'translation': 'familie', 'audio_text': 'fah-MEE-lee-eh'},
            {'type': 'fill_blank', 'sentence': 'Wie _____ du?', 'options': ['heißt', 'bist', 'gehst'], 'correct': 'heißt', 'translation': 'What is your name?'},
            {'type': 'fill_blank', 'sentence': 'Ich _____ Deutsch.', 'options': ['spreche', 'esse', 'gehe'], 'correct': 'spreche', 'translation': 'I speak German.'},
        ],
        'level_2': [
            {'type': 'grammar', 'prompt': 'How do you say "I am" in German?', 'answer': 'ich bin', 'explanation': 'Use "ich bin" for identity'},
            {'type': 'translation', 'english': 'The house', 'translation': 'das haus', 'explanation': 'House is neuter in German'},
            {'type': 'grammar', 'prompt': 'How do you say "I have" in German?', 'answer': 'ich habe', 'explanation': 'Use "ich habe" for possession'},
            {'type': 'fill_blank', 'sentence': 'Sie _____ schön.', 'options': ['ist', 'hat', 'geht'], 'correct': 'ist', 'translation': 'She is beautiful.'},
            {'type': 'fill_blank', 'sentence': 'Wir _____ nach Hause.', 'options': ['gehen', 'sind', 'haben'], 'correct': 'gehen', 'translation': 'We go home.'},
        ],
        'level_3': [
            {'type': 'conversation', 'prompt': 'How do you ask "How are you?"', 'answer': 'wie geht es dir?', 'alternative': 'wie geht es ihnen?'},
            {'type': 'conversation', 'prompt': 'How do you say "I am from Germany"?', 'answer': 'ich komme aus deutschland', 'alternative': 'ich bin aus deutschland'},
            {'type': 'conversation', 'prompt': 'How do you ask "Where is the train station?"', 'answer': 'wo ist der bahnhof?', 'alternative': 'wo befindet sich der bahnhof?'},
            {'type': 'conversation', 'prompt': 'How do you say "I would like"?', 'answer': 'ich möchte', 'alternative': 'ich hätte gern'},
            {'type': 'story_completion', 'context': 'At a restaurant', 'prompt': 'Complete: "Ich möchte ein _____, bitte."', 'answer': 'bier', 'translation': 'I would like a beer, please.'},
        ]
    }
}

# Language codes and names
language_codes = {
    'spanish': 'es',
    'french': 'fr', 
    'german': 'de'
}

language_names = {
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German'
}

# Initialize session state with improved structure
def initialize_session_state():
    if 'current_level' not in st.session_state:
        st.session_state.current_level = 1
    if 'current_language' not in st.session_state:
        st.session_state.current_language = None
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 0
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'level_progress' not in st.session_state:
        st.session_state.level_progress = {1: 0, 2: 0, 3: 0}  # Track questions completed per level
    if 'level_unlocked' not in st.session_state:
        st.session_state.level_unlocked = {1: True, 2: False, 3: False}
    if 'current_questions' not in st.session_state:
        st.session_state.current_questions = []
    if 'question_types' not in st.session_state:
        st.session_state.question_types = []
    if 'recognized_text' not in st.session_state:
        st.session_state.recognized_text = None
    if 'speech_input' not in st.session_state:
        st.session_state.speech_input = ""

@st.cache_resource
def initialize_tts_engine():
    """Simplified TTS engine initialization"""
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        return engine
    except:
        return None

def text_to_speech_real(text, language='en'):
    """Simplified TTS with browser fallback"""
    try:
        st.info(f"🔊 *Speaking:* {text}")
        
        # Use browser TTS
        audio_html = f"""
        <script>
        if ('speechSynthesis' in window) {{
            var utterance = new SpeechSynthesisUtterance("{text}");
            utterance.lang = "{get_speech_lang_code(language)}";
            utterance.rate = 0.8;
            window.speechSynthesis.speak(utterance);
        }}
        </script>
        """
        components.html(audio_html, height=0)
        st.success("✅ Audio played!")
        
    except Exception as e:
        st.write(f"🔊 *Read aloud:* {text}")

def text_to_speech_fallback(text, language='en'):
    """Fallback TTS"""
    text_to_speech_real(text, language)

def get_speech_lang_code(language):
    """Get proper language codes for browser speech synthesis"""
    lang_codes = {
        'es': 'es-ES',  # Spanish
        'fr': 'fr-FR',  # French
        'de': 'de-DE',  # German
        'en': 'en-US'   # English
    }
    return lang_codes.get(language, 'en-US')

def text_to_speech_simulation(text, language='en'):
    """Simulation function"""
    text_to_speech_real(text, language)

def speech_to_text_real():
    """Fixed Speech-to-Text with proper fallback"""
    st.write("🎤 *Speech Input*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("*Option 1: Voice Input*")
        # Improved browser speech recognition
        if st.button("🎤 Start Recording", key="voice_btn"):
            speech_html = f"""
            <div style="padding: 10px; border: 1px solid #ccc; border-radius: 5px;">
                <button onclick="startSpeech()" style="padding: 10px 20px; background: #4CAF50; color: white; border: none; border-radius: 5px;">🎤 Click to Speak</button>
                <div id="result" style="margin-top: 10px; font-weight: bold;"></div>
                <div id="status" style="margin-top: 5px; color: #666;"></div>
            </div>
            <script>
            function startSpeech() {{
                if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {{
                    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                    const recognition = new SpeechRecognition();
                    
                    recognition.continuous = false;
                    recognition.interimResults = false;
                    recognition.lang = '{get_speech_lang_code(st.session_state.get("current_language", "en"))}';
                    
                    document.getElementById('status').innerHTML = '🎤 Listening...';
                    
                    recognition.onresult = function(event) {{
                        const transcript = event.results[0][0].transcript;
                        document.getElementById('result').innerHTML = 'You said: "' + transcript + '"';
                        document.getElementById('status').innerHTML = '✅ Recording complete!';
                        
                        // Store result in a way Streamlit can access (simplified approach)
                        console.log('Speech result:', transcript);
                    }};
                    
                    recognition.onerror = function(event) {{
                        document.getElementById('status').innerHTML = '❌ Error: ' + event.error;
                    }};
                    
                    recognition.onend = function() {{
                        document.getElementById('status').innerHTML = '🔴 Recording stopped';
                    }};
                    
                    recognition.start();
                }} else {{
                    document.getElementById('result').innerHTML = '❌ Speech recognition not supported in this browser';
                }}
            }}
            </script>
            """
            components.html(speech_html, height=150)
    
    with col2:
        st.write("*Option 2: Text Input*")
        # Text input fallback (primary method)
        user_input = st.text_input(
            "Type your answer:", 
            key=f"text_input_{st.session_state.current_question_index}",
            placeholder="Enter your answer here..."
        )
        
        if user_input:
            st.session_state.speech_input = user_input
            return user_input.lower().strip()
    
    # Return any existing input
    return st.session_state.speech_input.lower().strip() if st.session_state.speech_input else None

def shuffle_questions(level, language_code):
    """Shuffle questions for the current level with validation"""
    questions = sample_prompts.get(language_code, {}).get(f'level_{level}', [])
    
    if not questions:
        st.error(f"No questions found for {language_names.get(language_code, 'Unknown')} Level {level}")
        return []
    
    shuffled = questions.copy()
    random.shuffle(shuffled)
    return shuffled

def check_level_completion(level):
    """Check if level is completed and unlock next level"""
    required_correct = 6  # Require 6 correct answers to unlock next level
    
    if st.session_state.level_progress[level] >= required_correct:
        if level < 3:
            st.session_state.level_unlocked[level + 1] = True
        return True
    return False

def add_to_chat_history(speaker, message, language='en'):
    """Add message to chat history"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.chat_history.append({
        'timestamp': timestamp,
        'speaker': speaker,
        'message': message,
        'language': language
    })

def run_vocabulary_question(prompt, target_language):
    """Handle vocabulary questions"""
    st.session_state.current_prompt = prompt
    
    word = prompt['word']
    context = prompt['context']
    correct_translation = prompt['translation']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"*English Word:* {word}")
        st.write(f"*Context:* {context}")
        
        if st.button("🔊 Listen to pronunciation", key="vocab_listen"):
            text_to_speech_real(f"The word {word} in {language_names[target_language]} is {correct_translation}", target_language)
    
    with col2:
        st.write(f"*Translate to {language_names[target_language]}:*")
        
        # Get user input (speech or text)
        user_input = speech_to_text_real()
        
        if user_input and st.button("✅ Check Answer", key="vocab_check"):
            add_to_chat_history("You", user_input)
            
            if user_input == correct_translation.lower():
                st.success("🎉 Correct!")
                st.session_state.score += 1
                st.session_state.level_progress[st.session_state.current_level] += 1
                text_to_speech_real("Correct! Well done!", target_language)
                return True
            else:
                st.error(f"❌ Incorrect. The correct answer is: *{correct_translation}*")
                text_to_speech_real(f"Incorrect. The correct answer is {correct_translation}", target_language)
                return False
    
    return None

def run_fill_blank_question(prompt, target_language):
    """Handle fill-in-the-blank questions"""
    sentence = prompt['sentence']
    options = prompt['options']
    correct = prompt['correct']
    translation = prompt.get('translation', '')
    
    st.write(f"*Complete the sentence:*")
    st.write(f"{sentence}")
    if translation:
        st.write(f"Translation: {translation}")
    
    # Randomize options
    shuffled_options = options.copy()
    random.shuffle(shuffled_options)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔊 Listen to sentence", key="blank_listen"):
            text_to_speech_real(sentence, target_language)
    
    with col2:
        selected_option = st.radio("Choose the correct word:", shuffled_options, key=f"blank_radio_{st.session_state.current_question_index}")
        
        if st.button("✅ Submit Answer", key="blank_submit"):
            add_to_chat_history("You", selected_option)
            
            if selected_option == correct:
                st.success("🎉 Correct!")
                st.session_state.score += 1
                st.session_state.level_progress[st.session_state.current_level] += 1
                text_to_speech_real("Correct! Great job!", target_language)
                return True
            else:
                st.error(f"❌ Incorrect. The correct answer is: *{correct}*")
                text_to_speech_real(f"Incorrect. The correct answer is {correct}", target_language)
                return False
    
    return None

def run_grammar_question(prompt, target_language):
    """Handle grammar questions"""
    question = prompt['prompt']
    correct_answer = prompt['answer']
    explanation = prompt.get('explanation', '')
    
    st.write(f"*Question:* {question}")
    if explanation:
        st.info(f"💡 *Tip:* {explanation}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔊 Listen to question", key="grammar_listen"):
            text_to_speech_real(question, target_language)
    
    with col2:
        user_input = speech_to_text_real()
        
        if user_input and st.button("✅ Check Answer", key="grammar_check"):
            add_to_chat_history("You", user_input)
            
            if correct_answer.lower() in user_input.lower():
                st.success("🎉 Correct!")
                st.session_state.score += 1
                st.session_state.level_progress[st.session_state.current_level] += 1
                text_to_speech_real("Excellent! That's correct!", target_language)
                return True
            else:
                st.error(f"❌ Incorrect. The correct answer is: *{correct_answer}*")
                text_to_speech_real(f"Incorrect. The correct answer is {correct_answer}", target_language)
                return False
    
    return None

def run_translation_question(prompt, target_language):
    """Handle translation questions"""
    english_text = prompt['english']
    correct_translation = prompt['translation']
    explanation = prompt.get('explanation', '')
    
    st.write(f"*Translate to {language_names[target_language]}:*")
    st.write(f"*English:* {english_text}")
    if explanation:
        st.info(f"💡 *Note:* {explanation}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔊 Listen to English", key="trans_listen"):
            text_to_speech_real(english_text, 'en')
    
    with col2:
        user_input = speech_to_text_real()
        
        if user_input and st.button("✅ Check Translation", key="trans_check"):
            add_to_chat_history("You", user_input)
            
            if correct_translation.lower() in user_input.lower():
                st.success("🎉 Correct!")
                st.session_state.score += 1
                st.session_state.level_progress[st.session_state.current_level] += 1
                text_to_speech_real("Perfect translation!", target_language)
                return True
            else:
                st.error(f"❌ Incorrect. The correct answer is: *{correct_translation}*")
                text_to_speech_real(f"Incorrect. The correct answer is {correct_translation}", target_language)
                return False
    
    return None

def run_level(level, target_language):
    """Run questions for a specific level with randomization"""
    if not st.session_state.level_unlocked[level]:
        st.warning(f"🔒 Level {level} is locked. Complete the previous level first!")
        return
    
    st.subheader(f"📚 Level {level}: {get_level_name(level)}")
    
    # Initialize questions for this level if not done
    if not st.session_state.current_questions or st.session_state.current_level != level:
        st.session_state.current_questions = shuffle_questions(level, target_language)
        st.session_state.current_level = level
        st.session_state.current_question_index = 0
        st.session_state.speech_input = ""  # Reset speech input
    
    # Check if we have questions
    if not st.session_state.current_questions:
        st.error(f"No questions available for {language_names[target_language]} Level {level}")
        return
    
    # Progress bar
    total_questions = len(st.session_state.current_questions)
    completed_questions = st.session_state.current_question_index
    
    progress = completed_questions / total_questions if total_questions > 0 else 0
    st.progress(progress)
    st.write(f"Progress: {completed_questions}/{total_questions} questions")
    
    # Check if level is completed
    if completed_questions >= total_questions:
        if check_level_completion(level):
            st.success(f"🎉 Congratulations! You completed Level {level}!")
            
            if level < 3:
                st.info(f"🔓 Level {level + 1} is now unlocked!")
                if st.button(f"Continue to Level {level + 1}"):
                    st.session_state.current_level = level + 1
                    st.session_state.current_question_index = 0
                    st.session_state.current_questions = []
                    st.rerun()
            else:
                st.balloons()
                st.success("🏆 You've completed all levels! You're amazing!")
        else:
            st.warning(f"Complete more questions correctly to unlock the next level. Need {6 - st.session_state.level_progress[level]} more correct answers.")
        return
    
    # Current question
    if st.session_state.current_questions:
        current_prompt = st.session_state.current_questions[st.session_state.current_question_index]
        
        # Handle different question types
        result = None
        question_type = current_prompt.get('type', 'vocabulary')
        if question_type == 'vocabulary':
            result = run_vocabulary_question(current_prompt, target_language)
        elif question_type == 'fill_blank':
            result = run_fill_blank_question(current_prompt, target_language)
        elif question_type == 'grammar':
            result = run_grammar_question(current_prompt, target_language)
        elif question_type == 'translation':
            result = run_translation_question(current_prompt, target_language)
        elif question_type == 'conversation':
            result = run_conversation_question(current_prompt, target_language)
        elif question_type == 'story_completion':
            result = run_story_completion_question(current_prompt, target_language)
        
        # Handle question completion
        if result is not None:
            time.sleep(1)  # Brief pause before next question
            st.session_state.current_question_index += 1
            st.session_state.total_questions += 1
            st.session_state.speech_input = ""  # Reset speech input
            st.rerun()

def run_conversation_question(prompt, target_language):
    """Handle conversation questions"""
    question = prompt['prompt']
    correct_answer = prompt['answer']
    alternative = prompt.get('alternative', '')
    
    st.write(f"*Conversation Practice:*")
    st.write(f"*Question:* {question}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔊 Listen to question", key="conv_listen"):
            text_to_speech_real(question, 'en')
    
    with col2:
        user_input = speech_to_text_real()
        
        if user_input and st.button("✅ Check Answer", key="conv_check"):
            add_to_chat_history("You", user_input)
            
            # Check if answer matches correct answer or alternative
            is_correct = (correct_answer.lower() in user_input.lower() or 
                         (alternative and alternative.lower() in user_input.lower()))
            
            if is_correct:
                st.success("🎉 Excellent conversation skills!")
                st.session_state.score += 1
                st.session_state.level_progress[st.session_state.current_level] += 1
                text_to_speech_real("Great job! That's perfect!", target_language)
                return True
            else:
                st.error(f"❌ Try again. Correct answer: *{correct_answer}*")
                if alternative:
                    st.info(f"Alternative: *{alternative}*")
                text_to_speech_real(f"The correct answer is {correct_answer}", target_language)
                return False
    
    return None

def run_story_completion_question(prompt, target_language):
    """Handle story completion questions"""
    context = prompt.get('context', '')
    question = prompt['prompt']
    correct_answer = prompt['answer']
    translation = prompt.get('translation', '')
    
    st.write(f"*Story Completion:*")
    if context:
        st.write(f"*Context:* {context}")
    st.write(f"*Complete the sentence:* {question}")
    if translation:
        st.write(f"Translation: {translation}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔊 Listen to prompt", key="story_listen"):
            text_to_speech_real(question, target_language)
    
    with col2:
        user_input = speech_to_text_real()
        
        if user_input and st.button("✅ Check Answer", key="story_check"):
            add_to_chat_history("You", user_input)
            
            if correct_answer.lower() in user_input.lower():
                st.success("🎉 Perfect story continuation!")
                st.session_state.score += 1
                st.session_state.level_progress[st.session_state.current_level] += 1
                text_to_speech_real("Excellent storytelling!", target_language)
                return True
            else:
                st.error(f"❌ Try again. The word is: *{correct_answer}*")
                text_to_speech_real(f"The correct word is {correct_answer}", target_language)
                return False
    
    return None

def get_level_name(level):
    """Get descriptive name for each level"""
    level_names = {
        1: "Beginner - Basic Vocabulary",
        2: "Intermediate - Grammar & Structure", 
        3: "Advanced - Conversation & Stories"
    }
    return level_names.get(level, f"Level {level}")

def display_progress_sidebar():
    """Display progress and stats in sidebar"""
    with st.sidebar:
        st.header("📊 Your Progress")
        
        if st.session_state.current_language:
            lang_name = language_names[st.session_state.current_language]
            st.write(f"*Language:* {lang_name}")
            
            # Overall stats
            accuracy = (st.session_state.score / max(st.session_state.total_questions, 1)) * 100
            st.metric("Overall Accuracy", f"{accuracy:.1f}%")
            st.metric("Questions Answered", st.session_state.total_questions)
            st.metric("Correct Answers", st.session_state.score)
            
            st.divider()
            
            # Level progress
            st.subheader("🎯 Level Progress")
            for level in [1, 2, 3]:
                progress = st.session_state.level_progress[level]
                is_unlocked = st.session_state.level_unlocked[level]
                status = "🔓" if is_unlocked else "🔒"
                
                st.write(f"{status} *Level {level}:* {progress}/6 correct")
                if is_unlocked:
                    st.progress(min(progress / 6, 1.0))
                else:
                    st.progress(0)
            
            st.divider()
            
            # Quick actions
            st.subheader("⚡ Quick Actions")
            if st.button("🔄 Reset Progress", key="reset_progress"):
                reset_progress()
                st.success("Progress reset!")
                st.rerun()
                
            if st.button("🏠 Back to Home", key="back_home"):
                st.session_state.current_language = None
                st.rerun()

def reset_progress():
    """Reset all progress for current language"""
    st.session_state.current_level = 1
    st.session_state.current_question_index = 0
    st.session_state.score = 0
    st.session_state.total_questions = 0
    st.session_state.level_progress = {1: 0, 2: 0, 3: 0}
    st.session_state.level_unlocked = {1: True, 2: False, 3: False}
    st.session_state.current_questions = []
    st.session_state.chat_history = []
    st.session_state.speech_input = ""

def display_chat_history():
    """Display recent chat history"""
    if st.session_state.chat_history:
        st.subheader("💬 Recent Activity")
        
        # Show last 5 interactions
        recent_history = st.session_state.chat_history[-5:]
        
        for entry in recent_history:
            with st.container():
                timestamp = entry['timestamp']
                speaker = entry['speaker']
                message = entry['message']
                
                if speaker == "You":
                    st.write(f"{timestamp} - You:** {message}")
                else:
                    st.write(f"{timestamp} - Tutor:** {message}")

def main():
    """Main application function"""
    initialize_session_state()
    
    # Header
    st.title("🗣 CortexTalk")
    st.write("Learn languages with interactive lessons, speech recognition, and AI-powered feedback!")
    
    # Language selection
    if not st.session_state.current_language:
        st.header("🌍 Choose Your Language")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🇪🇸 Learn Spanish", key="spanish", use_container_width=True):
                st.session_state.current_language = 'es'
                reset_progress()
                st.rerun()
        
        with col2:
            if st.button("🇫🇷 Learn French", key="french", use_container_width=True):
                st.session_state.current_language = 'fr'
                reset_progress()
                st.rerun()
        
        with col3:
            if st.button("🇩🇪 Learn German", key="german", use_container_width=True):
                st.session_state.current_language = 'de'
                reset_progress()
                st.rerun()
        
        
        if st.button("🕶 Learn in VR"):
            st.info("🚧 VR Mode coming soon! We're building an immersive experience for you. Stay tuned!")
       
        # Features overview
        st.header("✨ Features")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("🎤 *Speech Recognition*\nPractice pronunciation with voice input")
        
        with col2:
            st.info("🔊 *Text-to-Speech*\nHear native pronunciation")
        
        with col3:
            st.info("🎯 *Progressive Learning*\nUnlock levels as you improve")
        
        return
    
    # Main learning interface
    display_progress_sidebar()
    
    # Level selection tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📚 Level 1", "📖 Level 2", "🎓 Level 3", "💬 Chat History"])
    
    with tab1:
        if st.session_state.level_unlocked[1]:
            run_level(1, st.session_state.current_language)
        else:
            st.warning("🔒 This level is locked!")
    
    with tab2:
        if st.session_state.level_unlocked[2]:
            run_level(2, st.session_state.current_language)
        else:
            st.warning("🔒 Complete Level 1 first!")
    
    with tab3:
        if st.session_state.level_unlocked[3]:
            run_level(3, st.session_state.current_language)
        else:
            st.warning("🔒 Complete Level 2 first!")
    
    with tab4:
        display_chat_history()
    
    # Footer
    st.divider()
    st.write("🚀 *Built with Streamlit* | 🎯 *Interactive Language Learning*")

if __name__ == "__main__":
    main()
