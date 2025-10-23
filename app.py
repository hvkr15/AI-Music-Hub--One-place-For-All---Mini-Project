from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from recommendation import MusicRecommender
from weather_recommendation import WeatherMusicRecommender

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Initialize recommenders
music_recommender = None
weather_recommender = None

def load_data():
    """Load music dataset and initialize recommenders"""
    global music_recommender, weather_recommender
    try:
        # Load the music dataset
        if os.path.exists('data/music_data.csv'):
            df = pd.read_csv('data/music_data.csv')
            music_recommender = MusicRecommender(df)
            weather_recommender = WeatherMusicRecommender(df)
            print("✓ Data loaded successfully!")
            return True
        else:
            print("⚠ Warning: music_data.csv not found. Please add dataset.")
            return False
    except Exception as e:
        print(f"Error loading data: {e}")
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
        genre = data.get('genre', 'pop')
        mood = data.get('mood', 'happy')
        
        if not theme:
            return jsonify({'error': 'Theme is required'}), 400
        
        # Simple lyrics generation (template-based)
        lyrics = generate_lyrics_template(theme, genre, mood)
        
        return jsonify({
            'success': True,
            'lyrics': lyrics,
            'theme': theme,
            'genre': genre,
            'mood': mood
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_lyrics_template(theme, genre, mood):
    """Generate lyrics using templates based on genre and mood"""
    
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
