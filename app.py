from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from recommendation import MusicRecommender
from spotify_recommender import SpotifyMusicRecommender
from weather_recommendation import WeatherMusicRecommender

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Initialize recommenders
music_recommender = None
weather_recommender = None
use_spotify_dataset = False

def load_data():
    """Load music dataset and initialize recommenders"""
    global music_recommender, weather_recommender, use_spotify_dataset
    try:
        # Try to load Spotify Million Song Dataset first
        if os.path.exists('data/spotify_million_songs.csv'):
            print("📊 Loading Spotify Million Song Dataset...")
            df = pd.read_csv('data/spotify_million_songs.csv')
            
            # Use Spotify recommender for the large dataset
            music_recommender = SpotifyMusicRecommender(df)
            use_spotify_dataset = True
            print("✓ Spotify dataset loaded successfully!")
            
            # For weather recommendations, we'll use a sample or create genre mapping
            # Since Spotify dataset doesn't have genre/mood, we'll skip weather recommendations
            # or implement a fallback
            print("ℹ️  Weather-based recommendations using Spotify dataset (limited features)")
            weather_recommender = None  # Disable for now as Spotify dataset lacks mood/genre
            
            return True
            
        # Fallback to original dataset
        elif os.path.exists('data/music_data.csv'):
            print("📊 Loading original music dataset...")
            df = pd.read_csv('data/music_data.csv')
            music_recommender = MusicRecommender(df)
            weather_recommender = WeatherMusicRecommender(df)
            use_spotify_dataset = False
            print("✓ Original dataset loaded successfully!")
            return True
            
        else:
            print("⚠ Warning: No dataset found. Please add dataset.")
            return False
            
    except Exception as e:
        print(f"Error loading data: {e}")
        import traceback
        traceback.print_exc()
        return False

@app.route('/')
def home():
    """Home page route"""
    return render_template('index.html')

@app.route('/lyrics-generator')
def lyrics_generator():
    """Lyrics Generator page route"""
    return render_template('lyrics_generator.html')

@app.route('/song-creator')
def song_creator():
    """Song Creator page route"""
    return render_template('song_creator.html')

@app.route('/song-generator')
def song_generator():
    """Song Generator page route"""
    return render_template('song_generator.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    """Get music recommendations based on selected song"""
    try:
        data = request.get_json()
        song_name = data.get('song_name', '')
        
        if not music_recommender:
            return jsonify({'error': 'System not initialized. Please check dataset.'}), 500
        
        recommendations = music_recommender.get_recommendations(song_name, n_recommendations=10)
        
        if recommendations is None or len(recommendations) == 0:
            return jsonify({'error': 'Song not found or no recommendations available'}), 404
        
        return jsonify({
            'success': True,
            'recommendations': recommendations.to_dict('records')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/weather-recommend', methods=['POST'])
def weather_recommend():
    """Get music recommendations based on current weather"""
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if not weather_recommender:
            return jsonify({'error': 'System not initialized. Please check dataset.'}), 500
        
        result = weather_recommender.get_weather_based_recommendations(
            latitude, longitude, n_recommendations=15
        )
        
        if result is None:
            return jsonify({'error': 'Unable to fetch weather data'}), 500
        
        return jsonify({
            'success': True,
            'weather': result['weather'],
            'mood': result['mood'],
            'recommendations': result['recommendations'].to_dict('records')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-songs', methods=['GET'])
def get_songs():
    """Get list of all available songs"""
    try:
        if not music_recommender or music_recommender.df is None:
            return jsonify({'error': 'System not initialized'}), 500
        
        songs = music_recommender.df['song'].tolist()
        return jsonify({
            'success': True,
            'songs': songs
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/search-songs', methods=['GET'])
def search_songs():
    """Search songs by query"""
    try:
        query = request.args.get('q', '').lower()
        
        if not music_recommender or music_recommender.df is None:
            return jsonify({'error': 'System not initialized'}), 500
        
        if not query:
            songs = music_recommender.df['song'].head(50).tolist()
        else:
            songs = music_recommender.df[
                music_recommender.df['song'].str.lower().str.contains(query, na=False)
            ]['song'].head(50).tolist()
        
        return jsonify({
            'success': True,
            'songs': songs
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-lyrics', methods=['POST'])
def generate_lyrics():
    """Generate AI lyrics based on user input"""
    try:
        data = request.get_json()
        theme = data.get('theme', '')
        language = data.get('language', 'english')
        genre = data.get('genre', 'pop')
        mood = data.get('mood', 'happy')
        
        if not theme:
            return jsonify({'error': 'Theme is required'}), 400
        
        # Generate lyrics with language support
        lyrics = generate_lyrics_template(theme, genre, mood, language)
        
        return jsonify({
            'success': True,
            'lyrics': lyrics,
            'theme': theme,
            'genre': genre,
            'mood': mood,
            'language': language
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-song', methods=['POST'])
def generate_song():
    """Generate AI song description based on user input"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        duration = data.get('duration', 'medium')
        tempo = data.get('tempo', 'medium')
        vocals = data.get('vocals', 'mixed')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Generate song description
        song_description = generate_song_description(prompt, duration, tempo, vocals)
        
        return jsonify({
            'success': True,
            'song_description': song_description,
            'prompt': prompt
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_song_description(prompt, duration, tempo, vocals):
    """Generate detailed song description for AI music platforms"""
    
    # Map tempo to BPM range
    tempo_map = {
        'slow': '60-80 BPM',
        'medium': '90-120 BPM',
        'fast': '130-160 BPM'
    }
    
    # Map duration to structure
    duration_map = {
        'short': 'Intro → Verse → Chorus → Verse → Chorus → Outro',
        'medium': 'Intro → Verse 1 → Chorus → Verse 2 → Chorus → Bridge → Final Chorus → Outro',
        'long': 'Intro → Verse 1 → Pre-Chorus → Chorus → Verse 2 → Pre-Chorus → Chorus → Bridge → Instrumental Break → Final Chorus → Extended Outro'
    }
    
    # Analyze the prompt to extract key elements
    prompt_lower = prompt.lower()
    
    # Detect genre hints
    genre_hints = []
    if any(word in prompt_lower for word in ['rock', 'guitar', 'drums', 'electric']):
        genre_hints.append('Rock')
    if any(word in prompt_lower for word in ['pop', 'catchy', 'upbeat', 'radio']):
        genre_hints.append('Pop')
    if any(word in prompt_lower for word in ['electronic', 'edm', 'synth', 'beat']):
        genre_hints.append('Electronic')
    if any(word in prompt_lower for word in ['jazz', 'saxophone', 'swing']):
        genre_hints.append('Jazz')
    if any(word in prompt_lower for word in ['classical', 'orchestra', 'piano']):
        genre_hints.append('Classical')
    if any(word in prompt_lower for word in ['hip-hop', 'rap', 'trap', 'beats']):
        genre_hints.append('Hip-Hop')
    
    genre_text = ', '.join(genre_hints) if genre_hints else 'Contemporary'
    
    # Detect mood/emotion
    mood_hints = []
    if any(word in prompt_lower for word in ['happy', 'upbeat', 'cheerful', 'joyful', 'fun']):
        mood_hints.append('uplifting and energetic')
    if any(word in prompt_lower for word in ['sad', 'melancholic', 'emotional', 'heartbreak']):
        mood_hints.append('emotional and introspective')
    if any(word in prompt_lower for word in ['romantic', 'love', 'passion']):
        mood_hints.append('romantic and tender')
    if any(word in prompt_lower for word in ['aggressive', 'intense', 'powerful']):
        mood_hints.append('intense and powerful')
    if any(word in prompt_lower for word in ['calm', 'peaceful', 'relaxing', 'chill']):
        mood_hints.append('calm and soothing')
    
    mood_text = ', '.join(mood_hints) if mood_hints else 'balanced and expressive'
    
    # Detect instruments
    instruments = []
    if 'guitar' in prompt_lower:
        instruments.append('electric guitar' if 'electric' in prompt_lower else 'acoustic guitar')
    if any(word in prompt_lower for word in ['piano', 'keys', 'keyboard']):
        instruments.append('piano')
    if 'drums' in prompt_lower or 'percussion' in prompt_lower:
        instruments.append('dynamic drums and percussion')
    if any(word in prompt_lower for word in ['synth', 'electronic']):
        instruments.append('synthesizers')
    if 'bass' in prompt_lower:
        instruments.append('bass guitar')
    if 'strings' in prompt_lower or 'violin' in prompt_lower:
        instruments.append('string section')
    
    instruments_text = ', '.join(instruments) if instruments else 'varied instrumentation'
    
    # Build the description
    description = f"""🎵 AI SONG DESCRIPTION
{'=' * 60}

📋 ORIGINAL PROMPT:
{prompt}

{'=' * 60}

🎼 SONG SPECIFICATIONS:

Genre: {genre_text}
Mood/Emotion: {mood_text}
Tempo: {tempo.capitalize()} ({tempo_map[tempo]})
Duration: {duration.capitalize()}
Vocals: {vocals.capitalize()}

{'=' * 60}

🎹 MUSICAL ELEMENTS:

Main Instruments: {instruments_text}
Production Style: Modern, polished production with clear mix
Vocal Style: {'Professional studio vocals with emotion and clarity' if vocals != 'instrumental' else 'No vocals - purely instrumental'}

{'=' * 60}

🎭 SONG STRUCTURE:
{duration_map[duration]}

{'=' * 60}

✨ DETAILED DESCRIPTION FOR AI:

Create a {tempo.lower()}-tempo {genre_text.lower()} song with a {mood_text} vibe. 
The song should feature {instruments_text.lower()} as the primary sonic elements. 

{prompt}

The production should be modern and radio-ready, with a focus on:
- Clear and balanced mix
- Dynamic arrangement that builds throughout the song
- Professional mastering quality
- Attention to emotional delivery and atmosphere

{f"Vocal performance should be {vocals} with professional technique, clear articulation, and emotional depth appropriate to the song's theme." if vocals != 'instrumental' else "As an instrumental track, focus on melodic development and instrumental expression to convey emotion."}

Target a {duration.lower()} format suitable for streaming platforms, 
maintaining listener engagement throughout with varied sections and dynamic changes.

{'=' * 60}

💡 USE THIS DESCRIPTION:
Copy the detailed description above and paste it into AI music generation 
platforms like Suno AI, Udio, or MusicLM for best results!
"""
    
    return description

def generate_multilingual_lyrics(theme, genre, mood, language):
    """Generate lyrics in different Indian languages"""
    
    # Language-specific templates
    lyrics_templates = {
        'hindi': {
            'verse': [
                f"दिल में है {theme} की आग",
                f"जो जलती है हर एक राग",
                f"{theme} के साथ है ये सफर",
                f"हर पल में मिले नया असर"
            ],
            'chorus': [
                f"ओ {theme}, तू ही है मेरी जान",
                f"तेरे बिना अधूरी ये कहान",
                f"{theme} से है ये प्यार",
                f"दिल की धड़कन, जीवन का आधार"
            ],
            'bridge': f"जब भी लगे अंधेरा\n{theme} बने सहारा मेरा",
            'outro': f"{theme}... {theme}...\nसदा रहे दिल में बसा"
        },
        'kannada': {
            'verse': [
                f"{theme} ನನ್ನ ಹೃದಯದಲ್ಲಿ",
                f"ಸದಾ ನಿನ್ನ ನೆನಪಿನಲ್ಲಿ",
                f"{theme} ನೀನು ನನ್ನ ಜೀವನ",
                f"ಪ್ರತಿ ಕ್ಷಣ ಹೊಸ ಸಂತೋಷ"
            ],
            'chorus': [
                f"ಓ {theme}, ನೀನೇ ನನ್ನ ಪ್ರಾಣ",
                f"ನಿನ್ನ ಬಿಟ್ಟು ಇಲ್ಲ ನನಗೆ ಸ್ಥಾನ",
                f"{theme} ಯೊಂದಿಗೆ ಪ್ರೀತಿ",
                f"ಹೃದಯದ ಗೀತೆ, ಜೀವನದ ರೀತಿ"
            ],
            'bridge': f"ಕತ್ತಲು ಆವರಿಸಿದಾಗ\n{theme} ನೀನೇ ನನ್ನ ಬೆಳಕು",
            'outro': f"{theme}... {theme}...\nಎಂದೆಂದಿಗೂ ನನ್ನೊಂದಿಗೆ"
        },
        'tamil': {
            'verse': [
                f"{theme} என் மனதில்",
                f"நீ எப்போதும் நினைவில்",
                f"{theme} நீயே என் வாழ்க்கை",
                f"ஒவ்வொரு நொடியும் புதிய மகிழ்ச்சி"
            ],
            'chorus': [
                f"ஓ {theme}, நீதான் என் உயிர்",
                f"உன்னை விட்டால் எனக்கு இடமில்லை",
                f"{theme} உடன் காதல்",
                f"இதயத்தின் பாட்டு, வாழ்க்கையின் வழி"
            ],
            'bridge': f"இருள் சூழும் போது\n{theme} நீயே என் ஒளி",
            'outro': f"{theme}... {theme}...\nஎன்றென்றும் என்னுடன்"
        },
        'telugu': {
            'verse': [
                f"{theme} నా హృదయంలో",
                f"నీవు ఎప్పుడూ జ్ఞాపకంలో",
                f"{theme} నువ్వే నా జీవితం",
                f"ప్రతి క్షణం కొత్త ఆనందం"
            ],
            'chorus': [
                f"ఓ {theme}, నువ్వే నా ప్రాణం",
                f"నిన్ను లేకుండా నాకు స్థానం లేదు",
                f"{theme} తో ప్రేమ",
                f"హృదయపు పాట, జీవిత మార్గం"
            ],
            'bridge': f"చీకటి ఆవరించినప్పుడు\n{theme} నువ్వే నా వెలుగు",
            'outro': f"{theme}... {theme}...\nఎప్పటికీ నాతో"
        },
        'malayalam': {
            'verse': [
                f"{theme} എന്റെ ഹൃദയത്തിൽ",
                f"നീ എപ്പോഴും ഓർമ്മയിൽ",
                f"{theme} നീയാണ് എന്റെ ജീവിതം",
                f"ഓരോ നിമിഷവും പുതിയ സന്തോഷം"
            ],
            'chorus': [
                f"ഓ {theme}, നീയാണ് എന്റെ പ്രാണൻ",
                f"നിന്നെ കൂടാതെ എനിക്ക് സ്ഥലമില്ല",
                f"{theme} യോടൊപ്പം സ്നേഹം",
                f"ഹൃദയത്തിന്റെ പാട്ട്, ജീവിതത്തിന്റെ വഴി"
            ],
            'bridge': f"ഇരുട്ട് വരുമ്പോൾ\n{theme} നീയാണ് എന്റെ വെളിച്ചം",
            'outro': f"{theme}... {theme}...\nഎന്നെന്നേക്കും എന്നോടൊപ്പം"
        },
        'marathi': {
            'verse': [
                f"{theme} माझ्या हृदयात",
                f"तू नेहमी आठवणीत",
                f"{theme} तूच माझे जीवन",
                f"प्रत्येक क्षण नवा आनंद"
            ],
            'chorus': [
                f"ओ {theme}, तूच माझा प्राण",
                f"तुझ्याशिवाय मला स्थान नाही",
                f"{theme} सोबत प्रेम",
                f"हृदयाचे गीत, जीवनाचा मार्ग"
            ],
            'bridge': f"जेव्हा अंधार येतो\n{theme} तूच माझा प्रकाश",
            'outro': f"{theme}... {theme}...\nसदैव माझ्यासोबत"
        },
        'bengali': {
            'verse': [
                f"{theme} আমার হৃদয়ে",
                f"তুমি সর্বদা স্মৃতিতে",
                f"{theme} তুমিই আমার জীবন",
                f"প্রতি মুহূর্তে নতুন আনন্দ"
            ],
            'chorus': [
                f"ও {theme}, তুমিই আমার প্রাণ",
                f"তোমাকে ছাড়া আমার কোনো স্থান নেই",
                f"{theme} এর সাথে ভালোবাসা",
                f"হৃদয়ের গান, জীবনের পথ"
            ],
            'bridge': f"যখন অন্ধকার আসে\n{theme} তুমিই আমার আলো",
            'outro': f"{theme}... {theme}...\nচিরকাল আমার সাথে"
        },
        'punjabi': {
            'verse': [
                f"{theme} ਮੇਰੇ ਦਿਲ ਵਿੱਚ",
                f"ਤੂੰ ਹਮੇਸ਼ਾ ਯਾਦਾਂ ਵਿੱਚ",
                f"{theme} ਤੂੰ ਹੀ ਮੇਰੀ ਜ਼ਿੰਦਗੀ",
                f"ਹਰ ਪਲ ਨਵੀਂ ਖੁਸ਼ੀ"
            ],
            'chorus': [
                f"ਓ {theme}, ਤੂੰ ਹੀ ਮੇਰੀ ਜਾਨ",
                f"ਤੇਰੇ ਬਿਨਾ ਨਹੀਂ ਕੋਈ ਥਾਂ",
                f"{theme} ਨਾਲ ਪਿਆਰ",
                f"ਦਿਲ ਦਾ ਗੀਤ, ਜੀਵਨ ਦਾ ਰਾਹ"
            ],
            'bridge': f"ਜਦੋਂ ਹਨੇਰਾ ਆਵੇ\n{theme} ਤੂੰ ਹੀ ਮੇਰੀ ਰੋਸ਼ਨੀ",
            'outro': f"{theme}... {theme}...\nਹਮੇਸ਼ਾ ਮੇਰੇ ਨਾਲ"
        },
        'gujarati': {
            'verse': [
                f"{theme} મારા હૃદયમાં",
                f"તું હંમેશા યાદમાં",
                f"{theme} તું જ મારું જીવન",
                f"દરેક ક્ષણે નવો આનંદ"
            ],
            'chorus': [
                f"ઓ {theme}, તું જ મારો પ્રાણ",
                f"તારા વિના મને સ્થાન નથી",
                f"{theme} સાથે પ્રેમ",
                f"હૃદયનું ગીત, જીવનનો માર્ગ"
            ],
            'bridge': f"જ્યારે અંધકાર આવે\n{theme} તું જ મારો પ્રકાશ",
            'outro': f"{theme}... {theme}...\nસદા મારી સાથે"
        }
    }
    
    template = lyrics_templates.get(language, lyrics_templates['hindi'])
    
    # Build lyrics structure
    lyrics = f"""[Verse 1]
{template['verse'][0]}
{template['verse'][1]}
{template['verse'][2]}
{template['verse'][3]}

[Chorus]
{template['chorus'][0]}
{template['chorus'][1]}
{template['chorus'][2]}
{template['chorus'][3]}

[Verse 2]
{template['verse'][0]}
{template['verse'][2]}
{template['verse'][1]}
{template['verse'][3]}

[Chorus]
{template['chorus'][0]}
{template['chorus'][1]}
{template['chorus'][2]}
{template['chorus'][3]}

[Bridge]
{template['bridge']}

[Final Chorus]
{template['chorus'][0]}
{template['chorus'][1]}
{template['chorus'][2]}
{template['chorus'][3]}

[Outro]
{template['outro']}
"""
    
    return lyrics

def generate_lyrics_template(theme, genre, mood, language='english'):
    """Generate lyrics using templates based on genre, mood, and language"""
    
    # If language is not English, generate transliterated/regional lyrics
    if language != 'english':
        return generate_multilingual_lyrics(theme, genre, mood, language)
    
    # Theme-based verse templates
    verse_templates = {
        'happy': [
            f"When I think about {theme}, my heart starts to glow",
            f"Every moment with {theme}, letting feelings flow",
            f"Dancing through the day, {theme} lights my way",
            f"Nothing can compare to this joy I display"
        ],
        'sad': [
            f"Memories of {theme} fade like morning dew",
            f"Lost in thoughts of {theme}, feeling so blue",
            f"Searching for the light, through the darkest night",
            f"Hoping {theme} will make things right"
        ],
        'energetic': [
            f"Let's go, {theme} is calling out my name",
            f"Feel the beat, {theme} sets my soul aflame",
            f"No stopping now, we're breaking all the chains",
            f"Living for {theme}, running through the veins"
        ],
        'calm': [
            f"Peaceful moments with {theme} by my side",
            f"Gentle whispers where {theme} resides",
            f"In the stillness, {theme} helps me find",
            f"A quiet place within my mind"
        ]
    }
    
    chorus_templates = {
        'pop': [
            f"Oh {theme}, you're everything I need",
            f"{theme}, you're the one who sets me free",
            f"Together we can fly so high",
            f"With {theme}, reaching for the sky"
        ],
        'rock': [
            f"{theme}! Breaking through the night!",
            f"{theme}! We're ready for the fight!",
            f"Nothing's gonna hold us back!",
            f"With {theme}, we're on the attack!"
        ],
        'jazz': [
            f"{theme} in the moonlight, soft and slow",
            f"Swaying to the rhythm, letting feelings show",
            f"In this jazzy paradise we've found",
            f"With {theme}, love knows no bound"
        ],
        'hip-hop': [
            f"Yeah, {theme} on my mind all day",
            f"Living life my own unique way",
            f"{theme} got me feeling so fly",
            f"Reaching for the stars up in the sky"
        ]
    }
    
    # Select templates based on mood and genre
    verses = verse_templates.get(mood, verse_templates['happy'])
    chorus = chorus_templates.get(genre, chorus_templates['pop'])
    
    # Build the complete lyrics
    lyrics = f"""[Verse 1]
{verses[0]}
{verses[1]}
{verses[2]}
{verses[3]}

[Chorus]
{chorus[0]}
{chorus[1]}
{chorus[2]}
{chorus[3]}

[Verse 2]
The rhythm of {theme} pulses through my soul
With every beat, {theme} makes me whole
Can you feel the magic in the air?
{theme}'s presence everywhere

[Chorus]
{chorus[0]}
{chorus[1]}
{chorus[2]}
{chorus[3]}

[Bridge]
When the world feels cold and gray
{theme} shows me the way
Through the highs and through the lows
{theme}'s the melody that flows

[Final Chorus]
{chorus[0]}
{chorus[1]}
{chorus[2]}
{chorus[3]}

[Outro]
{theme}... {theme}...
Forever in my heart, {theme}
"""
    
    return lyrics

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🎵 AI Music Recommendation System with Weather Integration")
    print("=" * 60)
    
    # Load data
    if load_data():
        print("\n🚀 Starting server...")
        print("📍 Open http://127.0.0.1:5000 in your browser")
        print("=" * 60)
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("\n❌ Failed to start: Dataset not found")
        print("Please add 'data/music_data.csv' and restart")
        print("=" * 60)
